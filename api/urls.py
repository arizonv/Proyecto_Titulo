from django.urls import path
from .views import LoginAPIView,UserLogout,UserList,Register,ExcelReportView
from .transbank import TransbankCreateView, TransbankCommitView, TransbankReverseOrCancelView
from . import views

app_name = 'api'

urlpatterns = [
    path('log/', LoginAPIView.as_view(), name='login'),
    path('out/', UserLogout.as_view(), name='logout'),
    path('list-user/', UserList().as_view()),
    path('register-user/', Register().as_view()),
    # update_user
    # update_pass
    # Reporte
    path('generate_excel/', ExcelReportView.as_view(), name='generate_excel'),
    #transbank
    path('transbank/transaction/create', TransbankCreateView.as_view()),
    path('transbank/transaction/commit/<str:tokenws>', TransbankCommitView.as_view()),
    path('transbank/transaction/reverse-or-cancel/<str:tokenws>', TransbankReverseOrCancelView.as_view()),

    #funciones para movil
    path('reserva/codigo/', views.ReservaPorCodigoAPIView.as_view(), name='reserva-por-codigo'),
]

