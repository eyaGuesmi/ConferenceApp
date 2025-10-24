from django.contrib import admin
from .models import Conference, Submission, OrganisationCommittee
# Register your models here.

#admin.site.register(Conference)
#admin.site.register(Submission)
admin.site.register(OrganisationCommittee)
admin.site.site_title = "Gestion Conference IA"
admin.site.site_header = "Gestion Conference IA Admin"
admin.site.index_title = "Welcome Django App Conference"

class SubmissionStackedInline(admin.StackedInline):
    model = Submission
    extra = 1
    readonly_fields = ( 'submission_date',)
    fields = ("submission_id", "title", "abstract", "status", "payed", "user", "submission_date")
    readonly_fields = ("submission_id", "submission_date")

class SubmissionTabularInline(admin.TabularInline):
    model = Submission
    extra = 0
    fields = ("title", "status", "user", "payed")
    
@admin.register(Conference)
class AdminConferenceModel(admin.ModelAdmin):
    list_display = ('name', 'theme', 'location', 'date_debut', 'date_fin', 'duration')
    search_fields = ('name', 'theme', 'location')
    list_filter = ('theme', 'date_debut', 'date_fin')
    ordering = ('date_debut',)
    date_hierarchy = 'date_debut'
    fieldsets = (
        ("informations de la conference", {
            'fields': ('conference_id','name', 'theme', 'description' )
        }),
        ("Details", {
            'fields': ('location', 'date_debut', 'date_fin' )
        }),   
                    
    )
    readonly_fields = ('conference_id', 'create_at', 'update_at')
    def duration(self, objet):
        if objet.date_debut and objet.date_fin:
            return (objet.date_fin - objet.date_debut).days
        return "RAS"
    duration.short_description = "Duration (days)"

    inlines = [SubmissionStackedInline]
   # inlines = [SubmissionTabularInline]




@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "user",
        "conference",
        "submission_date",
        "payed",
        "short_abstract",
    )

    def short_abstract(self, obj):
        if obj.abstract:  
            if len(obj.abstract) > 50:
                return obj.abstract[:50] + "..."  
            else:
                return obj.abstract
        return "RAS"  
    list_filter = ("status", "payed", "conference", "submission_date")
    search_fields = ("title", "keywords", "user__username")
    list_editable = ("status", "payed")
    fieldsets = (
        ("Infos générales", {
            "fields": ("submission_id", "title", "abstract", "keywords")
        }),
        ("Fichier et conférence", {
            "fields": ("paper", "conference")
        }),
        ("Suivi", {
            "fields": ("status", "payed", "submission_date", "user")
        }),
    )
    readonly_fields = ("submission_id", "submission_date")

    actions = ("mark_as_payed", "accept_submissions")

    def mark_as_payed(self, request, queryset):
        
        updated = queryset.update(payed=True)
        self.message_user(request, f"{updated} soumission(s) marquée(s) comme payées.")
    mark_as_payed.short_description = "Marquer comme payées"

    def accept_submissions(self, request, queryset):

        updated = queryset.update(status="accepted")
        self.message_user(request, f"{updated} soumission(s) acceptée(s).")
    accept_submissions.short_description = "Accepter les soumissions sélectionnées"