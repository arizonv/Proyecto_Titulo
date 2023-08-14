from django.urls import path , include
from django.conf import settings
from login import views
from .views import AdminLoginView,LoginView,LogoutView

app_name = 'Login'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('admin/', AdminLoginView.as_view(), name='loginAdmin'),
    path('out/', LogoutView.as_view(), name='logout')
]
  


  