from django import forms
from .models import *


class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['item', 'description', 'startingBid', 'category', 'image']
        labels = {'startingBid': 'Starting Bid'}
        widgets = {
            'item': forms.TextInput(attrs={
                'class': 'form-control form-group'
            }),

            'description': forms.TextInput(attrs={
                'class': 'form-control form-group'
            }),

            'startingBid': forms.NumberInput(attrs={
                'class': 'form-control form-group', 
                'min': '0.01', 
                'max': '99999999999.99',
                'step': '0.01'
            }),

            'category': forms.Select(attrs={
                'class': 'form-control form-group'
            })
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["price"]
        labels = {'price': ''}
        widgets = {
            'price': forms.NumberInput(attrs={
                'placeholder': 'Bid',
                'class': 'form-control form-group', 
                'min': Listing.currentBid if Listing.currentBid else Listing.startingBid,
                'step': '0.1'
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.TextInput(attrs={
                'class': 'form-control form-group'
            })
        }