from django.urls import path
from wiki.views import index, detail, edit, login

urlpatterns = [
	path('', index.as_view(), name='index'),
	path('login/', login.as_view(), name='login'),
    path('<int:post_id>/', detail.as_view(), name='detail'),
    path('<int:post_id>/edit/', edit.as_view(), name='edit'),
]
