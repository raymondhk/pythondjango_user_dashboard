from django.shortcuts import render, redirect
from django.contrib import messages
from models import User

# Create your views here.
def index(request):
    return render(request, ('users/index.html'))

def register(request):
    return render(request, ('users/register.html'))

def registration(request):
    results = User.objects.basic_validator(request.POST)
    if results[0]:
        request.session['id'] = results[1].id
        request.session['register'] = True
        request.session['login'] = False
        return redirect('/success')
    else:
        for tag, error in results[1].iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/success')