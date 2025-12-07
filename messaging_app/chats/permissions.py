from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so long as the user is a participant.
        return request.user in obj.participants.all()
    


class IsMessageSender(permissions.BasePermission):
    """
    Custom permission to ensure:
    1. Users can only edit/delete their OWN messages.
    2. Users can read any message in a conversation they belong to.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # provided the view filters queryset correctly.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions (PUT, PATCH, DELETE) are only allowed to the sender.
        return obj.sender == request.user