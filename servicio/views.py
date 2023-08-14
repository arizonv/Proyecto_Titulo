from django.views.generic import ListView,CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cancha,TipoCancha,Agenda
from cliente.models import Reserva
from django.utils import timezone
from cliente.models import Cliente

from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone

from django.db.models import Q
from django.views.generic import ListView


class CanchaListView(ListView):
    model = Cancha
    template_name = 'servicios/listar.html'
    context_object_name = 'canchas'

class CanchaCreateView(CreateView):
    model = Cancha
    template_name = 'servicios/agregar.html'
    fields = '__all__'
    # form_class = ServicioForm

class CanchaUpdateView(UpdateView):
    model = Cancha
    template_name = 'servicios/actualizar.html'
    fields = '__all__'
    context_object_name = 'servicio'

class CanchaDeleteView(DeleteView):
    model = Cancha
    success_url = reverse_lazy('servicio-listar')

############# tipo ##############################
class TipoCanchaListView(ListView):
    model = TipoCancha
    template_name = 'servicios/tipo/listar.html'
    context_object_name = 'TipoCancha'

class TipoCanchaCreateView(CreateView):
    model = TipoCancha
    template_name = 'servicios/tipo/agregar.html'
    fields = '__all__'
    # form_class = ServicioForm

class TipoCanchaUpdateView(UpdateView):
    model = TipoCancha
    template_name = 'servicios/tipo/actualizar.html'
    fields = '__all__'
    context_object_name = 'TipoCancha'

class TipoCanchaDeleteView(DeleteView):
    model = TipoCancha
    success_url = reverse_lazy('TipoCancha-listar')


############# agenda ############################

from django.urls import reverse

class AgendaListView(ListView):
    model = Agenda
    template_name = 'agendas/listar.html'
    context_object_name = 'agendas'

    #ESTA FUNCION RECUERDA AL USUARIO ADMIN O TRABAJADOR RELLENAR SUS DATOS
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user

        if not (user.name and user.apellidos):
            messages.warning(self.request, "Completa tu nombre y apellidos antes de continuar.")
            profile_url = reverse('account:update_user') 
            return redirect(profile_url)

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = super().get_queryset()

        if query:
            queryset = queryset.filter(
                Q(cancha__tipo__nombre__icontains=query) |
                Q(cancha__numeracion__icontains=query) 
            )

        return queryset


class AgendaCreateView(CreateView):
    model = Agenda
    template_name = 'agendas/agregar.html'
    fields = '__all__'

class AgendaUpdateView(UpdateView):
    model = Agenda
    template_name = 'agendas/actualizar.html'
    fields = '__all__'
    context_object_name = 'agenda'

class AgendaDeleteView(DeleteView):
    model = Agenda
    success_url = reverse_lazy('agenda-listar')


#AQUI SE REALIZA EL PRIMER FILTRO YA QUE  NECESITAMOS QUE MUESTRE LOS TIPOS DE CANCHAS, LUEGO SEGUN EL TIPO.. LAS CANCHAS ASOCIADAS A ESE TIPO, LUEGO SEGUN LA CANCHAS MOSTRAR LAS AGENDAS(HORARIOS) ASOCIADAS AL TIPO DE CANCHA Y CANCHA ESCOGIDO ANTERIORMENTE.
class PreReserva(ListView):
    model = TipoCancha
    template_name = 'pre_reserva/pre_reserva.html'
    context_object_name = 'tipos_cancha'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('Login:login')

        try:
            cliente = request.user.cliente
        except Cliente.DoesNotExist:
            messages.warning(request, 'Necesitas los DATOS COMPLEMENTARIOS para realizar una reserva')
            return redirect('cliente:cliente_create')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        agendas_por_cancha = {}

        current_date = timezone.now().date()

        for tipo in context['tipos_cancha']:
            canchas = Cancha.objects.filter(tipo=tipo)
            agendas_por_cancha[tipo] = {}

            for cancha in canchas:
                agendas = Agenda.objects.filter(cancha=cancha, disponible=True)
                agendas_por_cancha[tipo][cancha] = agendas

        context['agendas_por_cancha'] = agendas_por_cancha

        return context






