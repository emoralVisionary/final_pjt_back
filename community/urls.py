from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('',views.post_list_create),
    path('<int:post_pk>/',views.post_detail),
    path('<int:post_pk>/comment/', views.comment_list_create),
    path('<int:post_pk>/comment/<int:comment_pk>/', views.comment_detail),
 ]
