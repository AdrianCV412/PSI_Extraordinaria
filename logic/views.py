import re
import json
from django.http import HttpResponseForbidden
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from datamodel import constants, models
from datamodel.models import Game, GameStatus, Move, counter_manager
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError


def anonymous_required(f):
    def wrapped(request):
        if request.user.is_authenticated:
            models.counter_manager.inc(models.counter_manager)
            return HttpResponseForbidden(errorHTTP(request, exception="Action restricted to anonymous users"))
        else:
            return f(request)
    return wrapped


def errorHTTP(request, exception=None):
    context_dict = {}
    context_dict[constants.ERROR_MESSAGE_ID] = exception
    return render(request, "mouse_cat/error.html", context_dict)

def index(request):
    return render(request, 'mouse_cat/index.html')

#Global counter for the current replay move
current_move = 0

@anonymous_required
def login_service(request):

    context_dict = {}
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        if user:
            request.session['user_id'] = user.id
            login(request, user)
            return redirect(reverse(index))
        else:
            context_dict['return_service'] = "Username/password is not valid"

    context_dict['user_form'] = forms.LoginForm()
    return render(request, 'mouse_cat/login.html', context_dict)

@anonymous_required
def signup_service(request):
    context_dict = {}
    special_chars = r"[\$#@!\*]"
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        signup_form = forms.SignupForm(data=request.POST)

        if len(password) < 6 and re.search(special_chars, password) is None:
            models.counter_manager.inc(models.counter_manager)
            return HttpResponse("<h1>Signup user</h1> The password is too short. It must contain at least 6 characters. This password is too common.")

        if len(password) < 6:
            models.counter_manager.inc(models.counter_manager)
            return HttpResponse("<h1>Signup user</h1> The password is too short. It must contain at least 6 characters.")

        if User.objects.filter(username=username).exists():
            models.counter_manager.inc(models.counter_manager)
            return HttpResponse("<h1>Signup user</h1> A user with that username already exists")

        if signup_form.is_valid():
            if password != password2:
                models.counter_manager.inc(models.counter_manager)
                return HttpResponse("<h1>Signup user</h1> Password and Repeat password are not the same")
            user = signup_form.save()
            user.set_password(user.password)
            request.session['user_id'] = user.id
            user.save()
            login(request, user)
            return redirect(reverse(index))

    context_dict['user_form'] = forms.SignupForm()
    return render(request, 'mouse_cat/signup.html', context_dict)

def counter_service(request):
    context_dict = {}
    context_dict['counter_global'] = models.counter_manager.get_current_value(models.counter_manager)
    return render(request, 'mouse_cat/counter.html', context_dict)

@login_required
def join_game_service(request, game_id = -1):

    context_dict = {}

    game_t = None

    if game_id == -1:
        for g in Game.objects.all():
            if g.mouse_user is None and g.cat_user is not None:
                if g.cat_user != request.user:
                    if game_t is None or game_t.id < g.id:
                        game_t = g;

        if game_t is None:
            models.counter_manager.inc(models.counter_manager)
            context_dict['msg_error'] = 'There is no available games'

        else:
            game_t.mouse_user = request.user
            game_t.save()
            request.session['game_selected'] = game_t.id
            context_dict['game'] = game_t
        return render(request, 'mouse_cat/join_game.html', context_dict)

    else:
        for g in Game.objects.all():
            if g.id == game_id:
                if g.mouse_user is None and g.cat_user is not None:
                    if g.cat_user != request.user:
                        game_t = g;

        if game_t is None:
            models.counter_manager.inc(models.counter_manager)
            context_dict['msg_error'] = 'There is no available games'

        else:
            game_t.mouse_user = request.user
            game_t.save()
            request.session['game_selected'] = game_t.id
            context_dict['game'] = game_t
        return render(request, 'mouse_cat/join_game.html', context_dict)



def logout_service(request):
    context_dict = {}
    if request.user.is_authenticated:
        context_dict['user'] = request.user.username
        request.session['counter'] = 0
        logout(request)
        return render(request, 'mouse_cat/logout.html', context_dict)
    return render(request, 'mouse_cat/index.html')

@login_required
def create_game_service(request):
    game = Game()
    game.cat_user = request.user
    game.save()
    context_dict = {}
    context_dict['game'] = game
    return render(request, 'mouse_cat/new_game.html', context_dict)

@login_required
def show_game_service(request):
    game = None
    context_dict = {}
    if 'game_selected' not in request.session.keys():
        request.session['game_selected'] = None
    for g in Game.objects.all():
        if request.session['game_selected'] == g.id:
            game = g

    context_dict['move_form'] = forms.MoveForm()

    if game == None:
        models.counter_manager.inc(models.counter_manager)
        errorHTTP(request, exception='No games selected')
    context_dict['game'] = game
    board = []
    for i in range(0,64):
        if g.cat1 == i:
            board.append(1)
        elif g.cat2 == i:
            board.append(1)
        elif g.cat3 == i:
            board.append(1)
        elif g.cat4 == i:
            board.append(1)
        elif g.mouse == i:
            board.append(-1)
        else:
            board.append(0)
    context_dict['board'] = board
    context_dict['odd_pos'] = [1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30,33,35,37,39,40,42,44,46,49,51,53,55,56,58,60,62]
    return render(request, 'mouse_cat/game.html', context_dict)

@login_required
def move_service(request):

    if request.method == "GET":
        models.counter_manager.inc(models.counter_manager)
        return HttpResponseNotFound(errorHTTP(request, exception="Move service not found"))

    if request.method == "POST":
        move_form = forms.MoveForm(data=request.POST)
        if move_form.is_valid():

            o = move_form.cleaned_data['origin']
            t = move_form.cleaned_data['target']

            g = None
            if 'game_selected' in request.session.keys():
                if Game.objects.filter(id=request.session['game_selected']).exists():
                    g = Game.objects.get(id=request.session['game_selected'])

            if g == None:
                models.counter_manager.inc(models.counter_manager)
                return HttpResponseNotFound(errorHTTP(request, exception="No game selected for the current move"))

            try:
                m_d = models.Move.objects.create(origin = o, target = t, player = request.user, game = g)
            except:
                models.counter_manager.inc(models.counter_manager)
                return HttpResponseNotFound(errorHTTP(request, exception="Invalid Move"))

            g = m_d.game

            context_dict = {}

            context_dict['game'] = g
            board = []
            for i in range(0,64):
                if g.cat1 == i:
                    board.append(1)
                elif g.cat2 == i:
                    board.append(1)
                elif g.cat3 == i:
                    board.append(1)
                elif g.cat4 == i:
                    board.append(1)
                elif g.mouse == i:
                    board.append(-1)
                else:
                    board.append(0)

            if g.status == GameStatus.FINISHED:
                if g.winner == 1:
                    context_dict['message'] = "Cats win!"
                elif g.winner == 0:
                    context_dict['message'] = "Mouse wins!"

            context_dict['board'] = board
            context_dict['odd_pos'] = [1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30,33,35,37,39,40,42,44,46,49,51,53,55,56,58,60,62]
            return render(request, 'mouse_cat/game.html', context_dict)



@login_required
def select_game_service(request, game_id = -1):
    context_dict = {}
    user = None

    if request.method == "GET":
        sel_game = None
        if game_id != -1:
            if Game.objects.filter(id=game_id).exists():
                sel_game = Game.objects.get(id=game_id)

            if sel_game == None:
                models.counter_manager.inc(models.counter_manager)
                return HttpResponseNotFound('<h1>Select Game</h1> Game does not exist')

            if sel_game.status == GameStatus.CREATED:
                models.counter_manager.inc(models.counter_manager)
                return HttpResponseNotFound(errorHTTP(request, exception="No mouse user in the game yet"))

            if sel_game.cat_user.id != request.user.id and sel_game.mouse_user.id != request.user.id:
                models.counter_manager.inc(models.counter_manager)
                return HttpResponseNotFound('<h1>Select Game</h1> Game does not have user as a player')

            request.session['game_selected'] = sel_game.id
            context_dict['move_form'] = forms.MoveForm()
            # ------------------------------------------------
            for g in Game.objects.all():
                if request.session['game_selected'] == g.id:
                    game = g

            context_dict['game'] = game
            board = []
            for i in range(0,64):
                if game.cat1 == i:
                    board.append(1)
                elif game.cat2 == i:
                    board.append(1)
                elif game.cat3 == i:
                    board.append(1)
                elif game.cat4 == i:
                    board.append(1)
                elif game.mouse == i:
                    board.append(-1)
                else:
                    board.append(0)

            if game.status == GameStatus.FINISHED:
                if game.winner == 1:
                    context_dict['message'] = "Cats win!"
                elif game.winner == 0:
                    context_dict['message'] = "Mouse wins!"

            context_dict['board'] = board
            context_dict['odd_pos'] = [1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30,33,35,37,39,40,42,44,46,49,51,53,55,56,58,60,62]
            return render(request, 'mouse_cat/game.html', context_dict)
            # ------------------------------------------------

        for g in Game.objects.all():

            if g.status == GameStatus.CREATED:
                if g.cat_user.id != request.user.id:
                    if 'games' in context_dict.keys():
                        context_dict['games'].append(g)
                    else:
                        context_dict['games'] = [g]

            if g.status == GameStatus.ACTIVE:
                if g.cat_user.id == request.user.id:
                    if 'games' in context_dict.keys():
                        context_dict['games'].append(g)
                    else:
                        context_dict['games'] = [g]
                if g.mouse_user != None:
                    if g.mouse_user.id == request.user.id:
                        if 'games' in context_dict.keys():
                            context_dict['games'].append(g)
                        else:
                            context_dict['games'] = [g]

            if g.status == GameStatus.FINISHED:
                if g.cat_user.id == request.user.id:
                    if 'games' in context_dict.keys():
                        context_dict['games'].append(g)
                    else:
                        context_dict['games'] = [g]
                if g.mouse_user != None:
                    if g.mouse_user.id == request.user.id:
                        if 'games' in context_dict.keys():
                            context_dict['games'].append(g)
                        else:
                            context_dict['games'] = [g]

        return render(request, 'mouse_cat/select_game.html', context_dict)

    elif request.method == "POST":
        request.session['selected_game'] = game_id


@login_required
def replay_game_service(request, game_id = -1):

    global current_move
    if request.method == "GET":
        sel_game = None
        if game_id == -1:
            models.counter_manager.inc(models.counter_manager)
            return HttpResponseNotFound('<h1>Replay Game</h1> No game specified for replay')

        else:
            context_dict = {}
            game = None
            for g in Game.objects.all():
                if g.id == game_id:
                    game = g

            if game == None:
                models.counter_manager.inc(models.counter_manager)
                return HttpResponseNotFound('<h1>Replay Game</h1> This game does not exist')

            if game.mouse_user != None:
                if game.cat_user.id != request.user.id and game.mouse_user.id != request.user.id:
                    models.counter_manager.inc(models.counter_manager)
                    return HttpResponseNotFound('<h1>Replay Game</h1> You did not take part in this game. Therefore you are not able to see the replay')

            if game.status != GameStatus.FINISHED:
                models.counter_manager.inc(models.counter_manager)
                return HttpResponseNotFound(errorHTTP(request, exception="This game is not finished"))

            context_dict['game'] = game
            request.session['game_selected'] = game.id

            board = []
            for i in range(0,64):
                if i in [0,2,4,6]:
                    board.append(1)
                elif i == 59:
                    board.append(-1)
                else:
                    board.append(0)
            context_dict['board'] = board
            context_dict['odd_pos'] = [1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30,33,35,37,39,40,42,44,46,49,51,53,55,56,58,60,62]
            current_move = 0
            return render(request, 'mouse_cat/replay_game.html', context_dict)

@login_required
def get_move_service(request):

    global current_move
    if request.method == 'GET':
        models.counter_manager.inc(models.counter_manager)
        return HttpResponseNotFound('Bad access to view method')

    if request.method == 'POST':

        if 'game_selected' not in request.session:
            models.counter_manager.inc(models.counter_manager)
            return HttpResponseNotFound('No game replay selected')

        else:
            game = None
            for g in Game.objects.all():
                if g.id == request.session['game_selected']:
                    game = g

            if game == None:
                models.counter_manager.inc(models.counter_manager)
                return HttpResponseNotFound('No game replay selected')

            shift = int(request.POST['shift'])

            moves = Move.objects.filter(game=game).order_by('id')

            #Next move
            if shift == 1:
                if current_move == len(moves):
                    move = moves[current_move+1]
                    previous = 1
                    next = 0
                    winner = None

                else:
                    move = moves[current_move]
                    previous = 1
                    next = 1
                    current_move = current_move + 1
                    winner = None

                if current_move == len(moves) and next != 0:
                    next = 0
                    if g.cat_turn == True:
                        winner = "Mouse"

                    else:
                        winner = "Cat"

                aux = { 'origin': move.origin, 'target': move.target, 'previous': previous, 'next': next, 'winner': winner }
                aux_dump = json.dumps(aux)

                return HttpResponse(aux_dump)

            elif shift == -1:

                if current_move == 0:
                    previous = 0
                    next = 1
                    winner = None
                    origin = None
                    target = None
                    aux = { 'origin': origin, 'target': target, 'previous': previous, 'next': next, 'winner': winner }
                    aux_dump = json.dumps(aux)
                    return HttpResponse(aux_dump)

                elif current_move > 0:

                    winner = None
                    next = 1

                    if current_move > 1:
                        previous = 1
                    else:
                        previous = 0

                    current_move = current_move - 1
                    move = moves[current_move]
                    aux = { 'origin': move.target, 'target': move.origin, 'previous': previous, 'next': next, 'winner': winner }
                    aux_dump = json.dumps(aux)
                    return HttpResponse(aux_dump)

                models.counter_manager.inc(models.counter_manager)
                return HttpResponseNotFound('Internal move retrieval error')

            models.counter_manager.inc(models.counter_manager)
            return HttpResponseNotFound('Internal move retrieval error')
