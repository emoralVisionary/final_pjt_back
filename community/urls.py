from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # 게시글 목록
    path('', views.post_list),
    path('create/', views.post_create),
    # 게시글 내용(디테일)
    path('<int:post_pk>/', views.post_detail), 
    # 게시글 수정/삭제
    path('<int:post_pk>/update_delete/', views.post_update_delete),

    # 게시글에 대한 댓글 목록
    path('<int:post_pk>/comments/', views.comment_list_create),
    # 댓글 삭제
    path('<int:post_pk>/delete/<int:comment_pk>/', views.comment_delete),
]
