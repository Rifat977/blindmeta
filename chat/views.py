from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as auth_login, update_session_auth_hash
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import NewUserForm, RoomForm, ProfileForm
from django.http import HttpResponse, JsonResponse
import speech_recognition
from django.db.models import Q
import pyttsx3
from .talk import *
import json


# Create your views here.
@login_required
def home(request):
    rooms = Room.objects.all()
    context = {
        'rooms' : rooms
    }
    return render(request, 'pages/home.html', context)

@login_required
def chat(request, room_id):
    rooms = Room.objects.all()
    room = Room.objects.get(slug=room_id)
    messages = Message.objects.filter(room=room)
    context = {
        'room' : room,
        'rooms' : rooms,
        'messages' : messages
    }
    return render(request, 'pages/chat.html', context)

@login_required
def chatSearch(request):
    room_name = request.GET.get('search')
    if(room_name==""):
        rooms = Room.objects.all()
    else:
        try:
            rooms = Room.objects.filter(Q(name__icontains=room_name))
        except:
            rooms = Room.objects.all()
    context = {
        'rooms' : rooms
    }
    return render(request, 'pages/chat.html', context)

@login_required
def audio(request):
    text = say().lower()
    return JsonResponse({'message':text}, status=200)

@login_required
def vAssist(request):
    return render(request, 'pages/vassist.html')

@login_required
def runAssist(request):
    wishMe(request.user.username)
    while True:
        command = say().lower()
        if 'time' in command:
            time = time_now()
            result  = "Current time is " + time
            speak(result)
        elif 'news' in command or 'breaking news' in command or 'breakingnews' in command:
            if 'sports' in command:
                speak("Okay, I am finding sports news.")
                result = sports_news()
            else:
                speak("Okay, I am finding breaking news.")
                result = breaking_news()
            speak(result)
            return JsonResponse({'command':command, 'result':result}, status=200)
        elif 'sports' in command:
            speak("Okay, I am finding sports news.")
            result = sports_news()
            speak(result)
            return JsonResponse({'command':command, 'result':result, 'speak':True}, status=200)
        elif 'play' in command:
            video = command.replace("play", "")
            speak("Okay, I am playing "+video+" from youtube.")
            play_yt(video)
            result = "Music playing"
            return JsonResponse({'command':command, 'result':result}, status=200)
        elif 'stop' in command or 'exit' in command or 'sleep' in command:
            result = "Thanks giving your time!"
            speak(result)
            break
        elif 'name' in command:
            speak("I am Blind Meta. Your personal Virtual Assistant from Daffodil international university, department of software engineering")
    data = {
        'result' : result,
        'command' : command
    }
    return JsonResponse({'command':command, 'result':result}, status=200)

@login_required
def profile(request):
    if request.method == "POST":
        person = Profile.objects.get(user=request.user.id)
        form = ProfileForm(request.POST, request.FILES or None, instance=person)
        if form.is_valid():
            form.save()
    return render(request, 'pages/profile.html')

@login_required
def groupCreate(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            print("success/n")
        else:
            print(form.errors)
    return redirect('lifehack:chat-page')   


@login_required
def chatPage(request):
    rooms = Room.objects.all()
    context = {
        'rooms' : rooms
    }
    return render(request, 'pages/chat.html', context)

@unauthenticated_user
def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('lifehack:home')
        else:
            messages.info(request, 'Username or password is incorrect')
    return render(request, 'pages/login.html')

@unauthenticated_user
def Register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("lifehack:home")
        else:
            messages.error(request, form.errors)
        form = NewUserForm()
    return render(request, 'pages/register.html')

@login_required
def Logout(request):
    logout(request)
    return redirect('lifehack:login')