from django.forms import *

from apps.website.models import Sugerencias


class SuggestForm(ModelForm):
    class Meta:
        model = Sugerencias
        fields = ['nombre', 'email', 'telefono', 'longitud', 'latitud', 'sugerencia']
        widgets = {
            'sugerencia': Textarea(attrs={'cols': 40, 'rows': 7,'col': 12, 'placeholder': 'Escribe tus sugerencias o comentarios aquí. Si estás interesado en contratar nuestros servicios, también puedes solicitar una inspección.', 'class': "form-control", 'aria-invalid': False, 'name': 'field-header-3'}),
            'nombre': TextInput(attrs={'col': 12, 'class_label': 'name-label', 'class': 'form-control name-input', 'aria-required': True, 'aria-invalid': False, 'style': 'padding: 26px 26px!important;', 'required': True}),
            'telefono': TextInput(attrs={'col': 12, 'class_label': 'name-label', 'class': 'form-control name-input',  'aria-required': True, 'aria-invalid': False, 'style': 'padding: 26px 26px!important;', 'required': True}),
            'email': TextInput(attrs={'col': 12, 'class_label': 'name-label', 'class': 'form-control name-input',  'aria-required': True, 'aria-invalid': False, 'style': 'padding: 26px 26px!important;', 'required': True}),
            'longitud': TextInput(attrs={'col': 6, 'class': 'form-control name-input',  'aria-required': True, 'aria-invalid': False, 'readonly': True, 'style': 'padding: 26px 26px!important;', 'required': True}),
            'latitud': TextInput(attrs={'col': 6, 'class': 'form-control name-input',  'aria-required': True, 'aria-invalid': False, 'readonly': True, 'style': 'padding: 26px 26px!important;', 'required': True}),
        }



