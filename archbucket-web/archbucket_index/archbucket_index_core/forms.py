from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm 
from .models import Item, Comment, Rating, User

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

class SetPasswordForm(forms.Form):
    user = forms.CharField(widget=forms.HiddenInput)
    current_password = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'type':'password', 
        'placeholder':'Current password'
        }))

    new_password1 = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'type':'password', 
        'placeholder':'New password'
        }))

    new_password2 = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'type':'password', 
        'placeholder':'Confirm new password'
        }))

    def clean(self):
        username = self.cleaned_data['user']
        current_password = self.cleaned_data['current_password']
        new_password1 = self.cleaned_data['new_password1']
        new_password2 = self.cleaned_data['new_password2']
        
        user = authenticate(username=username, password=current_password)

        if not user:
            msg = 'Current password is invalid'
            self._errors['current_password'] = self.error_class([msg])
            self.cleaned_data.pop('current_password')

        if new_password1 != new_password2:
            msg = 'Passwords do not match'
            self._errors['new_password2'] = self.error_class([msg])
            self.cleaned_data.pop('new_password1')
            self.cleaned_data.pop('new_password2')

        return self.cleaned_data