from django import forms
from .models import Comment, Category


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px'}),
        }


class PostSearchForm(forms.Form):
    q = forms.CharField()
    c = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all().order_by('name'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['c'].required = False
        self.fields['q'].required = False
