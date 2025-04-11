# control/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
import datetime
from django.core.paginator import Paginator
from .forms import DetalleVentaForm


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



from .models import Venta, DetalleVenta, Sucursal, Jugo
from .forms import DetalleVentaForm

@login_required
def registro_view(request):
    # Utiliza la sesión para mantener el carrito entre solicitudes
    if 'carrito' not in request.session:
        request.session['carrito'] = []

    carrito = request.session['carrito']

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'agregar':
            form = DetalleVentaForm(request.POST)
            if form.is_valid():
                # Agregar al carrito con conversiones necesarias
                item = {
                    'jugo_id': form.cleaned_data['jugo'].id,
                    'jugo_nombre': form.cleaned_data['jugo'].nombre,
                    'cantidad': form.cleaned_data['cantidad'],
                    'precio': float(form.cleaned_data['jugo'].precio)  # Convertir a float
                }
                carrito.append(item)
                request.session.modified = True  # Marca la sesión como modificada

        elif action == 'pagar':
            if carrito:
                sucursal_id = request.POST.get('sucursal')
                sucursal = get_object_or_404(Sucursal, id=sucursal_id)  # Maneja el caso en que la sucursal no exista
                venta = Venta.objects.create(sucursal=sucursal)
                for item in carrito:
                    jugo = Jugo.objects.get(id=item['jugo_id'])
                    DetalleVenta.objects.create(
                        venta=venta,
                        jugo=jugo,
                        cantidad=item['cantidad'],
                        precio=item['precio']
                    )
                # Limpia el carrito después de pagar
                carrito.clear()
                request.session.modified = True
                return redirect('registro')

        elif action == 'limpiar':
            # Limpiar el carrito
            carrito.clear()
            request.session.modified = True
            return redirect('registro')

    else:
        form = DetalleVentaForm()

    ventas = Venta.objects.filter(fecha=date.today())
    total_ventas = sum(venta.total for venta in ventas)
    resumen = ventas.values('sucursal__nombre').annotate(total=Sum('detalleventa__cantidad'))

    return render(request, 'control/registro.html', {
        'form': form,
        'carrito': carrito,
        'ventas': ventas,
        'resumen': resumen,
        'total_ventas': total_ventas,
        'sucursales': Sucursal.objects.all()  # Pasa las sucursales al template
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