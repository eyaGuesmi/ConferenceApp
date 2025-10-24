from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

def list_conferences(request):
    conferences = Conference.objects.all()
    return render(request, "conference/list.html", {"liste": conferences})    

class ConferenceList(ListView):
    model = Conference
    template_name = "conference/list.html"
    context_object_name = "liste"

class ConferenceDetail(DetailView):
    model = Conference
    template_name = "conference/detail.html"
    context_object_name = "conference"

class ConferenceCreate(CreateView):
    model = Conference
    template_name = "conference/form.html"
    fields = "__all__"
    success_url = reverse_lazy('list_conferences')

class ConferenceUpdate(UpdateView):
    model = Conference
    template_name = "conference/form.html"
    fields = "__all__"
    success_url = reverse_lazy('list_conferences')

class ConferenceDelete(DeleteView):
    model = Conference
    template_name = "conference/confirm_delete.html"
    success_url = reverse_lazy('list_conferences')