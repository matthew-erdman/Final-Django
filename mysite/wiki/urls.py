from django.urls import path
from wiki.views import index, detail, edit

urlpatterns = [
	path('', index.as_view()),
    # ex: /wiki/5/
    path('<int:post_id>/', detail.as_view(), name="detail"),
    # ex: /wiki/5/edit/
    path('<int:post_id>/edit/', edit.as_view()),
]
