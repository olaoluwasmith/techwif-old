from django.urls import path
from . import views
from .views import *


urlpatterns = [
    #Notification list
    path('notifications/', CommentNoticeListView.as_view(), name='notification_list'),
    #Update notification status
    path('notifications/mark_al_as_read/', CommentNoticeUpdateView.as_view(), name='notification_update'),
]