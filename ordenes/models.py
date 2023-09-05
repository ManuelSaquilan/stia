from django.db import models

# Create your models here.
class Comercio(models.Model):
    id = models.AutoField(primary_key=True)
    comercio = models.CharField(max_length=30,verbose_name='Comercio',null=False) # VERBOSE nombre de las filas en superususario #
    titular = models.CharField(max_length=30,verbose_name='Titular de Comercio',null=False)
    activo = models.BooleanField(verbose_name='Activo',null=True,default=True)

    def __str__(self):
        fila = self.comercio
        return fila
    
    def get_fields(self):
        return [
            (field.verbose_name, field.value_from_object(self))
            for field in self.__class__._meta.fields[1:]
        ]
    
    class Meta:
        verbose_name = 'Comercio'
        verbose_name_plural = 'Comercios'
        db_table = 'comercio'
        ordering = ['comercio']
                

class Empleado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30,verbose_name="Nombre y Apellido",null=False)
    legajo = models.IntegerField(verbose_name='Legajo N°',null=False)
    dni = models.IntegerField(verbose_name='DNI',null=False)
    activo = models.BooleanField(verbose_name='Activo',null=True,default=True)

    # ESTO SE MUESTRA EN EL ADMIN SUPERUSUARIO #
    def __str__(self):
        fila = self.nombre
        return fila

    def get_fields(self):
        return [
            (field.verbose_name, field.value_from_object(self))
            for field in self.__class__._meta.fields[1:]]

    class Meta:
        verbose_name='empleado'
        verbose_name_plural='empleados'
        db_table='empleado'
        ordering = ['nombre']

class Orden(models.Model):
    id = models.AutoField(primary_key=True)
    empleado = models.ForeignKey(Empleado,on_delete=models.CASCADE,null=False, blank=False)
    comercio = models.ForeignKey(Comercio,on_delete=models.CASCADE,null=False, blank=False)
    importe = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Total Compra',null=False)
    cuotas = models.IntegerField(verbose_name='Cuotas',null=False)
    valorcuota = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Valor de Cuota',null=False)
    fecha = models.DateField(verbose_name='Fecha de Compra', auto_now=True,null=False)
    
    def __str__(self):
        fila = "Empleado: " + str(self.empleado) + " - " + " Comercio: " + str(self.comercio) + " Importe: " + str(self.importe) + " Cuotas: " + str(self.cuotas)+ " Valor de Cuota: " + str(self.valorcuota) + " fecha y hora: " + str(self.fecha)
        return fila
    
    def get_fields(self):
        return [
            (field.verbose_name, field.value_from_object(self))
            for field in self.__class__._meta.fields[1:]
        ]

    class Meta:
        verbose_name='orden'
        verbose_name_plural='ordenes'
        db_table = 'ordenes_orden'
    

class Margen(models.Model):
    id=models.AutoField(primary_key=True)
    margen = models.IntegerField(verbose_name='Margen',null=False)

    def __str__(self):
        fila = "Margen: " + str(self.margen)
        return fila

    class Meta:
        verbose_name='margen'
        verbose_name_plural='margenes'
        db_table = 'margen'