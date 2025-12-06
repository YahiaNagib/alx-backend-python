from django.contrib import admin
from .models import User, Message, Conversation
from django.contrib.auth.admin import UserAdmin # Import this!

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Message)
admin.site.register(Conversation)

 