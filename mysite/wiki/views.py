from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Entry, Comment

# Create your views here.
def index(request):
    if request.method == 'POST':
        # This tests if the form is the log *in* form
        if 'inputUsername' in request.POST.keys():
            # IF so, try to authenticate
            user = authenticate(username=request.POST['inputUsername'],
                password=request.POST['inputPassword'])
            if user is not None:
                # IF success, then use the login function so the session persists.
                login(request, user)
            else:
                pass
                # Message for failed login.
        # This tests if the form is the log *out* form
        elif 'logout' in request.POST.keys():
            # If so, don't need to check anything else, just kill the session.
            logout(request)
    # After we check the forms, set a flag for use in the template.
    loggedIn = request.user.is_authenticated
    # Find the template
    return render(request, 'wiki/index.html', {'loggedIn': loggedIn, 'user': request.user})

def detail(request, post_id):
    entry = get_object_or_404(Entry, pk=post_id)
    return render(request, 'wiki/detail.html', {'entry': entry})

def edit(request, post_id):
    logged_in = True
    if logged_in:
        response = "You're editing post %s as a logged in user."
        return HttpResponse(response % post_id)
    else:
        response = "You're trying to edit post %s but aren't logged in."
        return HttpResponse(response % post_id)
