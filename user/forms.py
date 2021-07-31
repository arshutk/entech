from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm

from user.models import Account



class SignupForm(UserCreationForm):
    ''' Model for Custom User model'''
    
    class Meta:
        model = Account
        fields = ('email', 'password1', 'password2')



class LoginForm(forms.Form):
    ''' Custom form for handdling the login'''

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean_email(self):
        email = Account.objects.filter(email=self.cleaned_data.get('email'))
        if email.exists():
            return self.cleaned_data['email']
        raise forms.ValidationError('user not found')


class AccountAdminCreationForm(forms.ModelForm):
    password1 = forms.RegexField(widget=forms.PasswordInput, regex='^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'status', 'is_active', 'is_staff', 'is_superuser')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(AccountAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AccountAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model   = Account
        fields  = ('email', 'password', 'status', 'is_active', 'is_staff', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]
