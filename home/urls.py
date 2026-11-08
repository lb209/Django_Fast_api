from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # JWT API Routes (Postman ke liye)
    path(
        "api/token/",
        views.EmailTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path(
        "api/tasks/", views.api_tasks_list, name="api_tasks_list"
    ),  # Naya Task API Route
    
    # Browser / Template Routes
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login_view"),
    path("", views.index_view, name="index"),
    path("logout/", views.logout_view, name="logout"),
]