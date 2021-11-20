from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # 전체 영화 리스트
    path('', views.list, name="list"),
    path('<int:movie_id>/', views.detail, name="detail"),
    
    # 영화에 대한 리뷰 목록
    path('<int:movie_pk>/review/', views.review_list_create),
    # 영화에 대한 리뷰 수정/삭제
    path('<int:movie_pk>/review/<int:review_pk>/', views.review_update_delete),

    # 리뷰에 대한 댓글 목록
    path('<int:review_pk>/review_comment/', views.review_comment_list_create),
    # 리뷰에 대한 댓글 삭제
    path('<int:review_pk>/review_comment/<int:review_comment_pk>/', views.review_comment_delete),
]
