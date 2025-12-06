from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

# 1. User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id', 'email', 'first_name', 'last_name', 
            'phone_number', 'role', 'password', 'created_at'
        ]
        # Security: Password can be written (registration) but is never read (API response)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # We override create to ensure the password is hashed correctly
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

# 2. Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    # Nesting: Display full sender details instead of just the ID
    sender = UserSerializer(read_only=True)
    
    # Write-only: When sending a message, we only need the sender's ID
    sender_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id', 'conversation', 'sender', 'sender_id', 
            'message_body', 'sent_at'
        ]

# 3. Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    # Nesting: Show full details of participants
    participants = UserSerializer(many=True, read_only=True)
    
    # Optional: Include the latest message or all messages? 
    # Usually, we don't nest ALL messages here to avoid huge payloads.
    # We just provide the conversation ID/details.

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at']