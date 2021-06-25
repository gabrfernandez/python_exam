from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, data):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(data['first_name'])<3:
            errors['first_name']="First Name must be 3 characters minimum"
        if len(data['last_name'])<3:
            errors["last_name"]="Last Name must be 3 characters minimum"
        if len(data['email'])<1:
            errors["email"]="Please enter an email!"
        elif not EMAIL_REGEX.match(data['email']):  
            errors['email'] = "Invalid email address!"
        if len(data['password'])<8:
            errors['password']="Please enter at least 8 characters for your password!"
        if data['pw_confirm']!= data["password"]:
            errors['pw_confirm']="Please match your password to its confirmation!"

        return errors

class JobManager(models.Manager):
    def basic_validator(self, data):
        errors={}
        if len(data['title'])<3:
            errors['title']="Title must be at least 3 characters."
        if len(data['description'])<3:
            errors["description"]="Description must be at least 3 characters."
        if len(data['location'])<3:
            errors["location"]="Location must be at least 3 characters."

        return errors


class User(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()


class Job(models.Model):
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    location=models.CharField(max_length=240)
    category=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, related_name="jobs", on_delete = models.CASCADE) 
    objects=JobManager()

    