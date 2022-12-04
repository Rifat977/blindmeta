from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room, Profile


# Create your forms here.
class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	username = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('image', 'name','gender',)
