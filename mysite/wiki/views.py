from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Welcome to the wiki index!")

def detail(request, post_id):
	return HttpResponse("You're looking at post %s." % post_id)

def edit(request, post_id):
	logged_in = True
	if logged_in:
		response = "You're editing post %s as a logged in user."
		return HttpResponse(response % post_id)
	else:
		response = "You're trying to edit post %s but aren't logged in."
		return HttpResponse(response % post_id)
