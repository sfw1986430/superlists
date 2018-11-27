#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from django.test import TestCase
from unittest.mock import patch, Mock
from lists.models import Item, List
from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm, NewListForm
)

class ItemFormTest(TestCase):
    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control form-control-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            ["You can not have an empty list item"]
        )

    # def test_form_save_handles_saving_to_a_list(self):
    #     list_ = List.objects.create()
    #     form = ItemForm(data={'text':'do me'})
    #     new_item = form.save(for_list = list_)
    #     self.assertEqual(new_item, Item.objects.first())
    #     self.assertEqual(new_item.text, 'do me')
    #     self.assertEqual(new_item.list, list_)

class ExistingListItemFormTest(TestCase):
    def test_form_render_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"',form.as_p())

    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_dupliacate_items(self):
        list_  = List.objects.create()
        Item.objects.create(list=list_, text='test')
        form = ExistingListItemForm(for_list=list_, data={'text':'test'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'hi'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])

class NewListFormTest(unittest.TestCase):
    # @patch('lists.forms.List')
    # @patch('lists.forms.Item')
    # def test_save_creates_new_list_and_item_from_post_dat(self, mockItem, mockList):
    #     mock_item = mockItem.return_value
    #     mock_list = mockList.return_value
    #
    #     user = Mock()
    #     form = NewListForm(data={'text': 'new item text'})
    #     form.is_valid()
    #
    #     def check_item_text_and_list():
    #         self.assertEqual(mock_item.text, 'new item text')
    #         self.assertEqual(mock_item.list, mock_list)
    #         self.assertTrue(mock_list.save.called)
    #
    #     mock_item.save.side_effect = check_item_text_and_list
    #
    #     form.save(owner=user)
    #     self.assertTrue(mock_item.save.called)

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_post_data_if_user_not_authenticated(self, mock_List_create_new):
        user = Mock(is_authenticated=False)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text='new item text'
        )

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_lis_with_owner_if_user_authenticated(self, mock_List_create_new):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text='new item text', owner=user
        )

    @patch('lists.forms.List.create_new')
    def test_save_returns_new_list_object(self, mock_List_create_new):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        response = form.save(owner=user)
        self.assertEqual(response, mock_List_create_new.return_value)
        

        
        
            



    



        