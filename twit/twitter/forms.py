from django import forms

class CommentForm(forms.Form):
    your_comment = forms.CharField(label='', max_length=250)
