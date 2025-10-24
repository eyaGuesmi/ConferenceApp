from django.db import models
from userapp.models import User
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator,FileExtensionValidator
from django.utils import timezone
import string, random
# Create your models here.

title_validators = RegexValidator(
    regex=r'^[a-zA-Z\s-]+$',
    message='le titre doit contenir uniquement des lettres et espaces')

class Conference(models.Model):
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, validators=[title_validators])
    THEME_CHOICES = [
        ("AI", "Artificial Intelligence"),
        ("ML", "Machine Learning"),
        ("DS", "Data Science"),
        ("CV", "Computer Vision"),
        ("NLP", "Natural Language Processing"),
    ]
    theme = models.CharField(max_length=255, choices=THEME_CHOICES)
    location = models.CharField(max_length=255)
    date_debut = models.DateField()
    date_fin = models.DateField()
    description = models.TextField(
    validators=[MinLengthValidator(30, message="La description doit contenir au moins 30 caracteres.")]
)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"la conference a comme nom : {self.name} et comme theme : {self.theme}"

    def clean(self):
        if self.date_debut and self.date_fin and self.date_debut > self.date_fin:
             raise ValidationError({'date_fin': "La date de fin doit etre posterieure a la date de debut."})

    
      
class Submission(models.Model):
    submission_id = models.CharField(max_length=255, primary_key=True, unique=True,  editable=False)
    title = models.CharField(max_length=50)
    abstract = models.TextField()
    keywords = models.TextField(max_length=255, help_text="Séparez les mots-clés par des virgules (ex : IA, données, santé)")
    paper = models.FileField(
        upload_to='papers/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf'],
                message="Seuls les fichiers PDF (.pdf) sont autorisés."
            )
        ]
    )
    STATUS_CHOICES = [
        ("submitted", "submitted"),
        ("under review", "under review"),
        ("accepted", "accepted"),
        ("rejected", "rejected"),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    submission_date = models.DateTimeField(auto_now_add=True)
    payed = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='submissions')
    user =models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    """def validate_keywords_count(self):
        if not self.keywords:
            return

        # Supprimer les espaces, puis séparer les mots-clés
        mots_cles = [mot.strip() for mot in self.keywords.split(',') if mot.strip() != '']

        if len(mots_cles) > 10:
            raise ValidationError({
                'keywords': f"Le nombre de mots-clés ne doit pas dépasser 10 (actuellement {len(mots_cles)})."
            })"""
    def validate_keywords_count(self):
            keywords_list=[]
            if self.keywords:
                for k in self.keywords.split(','):
                    k=k.strip()
                    if k:
                        keywords_list.append(k)
            if len(keywords_list) > 10:
                raise ValidationError({
                    'keywords': f"Le nombre de mots-clés ne doit pas dépasser 10 (actuellement {len(keywords_list)})."
                })
        

    def clean(self):
        self.validate_keywords_count()

        """
        # ---- RÈGLE 1 : soumission uniquement pour une conférence à venir ----
        # (on accepte seulement si la conférence commence après aujourd'hui)
        if self.conference_id:
            today = timezone.localdate()
            if not (self.conference.date_debut > today):
                # message attaché à submission_date (tu peux aussi le mettre sur 'conference')
                raise ValidationError("La soumission est autorisée uniquement pour des conférences à venir.")

        # ---- RÈGLE 2 : max 3 soumissions / jour / participant ----
        # Si submission_date est auto_now_add, sa valeur n'existe pas encore en mémoire :
        # on utilise donc la date du jour (qui sera celle enregistrée).
        target_day = (
            self.submission_date.date() if getattr(self.submission_date, "date", None) else timezone.localdate()
        )

        if self.user_id:
            # on compte les soumissions du même utilisateur le même jour
            qs = Submission.objects.filter(
                user_id=self.user_id,
                submission_date__date=target_day,   # ← compare uniquement la date (pas l'heure)
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)  # ne pas se compter soi-même en édition

            if qs.count() >= 3:
                raise ValidationError( "Limite atteinte : au maximum 3 soumissions par jour et par participant.")
        """
        if self.submission_date and self.conference_id:
            if self.conference.date_debut < timezone.localdate() and self.submission_date > self.conference.date_fin:
                raise ValidationError("La soumission est autorisée uniquement pour des conférences à venir.")
        
    def generate_submission_id(self):
        """Génère un identifiant unique au format SUB-ABCDEFGH"""
        prefix = "SUB-"
        letters = string.ascii_uppercase
        random_part = ''.join(random.choices(letters, k=8))
        return prefix + random_part
    
    def save(self, *args, **kwargs):
        if not self.submission_id:
            newid = self.generate_submission_id()
            while Submission.objects.filter(submission_id=newid).exists():
                newid = self.generate_submission_id()
            self.submission_id = newid
        super().save(*args, **kwargs)


class OrganisationCommittee(models.Model):
    committee_id = models.CharField(max_length=255, primary_key=True, unique=True)
    
    ROLE_CHOICES = [
        ("chair", "chair"),
        ("co-chair", "co-chair"),
        ("member", "member"),
    ]
    role = models.CharField(max_length=255, choices=ROLE_CHOICES)
    date_joined = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='committees')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='committees')