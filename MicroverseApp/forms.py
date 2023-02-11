from .models import CustomUser, BankAccount, Card
from django import forms
from django.contrib.auth.forms import UserCreationForm  


class UserForm(UserCreationForm): 
    class Meta: 
        model = CustomUser 
        fields = ('national_ID', 'phone_number','first_name','last_name', 'gender', 'password1', )
class LoginForm(forms.Form):
    national_ID = forms.CharField(max_length=16)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.fields['national_ID'].widget.attrs.update({ 
            'class': 'form-control ', 
            'required':'', 
            'name':'national_ID', 
            'id':'national_ID', 
            'type':'text', 
            'placeholder':'National ID Number', 
            'maxlength':'20'
                        
        })
        self.fields['password'].widget.attrs.update({ 
            'class': 'form-control ', 
            'required':'', 
            'name':'password', 
            'id':'password', 
            'type':'text', 
            'minlength': '8', 
                        
        })

