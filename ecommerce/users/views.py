from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('inventory:products')  # Redirect to products page

    def form_valid(self, form):
        # Save the user and log them in after successful registration
        response = super().form_valid(form)
        login(self.request, self.object)  # self.object is the saved user
        return response
