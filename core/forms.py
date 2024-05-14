from django import forms
from .models import Usuario

class FormCrearUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'contrasena', 'rol']
        widgets = {
            'nombre: ': forms.TextInput(attrs={
                'placeholder': 'Nombre del Usuario'
                
            })
        }
        labels = {
            'nombre': 'Nombre del Usuario',
            'apellido': 'Apellido del Usuario', 
            'email': 'Correo Electronico',
            'contrasena':'Contraseña',
            'rol':'Rol de Usuario:'
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('El correo electrónico ya está registrado.')
        return email

class FormEditarUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'rol']

    def clean_email(self):
        email = self.cleaned_data['email']
        usuario_actual = self.instance
        if Usuario.objects.filter(email=email).exclude(id=usuario_actual.id).exists():
            raise forms.ValidationError('El correo electrónico ya está registrado.')
        return email
    
