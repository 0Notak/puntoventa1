from django import forms
from .models import Venta, Jugo

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['jugo', 'cantidad', 'sucursal']

    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        self.fields['precio'] = forms.DecimalField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        jugo = cleaned_data.get('jugo')
        if jugo:
            self.instance.precio = jugo.precio
        return cleaned_data
