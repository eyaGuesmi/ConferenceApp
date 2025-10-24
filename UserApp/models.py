from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here.

import uuid
def generate_user_id():
    return "USER"+uuid.uuid4().hex[:4].upper()


def verify_email(email):
    domaines = ["esprit.tn","seasame.com","tek.tn"]

    """return any( email.endswith('@' + d) for d in domaine)"""
    sous_chaine = email.split('@')[1]
    if sous_chaine not in domaines:
        raise ValidationError("Email domain is not allowed.")
    
name_validators = RegexValidator(
    regex=r'^[a-zA-Z\s-]+$',
    message='This field should only contain letters, spaces, and hyphens.'
)

class User(AbstractUser):
    user_id = models.CharField(max_length=8,primary_key=True,unique=True,editable=False)
    first_name = models.CharField(max_length=255, validators=[name_validators])
    last_name = models.CharField(max_length=255, validators=[name_validators])
    ROLE=[
        ("participant","participant"),
        ("committee","organisation committee member")
    ]
    role = models.CharField(max_length=50,choices=ROLE,default="participant")
    affiliation = models.CharField(max_length=255)
    email = models.EmailField(unique=True,validators=[verify_email])
    nationality = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.user_id:
            newid = generate_user_id()
            while User.objects.filter(user_id=newid).exists():
                newid = generate_user_id()
            self.user_id = newid
        super().save(*args, **kwargs)
    
    

    