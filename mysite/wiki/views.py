from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Entry, Comment

# Create your views here.
def index(request):
    return HttpResponse("Welcome to the wiki index!")

def detail(request, post_id):
	entry = get_object_or_404(Entry, pk=post_id)
	return render(request, 'wiki/detail.html', {'entry': entry}, {'logged_in': True})

def edit(request, post_id):
	logged_in = True
	if logged_in:
		response = "You're editing post %s as a logged in user."
		return HttpResponse(response % post_id)
	else:
		response = "You're trying to edit post %s but aren't logged in."
		return HttpResponse(response % post_id)
