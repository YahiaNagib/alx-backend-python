# chats/urls.py
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as NestedDefaultRouter
from . import views

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet, basename='user')
router.register(r'conversations', views.ConversationViewSet, basename='conversation')
router.register(r'messages', views.MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]