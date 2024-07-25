from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from .forms import GameEditForm, CommentEditForm
import statistics
# from .models import Game
from Games.models import Comment, Game

@staff_member_required(login_url='/useradmin/login/')
def comment_delete(request):
    if request.method == 'POST':
        if "delete" in request.POST:
            comment_id = request.POST['comment_id']
            Comment.objects.get(id=comment_id).delete()
        elif "unreport" in request.POST:
            comment_id = request.POST['comment_id']
            comment = Comment.objects.get(id=comment_id)
            comment.reported = False
            comment.save()
        return redirect('comment-delete')
    else:
        user = request.user
        can_delete = user.can_delete()
        comments = Comment.objects.filter(reported=True)
        for comment in comments:
            comment.rating = int(comment.rating)
        context = {'can_delete': can_delete,
                   'all_the_comments': comments,
                  }
        can_delete = False
        if not user.is_anonymous:
            can_delete = user.can_delete()
        return render(request, 'comment-delete.html', context)

@staff_member_required(login_url='/useradmin/login/')
def game_edit_delete(request, pk: str):
    game_id = pk
    if request.method == 'POST':
        user = request.user
        if 'edit' in request.POST:
            form = GameEditForm(request.POST, request.FILES)
            if form.is_valid():
                game = Game.objects.get(id=game_id)
                # if game.user.id!=request.user.id:
                #     return redirect('game-detail', game.game.id)
                new_name = form.cleaned_data['name']
                game.name = new_name
                new_description = form.cleaned_data['description']
                game.description = new_description
                new_genre = form.cleaned_data['genre']
                game.genre = new_genre
                new_fsk = form.cleaned_data['fsk']
                game.fsk = new_fsk
                new_price = int(form.cleaned_data['price'])
                game.price = new_price
                new_pdf = form.cleaned_data['pdf']
                if new_pdf:
                    game.pdf = new_pdf
                new_picture = form.cleaned_data['picture']
                if new_picture:
                    game.picture = new_picture
                game.save()
        elif 'delete' in request.POST:
            Game.objects.get(id=game_id).delete()
        return redirect('game-list')

    else:
        can_delete = False
        user = request.user
        if not user.is_anonymous:
            can_delete = user.can_delete()
        game = Game.objects.get(id=game_id)
        # game.date_published=str(game.date_published)
        form = GameEditForm(instance=game)
        rating = -1
        comments = Comment.objects.filter(game=game)
        if len(comments)>0:
            ratings=[]
            for c in comments:
                c.rating=int(c.rating)
                crating = c.rating or 0
                ratings.append(int(crating))
            rating = round(statistics.mean(ratings))
        context = {'form': form,
                   'can_delete': can_delete,
                   'game': game,
                   'rating': rating
                  }
        return render(request, 'game-edit-delete.html', context)


def comment_edit_delete(request, pk: str):
    comment_id = pk
    if request.method == 'POST':
        user = request.user
        if 'edit' in request.POST:
            form = CommentEditForm(request.POST)
            if form.is_valid():
                comment = Comment.objects.get(id=comment_id)
                if comment.user.id!=request.user.id:
                    return redirect('game-detail', comment.game.id)
                new_rating = int(form.cleaned_data['rating'])
                comment.rating = new_rating
                new_text = form.cleaned_data['text']
                comment.text = new_text
                comment.save()
        elif 'delete' in request.POST:
            comment = Comment.objects.get(id=comment_id)
            game = comment.game
            comment.delete()
            return redirect('game-detail', game.id)
        return redirect('game-detail', comment.game.id)
    else:
        can_delete = False
        user = request.user
        if not user.is_anonymous:
            can_delete = user.can_delete()
        comment = Comment.objects.get(id=comment_id)
        print(comment.user.id)
        print(user.id)
        if comment.user.id!=user.id:
            return redirect('game-detail', comment.game.id)
        comment.timestamp=str(comment.timestamp)
        form = CommentEditForm(request.POST or None, instance=comment)
        rating = -1
        context = {'form': form,
                   'can_delete': can_delete,
                   'comment': comment
                  }
        return render(request, 'comment-edit-delete.html', context)
