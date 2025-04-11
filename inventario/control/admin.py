from django.contrib import admin

# Register your models here.
from .models import Jugo, Sucursal, Venta  # Importa los modelos

# Registrar los modelos en el panel de administración
admin.site.register(Jugo)
admin.site.register(Sucursal)
admin.site.register(Venta)