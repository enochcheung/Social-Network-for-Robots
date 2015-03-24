from django import forms

from django.contrib.auth.models import User
from models import UserProfile, Post, Comment, Script
from django.core.validators import validate_email

MAX_UPLOAD_SIZE = 2500000


class RegistrationForm(forms.Form):
    username   = forms.CharField(max_length = 20)
    password1  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
    password2  = forms.CharField(max_length = 200, 
                                 label='Confirm password',  
                                 widget = forms.PasswordInput())
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)
    email = forms.CharField(max_length = 40, validators = [validate_email])


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username

class EditProfileForm(forms.Form):
    password1  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput(),
                                 required=False)
    password2  = forms.CharField(max_length = 200, 
                                 label='Confirm password',  
                                 widget = forms.PasswordInput(),
                                 required=False)
    first_name = forms.CharField(max_length=20, required=False)
    last_name  = forms.CharField(max_length=20, required=False)
    age = forms.IntegerField(required=False)
    bio = forms.CharField(max_length=430, required=False)
    picture = forms.FileField(required=False)


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(EditProfileForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    def clean_picture(self):
        picture = self.cleaned_data['picture']

        if not picture:
            return None
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['post','content']

class ScriptForm(forms.ModelForm):
    class Meta:
        model = Script
        fields = ['code','data','on_post','on_comment']

