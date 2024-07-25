from django import forms
from Games.models import Comment, Game


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'comment_id': forms.HiddenInput(),
        }

class GameEditForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'description', 'date_published', 'genre', 'fsk', 'pdf', 'price', 'picture']
        widgets = {
            'game_id': forms.HiddenInput(),
        }
