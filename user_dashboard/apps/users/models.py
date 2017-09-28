from __future__ import unicode_literals
from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def registration_validation(self, postData):
        flag = True
        errors = {}
        if len(postData['first_name']) < 2:
            flag = False
            errors["first_name"] = "First name should be more than 1 character"
        if postData['first_name'].isalpha() is False:
            flag = False
            errors["first_name"] = "First name must contain only letters"
        if len(postData['last_name']) < 2:
            flag = False
            errors["last_name"] = "Last name should be more than 1 character"
        if postData['last_name'].isalpha() is False:
            flag = False
            errors["last_name"] = "Last name must contain only letters"
        if len(postData['email']) < 1:
            flag = False
            errors["email"] = "Email should not be left blank"
        if not EMAIL_REGEX.match(postData['email']):
            flag = False
            errors["email"] = "Email is not valid!"
        if len(postData['pwd']) < 8:
            flag = False
            errors["pwd"] = "Password should contain atleast 8 characters"
        if postData['pwd'] != postData['confirm_pwd']:
            flag = False
            errors["pwd"] = "Password does not match Confirm Password"

        if flag:
            hashpwd = bcrypt.hashpw(postData['pwd'].encode('utf-8'), bcrypt.gensalt())
            print hashpwd
            user = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=hashpwd)
            return (True, user)
        else:
            return (False, errors)

    def login_validator(self, postData):
        flag = True
        errors = {}
        email = postData["email"]
        try:
            user = User.objects.get(email=email)
        except:
            flag = False
            errors["email"] = "Email does not exist in database please register or try again"
            return (False, errors)
        pwd = User.objects.get(email=email).password
        user_pwd = postData['pwd']
        if not EMAIL_REGEX.match(email):
            flag = False
            errors["email"] = "Email is not valid!"
        if len(email) < 1:
            flag = False
            errors["email"] = "Email should not be left blank"
        if not bcrypt.checkpw(user_pwd.encode('utf-8'), pwd.encode('utf-8')):
            flag = False
            errors["password"] = "Password does not match please try again"
        
        if flag:
            user = User.objects.get(email=email)
            return (True, user)
        else:
            return (False, errors)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()