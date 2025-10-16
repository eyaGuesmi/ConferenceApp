from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
# Create your models here.

class Conference(models.Model):#modifier le comportement de la classe 
    conference_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    THEME=[
        ("IA","computer science & ia"),
        ("SE","Science & eng"),
        ("SC","Social sciences"),
        ("IT","interdiscriplinary Themes")
    ]
    theme=models.CharField(max_length=255,choices=THEME)
    location=models.CharField(max_length=50)
    desciption=models.TextField(validators=[MinLengthValidator(30,"la description doit contenir au moins 30 caractéres")])
    start_date=models.DateField()
    end_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("la date de fin doit etre superieur a la date de debut")

class Submission (models.Model):
    submission_id=models.CharField(max_length=255,primary_key=True,unique=True)
    title=models.CharField(max_length=255)
    abstract=models.TextField()
    keywords=models.TextField()
    paper=models.FileField(
        upload_to="paper/"
    )
    STATUS=[
        ("submitted","submitted"),
        ("under review","under review"),
        ("accepted","accepted"),
        ("rejected","rejected"),
    ]
    status=models.CharField(max_length=50,choices=STATUS)
    payed=models.BooleanField(default=False)
    submission_date=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey("UserApp.User",on_delete=models.CASCADE,related_name="submissions")
    conference=models.ForeignKey(Conference,on_delete=models.CASCADE, related_name="submissions")