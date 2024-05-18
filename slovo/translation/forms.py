from django import forms



class TranslateForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Bonjour',
        'class':' py-4 px-6 rounded-xl ',
        'rows':3,
        'cols':50
    }))
    translation = forms.CharField(disabled=True,required=False,widget=forms.Textarea(attrs={
        'placeholder': 'Dzien dobry',
        'class':' py-4 px-6 rounded-xl ',
        'rows':3,
        'cols':50,
        'id':'translateField'
    }))

class FeedbackForm(forms.Form):

    text = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Bonjour',
        'class':' py-4 px-6 rounded-xl ',
        'rows':3,
        'cols':50
    }))
    translation = forms.CharField(disabled=False,required=True,widget=forms.Textarea(attrs={
        'placeholder': 'Dzien dobry',
        'class':' py-4 px-6 rounded-xl ',
        'rows':3,
        'cols':50,
        'id':'translateField'
    }))