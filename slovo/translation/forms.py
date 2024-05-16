from django import forms

class TranslateForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Bonjour',
        'class':'w-full py-4 px-6 rounded-xl'
    }))