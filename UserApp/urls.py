from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('create-article/', views.create_article, name='create_article'),
    path('edit-article/<int:article_id>/', views.edit_article, name='edit_article'),
    path('moderate-articles/', views.moderate_articles, name='moderate_articles'),
    path('toggle-article/<int:article_id>/', views.toggle_article_status, name='toggle_article_status'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
]
