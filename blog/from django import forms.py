from django import forms
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    specify how they have to be displayed, and indicate how they have to validate input data. The Django forms framework offers a flexible way to render forms in HTML and handle data. Django comes with two base classes to build forms: Form: This allows you to build standard forms by defining fields and validations. ModelForm: This allows you to build forms tied to model instances. It provides all the functionalities of the base Form class, but form fields can be explicitly declared, or automatically generated, from model fields. The form can be used to create or edit model instances. First, create a forms.py file inside the directory of your blog application and add the following code to it: from django import forms
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea
    )