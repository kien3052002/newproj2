from django import forms
from .models import Comment, Category
from mptt.forms import TreeNodeChoiceField



class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class PostSearchForm(forms.Form):
    q = forms.CharField()
    c = forms.MultipleChoiceField(
        choices=Category.objects.all().order_by('name'), widget=forms.SelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['c'].required = False
        self.fields['q'].required = False

