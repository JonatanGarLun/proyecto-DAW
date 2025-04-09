from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from battlebound_tactics.forms import RegistroForm

# Create your views here.

class HomePageView(TemplateView, LoginRequiredMixin):
    template_name = 'app/home.html'

class RegistroPageView(FormView):
    template_name = 'app/registro_usuario.html'
    form_class = RegistroForm
    success_url = reverse_lazy('battlebound_tactics:')

class LoginUserView(LoginView):
    template_name = 'registration/login.html'