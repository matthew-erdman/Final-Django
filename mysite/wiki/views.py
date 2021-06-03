from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
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
            if user is not None:
                # Valid uname/pw, log user in
                login(request, user = user)
            else:
                return redirect('fail', msg='could not authenticate user')
        else:
            return redirect('fail', msg=form.errors.as_data())

# User/Account view, handles login/logout and shows all posts by current user
class UserView(View):
    def get(self, request):
        loggedIn = request.user.is_authenticated
        user = request.user
        form = AuthenticationForm()
        # All entries from user who requested page
        entries = ''
        if loggedIn:
            entries = Entry.objects.filter(entry_author=user)

        context = {
        'loggedIn': loggedIn,
        'user': user,
        'form': form,
        'entries': entries,
        }
        return render(request, 'wiki/user.html', context)

    def post(self, request):
        # Handle login/logout POST forms and redirect back to the user page
        authUser(request)
        return redirect('user')

# Main, landing page view
class Index(View):
    def get(self, request):
        context = {
        'loggedIn': request.user.is_authenticated,
        'user': request.user,
        'entries': Entry.objects.all(),
        }
        return render(request, 'wiki/index.html', context)

# View for creating new posts
class Create(View):
    def get(self, request):
        context = {
        'loggedIn': request.user.is_authenticated,
        'user': request.user,
        }
        return render(request, 'wiki/create.html', context)

    # POST with a title and/or description was submitted; blank fields are filled
    def post(self, request):
        submitTitle = request.POST.get('submitTitle')
        submitText = request.POST.get('submitText')
        # If a field was left blank, fill with example text
        if not submitTitle:
            submitTitle = 'Example Title'
        elif not submitText:
            submitText = 'Example Text'

        # Create short description, truncating at 47 char + ellipsis; <= 50 char
        if len(submitText) > 50:

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
        context = {
        'loggedIn': request.user.is_authenticated,
        'user': request.user,
        'entry': get_object_or_404(Entry, pk=post_id),
        }
        return render(request, 'wiki/detail.html', context)

# Edit view allows users or administrators to edit the content of posts
class Edit(View):
    def get(self, request, post_id):
        context = {
        'loggedIn': request.user.is_authenticated,
        'user': request.user,
        'entry': get_object_or_404(Entry, pk=post_id),
        }
        return render(request, 'wiki/edit.html', context)

    # POST with a title and/or description was submitted; blank fields are filled
    # TODO: More robust handling of multiple and empty fields
    def post(self, request, post_id):
        entry = get_object_or_404(Entry, pk=post_id)
        loggedIn = request.user.is_authenticated
        editTitle = request.POST.get('editTitle')
        editText = request.POST.get('editText')

        # Verify that the editor is the OP or admin
        if request.user == entry.entry_author or request.user.username == 'admin':
            # Only update filled fields
            if editTitle:
                entry.entry_title = request.POST['editTitle']
            if editText:
                print('schmmovin')
                entry.entry_text = request.POST['editText']
                # Short desc, truncate at 47 char + ellipsis
                if len(request.POST['editText']) > 50:
                    entry.entry_text_short = request.POST['editText'][:47] + '...'
            # Save modified entry back into DB
            entry.save()
        else:
            # Invalid account attempted to edit
            return redirect('fail', msg='user does not have permission to edit this post')
        context = {
        'loggedIn': loggedIn,
        'user': request.user,
        'entry': entry,
        }
        return render(request, 'wiki/edit.html', context)

# View for registering new users
class Register(View):
    def get(self, request):
        context = {
        'form': UserCreationForm(),
        }
        return render(request, 'wiki/register.html', context)

    # POST with a uname/pw was submitted
    def post(self, request):
        allUsers = get_user_model().objects.all()
        form = UserCreationForm(data=request.POST)
        # Validate and clean form data
        if form.is_valid():
            form.save()
        else:
            return redirect('fail', msg=form.errors.as_data())

        # Redirect to user page
        return redirect('user')


# View to handle failures and unexpected behavior with error message
class Fail(View):
    def get(self, request, msg):
        context = {
        'msg': msg,
        }
        return render(request, 'wiki/fail.html', context)
