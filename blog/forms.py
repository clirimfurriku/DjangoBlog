from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Form, ChoiceField

from blog.models import UserModel


class SignUpForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['email'].labell = 'Email Address'


class SignUpInfoForm(ModelForm):
    # TODO: Fix form submitting save
    user_type = ChoiceField(choices=UserModel.USER_CHOICES)

    class Meta:
        fields = ('user_type', 'bio', 'twitter', 'instagram', 'facebook', 'avatar')
        model = UserModel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['user_type']
        self.fields['bio'].labell = 'Bio'
        self.fields['twitter'].labell = 'Twitter Url'
        self.fields['instagram'].labell = 'Instagram URL'
        self.fields['facebook'].labell = 'Facebook URL'

    # def save(self, commit=True):
    #     print(self.instance)
    #     return super(SignUpInfoForm, self).save()
    # self.instance.user = User.objects.get()


class CombinedFormBase(Form):
    form_classes = []

    def __init__(self, *args, **kwargs):
        super(CombinedFormBase, self).__init__(*args, **kwargs)
        for f in self.form_classes:
            name = f.__name__.lower()
            setattr(self, name, f(*args, **kwargs))
            form = getattr(self, name)
            self.fields.update(form.fields)
            self.initial.update(form.initial)

    def is_valid(self):
        isValid = True
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            if not form.is_valid():
                isValid = False
        # is_valid will trigger clean method
        # so it should be called after all other forms is_valid are called
        # otherwise clean_data will be empty
        if not super(CombinedFormBase, self).is_valid():
            isValid = False
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            self.errors.update(form.errors)
        return isValid

    def clean(self):
        cleaned_data = super(CombinedFormBase, self).clean()
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            cleaned_data.update(form.cleaned_data)
        return cleaned_data


class UserSignupForm(CombinedFormBase):
    form_classes = [SignUpForm, SignUpInfoForm]
