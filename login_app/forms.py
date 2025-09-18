from django.forms import ModelForm
from .models import User, Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm


# form1
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)


# form2
# class SignupForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('email', 'password1', 'password2')


class SignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=264, required=True)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user.profile.full_name = self.cleaned_data['full_name']
            user.profile.save()
        return user