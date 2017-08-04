from django.contrib.auth import login
from django.shortcuts import render, redirect
import django.views as views
from django.urls import reverse
from .models import *
from .forms import PlayerForm, UserForm, ActivityForm, TagForm
from random import choice
import re


# =============================================================================
def home(request):
    return render(request, 'website/home.html')


# =============================================================================
def new_activity(request):
    activity_form = ActivityForm()
    tag_form = TagForm()
    success = {'tag': None, 'activity': None}
    tag_list = Tag.objects.all()
    if request.method == 'POST':
        tag_form = TagForm(request.POST)
        activity_form = ActivityForm(request.POST)
        if activity_form.is_valid():
            activity = Activity.objects.create(text=activity_form.cleaned_data['text'])
            print('creating activity', activity.text)
            success['activity'] = 'Activité créée avec succès'
            tags_request = request.POST.get('tags')
            print(request.POST, tags_request)
            if tags_request:
                tags = [int(x) for x in tags_request.split(',')]
                print('tags request !', tags)
                objects = [Tag.objects.get(id=tag) for tag in tags]
                activity.tags.add(*objects)
        if tag_form.is_valid():
            Tag.objects.create(name=tag_form.cleaned_data['name'])
            success['tag'] = 'Tag créée avec succès'
    return render(request, 'website/new_activity.html', context={
        'genders': genders,
        'activity_form': activity_form,
        'tag_form': tag_form,
        'success': success,
        'tag_list': tag_list,
    })


# =============================================================================
def replace_balise(match, request):
    print('called :', match, request)
    if match.group(0) == '<H>':
        return choice(request.filter(gender='H').all()).name
    elif match.group(0) == '<F>':
        return choice(request.filter(gender='F').all()).name
    elif match.group(0) == '<N>':
        return choice(request.all()).name


def playing(request, game_id):
    print('=' * 80)
    print('Playing the game number', game_id)
    current_game = Game.objects.get(id=game_id)
    players = current_game.player_set
    print('request :', players)
    text = Activity.random().text
    print('selected :', text)
    act = re.sub(r'<.>', lambda x, _=players: replace_balise(x, _), text)
    print('new ? :', act)
    return render(request, 'website/playing.html', context={
        'current_game': current_game,
        'activity': act,
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
