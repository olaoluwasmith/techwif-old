from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from tech.models import Forum

# Create your views here.

class CommentNoticeListView(LoginRequiredMixin, ListView):
    context_object_name = 'notices'
    template_name = 'user/notification.html'
    login_url = '/login/'

    def get_queryset(self):
        return self.request.user.notifications.all()


class CommentNoticeUpdateView(View):
    def get(self, request):
        #Get unread message
        notice_id = request.GET.get('notice_id')
        #Update single notice
        if notice_id:
            forum = Forum.objects.get(id=request.GET.get('forum_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(forum)
        #Update all notifications
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notification_list')