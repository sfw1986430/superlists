#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from lists.models import Item, List
from django.core.exceptions import ValidationError

EMPTY_ITEM_ERROR = "You can not have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control form-control-lg',
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }

    # def save(self, for_list):
    #     self.instance.list = for_list
    #     return super().save()


class NewListForm(ItemForm):
    def save(self, owner):
        if owner.is_authenticated:
            return List.create_new(first_item_text=self.cleaned_data['text'], owner=owner)
        else:
           return List.create_new(first_item_text=self.cleaned_data['text'])

class ExistingListItemForm(ItemForm):
    def __init__(self,for_list, *args, **argv):
        super().__init__(*args, **argv)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
    #
    # def save(self):
    #     return forms.models.ModelForm.save(self)
