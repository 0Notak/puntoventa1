from django import forms
from .models import DetalleVenta, Jugo

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['jugo', 'cantidad']  # No incluir 'sucursal' aquí

    def __init__(self, *args, **kwargs):
        super(DetalleVentaForm, self).__init__(*args, **kwargs)
        self.fields['precio'] = forms.DecimalField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        jugo = cleaned_data.get('jugo')
        if jugo:
            self.instance.precio = jugo.precio
        return cleaned_data
