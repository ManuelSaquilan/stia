from django.urls import path, include
from . import views

from .views import      OrdenListView\
                    ,   OrdenDetailView\
                    ,   OrdenCreateView\
                    ,   OrdenUpdateView\
                    ,   ComercioListView\
                    ,   ComercioDetailView\
                    ,   ComercioCreateView\
                    ,   ComercioUpdateView\
                    ,   EmpleadoListView\
                    ,   EmpleadoDetailView\
                    ,   EmpleadoCreateView\
                    ,   EmpleadoUpdateView\
                    ,   busca\
                    ,   CrearOrden\
                    ,   Imprimir\
                    ,   ImprimirUltima\
                    ,   MargenEmpleado\
                    ,   OrdenEmpleado\
                    ,   CompraEmpleado\
                    ,   Buscaempleado
                    
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.auth.decorators import login_required

app_name = "ordenes"

urlpatterns = [
    path("", login_required(OrdenListView.as_view()), name="orden_all"),
    path("create/<int:empleado>/<int:comercio>/<margen>", CrearOrden,name="create_orden"),
    path('orden/create',OrdenCreateView.as_view(), name="orden_create"),
    path("<int:pk>/orden/detail/", OrdenDetailView.as_view(), name="orden_detail"),
    path("<int:pk>/orden/update/", OrdenUpdateView.as_view(), name="orden_update"),
    path("comercio", login_required(ComercioListView.as_view()), name="comercio_all"),
    path("comercio/create/", ComercioCreateView.as_view(), name="comercio_create"),
    path("<int:pk>/comercio/detail/", ComercioDetailView.as_view(), name="comercio_detail"),
    path("<int:pk>/comercio/update/", ComercioUpdateView.as_view(), name="comercio_update"),
    #path("empleado", login_required(EmpleadoListView.as_view()), name="empleado_all"),
    path("empleado", login_required(Buscaempleado), name="empleado_all"),
    path("empleado/create/", EmpleadoCreateView.as_view(), name="empleado_create"),
    path("create/preconsulta/", busca, name="preconsulta"),
    path("<int:pk>/empleado/detail/", EmpleadoDetailView.as_view(), name="empleado_detail"),
    path("<int:pk>/empleado/update/", EmpleadoUpdateView.as_view(), name="empleado_update"),
    path("<int:pk>/export/", Imprimir.as_view(), name="export_pdf"),
    path("export/", ImprimirUltima.as_view(), name="imprime_last"),
    path("consulta/margen/", MargenEmpleado, name="consulta_saldo"),
    path("consulta/orden/", OrdenEmpleado, name="consulta_orden"),
    path("consulta/compras/", CompraEmpleado, name="consulta_compras"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

