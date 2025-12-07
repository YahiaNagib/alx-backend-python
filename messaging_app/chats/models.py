import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):

    user_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
        db_index=True
    )
   
    ROLE = [('guest', 'Guest'), ('host', 'Host'), ('admin', 'Admin')]

    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)

    email = models.EmailField(unique=True, blank=False, null=False)

    phone_number = models.CharField(max_length=20, blank=True, null=True)

    role = models.CharField(
        max_length=10, 
        choices=ROLE, 
        default='guest',
        blank=False,
        null=False
    )

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'role']

    def __str__(self):
        return self.email


class Message(models.Model):

    message_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
        db_index=True
    )

    # sender_id: Foreign Key to User
    # on_delete=models.CASCADE means if the User is deleted, their messages are deleted.
    # related_name='messages' allows you to do user.messages.all()
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
    User, 
    on_delete=models.CASCADE, 
    related_name='received_messages'
)

    # message_body: TEXT, NOT NULL
    message_body = models.TextField(blank=False, null=False)

    # sent_at: TIMESTAMP
    sent_at = models.DateTimeField(auto_now_add=True)

    conversation = models.ForeignKey(
        'Conversation', 
        on_delete=models.CASCADE, 
        related_name='messages'
    )

    class Meta:
        # Default ordering: newest messages first
        ordering = ['-sent_at']

    def __str__(self):
        # Returns a snippet of the message for easy ID in admin/shell
        return f"{self.sender} - {self.sent_at}: {self.message_body[:20]}..."
    


class Conversation(models.Model):
    
    conversation_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
        db_index=True
    )

    # participants: ManyToMany (Allows multiple users in one conversation)
    participants = models.ManyToManyField(
        User, 
        related_name='conversations'
    )
    
    # created_at: TIMESTAMP
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"