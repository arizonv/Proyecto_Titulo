from django.urls import path
from . import views
from . import roles_permisos


app_name = 'account'

urlpatterns = [
    path('index/', views.index, name='index'),

    path('registro-user/', views.register, name='register'),

    path('update-user/', views.update_user, name='update_user'),
    path('update-pass/', views.update_password, name='update_password'),
 
    path('user-list/', views.user_list, name='user_list'),
    path('user-admin-list/', views.user_admin_list, name='user_admin_list'),
    path('user-delete/<int:pk>/', views.user_delete, name='user_delete'),
]
