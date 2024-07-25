from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import GameForm, CommentForm, SearchForm, CommentReportForm
from .models import Game, Comment
from Shoppingcart.models import ShoppingCart
import random

def random_wordsize():
    return random.randrange(2,13)


@login_required(login_url='/useradmin/login/')
def game_list(request):
    if request.method == 'POST':
        games_found = Game.objects.all()
        games_total = games_found.count()
        search_string_name = request.POST['name']
        if search_string_name:
            games_found = games_found.filter(name__contains=search_string_name)

        search_description = request.POST['description']
        if search_description:
            games_found = games_found.filter(description__contains=search_description)

        search_rating_min = int(request.POST['rating_min'])
        search_rating_max = int(request.POST['rating_max'])
        for g in Game.objects.all():
            rating = g.get_rating()
            print(search_rating_min, search_rating_max, g.get_rating())
            if not ((rating >= search_rating_min and rating <= search_rating_max) or rating==-1):
                games_found = games_found.exclude(id=g.id)
                print(len(games_found),g.id)

        max_results = int(request.POST['max_results']) or 20
        if max_results > len(games_found):
            max_results = len(games_found)
        else:
            games_found = games_found[:max_results]

        form_in_function_based_view = SearchForm()
        found_something=len(games_found)>0
        user = request.user
        context = {
                   'site': 'game-list',
                   'form': form_in_function_based_view,
                   'games_found': games_found,
                   'games_found_count': len(games_found),
                   'games_total': games_total,
                   'show_results': True,
                   'found_something': found_something,
                   'random_wordsize': random_wordsize,
                   'search_string_name': search_string_name,
                   'search_string_description': search_description,
                   'search_string_rating_min': search_rating_min,
                   'search_string_rating_max': search_rating_max,
                   'search_string_max_results': int(request.POST['max_results']),
                   'can_delete': user.can_delete(),
                   'can_edit': user.can_edit()}
        return render(request, 'game-list.html', context)

    else:
        user = request.user
        games_found = Game.objects.all()
        max_results = 20
        form_in_function_based_view = SearchForm()
        found_something=len(games_found)>0
        context = {
                   'site': 'game-list',
                   'form': form_in_function_based_view,
                   'games_found': games_found,
                   'games_found_count': len(games_found),
                   'games_total': len(games_found), #no filter means every game is on display
                   'show_results': False,
                   'found_something': found_something,
                   'random_wordsize': random_wordsize,
                   'search_string_name': '',
                   'search_string_description': '',
                   'search_string_rating_min': 1,
                   'search_string_rating_max': 5,
                   'search_string_max_results': max_results,
                   'can_delete': user.can_delete(),
                   'can_edit': user.can_edit()}
        return render(request, 'game-list.html', context)

# def game_list(request):
#     template_name = 'game-list.html'  # Default: game_list.html
#     context = {}
#     context["all_the_games"] = Game.objects.all()
#     return render(request, template_name, context=context)

@login_required(login_url='/useradmin/login/')
def game_detail(request, pk):
    game = Game.objects.get(pk=pk)
    user = request.user
    # Add comment
    if request.method == 'POST':
        if 'add_comment' in request.POST:
            #limit to one comment per user
            if not Comment.objects.filter(game=game, user=request.user).count()>0:
                form = CommentForm(request.POST)
                form.instance.game = game
                form.instance.user = user
                if form.is_valid():
                    form.save()
                else:
                    print(form.errors)
        if 'add_shopping_cart' in request.POST:
            user = request.user
            if "quantity" in request.POST:
                quantity=request.POST["quantity"]
                ShoppingCart.add_item(user,game,quantity)
            else:
                ShoppingCart.add_item(user,game)
    comments = Comment.objects.filter(game=game)
    can_comment = Comment.objects.filter(game=game, user=request.user).count()<=0
    if len(comments)>0:
        for c in comments:
            c.rating=int(c.rating)
    rating = game.get_rating()
    context = {'that_one_game': game,
            'comments_for_that_one_game': comments,
            'comment_form': CommentForm,
            'can_comment': can_comment,
            'random_wordsize': random_wordsize,
            'user': user,
            'can_delete': user.can_delete(),
            'can_edit': user.can_edit(),
            'rating': rating}
    template_name = 'game-detail.html'  # Default: game_list.html
    return render(request, template_name, context=context)

    # else:
    #     user = request.user
    #     ShoppingCart.add_item(user,game)

@login_required(login_url='/useradmin/login/')
def comment_report(request, pk):
    if request.method == 'POST':
        form = CommentReportForm(request.POST)
        comment = Comment.objects.get(pk=pk)
        if not comment.reported:
            comment.reported=True
            comment.save()
        return redirect('game-detail', comment.game.id)
    else:  # request.method == 'GET'
        form = CommentReportForm()
        comment = Comment.objects.get(pk=pk)
        context = {'form': form,
                   'comment': comment,
                   'random_wordsize': random_wordsize}
        return render(request, 'comment-report.html', context)

@staff_member_required(login_url='/useradmin/login/')
def game_create(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            # print("I saved new game")
        else:
            pass
            print(form.errors)
            context = {'form': form}
            return render(request, 'game-create.html', context)
        return redirect('game-list')
    else:  # request.method == 'GET'
        form = GameForm()
        context = {
        'form': form,
        'random_wordsize': random_wordsize
        }
        return render(request, 'game-create.html', context)

# @staff_member_required(login_url='/useradmin/login/')
# def game_edit(request):
#     if request.method == 'POST':
#         form = GameForm(request.POST, request.FILES)
#         form.instance.user = request.user
#         if form.is_valid():
#             form.save()
#             print("I saved new game")
#         else:
#             pass
#             print(form.errors)
#             context = {
#             'form': form,
#             'random_wordsize': random_wordsize
#             }
#             return render(request, 'game-edit.html', context)
#         return redirect('game-list')
#     else:  # request.method == 'GET'
#         form = GameForm()
#         context = {'form': form}
#         return render(request, 'game-create.html', context)

@staff_member_required(login_url='/useradmin/login/')
def game_delete(request, pk):
    model = Game
    context_object_name = 'that_one_game'  # Default: game
    if request.method == 'POST':
        if Game.objects.get(pk=pk):
            Game.objects.get(pk=pk).delete()
        return redirect('game-list')
    else:  # request.method == 'GET'
        form = GameForm()
        context = {
        'form': form, context_object_name: model.objects.get(pk=pk),
        'random_wordsize': random_wordsize
        }
        return render(request, 'game-delete.html', context)

def vote(request, pk: str, up_or_down: str):
    comment = Comment.objects.get(id=int(pk))
    user = request.user
    comment.vote(user, up_or_down)
    return redirect('game-detail', pk=comment.game.pk)
