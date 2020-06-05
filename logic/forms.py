from django import forms
from django.contrib.auth.models import User
from datamodel.models import Move

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password',)

class SignupForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

class MoveForm(forms.Form):
    origin = forms.IntegerField()
    target = forms.IntegerField()

    class Meta:
        model = Move
        fields = ('origin', 'target',)

    def is_valid(self):
        non_valid_pos = [1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30,33,35,37,39,40,42,44,46,49,51,53,55,56,58,60,62]

        valid = super(MoveForm, self).is_valid()

        if not valid:
            return valid

        if self.cleaned_data['origin'] < 0 or self.cleaned_data['origin'] > 63:
            return False
        if self.cleaned_data['target'] < 0 or self.cleaned_data['target'] > 63:
            return False
        if self.cleaned_data['origin'] in non_valid_pos or self.cleaned_data['target'] in  non_valid_pos:
            return False

        return True
