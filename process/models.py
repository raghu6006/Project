from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class PhoneStore(models.Model):
    number = models.CharField(max_length=15, unique=True, null=False)

    def __str__(self):
        return self.number

class EmailStore(models.Model):
    email = models.EmailField(max_length=30, unique=True, null=False)

    def __str__(self):
        return self.email
    



class Contact(models.Model):
    phoneNumber = models.ForeignKey(to=PhoneStore, null=True, on_delete=models.CASCADE)
    email = models.ForeignKey(to=EmailStore, null=True, on_delete=models.CASCADE)
    linkedId = models.IntegerField(null=True)

    primary = "primary"
    sec = "secondary"
    possible_links=[
        (primary, "primary"),
        (sec, "secondary")
    ]

    linkPrecedence = models.CharField(max_length=20, choices=possible_links)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField(null=True)
    deletedAt = models.DateTimeField(null=True)

    def __str__(self):
        return f"Contact ID: {self.id}, Phone: {self.phoneNumber}, Email: {self.email}, " \
               f"Linked ID: {self.linkedId}, Link Precedence: {self.linkPrecedence}, " \
               f"Created At: {self.createdAt}, Updated At: {self.updatedAt}, Deleted At: {self.deletedAt}"
    
class Group(models.Model):
    number = models.IntegerField(null=False)
    contact = models.ForeignKey(to=Contact, on_delete=models.CASCADE, related_name="groups")
    def __str__(self) -> str:
        return f"Group:{self.number}, Contact:{self.contact_id}"

'''
class Phone(models.Model):
    phone_id = models.IntegerField(null=False)
    contact_id = models.IntegerField(null=False)

class Email(models.Model):
    email_id = models.IntegerField(null=False)
    contact_id = models.IntegerField(null=False)

'''
