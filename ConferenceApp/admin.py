from django.contrib import admin
from .models import Conference, Submission
<<<<<<< HEAD
# Register your models here.
admin.site.site_title="Gestion Conférence 25/26"
admin.site.site_header="Gestion Conférences"
admin.site.index_title="django App conférence"
#admin.site.register(Conference)
#admin.site.register(Submission)

class SubmissionInline(admin.TabularInline):
    model = Submission
    extra= 1
    readonly_fields =("submission_date",)

@admin.register(Conference)
class AdminConferenceModel(admin.ModelAdmin):
    list_display=("name","theme","start_date","end_date","a")
    ordering=("start_date",)
    list_filter=("theme",)
    search_fields=("description","name")
    date_hierarchy="start_date"
    fieldsets =(
        ("Information general", {
            "fields":("conference_id","name","theme","description")
        }),
        ("logistics Info", {
            "fields":("location","start_date","end_date")
        })
    )
    readonly_fields=("conference_id",)
    def a(self,objet):
        if objet.start_date and objet.end_date:
            return (objet.end_date-objet.start_date).days
        return "RAS"
    a.short_description="Duration (days)"
    inlines=[SubmissionInline]

@admin.action(description="marquer les soumissions comme payés")
def mark_as_payed(modeladmin,req,queryset):
    queryset.update(payed=True)
@admin.action
def mark_as_accepted(m,rq,q):
    q.update(status="accepted") 


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display =("title", "status", "payed","submission_date")
    fieldsets =(
        ("Information general", {
            "fields":("title","abstract","keywords")
        }),
        ("document", {
            "fields":("paper","user","conference")
        }),
        ("Status", {
            "fields":("status","payed")
        })
    )
    actions =[mark_as_payed,mark_as_accepted]
=======

# Customize admin site titles
admin.site.site_title = "Gestion Conference 25/26"
admin.site.site_header = "Gestion Conference"
admin.site.index_title = "Django App Conference"

# Register Submission model
admin.site.register(Submission)

# Inline for Submissions inside Conference admin
class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 1
    readonly_fields = ("Submission_date",)

# Conference admin with inline
@admin.register(Conference)
class AdminConferenceModel(admin.ModelAdmin):
    list_display = ("name", "theme", "start_date", "end_date", "duration")
    ordering = ("start_date",)
    search_fields = ("name", "theme")
    list_filter = ("theme",)
    date_hierarchy = "start_date"

    fieldsets = (
        ("Information générale", {
            "fields": ("conference_id", "name", "theme", "description")
        }),
        ("Informations logistiques", {
            "fields": ("location", "start_date", "end_date")
        }),
    )

    readonly_fields = ("conference_id",)

    inlines = [SubmissionInline]

    # Custom column for duration
    def duration(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return "RAS"
    duration.short_description = "Durée (jours)"



#personalisation attributs sans actions
>>>>>>> df5daa56f74cd80f69add844502b78735ab8bc6a
