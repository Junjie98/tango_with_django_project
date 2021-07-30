from django import forms
from django.forms import fields
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        #Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)#set model attribute to the model you wish to use.

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=Page.URL_MAX_LENGTH, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self): #cleans the data being passed thru the form before storing.
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

    #if url not empty, and doesnts tart with http:// we prepend http://
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        return cleaned_data

    class Meta:
        #Provide an association between the ModelForm and a model
        model = Page
        exclude = ('category',)
        #or specify the fields to include (don't include the category field).
        #fields = ('title', 'url', 'views')

#Note: nested Meta class describes additional properties about the
#particular class to which it belongs. Each meta class must supply a model field.
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())#overwrites the default password attribute
    #so that it hides the password input.

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)
    