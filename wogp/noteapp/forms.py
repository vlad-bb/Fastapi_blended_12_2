from django.forms import ModelForm, CharField, TextInput, Textarea, DateField, DateInput, Select, ModelChoiceField, ModelMultipleChoiceField

from .models import Author, Tag, Quote


class AuthorForm(ModelForm):
    fullname = CharField(max_length=40, min_length=3, widget=TextInput(attrs={'class': 'form-control'}))
    born_date = DateField(widget=DateInput(attrs={'class': 'form-control'}))
    born_location = CharField(max_length=100, widget=TextInput(attrs={'class': 'form-control'}))
    description = CharField(widget=Textarea(attrs={'class': 'form-control',
                                                   'id': 'exampleFormControlTextarea1',
                                                   'rows': '3'}))

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class TagForm(ModelForm):
    name = CharField(max_length=20, min_length=3, widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(ModelForm):
    quote = CharField(max_length=150,
                      widget=TextInput(attrs={'class': 'form-control'}))
    author = ModelChoiceField(queryset=Author.objects.all(),
                              widget=Select(attrs={'class': 'form-select'}))
    # tag = ModelChoiceField(queryset=Tag.objects.all(),
    #                        widget=Select(attrs={'class': 'form-select', 'size': '3', 'multiple': True}))

    class Meta:
        model = Quote
        fields = ['quote', 'author']
        exclude = ['tag']
