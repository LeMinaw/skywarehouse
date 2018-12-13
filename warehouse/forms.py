from django import forms
from warehouse.models import Comment, Review, Blueprint, User

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
        labels = {'content': "Type your comment here..."}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['aesthetic_grade', 'technic_grade']
        labels = {
            'aesthetic_grade': "Aesthetic grade, /5",
            'technic_grade': "Technic grade, /5"
        }


class BlueprintForm(forms.ModelForm):
    file = forms.FileField(required=True, label="File (MPS/SWBP)")

    class Meta:
        model = Blueprint
        fields = ['categ', 'name', 'image', 'desc']
        labels = {
            'categ':  "Category",
            'name':   "Name",
            'image':  "Cover picture",
            'desc':   "Description"
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['bio', 'avatar']
        labels = {
            'bio':    "Bio",
            'avatar': "Profile picture"
        }
        help_texts = {
            'bio': "Write a few lines to describe yourself.",
            'avatar': "Max size is 1MB."
        }
