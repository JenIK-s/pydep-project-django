from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignInForm
from .forms import SignUpForm
from .mixins import AnonymousRequiredMixin


def SignIn(request):
    if request.user.is_authenticated:
        return redirect('lesson:profile')
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lesson:profile')
    else:
        form = SignInForm()
    return render(request, 'users/signin.html', {'form': form})


class SignUp(AnonymousRequiredMixin, CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('users:signin')
    template_name = 'users/signup.html'
