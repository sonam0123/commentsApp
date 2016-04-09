from django import forms


from .models import UserComments


class CommentsForm(forms.ModelForm):
    class Meta:
        model = UserComments
        fields = ['comment', 'text']
