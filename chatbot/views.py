from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from dotenv import load_dotenv, find_dotenv
import openai
import os

# Load .env variables
load_dotenv(find_dotenv())

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@login_required
@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        if user_message:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_message}]
                )
                choices = response['choices'][0]
                bot_reply = choices['message']['content'].strip() if 'message' in choices else choices.get('text', '').strip()

            except openai.error.RateLimitError as e:
                print("OpenAI API error:", e)
                bot_reply = "API quota exceeded. Please check your OpenAI API plan and billing details."
            except Exception as e:
                print("OpenAI API error:", e)
                bot_reply = "Sorry, I couldn't process your request."

            return JsonResponse({'response': bot_reply})

    return render(request, 'chatbot.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('chatbot')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')
