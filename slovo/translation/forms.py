from django import forms



class TranslateForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Bonjour',
        'class':'w-full py-4 px-6 rounded-xl ',
        'rows':3,
        'cols':100
    }))