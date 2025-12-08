from django.db import models
<<<<<<< HEAD
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError
import uuid

# Create your models here.
import uuid
def generate_submission_id():
    return "SUB"+uuid.uuid4().hex[:8].upper()
class Conference(models.Model):
    conference_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    THEME=[
        ("IA","Computer science & ia"),
        ("SE","Science & eng"),
        ("SC","Social sciences"),
    ]
    theme=models.CharField(max_length=255,choices=THEME)
    location=models.CharField(max_length=50)
    description=models.TextField(validators=[
            MaxLengthValidator(30,"vous avez utuliser la limite des mots autorisés")
    ])
    start_date=models.DateField()
    end_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"la conférence a comme titre {self.name}"
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("la date de début de la conférence doit être antérieur à la date fin ")
class Submission(models.Model):
    submission_id=models.CharField(max_length=255,primary_key=True,unique=True,editable=False)
    title=models.CharField(max_length=50)
    abstract=models.TextField()
    keywords=models.TextField()
    paper=models.FileField(
        upload_to="papers/"
    )
    STATUS= [
        ("submitted","submitted"),
        ("under review","under review"),
        ("accepted","accepted"),
        ("rejected","rejected"),
    ]
    status=models.CharField(max_length=50,choices=STATUS)
    payed=models.BooleanField(default=False)
    submission_date=models.DateField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey("UserApp.User",on_delete=models.CASCADE,
                           related_name="submissions")
    conference=models.ForeignKey(Conference,on_delete=models.CASCADE,
                                 related_name="submissions")

    def save(self,*args,**kwargs):
        if not self.submission_id:
            newid=generate_submission_id()
            while Submission.objects.filter(submission_id=newid).exists():
                newid=generate_submission_id()
            self.submission_id=newid
        super().save(*args,**kwargs)

    

    
=======
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.utils import timezone
import random, string

# Create your models here.
title_validator = RegexValidator(
    regex='^[a-zA-Z\s-]+$',
    message="ce champ ne doit contenir que des lettres"
)

class Conference(models.Model):
    conference_id = models.AutoField(primary_key=True)  # int primary key
    name = models.CharField(max_length=255, validators=[title_validator])  # varchar
    
    THEME = [
        ("IA", "Computer science & ia"),
        ("SE", "Science & Engineering"),
        ("SC", "Social Sciences & Education"),
        ("IT", "Interdisciplinary Themes."),
    ]
    theme = models.CharField(max_length=50, choices=THEME)

    location = models.CharField(max_length=50)
    description = models.TextField(
        validators=[MinLengthValidator(30, message="Vous devez saisir au moins 30 caractères")]
    )
    start_date = models.DateField()  # date
    end_date = models.DateField()    # date
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"la conference a comme titre {self.name}"

    def clean(self):
        # Vérifie que les dates existent avant de comparer
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError("La date de début doit être antérieure à la date de fin")

class Submission(models.Model):
    Submission_id = models.CharField(max_length=255, primary_key=True, unique=True)
    title = models.CharField(max_length=50)
    abstract = models.TextField()
    keywords = models.TextField()
    paper = models.FileField(
        upload_to="paper/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])]
    )

    STATUS = [
        ("submitted", "submitted"),
        ("under review", "under review"),
        ("accepted", "accepted"),
        ("rejected", "rejected"),
    ]

    status = models.CharField(max_length=50, choices=STATUS)
    payed = models.BooleanField(default=False)
    Submission_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("UserApp.User", on_delete=models.CASCADE, related_name="submissions")
    Conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name="submissions")

    def clean(self):
        # 🔹 Vérification dates : uniformiser date/datetime
        if self.Conference and self.Conference.start_date and self.Submission_date:
            start_date = self.Conference.start_date
            submission_date = self.Submission_date.date()  # convert datetime -> date
            if start_date < timezone.now().date() and submission_date > start_date:
                raise ValidationError("La soumission ne peut être faite que pour des conférences à venir.")

        # 🔹 Vérification mots-clés
        keyword_list = []
        if self.keywords:
            for k in self.keywords.split(","):
                k = k.strip()
                if k:
                    keyword_list.append(k)
                    if len(keyword_list) > 10:
                        raise ValidationError({"keywords": "Vous ne pouvez pas saisir plus de 10 mots-clés."})

        # 🔹 Limite de soumissions par jour
        if self.user_id:
            today = timezone.now().date()
            submissions_today = Submission.objects.filter(
                user=self.user,
                Submission_date__date=today
            ).count()
            if submissions_today >= 3 and not self.pk:  # exclude if updating
                raise ValidationError("Vous ne pouvez pas soumettre plus de 3 conférences par jour.")

    # 🔹 Génération automatique de Submission_id
    def save(self, *args, **kwargs):
        if not self.Submission_id:
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            self.Submission_id = f"SUB-{random_part}"

        self.full_clean()  # Call validations before saving
        super().save(*args, **kwargs)
>>>>>>> df5daa56f74cd80f69add844502b78735ab8bc6a
