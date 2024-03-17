from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .forms import RegisterForm


class SignUpView(View):
    template_name = 'signup.html'
    form_class = RegisterForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account with username: "{username}" successfully created')
            return redirect(to='account:signin')
        return render(request, self.template_name, {'form': form})
