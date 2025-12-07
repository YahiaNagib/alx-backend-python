from rest_framework import serializers
from .models import User
from .models import Conversation, Message

# -------------------------
# User Serializer
# -------------------------
class UserSerializer(serializers.ModelSerializer):

    # We use this to ensure the password is not readable in the API response
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'password']

    def create(self, validated_data):
        """
        Overriding create to ensure passwords are hashed correctly.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


# -------------------------
# Message Serializer
# -------------------------
class MessageSerializer(serializers.ModelSerializer):
    # Nested serializer to show sender details instead of just ID
    sender_info = UserSerializer(source='sender', read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'sender_info', 'message_body', 'sent_at']
        read_only_fields = ['sent_at', 'sender']

    def validate_text(self, value):
        """
        Check that the message text is not empty or offensive.
        Requirement: serializers.ValidationError
        """
        if not value or value.strip() == "":
            raise serializers.ValidationError("Message text cannot be empty.")
        
        banned_words = ["spam", "virus"]
        if any(word in value.lower() for word in banned_words):
            raise serializers.ValidationError("Message contains prohibited content.")
            
        return value


# -------------------------
# Conversation Serializer
# -------------------------
class ConversationSerializer(serializers.ModelSerializer):
    
    # Used to dynamically calculate the last message for the chat list UI
    last_message = serializers.SerializerMethodField()
    
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'last_message']

    def get_last_message(self, obj):
        """
        Retrieves the most recent message in this conversation.
        """
        # Assuming you have a related_name='messages' in your Message model
        message = obj.messages.order_by('-sent_at').first()
        if message:
            return {
                "message_body": message.message_body,
                "sent_at": message.sent_at,
                "sender": message.sender.username
            }
        return None