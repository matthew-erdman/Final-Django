from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Entry, Comment


# Reusable function to handle user login and logout
def authUser(request):
    if 'logout' in request.POST.keys():
        # User logging out
        logout(request)
    else:
        # User logging in
        form = AuthenticationForm(data=request.POST)
        # Validate and clean form data
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Authenticate form data
            user = authenticate(username = username, password = password)
            print(user)
            if user is not None:
                # Valid uname/pw, log user in
                login(request, user = user)
            else:
                return redirect('fail')
        else:
            return redirect('fail')

# User/Account based view, handles login/logout and shows all posts by current user
class UserView(View):
    def get(self, request):
        loggedIn = request.user.is_authenticated
        form = AuthenticationForm()
        entries = ''
        # All entries from user who requested page
        if loggedIn:
            entries = Entry.objects.filter(entry_author=request.user)

        return render(request, 'wiki/user.html', {'loggedIn': loggedIn, 'user': request.user, 'form': form, 'entries': entries})

    def post(self, request):
        # Handle login/logout POST forms and redirect back to the user page
        # TODO: Add login fail condition
        authUser(request)
        return redirect('user')

# Main, landing page view
class Index(View):
    def get(self, request):
        loggedIn = request.user.is_authenticated
        return render(request, 'wiki/index.html', {'loggedIn': loggedIn, 'user': request.user, 'entries': Entry.objects.all()})

    def post(self, request):
        # Redirect to login/logout page
        if 'loginRedirect' in request.POST.keys():
            return redirect('user')
        else:
            return redirect('fail')

# View for creating new posts
class Create(View):
    def get(self, request):
        loggedIn = request.user.is_authenticated
        return render(request, 'wiki/create.html', {'loggedIn': loggedIn, 'user': request.user})

    # POST with a title and/or description was submitted; blank fields are vaild
    def post(self, request):
        # TODO: 'Example' not filling, bad syntax for request.POST.get?
        submitTitle = request.POST.get('submitTitle', 'Example Title')
        submitText = request.POST.get('submitText', 'Example Text')
        if len(submitText) > 50:
            # Create short description, truncating at 47 char + ellipsis
            entry_text_short = submitText[:47] + '...'
        else:
            entry_text_short = submitText
        # New Entry object
        newEntry = Entry(entry_title=submitTitle, entry_text=submitText, entry_author=request.user, entry_text_short=entry_text_short)
        # Save into DB
        newEntry.save()
        # Redirect to detail page of newly created post
        return redirect('detail', post_id=newEntry.id)

# Detail view dumps information about one post
class Detail(View):
    def get(self, request, post_id):
        entry = get_object_or_404(Entry, pk=post_id)
        return render(request, 'wiki/detail.html', {'entry': entry})

# Edit view allows users or administrators to edit the content of posts
class Edit(View):
    def get(self, request, post_id):
        entry = get_object_or_404(Entry, pk=post_id)
        loggedIn = request.user.is_authenticated
        return render(request, 'wiki/edit.html', {'loggedIn': loggedIn, 'user': request.user, 'entry': entry})

    # POST with a title and/or description was submitted; blank fields are vaild
    # Should blank fields really be valid?
    # TODO: More robust handling of multiple and empty fields
    def post(self, request, post_id):
        entry = get_object_or_404(Entry, pk=post_id)
        loggedIn = request.user.is_authenticated
        # Verify that the user is logged in
        # TODO: Auth checks current logged in acct against op acct
        if loggedIn:
            if 'editTitle' in request.POST.keys():
                entry.entry_title = request.POST['editTitle']
            elif 'editText' in request.POST.keys():
                entry.entry_text = request.POST['editText']
                # Short desc, truncate at 47 char + ellipsis
                if len(request.POST['editText']) > 50:
                    entry.entry_text_short = request.POST['editText'][:47] + '...'
            # Save modified entry back into DB
            entry.save()
        else:
            return redirect('fail')
        return render(request, 'wiki/edit.html', {'loggedIn': loggedIn, 'user': request.user, 'entry': entry})

# View to handle failures
class Fail(View):
    def get(self, request):
        return render(request, 'wiki/fail.html')
