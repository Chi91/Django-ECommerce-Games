from django.urls import path
from . import views

urlpatterns = [
    path('show/', views.game_list, name='game-list'),
    path('show/<int:pk>/', views.game_detail, name='game-detail'),
    path('show/<int:pk>/vote/<str:up_or_down>/', views.vote, name='game-vote'),
    path('add/', views.game_create, name='game-create'),
    path('delete/<int:pk>/', views.game_delete, name='game-delete'),
    path('report/<int:pk>/', views.comment_report, name='comment-report')
]
