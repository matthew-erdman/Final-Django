from django.urls import path
from wiki.views import *

urlpatterns = [
	path('', Index.as_view(), name='index'),
	path('user/', UserView.as_view(), name='user'),
	path('create/', Create.as_view(), name='create'),
	path('fail/', Fail.as_view(), name='fail'),
	path('register/', Register.as_view(), name='register'),
    path('<int:post_id>/', Detail.as_view(), name='detail'),
    path('<int:post_id>/edit/', Edit.as_view(), name='edit'),
]
