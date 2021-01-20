from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Textarea, CharField, PasswordInput, BaseForm, ModelMultipleChoiceField, \
    ModelChoiceField, SelectMultiple, CheckboxSelectMultiple, DateField, DateInput
from manager.models import Book, Comment, Profile
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=TextInput(attrs={'autofocus': True, "class": "form-control"}))
    password = CharField(
        label="Password",
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'current-password', "class": "form-control"}),
    )


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        pass
    username = UsernameField(widget=TextInput(attrs={'class': 'form-control'}))
    password1 = CharField(
        label="Password",
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'})
        )
    password2 = CharField(
        label="Password confirmation",
        widget=PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False
    )


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["title", "text", "genre", "cover"]
        widgets = {
            "title": TextInput(attrs={"class": "form-control"}),
            "text": Textarea(attrs={"class": "form-control", "rows": 5, "cols": 50}),
            "genre": SelectMultiple(attrs={"class": "form-control"})
            }
        help_texts = {
            "title": "",
            "text": ""
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": Textarea(attrs={'id': 'comment-text', "class": "form-control", "rows": 5, "cols": 50})
        }
        help_texts = {
            "text": ""
        }


class GenreForm(ModelForm):
    genre = ModelChoiceField(queryset=Book.objects.filter(genre=True))


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('about_user', 'date_of_birth', 'photo')
        widgets = {
            "about_user": Textarea(attrs={"class": "form-control", "rows": 5, "cols": 20}),
            "date_of_birth": DateInput()
        }
