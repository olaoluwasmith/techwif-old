from django.urls import path, include
from django.contrib.auth import views as auth_views
import notifications.urls


from . import views
from .views import *


urlpatterns = [
    path('signup/', views.RegisterPage, name='register'),
    path('signin/', views.LoginPage, name='login'),
    path('update_profile/', views.ProfileUpdate, name='profile_update'),
    path('signout/', views.LogoutUser, name='logout'),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),

    path('reset_password/', 
        auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), 
        name='reset_password'),
    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_sent.html'), 
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_form.html'), 
        name='password_reset_confirm'),
    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), 
        name='password_reset_complete'),

    path('privacy_policy/', views.privacy_policy, name='privacy_policy'), 
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('advertise/', views.advertise, name='advertise'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('about/', views.about, name='about'),

    path('services/', ServiceListView.as_view(), name='service_list'),
    path('services/<slug:slug>/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('services/<slug:slug>/<int:pk>/update/', ServiceUpdateView.as_view(), name='service_update'),
    path('services/<slug:slug>/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service_delete'),
    path('service_form/', ServiceCreateView.as_view(), name='service_form'),

    path('jobs/', ReviewListView.as_view(), name='review_list'),
    path('jobs/<slug:slug>/<int:pk>/', views.ReviewDetailView, name='review_detail'),
    path('jobs/<slug:slug>/<int:pk>/update/', ReviewUpdateView.as_view(), name='review_update'),
    path('jobs/<slug:slug>/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    path('job_form/', ReviewCreateView.as_view(), name='review_form'),
    
    path('articles/<slug:slug>/<int:pk>/', views.BlogDetailView, name='article_detail'),
    path('articles/<slug:slug>/<int:pk>/update/', BlogUpdateView.as_view(), name='article_update'),
    path('articles/<slug:slug>/<int:pk>/delete/', BlogDeleteView.as_view(), name='article_delete'),
    path('article_form/', BlogCreateView.as_view(), name='article_form'),
    path('categories/<category_slug>/', views.BlogCategory, name='category'),

    path('forum/', ForumListView.as_view(), name='forum_list'),
    path('forum/<slug:slug>/<int:pk>/', views.ForumDetailView, name='forum_detail'),
    path('like_forum/', views.like_forum, name='like_forum'),
    path('forum/<slug:slug>/<int:pk>/update/', ForumUpdateView.as_view(), name='forum_update'),
    path('forum/<slug:slug>/<int:pk>/update_image/', views.ForumImageUpdate, name='forum_update_image'),
    path('forum/<slug:slug>/<int:pk>/favourite_posts/', views.FavouritePost, name='favourite_posts'),
    path('forum/favourite_posts/', views.FavouritePostView, name='favourite_posts_view'),
    path('forum/<slug:slug>/<int:pk>/delete/', ForumDeleteView.as_view(), name='forum_delete'),
    path('delete_comment/<int:pk>/', ForumCommentDeleteView.as_view(), name='comment_delete'),
    path('forum_form/', views.ForumCreateView, name='forum_form'),
    path('sections/<section_slug>/', views.ForumSection, name='section'),

    path('<str:username>/', ProfileView.as_view(), name='profile_view'),

    path('', BlogListView.as_view(), name='homepage'),
]
