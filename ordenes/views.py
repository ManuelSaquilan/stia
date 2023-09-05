from typing import Any
from django.db import models
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from .models import Orden, Comercio, Empleado, Margen
from django.views import View

from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic.detail import DetailView

import datetime
from django.db.models import Q

from django.contrib import messages

from django.template.loader import render_to_string
from weasyprint import HTML

from django.http import HttpResponseRedirect
from datetime import date, timedelta



# Create your views here.
#  O R D E N E S #

class OrdenBaseView(View):
    login_url = "/login/"
    redirect_field_name = "landing"
    template_name = "orden.html"
    model         = Orden
    fields        = "__all__"
    success_url   = reverse_lazy('ordenes:orden_all')

    def get_queryset(self):
        return Orden.objects.all().order_by('-id')[:8]
    

class OrdenListView(OrdenBaseView,ListView):
    '''ESTO ME PERMITE CREAR UNA VISTA CON LOS ORDENES'''

class OrdenDetailView(OrdenBaseView,ListView):
    template_name = 'orden_template.html'

class OrdenCreateView(CreateView):
    empleados = Empleado.objects.all()
    comercios = Comercio.objects.all()
    margen =  Margen.objects.all()[:1]
    template_name = 'orden_create.html'
    extra_context = {"tipo": "Crear Orden",'empleados':empleados,
                     'comercios':comercios,'limite':margen}
  
    success_url   = reverse_lazy('ordenes:orden_all')
    


   


def CrearOrden(request,empleado,comercio,margen):
    disponible=margen

    if request.method == 'POST':
        
        emp = request.POST.get('empleado')
        empleado = Empleado.objects.get(pk=emp)
        com = request.POST.get('comercio')
        comercio = Comercio.objects.get(pk=com)
        imp = request.POST.get('importe')
        cuo = request.POST.get('cuotas')
        fecha = request.POST.get('fecha')
        print(type(cuo))
        print(type(imp))
        valorcuota = int(imp)/int(cuo)
        nuevaorden = Orden(empleado= empleado, comercio= comercio, importe= imp, cuotas=cuo ,valorcuota=valorcuota,fecha=fecha)
        nuevaorden.save()
        #ultimaorden= Orden.objects.last()
        #idorden= ultimaorden.id
        #return redirect('ordenes:imprime_last')
        return redirect('ordenes:orden_all')
    
    if request.method == 'GET':
        orden = Orden.objects.all()
        comercios = Comercio.objects.filter(Q(id=comercio))
        empleados = Empleado.objects.filter(Q(id=empleado))
        empleado= empleado
        comercio = comercio
        margen=margen
        messages.success(request,'Empleado y Comercio agregado con exito')
        return render(request, 'orden_create.html',{'empleado':empleado,'margen':margen,
                'comercios':comercios,'comercio':comercio,'orden':orden,'empleados':empleados
            })





class OrdenUpdateView(OrdenBaseView,UpdateView):
    template_name = 'orden_create.html'
    extra_context = {"tipo": "Actualizar Orden"}

# C O M E R C I O S #
class ComercioBaseView(View):
    template_name = "comercio.html"
    model         = Comercio
    fields        = "__all__"
    success_url   = reverse_lazy('ordenes:comercio_all')

class ComercioListView(ComercioBaseView, ListView):
    '''ESTO ME PERMITE CREAR UNA VISTA CON LOS COMERCIOS'''

class ComercioDetailView(ComercioBaseView, ListView):
    template_name = 'comercio_template.html'

class ComercioCreateView(ComercioBaseView, CreateView):
    template_name = 'comercio_create.html'
    extra_context = {"tipo": "Crear Comercio"}

class ComercioUpdateView(ComercioBaseView, UpdateView):
    template_name = 'comercio_update.html'
    extra_context = {"tipo": "Actualizar Comercio"}

# E M P L E A D O S #

class EmpleadoBaseView(View):
    template_name = "empleado.html"
    model         = Empleado
    fields        = "__all__"
    success_url   = reverse_lazy('ordenes:empleado_all')

class EmpleadoListView(EmpleadoBaseView, ListView):
    '''ESTO ME PERMITE CREAR UNA VISTA CON LOS EMPLEADOS'''


class EmpleadoDetailView(EmpleadoBaseView, ListView):
    template_name = 'empleado_template.html'
    

class EmpleadoCreateView(EmpleadoBaseView, CreateView):
    template_name = 'empleado_create.html'
    extra_context = {"tipo": "Crear Empleado"}

class EmpleadoUpdateView(EmpleadoBaseView, UpdateView):
    template_name = 'empleado_update.html'
    extra_context = {"tipo": "Actualizar Empleado"}

#def nuevaorden(request):
#    resultado = Empleado.objects.all()
#    resultado2 = Comercio.objects.all()
#    return render(request,"orden_create.html",{"nombres":resultado,"comercios":resultado2})


def busca(request):
    
        busqueda = request.POST.get("buscarempleado")
        busqueda2 = request.POST.get("buscarcomercio")
        empleados =Empleado.objects.all().filter(activo=True)
        comercios =Comercio.objects.all().filter(activo=True)
        empleado =Empleado.objects.all()
        ordenes=Orden.objects.all()
        margen = Margen.objects.all()[:1]
        hoy = datetime.date.today()
        mes=hoy.month
        if mes<10:
            mes='0'+str(mes)
        fechahoy = int(str(hoy.year)+mes)
        valorcuota=0
        margendisponible=0
        limite=0
        for i in margen:
            margendisponible = margendisponible +i.margen
            limite = limite +i.margen

        if busqueda and busqueda2:
            
            empleado = Empleado.objects.filter(Q(id__icontains = busqueda))
            comercio = Comercio.objects.filter(Q(id__icontains = busqueda2))
            ordenes = Orden.objects.filter(Q(empleado_id=busqueda))
            saldo = 0
            for orden in ordenes:
                valorcuota = orden.importe/orden.cuotas
                if orden.cuotas > 1:
                    for i in range(1,orden.cuotas):
                        print(i)
                        mes1=orden.fecha.month
                        if mes1<10:
                            mes1='0'+str(mes1)
                        fecha = int(str(hoy.year)+mes1)
                        if fecha >= fechahoy:
                            saldo += valorcuota
                else:
                    saldo += valorcuota
            margendisponible = margendisponible - saldo
            return render(request, 'preconsulta.html',{'comercio':comercio,
                        'comercios':comercios,'empleado':empleado,
                        'empleados':empleados,'margen':'{0:.2f}'.format(margendisponible),
                        'limite':limite})
            
            #return HttpResponse({'margen':'{0:.2f}'.format(margendisponible)})
                        
        else:
            return render(request, 'preconsulta.html',{'comercios':comercios,
                        'empleados':empleados,})

# MARGEN EMPLEADO
def MargenEmpleado(request):
        busqueda = request.POST.get("margenempleado")
        fecha1 = date.today()-timedelta(days=60)
        fecha2 = date.today()
        empleados =Empleado.objects.all().filter(activo=True)
        empleado =Empleado.objects.all()
        ordenes=Orden.objects.all()
        margen = Margen.objects.all()[:1]
        hoy = datetime.date.today()
        mes=hoy.month
        if mes<10:
            mes='0'+str(mes)
        fechahoy = int(str(hoy.year)+mes)
        valorcuota=0
        margendisponible=0
        limite=0

        for i in margen:
            margendisponible = margendisponible +i.margen
            limite = limite +i.margen
        if busqueda:
            empleado = Empleado.objects.filter(Q(id__icontains = busqueda))
            ordenes = Orden.objects.filter(Q(empleado_id=busqueda))
            saldo = 0
            for orden in ordenes:
                valorcuota = orden.importe/orden.cuotas
                if orden.cuotas > 1:
                    for i in range(1,orden.cuotas):
                        mes1=orden.fecha.month
                        if mes1<10:
                            mes1='0'+str(mes1)
                        fecha = int(str(orden.fecha.year)+mes1)
                        if fecha >= fechahoy:
                            saldo += valorcuota
                else:
                    saldo += valorcuota
            margendisponible = margendisponible - saldo
            
            ordenes =Orden.objects.filter(Q(empleado_id=busqueda)).filter(fecha__range=(fecha1,fecha2)).order_by('-id')
            return render(request, 'consulta_margen.html',{'empleado':empleado,
                        'empleados':empleados,'margen':'{0:.2f}'.format(margendisponible),
                        'limite':limite,'orden':ordenes})
                       
        else:
            return render(request, 'consulta_margen.html',{'empleados':empleados,})

def CompraEmpleado(request):
        busqueda = request.POST.get("empleado")
        fecha1 = request.POST.get("fecha1")
        fecha2 = request.POST.get("fecha2")
        empleados =Empleado.objects.all()

        ordenes=Orden.objects.all()

        if busqueda:
            empleado = Empleado.objects.filter(Q(id__icontains = busqueda))
            ordenes =Orden.objects.filter(Q(empleado_id=busqueda)).filter(fecha__range=(fecha1,fecha2)).order_by('-id')
            return render(request, 'consulta_compras.html',{
                        'empleados':empleados,'orden':ordenes})
                       
        else:
            return render(request, 'consulta_compras.html',{'empleados':empleados,})

def OrdenEmpleado(request):
        busqueda = request.POST.get("ordenempleado")
        ordenes=Orden.objects.all()
        
        if busqueda:
            ordenes = Orden.objects.filter(Q(id=busqueda))
            return render(request, 'consulta_orden.html',{'orden':ordenes})
                       
        else:
            return render(request, 'consulta_orden.html',)
        
# impresion de comprobantes #

class Imprimir(View):
    success_url   = reverse_lazy('ordenes:orden_all')
    
    #def get(self,request,*args, **kwargs):
    def get(self,request,*args, **kwargs):
        #ultimaorden= Orden.objects.last()
        ultimaorden= Orden.objects.get(pk=self.kwargs['pk'])
        dni = ultimaorden.empleado.dni
        mes=ultimaorden.fecha.month
        year=ultimaorden.fecha.year
        context = {
                'id':ultimaorden.id,
                'empleado':ultimaorden.empleado,
                'comercio':ultimaorden.comercio,
                'importe':ultimaorden.importe,
                'cuotas':ultimaorden.cuotas,
                'fecha':ultimaorden.fecha,
                'valorcuota':ultimaorden.valorcuota,
                'mes':mes,
                'year':year,
                'dni':dni
                }
        html = render_to_string("orden_pdf.html", context)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "attachment; report.pdf"
        #response["Content-Disposition"] = "inline; report.pdf"

        HTML(string=html).write_pdf(response)
        
        return response

class ImprimirUltima(View):
    
    success_url   = reverse_lazy('ordenes:orden_all')
    
    def get(self,request,*args, **kwargs):
        ultimaorden= Orden.objects.last()
        #ultimaorden= Orden.objects.get(pk=self.kwargs['pk'])
        context = {
                'id':ultimaorden.id,
                'empleado':ultimaorden.empleado,
                'comercio':ultimaorden.comercio,
                'importe':ultimaorden.importe,
                'cuotas':ultimaorden.cuotas,
                'fecha':ultimaorden.fecha,
                }
        html = render_to_string("orden_pdf.html", context)

        response = HttpResponse(content_type="application/pdf")
        #response["Content-Disposition"] = "attachment; report.pdf"
        response["Content-Disposition"] = "inline; report.pdf"

        HTML(string=html).write_pdf(response)
        
        return response


def Buscaempleado(request):
    
    if request.method == 'POST':

        buscaempleado = request.POST.get("updateempleado")
        
        empleado =Empleado.objects.all()
        
        if buscaempleado:
            
            updateempleado = Empleado.objects.filter(Q(id__icontains = buscaempleado))
            
            return render(request, 'empleado.html',{'empleado':updateempleado,'empleado_list':empleado})
            
            #return HttpResponse({'margen':'{0:.2f}'.format(margendisponible)})
                        
        else:
            return render(request, 'empleado.html',{'empleado':empleado,})

    if request.method == 'GET':

        empleado =Empleado.objects.all()
        
        return render(request, 'empleado.html',{'empleado_list':empleado,})