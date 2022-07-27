from django.contrib import admin
from ClubApp.models import User, Event
# Register your models here.

admin.site.register(User)
# admin.site.register(Event)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'venue', 'event_manager')
    ordering = ('event_name',) # put '-' infront of name for reverse order
    search_fields = ('event_name', 'venue')