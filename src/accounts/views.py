from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth import logout
from src.accounts.forms import UserProfileForm, CustomLoginForm

from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:cross-auth')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('accounts:cross-auth')


@method_decorator(login_required, name='dispatch')
class CrossAuthView(View):

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect("accounts:login")

        if request.user.is_superuser:
            return redirect("admins:dashboard")

        return redirect("staff:dashboard")


@method_decorator(login_required, name='dispatch')
class UserUpdateView(View):

    def get(self, request):
        form = UserProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, template_name='accounts/user_update_form.html', context=context)

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            messages.success(request, "Your profile updated successfully")
            form.save(commit=True)
        context = {'form': form}
        return render(request, template_name='accounts/user_update_form.html', context=context)