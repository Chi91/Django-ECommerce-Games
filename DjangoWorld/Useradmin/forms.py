from django.contrib.auth.forms import UserCreationForm
from .models import MyUser


class MySignUpForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('username', 'profile_picture')
		# password ist wegen UserCreationForm schon mit dabei
