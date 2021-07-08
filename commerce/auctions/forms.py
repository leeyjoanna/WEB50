from django import forms 
from django.forms import ModelForm
from .models import Listing, Comment, Bid

# class NewItemForm(forms.Form):
#     item_name = forms.CharField(label="Name of item", max_length=120)
#     item_description = forms.CharField(label="Description", widget=forms.Textarea)
#     item_price = forms.DecimalField(label="Starting bid", decimal_places=2)
#     categories = (
#         ("necklace","necklace"), ("earring", "earring")
#     )
#     item_category = forms.MultipleChoiceField(label="Category", widget=forms.CheckboxSelectMultiple, choices = categories)

class NewItemForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['item_name', 'item_description', 'item_price', 'item_category']


class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class NewBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']