from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('post_list_create/', views.post_list_create),
    path('detail/<int:post_pk>/', views.post_detail), 
    path('post/<int:post_pk>/', views.post_update_delete),

    path('comments/<int:post_pk>', views.comment_list),
    path('<int:post_pk>/comment/', views.create_comment),
    path('comment/<int:post_pk>/<int:comment_pk>/', views.comment_delete),
]
