from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
import uuid

# JWT Imports
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# DRF API Imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserTask


# --- 1. JWT Custom Serializer (Email ke zariye Token lene ke liye) ---
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
  def validate(self, attrs):
    login_id = attrs.get("username") or attrs.get("email")
    password = attrs.get("password")

    try:
      user_obj = User.objects.get(email=login_id)
      attrs["username"] = user_obj.username
    except User.DoesNotExist:
      pass

    return super().validate(attrs)


class EmailTokenObtainPairView(TokenObtainPairView):
  serializer_class = EmailTokenObtainPairSerializer


# --- 2. Protected API View (Token laga kar Tasks dekhne ke liye) ---
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_tasks_list(request):
  # Sirf usi user ke tasks aayein ge jiska token hoga
  todos = UserTask.objects.filter(user=request.user)
  task_list = [
      {"name": t.name, "number": t.number, "message": t.message} for t in todos
  ]
  return Response({"tasks": task_list})


# --- 3. Web Views (Browser ke liye) ---
def signup(request):
  if request.method == "POST":
    name = request.POST.get("name")
    email = request.POST.get("email")
    password = request.POST.get("password")

    if User.objects.filter(email=email).exists():
      return render(
          request,
          "register.html",
          {
              "error": "Yeh email pehle se registered hai! Doosri email use karein.",
              "tab": "signup",
          },
      )

    unique_username = str(uuid.uuid4())[:8]

    user = User.objects.create_user(
        username=unique_username, email=email, password=password, first_name=name
    )

    login(request, user)
    return redirect("index")

  return render(request, "register.html", {"tab": "signup"})


def login_view(request):
  if request.method == "POST":
    email = request.POST.get("email")
    password = request.POST.get("password")

    try:
      matched_user = User.objects.get(email=email)
      user = authenticate(
          request, username=matched_user.username, password=password
      )
    except User.DoesNotExist:
      user = None

    if user is not None:
      login(request, user)
      return redirect("index")
    else:
      return render(
          request,
          "register.html",
          {
              "error": "Ghalat Email ya Password! Dobara koshish karein.",
              "tab": "login",
          },
      )

  return render(request, "register.html", {"tab": "login"})


@login_required(login_url="/login/")
def index_view(request):
  todos = UserTask.objects.filter(user=request.user)

  if request.method == "POST":
    name = request.POST.get("name")
    number = request.POST.get("number")
    message = request.POST.get("message")

    if name and message:
      UserTask.objects.create(
          user=request.user, name=name, number=number, message=message
      )
      return redirect("index")

  return render(request, "index.html", {"todos": todos})


def logout_view(request):
  logout(request)
  return redirect("login_view")