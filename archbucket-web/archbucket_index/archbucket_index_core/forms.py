from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Item, Comment, Rating

class ItemForm(forms.ModelForm):
    url = forms.CharField(widget=forms.HiddenInput,  required=False)
    class Meta:
        model = Item
        fields = ('name', 'description', 'documentation', 'source_code', 'item_type', 'status', 'votes')
        widgets = {
            'item_type': forms.HiddenInput,
            'status': forms.HiddenInput,
            'votes': forms.HiddenInput,
            'source_code': forms.Textarea(attrs={
                'class': 'txt',
                'id': 'text',
                'rows': '20',
                'cols': '150',
                'nowrap': 'nowrap',
                'wrap': 'off',
                'autocomplete': 'off',
                'autocorrect': 'off',
                'autocapitalize': 'off',
                'spellcheck': 'false',
                'onclick': 'selectionchanged(this)',
                'onkeyup': 'keyup(this, event)',
                'oninput': 'input_changed(this)',
                'onscroll': 'scroll_changed(this)'
                }),
            'name': forms.TextInput(attrs={'class': 'name-input'}),
            'description': forms.Textarea(attrs={'class': 'textarea'}),
            'documentation': forms.Textarea(attrs={'class': 'textarea'})
        }


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'comment-textarea'}), label='', )
    class Meta:
        model = Comment
        fields = ('item', 'user', 'text')
        widgets = {
            'item': forms.HiddenInput,
            'user': forms.HiddenInput
        }

class RatingForm(forms.ModelForm):
    value = forms.ChoiceField(choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5),))

    class Meta:
        model = Rating
        fields = ('item', 'user')
        widgets = {
            'item': forms.HiddenInput,
            'user': forms.HiddenInput
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )