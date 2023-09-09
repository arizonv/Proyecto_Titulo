from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    UpdateView,
    FormView,
    DetailView,
    ListView,
    DeleteView,
)
from .models import User, Rol 
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserAdminCreationForm

#decorador
from .decorators import has_permission
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

#alonso ( al final se asignaran los prmisos para cada funcion)
# @method_decorator(has_permission(['Listar_usuarios']), name='dispatch')

# view Sub Index de administracion
class IndexView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/index.html'
    login_url = reverse_lazy('Login:login')
        
    def get_object(self):
        return self.request.user

# FUNCIONES DE USUARIO
@method_decorator(has_permission(['leer user']), name='dispatch')
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'

class UserAdminListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'admin/user_admin.html'
    context_object_name = 'users'

    def get_queryset(self):
        roles_to_filter = ['trabajador']
        return User.objects.filter(roles__nombre__in=roles_to_filter)

class UserDeleteView(DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('account:user_list')
    context_object_name = 'user'

class RegisterView(CreateView):
    model = User
    form_class = UserAdminCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('account:index')

    def form_valid(self, form):
        cliente_role, created = Rol.objects.get_or_create(nombre='cliente')
        user = form.save(commit=False)
        user.roles = cliente_role
        user.save()

        return super().form_valid(form)

class UpdateUserView(LoginRequiredMixin, UpdateView):

    model = User
    login_url = reverse_lazy('Login:login')
    template_name = 'accounts/update_user.html'
    fields = ['name', 'apellidos', 'email']
    success_url = reverse_lazy('account:index')

    def get_object(self):
        return self.request.user

class UpdatePasswordView(LoginRequiredMixin, FormView):

    template_name = 'accounts/update_password.html'
    login_url = reverse_lazy('Login:login')
    success_url = reverse_lazy('account:index')
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_password_validation'] = False
        return context




index = IndexView.as_view()
register = RegisterView.as_view()
update_user = UpdateUserView.as_view()
update_password = UpdatePasswordView.as_view()
user_list = UserListView.as_view()
user_admin_list = UserAdminListView.as_view()
user_delete = UserDeleteView.as_view()






