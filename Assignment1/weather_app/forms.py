from django import forms


class FeedbackForm(forms.Form):
    firstName = forms.CharField(label='First Name', max_length=100, required=True,
                                widget=forms.TextInput(attrs={
                                    'placeholder': '*First name...'
                                }))
    lastName = forms.CharField(label='Last Name', max_length=100, required=True,
                               widget=forms.TextInput(attrs={
                                   'placeholder': '*Last name...'
                               }))
    email = forms.EmailField(label='E-mail', max_length=254, required=True,
                             widget=forms.TextInput(attrs={
                                 'placeholder': '*E-mail...'
                             }))
    feedback = forms.CharField(max_length=1000, required=True,
                               widget=forms.Textarea(attrs={
                                   'placeholder': '*Feedback message...',
                                   'rows': 5
                               }))


class WeatherForm(forms.Form):
    latitude = forms.CharField(label='Latitude', max_length=20, required=True,
                               widget=forms.TextInput(attrs={'placeholder': '0'}))
    longitude = forms.CharField(label='Longitude', max_length=20, required=True,
                                widget=forms.TextInput(attrs={'placeholder': '0'}))
