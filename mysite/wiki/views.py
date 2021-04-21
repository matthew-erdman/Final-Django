from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Entry, Comment

# Create your views here.
class index(View):
    def get(self, request):
        loggedIn = request.user.is_authenticated
        form = AuthenticationForm()
        return render(request, 'wiki/index.html', {'loggedIn': loggedIn, 'user': request.user, 'form': form})

    def post(self, request):
        # First check if we are coming here after hitting 'Logout'
        if 'logout' in request.POST.keys():
            # Then log out
            logout(request)
            # We load an empty form with no data
            form = AuthenticationForm()
        else:
            # We're if we got her after hitting 'Login'
            # So we match up the data with the form fields
            form = AuthenticationForm(data=request.POST)
            # Validate and clean the data
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                # Then authenticate and log in.
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request, user = user)
        loggedIn = request.user.is_authenticated
        form = AuthenticationForm()
        return render(request, 'wiki/index.html', {'loggedIn': loggedIn, 'user': request.user, 'form': form})

class detail(View):
    def get(self, request, post_id):
        entry = get_object_or_404(Entry, pk=post_id)
        return render(request, 'wiki/detail.html', {'entry': entry})

class edit(View):
    def get(self, request, post_id):
        entry = get_object_or_404(Entry, pk=post_id)
        loggedIn = request.user.is_authenticated
        return render(request, 'wiki/edit.html', {'loggedIn': loggedIn, 'user': request.user, 'entry': entry})

    def post(self, request, post_id):
        entry = get_object_or_404(Entry, pk=post_id)
        loggedIn = request.user.is_authenticated
        if loggedIn:
            if 'editTitle' in request.POST.keys():
                entry.entry_title = request.POST['editTitle']
                entry.save()
            elif 'editText' in request.POST.keys():
                entry.entry_text = request.POST['editText']
                entry.save()
        return render(request, 'wiki/edit.html', {'loggedIn': loggedIn, 'user': request.user, 'entry': entry})
