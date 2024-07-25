from django.urls import path
from . import views

urlpatterns = [
    path('comment/delete/', views.comment_delete, name='comment-delete'),
    path('comment/editdelete/<int:pk>/', views.comment_edit_delete, name='comment-edit-delete'),
    path('game/editdelete/<int:pk>/', views.game_edit_delete, name='game-edit-delete')
]
