from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterUserForm
from .forms import WordForm
from .models import hangmanWord, hangman_Game
import random

difficult_kid = 1
difficult_pro = 3

def index(request):
    return render(request, 'hangmanGame/index.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            messages.success(request, ("There was a error in logging in. Try again!!"))
            return redirect('login')
    else: 
        return render(request, 'registration/login.html')
    
def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            messages.success(request, "Registration successful!!")
            login(request, user)
            return redirect('gameMode')
    if request.method == "GET":          
        form = RegisterUserForm()
        context = {'form': form}
        return render(request, 'registration/register_user.html', context)

def gameMode(request):
    return render(request, 'hangmanGame/gameMode.html')

@login_required
def logout_user(request):
    messages.success(request, "You were logged out!!")
    logout(request)
    return redirect('login')

@require_POST
def add_word(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Word added successfully!')
            return redirect('add_word')
    else:
        form = WordForm()
    return render(request, 'hangmanGame/add_word.html', {'form': form})

@login_required
def gameReport(request):
    if request.method == "GET":
        games = hangman_Game.objects.filter(user=request.user).order_by('-game_id')
        return render(request, 'hangmanGame/gameReport.html', {'games': games})

def changeDifficult(done, difficult):
    if done:
        if difficult >= 1 and difficult < 5:
            difficult += 1
    elif difficult == 5 or difficult >= 1:
        difficult -= 1

def get_word(difficult):
    if difficult <= 3:
        easy_words = hangmanWord.objects.filter(difficulty="easy")
        word = random.choice(easy_words)
        return word
    else:
        hard_words = hangmanWord.objects.filter(difficulty='hard')
        word = random.choice(hard_words)
        return word
        
@login_required
def kidMode(request):
    if request.method == "GET":
        word = get_word(difficult_kid)
        game = hangman_Game(user=request.user, answer=word.text, difficulty=word.difficulty, mode='Kid Mode')
        game.save()
        game.image = "/static/hangmanGame/Images/hang0.png"
        game.display = "_ " * len(word.text)
        context = {'guessed': [], 'game': game}
        return render(request, 'hangmanGame/kidmode.html', context)
    else:
        return button_kid(request)

@login_required
def button_kid(request):
    game_id = int(request.POST['game_id'])
    game = hangman_Game.objects.get(game_id=game_id)
    answer = game.answer
    word_mean = hangmanWord.objects.get(text__exact = answer)
    
    if game.user != request.user:
        return render(request, 'hangmanGame/kidMode.html')
    
    cur_guess = request.POST['letter']
    guessed = list(game.guessed)
    
    if game.status == 'win' or game.status == 'lose':
        generate_finished_game_kid(game)
        return render(request, "hangmanGame/kidMode.html", {'guessed': guessed, 'game': game, 'word_mean': word_mean})
    
    if cur_guess not in guessed:
        guessed.append(cur_guess)
        game.guessed = "".join(guessed)
        game.save()
    
    word_to_display = ""
    match_num = 0
    
    for char in answer:
        if char in guessed:
            match_num += 1
            word_to_display += char + ' '
        else:
            word_to_display += '_ '
    
    if match_num == len(answer):
        game.status = "win"
        game.save()
    game.display = word_to_display
    
    num_wrong_guess = 0
    for char in guessed:
        if char not in answer:
            num_wrong_guess += 1
    if num_wrong_guess >= 7:
        game.status = 'lose'
        game.save()
        num_wrong_guess = 7
    game.image = "/static/hangmanGame/Images/hang" + str(num_wrong_guess) + ".png"
    word_mean = hangmanWord.objects.get(text__exact = answer)
    return render(request, 'hangmanGame/kidMode.html', {'guessed': guessed, 'game': game, 'word_mean': word_mean})

def generate_finished_game_kid(game):
    answer = game.answer
    guessed = list(game.guessed)
    if game.status == 'win':
        done = True
        changeDifficult(done, difficult_kid)
        game.display = " ".join(list(answer)) 
        game.image = "/static/hangmanGame/Images/hang" + str(wrong_num(guessed, answer)) + ".png"
        return
    else:
        done = False
        changeDifficult(done, difficult_kid)
        game.display = word_to_display(guessed, answer)
        game.image = "/static/hangmanGame/Images/hang7.png"
        return

def word_to_display(guessed, answer):
    display = ""
    match_num = 0
    for char in answer:
        if char in guessed:
            match_num += 1
            display += char + " "
        else:
            display += '_ '
    return display

def wrong_num(guessed, answer):
    num_wrong_guess = 0
    for char in guessed:
        if char not in answer:
            num_wrong_guess += 1
    if num_wrong_guess >= 7:
        num_wrong_guess = 7
    return num_wrong_guess

@login_required
def proMode(request):
    if request.method == "GET":
        word = get_word(difficult_pro)
        game = hangman_Game(user=request.user, answer=word.text, difficulty=word.difficulty, mode='Pro Mode')
        game.save()
        game.image = "/static/hangmanGame/Images/hang0.png"
        game.display = "_ " * len(word.text)
        context = {'guessed': [], 'game': game}
        return render(request, 'hangmanGame/promode.html', context)
    else:
        return button_pro(request)

@login_required
def button_pro(request):
    game_id = int(request.POST['game_id'])
    game = hangman_Game.objects.get(game_id=game_id)
    answer = game.answer
    word_mean = hangmanWord.objects.get(text__exact = answer)
    
    if game.user != request.user:
        return render(request, 'hangmanGame/proMode.html')
    
    cur_guess = request.POST['letter']
    guessed = list(game.guessed)
    
    if game.status == 'win' or game.status == 'lose':
        generate_finished_game_pro(game)
        return render(request, "hangmanGame/proMode.html", {'guessed': guessed, 'game': game, 'word_mean': word_mean})
    
    if cur_guess not in guessed:
        guessed.append(cur_guess)
        game.guessed = "".join(guessed)
        game.save()
    
    word_to_display = ""
    match_num = 0
    
    for char in answer:
        if char in guessed:
            match_num += 1
            word_to_display += char + ' '
        else:
            word_to_display += '_ '
    
    if match_num == len(answer):
        game.status = "win"
        game.save()
    game.display = word_to_display
    
    num_wrong_guess = 0
    for char in guessed:
        if char not in answer:
            num_wrong_guess += 1
    if num_wrong_guess >= 7:
        game.status = 'lose'
        game.save()
        num_wrong_guess = 7
    game.image = "/static/hangmanGame/Images/hang" + str(num_wrong_guess) + ".png"
    word_mean = hangmanWord.objects.get(text__exact = answer)
    return render(request, 'hangmanGame/proMode.html', {'guessed': guessed, 'game': game, 'word_mean': word_mean})

def generate_finished_game_pro(game):
    answer = game.answer
    guessed = list(game.guessed)
    if game.status == 'win':
        done = True
        changeDifficult(done, difficult_pro)
        game.display = " ".join(list(answer)) 
        game.image = "/static/hangmanGame/Images/hang" + str(wrong_num(guessed, answer)) + ".png"
        return
    else:
        done = False
        changeDifficult(done, difficult_kid)
        game.display = word_to_display(guessed, answer)
        game.image = "/static/hangmanGame/Images/hang7.png"
        return