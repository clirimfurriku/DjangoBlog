from django.contrib.auth.forms import UserCreationForm, UserModel
from django.forms import ChoiceField


class SignUpForm(UserCreationForm):
    user_type = ChoiceField(choices=UserModel.get_signup_types())

    class Meta:
        fields = ('username', 'email', 'password1', 'password2',
                  'user_type', 'bio', 'twitter', 'instagram',
                  'facebook', 'avatar')
        model = UserModel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['email'].labell = 'Email Address'
