from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
    # ex: /wiki/5/
    path('<int:post_id>/', views.detail, name='detail'),
    # ex: /wiki/5/edit/
    path('<int:post_id>/edit/', views.edit, name='edit'),
]
