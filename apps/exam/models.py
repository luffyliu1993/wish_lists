from __future__ import unicode_literals
from django.db import models
import bcrypt, re

# Create your models here.
class UserManager(models.Manager):
    def login(self,session,user_name,password):
        messages = {'errors':[]}
        if len(user_name) == 0:
            messages['errors'].append('Please enter an user name')
        if len(password) == 0:
            messages['errors'].append('Please enter a password')
        if len(messages['errors']) > 0:
            return (False, messages)
        result = self.filter(user_name=user_name)
        if len(result) == 0:
            messages['errors'].append('Incorrect user name!')
            return (False, messages)
        if not bcrypt.checkpw(str(password),str(result[0].password)):
            messages['errors'].append('Incorrect password!')
            return (False, messages)
        session['id'] = result[0].id
        return (True, messages)

    def register_check(self,session,name,user_name,password,conf_pw):
        messages = {'errors':[]}
        if len(name) < 3:
            messages['errors'].append('Name should be at least 2 characters long')
        elif not str.isalpha(name):
            messages['errors'].append('Name should be letters only')
        if len(user_name) == 0:
            messages['errors'].append('Username cannot be empty')
        elif len(self.filter(user_name=user_name)) > 0:
            messages['errors'].append('The user name you entered is used by another account')
        if len(password) < 8:
            messages['errors'].append('Password should have at least 8 characters')
        if len(conf_pw) == 0:
            messages['errors'].append('Please confirm your password')
        elif password != conf_pw:
            messages['errors'].append('Password and confirm password are not match')
        if len(messages['errors']) > 0:
            return (False, messages)
        result = self.create(name=name,user_name=user_name,password=bcrypt.hashpw(str(password),bcrypt.gensalt()))
        #session['id'] = self.all().order_by('-id')[0].id
        session['id'] = result.id
        return (True, messages)

class AddItemManager(models.Manager):
    def add_item(self,session,item):
        if len(item) == 0:
            return (False,'No item entry')
        if len(item) < 4:
            return (False, 'Item entry should be more than 3 characters')
        result = self.filter(item_name=item)
        if len(result) > 0:
            return (False, 'Item exists already')
        user = User.userManager.get(id=session['id'])
        item = self.create(item_name=item,add_user=user)
        item.wish_users.add(user)
        return (True, result)

class User(models.Model):
    name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    userManager = UserManager()

class AddItem(models.Model):
    item_name = models.CharField(max_length=255)
    add_user = models.ForeignKey('User',on_delete=models.CASCADE,related_name='add_user')
    wish_users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    addItemManager = AddItemManager()
