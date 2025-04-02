from http import client
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from e_learning.models import CustomUser, Question, Profile  
from django.views.decorators.csrf import csrf_exempt
import requests
from lumaai import LumaAI 
import time

from .utils import query_genai


def home(request):
    if request.user.is_authenticated:
        return render(request, "home_final.html")
    return redirect('login')


def signup_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('signup')

        # Create a new user with the custom user model
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, "signup_final.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')

    return render(request, "login_final.html")

# @csrf_exempt
# def submit_problem(request):
#     if request.method == "POST":
#         # if not request.user.is_authenticated:
#         #     messages.error(request, "You need to log in to submit a problem.")
#         #     return redirect('login')
        
#         problem_statement = request.POST.get('problem_statement')
#         print(problem_statement)
#         gemini_resp = query_genai(problem_statement)
#         print(gemini_resp)





def submit_problem(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You need to log in to submit a problem.")
            return redirect('login')

        # Get the problem statement from the form
        problem_statement = request.POST['problem_statement']
        
        # Step 1: Pass the problem statement to Gemini for a detailed explanation
        gemini_prompt = query_genai(problem_statement)
        
        # Step 2: Send the prompt to LumaAI for video generation
        video_generation = generate_video_from_prompt(gemini_prompt)
        
        # Step 3: Poll for video status and download when completed
        video_url = poll_for_video(video_generation)
        
        # Save the question in the database
        User = get_user_model()  # This ensures you're using the correct user model
        user_instance = User.objects.get(id=request.user.id)
        Question.objects.create(user=user_instance, text=problem_statement, generated_response=gemini_prompt)

        return render(request, "problem_response_final.html", {
            'user_prompt':problem_statement,
            'gemini_prompt': gemini_prompt,
            'video_url': video_url
        })
    
    return render(request, "problem_form.html")



def generate_video_from_prompt(prompt):
    # # Call LumaAI API to generate a video
    # generation = client.generations.create(prompt=prompt)
    return ""

def poll_for_video(generation):
    # # Poll until the video generation is completed
    # completed = False
    # while not completed:
    #     generation = client.generations.get(id=generation.id)
    #     if generation.state == "completed":
    #         completed = True
    #     elif generation.state == "failed":
    #         raise RuntimeError(f"Generation failed: {generation.failure_reason}")
    #     time.sleep(3)
    
    # # Once completed, return the video URL
    # return generation.assets.video
    return ""

def user_dashboard(request, user_id):
    user = request.user
    user = CustomUser.objects.get(id=user_id)
    questions = Question.objects.filter(user=user).order_by('-timestamp')
    context = {
        'user': user,
        'questions': questions,
    }
    return render(request, 'dashboard.html', context)


def profile_view(request):
    # Fetch the logged-in user
    user = request.user  # The logged-in user, which is an instance of CustomUser
    profile = get_object_or_404(Profile, user=user)  # Fetch the user's profile data (optional, if using Profile)
    questions = Question.objects.filter(user=user)  # Get questions asked by the user

    context = {
        'user': user,
        'profile': profile,  # Profile data if available
        'questions': questions,  # User's questions
    }

    return render(request, 'profile_final.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

