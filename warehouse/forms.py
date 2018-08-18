from django import forms
from django.contrib.auth.forms import UserCreationForm
from warehouse.models import *

class ListSortForm(forms.Form):
    sort_orders = (
        ('ASC', "Ascending" ),
        ('DSC', "Descending")
    )
    sort_choices = (
        ('added',           "Publication date"),
        ('aesthetic_grade', "Aesthetics grade"),
        ('technic_grade',   "Technical grade"),
        ('total_grade',     "Overall grade"   ),
        ('random',          "Random"          )
    )
    reverse_order = forms.ChoiceField(choices=sort_orders,  initial='DSC',   label="")
    sort_by       = forms.ChoiceField(choices=sort_choices, initial='added', label="")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': "Your comment"}


class BlueprintForm(forms.ModelForm):
    file = forms.FileField(required=True, label="File (SWBP)")

    class Meta:
        model = Blueprint
        fields = ['categ', 'name', 'image', 'desc']
        labels = {
            'categ':  "Category",
            'name':   "Name",
            'image':  "Cover picture",
            'desc':   "Description"
        }
