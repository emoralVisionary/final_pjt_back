from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.list, name="list"),
    path('<int:movie_id>/', views.detail, name="detail"),
]
