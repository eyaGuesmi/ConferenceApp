from django.contrib import admin
from .models import Conference, Submission
# Register your models here.
admin.site.site_title="Gestion de Conférence25-26"
admin.site.site_header="Administration de Conférence"
admin.site.index_title="django app conference"
admin.site.register(Conference)
admin.site.register(Submission)
