from django.contrib.auth import login
from django.shortcuts import render, redirect
import django.views as views
from django.urls import reverse
from .models import *
from .forms import PlayerForm, UserForm
from sqlite3 import IntegrityError


# =============================================================================
def home(request):
    return render(request, 'website/home.html')


# =============================================================================
def playing(request, game_id):
    current_game = Game.objects.get(id=game_id)
    return render(request, 'website/playing.html', context={
        'current_game': current_game,
    })

# =============================================================================
def create_game(request):
    new_game = Game.objects.create()
    return redirect(reverse('website:game', args=(new_game.id,)))
    # return render(request, 'website/new_game.html',
    #               context={'new_game': new_game})


# =============================================================================
def game(request, game_id):
    current_game = Game.objects.get(id=game_id)
    player_form = PlayerForm()
    integrity_error = ""
    if request.method == 'POST':
        player_form = PlayerForm(request.POST, prefix='player')
        try:
            Player.objects.create(
                name=player_form.data['name'],
                gender=player_form.data['gender'] if player_form.data['gender'] else 'N',
                game=current_game,
            )
        except:
            integrity_error = "Ce joueur existe déjà"

    player_list = current_game.player_set.all()
    return render(request, 'website/game.html', context={
        'current_game': current_game,
        'player_list': player_list,
        'player_form': player_form,
        'genders': genders,
        'integrity_error': integrity_error,
    })


# =============================================================================
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, prefix='user')
        if user_form.is_valid():
            user = User.objects.create_user(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password'],
            )
            user.save()
            login(request, user)
            return redirect(reverse('website:home'))
    else:
        user_form = UserForm(prefix='user')
    return render(request, 'registration/register.html', context={
        'user_form': user_form,
    })
