from django import forms
from .models import Game, Comment

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'description', 'genre', 'fsk', 'date_published', 'pdf', 'price', 'picture']
        widgets = {
            'genre': forms.Select(choices=Game.GAME_GENRES),
            'fsk': forms.Select(choices=Game.FSK_TYPES),
            'user': forms.HiddenInput(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'user': forms.HiddenInput(),
            'game': forms.HiddenInput(),
        }

class CommentReportForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['reported']
        widgets = {
            'comment_id': forms.HiddenInput(),
        }

class SearchForm(forms.ModelForm):
    name = forms.CharField(required=False)
    # genre = forms.Select(choices=Game.GAME_GENRES)

    class Meta:
        model = Game
        fields = ['name', 'description']
