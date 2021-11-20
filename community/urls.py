from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # 게시글 목록
    path('post_list_create/', views.post_list_create),
    # 게시글 내용(디테일)
    path('detail/<int:post_pk>/', views.post_detail), 
    # 게시글 수정/삭제
    path('post/<int:post_pk>/', views.post_update_delete),

    # 게시글에 대한 댓글 목록
    path('comments/<int:post_pk>', views.comment_list),
    path('<int:post_pk>/comment/', views.create_comment),
    path('comment/<int:post_pk>/<int:comment_pk>/', views.comment_delete),
]
