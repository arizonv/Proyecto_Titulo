import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from django.core.exceptions import ValidationError

class UserAdminCreationForm(UserCreationForm):
    
    username = forms.CharField(max_length=20)
    name = forms.CharField(max_length=20)
    apellidos = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=40)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'name','apellidos', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 4:
            raise ValidationError('El nombre de usuario debe tener al menos 4 caracteres.')
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise ValidationError('El nombre de usuario solo puede contener letras y números.')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Este nombre de usuario ya está en uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está en uso.')

        if not re.match(r'^[\w\.-]+@(gmail\.com|yahoo\.com|outlook\.com)$', email):
            raise ValidationError('El correo electrónico debe ser de tipo @gmail.com, @yahoo.com, @outlook.com')

        return email


    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Las contraseñas no coinciden.')
        return password2



#FORMULARIOS PARA ROLES Y PERMISOS SI ES QUE ES NECESARIO 