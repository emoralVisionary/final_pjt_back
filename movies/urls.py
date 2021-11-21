from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # 전체 영화 리스트
    path('', views.index),
    path('<int:movie_id>/', views.detail, name="detail"),
    
    # 영화에 대한 리뷰 목록
    path('<int:movie_pk>/reviews/', views.review_list_create),
    # 영화에 대한 리뷰 수정/삭제
    path('<int:movie_pk>/reviews/<int:review_pk>/update_delete/', views.review_update_delete),

    # 리뷰에 대한 댓글 목록
    path('<int:review_pk>/comments/', views.review_comment_list_create),
    # 리뷰에 대한 댓글 삭제
    path('<int:review_pk>/delete/<int:review_comment_pk>/', views.review_comment_delete),
]
