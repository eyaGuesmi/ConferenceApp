from django.db import models
from conferenceapp.models import Conference
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here.

room_validators = RegexValidator(
    regex=r'^[A-Za-z0-9]+$',
    message='le nom de la salle ne contient que des lettres et chiffres')
class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)    
    session_date = models.DateField()
    start_time = models.TimeField()   
    end_time = models.TimeField()
    room = models.CharField(max_length=255, validators=[room_validators])
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    #conference = models.ForeignKey("conferenceapp.Conference", on_delete=models.CASCADE related_name='sessions')
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='sessions')
    def validate_session_day(self):
        if not self.conference_id or not self.session_date:
            return
        conf = Conference.objects.only('date_debut', 'date_fin').get(pk=self.conference_id)
        if not (conf.date_debut <= self.session_date <= conf.date_fin):
            raise ValidationError({
                'session_date': (
                    "La date de la session doit etre comprise entre la date debut "
                    "et la date fin de la conference.")
             })
    
    def validate_time_order(self):
        if self.start_time is None or self.end_time is None:
            return
        if self.start_time >= self.end_time:
            raise ValidationError({
                'end_time': "L'heure de fin doit etre posterieure e l'heure de debut."
            })
        
    def clean(self):
        self.validate_session_day()
    #def clean(self):
        self.validate_time_order() 
    