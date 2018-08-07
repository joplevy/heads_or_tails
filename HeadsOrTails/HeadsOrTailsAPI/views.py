from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse
from django.db import models
from django import forms

from HeadsOrTailsAPI.models import Game

ETHER_UNIT = (
    ('W', 'wei'),
    ('G', 'gwei'),
    ('F', 'finney'),
    ('E', 'ether'),
)

class GameForm(forms.ModelForm):
	class Meta:
		model = Game
		fields = ['title', 'head', 'value']
	# title = forms.CharField()
	key = forms.CharField()
	unit = forms.ChoiceField(choices=ETHER_UNIT, initial='W')
	# head = forms.BooleanField()
	# value = forms.IntegerField()

class GameList(ListView):
	model = Game
	ordering = ['-id']

class GameCreate(CreateView):
	model = Game
	form_class = GameForm
	# fields = ['title', 'head', 'value']

	def get_success_url(self):
		print("shouldbe after")
		# self.request.session['success_message'] = 'Everything is fine'
		return reverse('games')	

	def form_valid(self, form):
		form.instance.author = self.request.user
		print(form.instance.title)
		if(form.instance.title == "toto"):
			# print(form.instance.key)
			# form.add_error("custom", "toto error")
			return super().form_invalid(form)
		return super().form_valid(form)

def sign_up_in(request):
	if request.method == "POST":
		if 'sign_in' in request.POST:
			form = AuthenticationForm(data=request.POST)
			username = request.POST.get('username', False)
			password = request.POST.get('password', False)
			user = authenticate(username=username, password=password)
			if user is not None and user.is_active:
				login(request, user)
				return redirect('home')
			args={
			'sign_up_form': UserCreationForm(),
			'sign_in_form': form,
			}
			return render(request, "login.html", args)
		elif 'sign_up' in request.POST:
			form = UserCreationForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('login')
			args={
			'sign_up_form': form,
			'sign_in_form': AuthenticationForm(),
			}
			return render(request, "login.html", args)
		else:
			args={
			'sign_up_form': UserCreationForm(),
			'sign_in_form': AuthenticationForm(),
			}
			return render(request, "login.html", args)
	else:
		args={
			'sign_up_form': UserCreationForm(),
			'sign_in_form': AuthenticationForm(),
			}
		return render(request, "login.html", args)
