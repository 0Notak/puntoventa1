# control/views.py
from django.shortcuts import render, redirect
from .forms import VentaForm
from .models import Venta, Sucursal
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
import datetime
from django.core.paginator import Paginator
# Vista para login (usaremos Django Auth)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirigir a la página deseada después de login
            return redirect('registro')  # Redirige a la página de registro
    else:
        form = AuthenticationForm()
    return render(request, 'control/login.html', {'form': form})

# Vista para el formulario de registro de ventas

@login_required
def registro_view(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro')
    else:
        form = VentaForm()

    # Filtrar ventas del día para mostrarlas
    ventas = Venta.objects.filter(fecha=date.today())

    # Calcular el total de ventas del día, usando la propiedad 'total' en el modelo
    total_ventas = sum(venta.total for venta in ventas)

    # Resumen de ventas por sucursal (calculamos el total de cada sucursal)
    resumen = ventas.values('sucursal__nombre').annotate(total=Sum('cantidad'))

    return render(request, 'control/registro.html', {
        'form': form,
        'ventas': ventas,
        'resumen': resumen,
        'total_ventas': total_ventas
    })
# Vista para mostrar los registros con gráficos
@login_required
def reporte_view(request):
    hoy = datetime.date.today()

    # Filtra las ventas por la fecha de hoy
    registros = Venta.objects.filter(fecha=hoy)

    # Sumar por sucursal y obtener el total de ventas por sucursal
    resumen = registros.values('sucursal__nombre').annotate(total=Sum('precio'))

    # Calcular el total de todas las ventas para mostrarlo en el template
    total_ventas = sum(item['total'] for item in resumen)

    # Pasar los datos al template
    return render(request, 'control/reporte.html', {
        'resumen': resumen, 
        'total_ventas': total_ventas
    })

@login_required
def concentrado_view(request):
    # Obtener todos los registros de ventas sin importar la fecha
    ventas = Venta.objects.all()

    # Configurar la paginación: 10 registros por página
    paginator = Paginator(ventas, 10)  # Mostrar 10 ventas por página
    page_number = request.GET.get('page')  # Obtener el número de página de la solicitud
    page_obj = paginator.get_page(page_number)  # Obtener los objetos paginados

    return render(request, 'control/concentrado.html', {'page_obj': page_obj})