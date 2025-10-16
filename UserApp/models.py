from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here.
import uuid
def generate_user_id():
    return "USER"+uuid.uuid4().hex[:4].upper()
def verify_email(email):
    domain=["esprit.tn","seasame.tn ","tek.tn","centrale.net"]
    email_domain=email.split('@')[1]
    if email_domain not in domain:
        raise ValidationError("l'email est invalide et doit appartenir a un domaine universitaire privé")
name_validators=RegexValidator(
    regex=r'^[a-zA-Z\s-]+$',
    message="ce champ ne doit contenir que des lettres, des espaces et des tirets",
)

class User(AbstractUser):
    user_id=models.CharField(max_length=8,primary_key=True,unique=True,editable=False)
    first_name=models.CharField(max_length=255,validators=[name_validators])
    last_name=models.CharField(max_length=255,validators=[name_validators])
    ROLE=[
        ("participant","participant"),
        ("organizer","organizer"),
        ("member","member commitee"),
    ]
    role=models.CharField(max_length=255,choices=ROLE,default="participant")
    affiliation=models.CharField(max_length=255)
    email=models.EmailField(unique=True, validators=[verify_email])
    nationality=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs): #*args is for a format of a tuple and **kwargs is  for a format of a dictionary
        if not self.user_id:
            newid = generate_user_id()
            while User.objects.filter(user_id=newid).exists():#tantque que le newid existe dans la base de donnee on genere un autre
                newid = generate_user_id()
            self.user_id=newid
        super().save(*args,**kwargs)


class Organizing_Committee(models.Model):
    COMMITTE_ROLE=[
        ("chair","chair"),
        ("co-chair","co-chair"),
        ("member","member"),
    ]
    committee_role=models.CharField(max_length=255,choices=COMMITTE_ROLE)
    date_joined=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="organizing_committees")
    conference=models.ForeignKey("ConferenceApp.Conference",on_delete=models.CASCADE,related_name="organizing_committees")
