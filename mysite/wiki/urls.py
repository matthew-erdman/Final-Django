from django.urls import path
from wiki.views import Index, Detail, Edit, Login

urlpatterns = [
	path('', Index.as_view(), name='index'),
	path('login/', Login.as_view(), name='login'),
    path('<int:post_id>/', Detail.as_view(), name='detail'),
    path('<int:post_id>/edit/', Edit.as_view(), name='edit'),
]
