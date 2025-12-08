from django import forms
<<<<<<< HEAD
from .models import Conference, Submission
=======
from .models import Conference,Submission
>>>>>>> df5daa56f74cd80f69add844502b78735ab8bc6a

class ConferenceForm(forms.ModelForm):
    class Meta:
        model=Conference
        fields=['name','theme','location','description','start_date','end_date']
        labels = {
            'name':"titre de la conférence",
            'theme':"Thématique de la conférence",
        }
        widgets ={
            'name' : forms.TextInput(
                attrs= {
                    'placeholder' :"Entrer un titre à la conférence" 
                }
            ),
            'start_date' : forms.DateInput(
                attrs ={
                    'type':"date"
                }
            ),
            'end_date' : forms.DateInput(
                attrs ={
                    'type':"date"
                }
            )
        }
<<<<<<< HEAD
#to add for homework 10
# Formulaire pour Conference
class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['name', 'theme', 'location', 'description', 'start_date', 'end_date']
        labels = {
            'name': "Titre de la conférence",
            'theme': "Thématique de la conférence",
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "Entrer un titre à la conférence"}),
            'start_date': forms.DateInput(attrs={'type': "date"}),
            'end_date': forms.DateInput(attrs={'type': "date"}),
        }

# Formulaire pour Submission
# forms.py
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['title', 'abstract', 'keywords', 'paper', 'conference']
=======
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['title', 'abstract', 'keywords', 'paper', 'Conference', 'payed','status']  
>>>>>>> df5daa56f74cd80f69add844502b78735ab8bc6a
