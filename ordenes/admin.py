from django.contrib import admin
from .models import Comercio, Empleado, Orden, Margen
# Register your models here.


class ComercioAdmin(admin.ModelAdmin):
    search_fields = ['comercio']
    ordering = ['comercio']

class EmpleadoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    ordering = ['nombre']

class OrdenAdmin(admin.ModelAdmin):
    autocomplete_fields = ['empleado','comercio']

class MargenAdmin(admin.ModelAdmin):
    search_fields = ['margen']
    ordering = ['margen']

admin.site.register(Comercio, ComercioAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Orden, OrdenAdmin)
admin.site.register(Margen, MargenAdmin)