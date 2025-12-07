from rest_framework import viewsets, permissions
from .models import Conversation, Message, User
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or registered.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Allow anyone to register (POST), but only authenticated users
        can list or retrieve user details.
        """
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Only return conversations where the current user is a participant.
        """
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        """
        When creating a new conversation, automatically add the 
        current user to the participants list if not already included.
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        1. Filter messages to only those in conversations the user belongs to.
        2. Support filtering by ?conversation_id=X in the URL.
        """
        user = self.request.user
        queryset = Message.objects.filter(conversation__participants=user)

        # Allow frontend to filter: /api/messages/?conversation_id=5
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
            
        return queryset

    def perform_create(self, serializer):
        """
        Automatically set the 'sender' to the currently logged-in user.
        """
        # We need to validate that the user is actually a participant 
        # of the conversation they are trying to post to.
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
             raise permissions.exceptions.PermissionDenied(
                 "You are not a participant of this conversation."
             )
             
        serializer.save(sender=self.request.user)