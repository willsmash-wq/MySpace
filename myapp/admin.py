from django.contrib import admin
from .models import Mission
from .forms import MissionForm

class MissionAdmin(admin.ModelAdmin):
    form = MissionForm
    list_display = ('title', 'mission_taker', 'created', 'total_views')
    list_filter = ('mission_taker', 'created')
    search_fields = ('title', 'mission_taker__username')
    date_hierarchy = 'created'
    readonly_fields = ('accept_date',)

admin.site.register(Mission, MissionAdmin)
