from django.contrib.auth.forms import AuthenticationForm
from django import forms
from grumblr.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=200, label="Username",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
                               required=True, error_messages={'required': 'Username is required'})
    first_name = forms.CharField(max_length=200, label="First name: ",
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': 'Given name e.g. John'}),
                                 required=True, error_messages={'required': 'First name is required'})
    last_name = forms.CharField(max_length=200, label="Last name: ",
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Family name e.g. Snow'}),
                                required=True, error_messages={'required': 'Last name is required'})
    email = forms.EmailField(max_length=200, label="Email: ",
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
                             required=True, error_messages={'required': 'Email is required'})
    password1 = forms.CharField(max_length=200, label="Password: ",
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                                required=True, error_messages={'required': 'Password is required'})
    password2 = forms.CharField(max_length=200, label="Confirm password: ", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
                                required=True, error_messages={'required': 'Confirm password is required'})

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password did not match.")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("The username is already taken.")

        return username


class EditProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=200, label="Username",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
                               required=True, error_messages={'required': 'Username is required'})
    first_name = forms.CharField(max_length=200, label="First name: ",
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': 'Given name e.g. John'}),
                                 required=True, error_messages={'required': 'First name is required'})
    last_name = forms.CharField(max_length=200, label="Last name: ",
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Family name e.g. Snow'}),
                                required=True, error_messages={'required': 'Last name is required'})
    age = forms.IntegerField(max_value=200, label="Age: ",
                             widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g.28'}),
                             required=False, error_messages={'invalid': 'It must be an integer:('})
    bio = forms.CharField(max_length=420, label="Bio: ",
                          widget=forms.Textarea(attrs={'class': 'form-control',
                                                       'placeholder': '420 characters max. e.g.My heart is in the Grumblr'}),
                          required=False, help_text='420 characters max.',
                          error_messages={'invalid': 'It has to be within 420 characters :('})
    picture = forms.FileField(label="Upload Image", widget=forms.FileInput(attrs={'class': 'form-control'}),
                              required=False)

    class Meta:
        model = User
        fields = {'picture', 'username', 'first_name', 'last_name', 'email', 'age', 'bio'}

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(id=self.instance.id).filter(username__exact=username):
            raise forms.ValidationError("The username is already taken.")
        return username

    def clean_age(self):
        age = str(self.cleaned_data.get('age'))
        if not age.isdigit() or int(age) < 0:
            raise forms.ValidationError("You input an invalid age.")
        return age

    def clean_bio(self):
        bio = str(self.cleaned_data.get('bio'))
        if len(bio) >= 420:
            raise forms.ValidationError("The biography is too long.")
        return bio

        # def __init__(self, *args, **kwargs):
        #     user = kwargs.pop('user', None)
        #     super(EditProfileForm, self).__init__(*args, **kwargs)
        #     self.initial['username'] = user.username
        #     self.initial['first_name'] = user.first_name
        #     self.initial['last_name'] = user.last_name
        #     if hasattr(user, 'profile'):
        #         profile = user.profile
        #         self.initial['age'] = profile.age
        #         self.initial['bio'] = profile.bio
        #         self.initial['picture'] = profile.picture

        # def picture_url(self):
        #     if self.cleaned_data.get('picture') and hasattr(self.cleaned_data.get('picture'), 'url'):
        #         return str(self.cleaned_data.get('picture').url).replace(settings.MEDIA_ROOT, '/media/')
        #     else:
        #         return '/media/no-img.jpg'

        # def save(self, commit=True):
        #     if not self.picture:
        #         self.picture = settings.MEDIA_ROOT+'no-img.jpg'
        #         return self.picture


class PostForm(forms.ModelForm):
    text = forms.CharField(max_length=42,
                           widget=forms.TextInput(attrs={'id':'post-text', 'name':'post-form-input', 'class': 'form-control newpost-textarea',
                                                         'placeholder': 'Add a new post within 42 characters...'}),
                           required=True, error_messages={'required': 'The post is empty.'})

    class Meta:
        model = Post
        fields = {'text'}

    def clean_text(self):
        post_text = str(self.cleaned_data.get('text'))
        if len(post_text) > 42:
            raise forms.ValidationError("The post is too long.")
        return post_text

class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=200,required=True, error_messages={'required': 'The comment is empty.'})

    class Meta:
        model = Comment
        fields = {'content'}

    def clean_content(self):
        comment_content = str(self.cleaned_data.get('content'))
        if len(comment_content) > 200:
            raise forms.ValidationError("The comment is too long.")
        return comment_content


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, label="Username",
                               widget=forms.TextInput(
                                   attrs={'name': 'log_username', 'placeholder': 'Username', 'class': 'form-control'}),
                               required=True, error_messages={'required': 'Username is required'})
    password = forms.CharField(max_length=200, label="Password: ",
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                               required=True, error_messages={'required': 'Password is required'})

    def clean(self):
        print("enter clean LoginForm")
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        print(username, "  ", password)

        user = authenticate(username=username, password=password)

        if user is not None:

            if not user.is_active:

                print("user disabled")
                raise forms.ValidationError("User disabled. Please try another.")
            else:
                return username

        else:
            print("Invalid input")
            raise forms.ValidationError("User does not exist/Incorrect password. Please try again.")
