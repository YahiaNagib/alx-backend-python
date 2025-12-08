from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        # 1. Check if user is logged in
        # Note: Use .is_authenticated (property), not .IsAuthenticated()
        
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. Check if user is in the participants list
        # We return the result of this comparison directly (True/False)
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