from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

def home(request):
    user = request.user
    context = {
            'user': user,
            'site': 'home'
            }
    template_name = './home.html'  # Default: game_list.html
    return render(request, template_name, context=context)
