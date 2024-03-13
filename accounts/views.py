from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth import login,logout
from .forms import UserRegistrationForm,UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.views import View
from django.shortcuts import redirect

class UserRegistrationView(FormView):
    template_name = "accounts/user_registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home') 

    # check validation
    def form_valid(self,form):
        # print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

# login view 
class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('profile')

# logout view
# class UserLogoutView(LogoutView):
#     def get_success_url(self):
#         if self.request.user.is_authenticated:
#             logout(self.request)
#         return reverse_lazy('home')
    
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse_lazy('home'))


class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})