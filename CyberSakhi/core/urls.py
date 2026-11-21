from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("check/", views.detector, name="detector"),
    path("reports/new/", views.report_create, name="report_create"),
    path("reports/<int:pk>/", views.report_detail, name="report_detail"),
    path("awareness/", views.awareness, name="awareness"),
    path("awareness/<int:pk>/", views.article_detail, name="article_detail"),
    path("quiz/", views.quiz, name="quiz"),
    path("saved-guides/", views.saved_guides, name="saved_guides"),
    path("awareness/<int:pk>/save/", views.toggle_saved_article, name="toggle_saved_article"),
    path("safety-checklist/", views.safety_checklist, name="safety_checklist"),
    path("trends/", views.trends, name="trends"),
]
