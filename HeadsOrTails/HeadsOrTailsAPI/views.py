from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect

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
