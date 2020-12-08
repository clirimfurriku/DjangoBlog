from django.contrib.auth.forms import UserCreationForm
from django.forms import ChoiceField, ModelForm

from blog.models import UserModel, BlogPost


class SignUpForm(UserCreationForm):
    user_type = ChoiceField(choices=UserModel.USER_CHOICES)

    class Meta:
        fields = ('username', 'email', 'password1', 'password2',
                  'user_type', 'bio', 'twitter', 'instagram',
                  'facebook', 'avatar')
        model = UserModel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['email'].labell = 'Email Address'


class PostForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = (
            'title',
            'short_description',
            'content',
            'thumbnail_image',
        )
