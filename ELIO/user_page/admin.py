from django.contrib import admin
from .models import MoodEntry


@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'mood_level', 'sleep_quality', 'had_panic_attack', 'date_time', 'note')
    list_filter = ('mood_level', 'had_panic_attack', 'date_time')
    search_fields = ('user__username', 'note')
    date_hierarchy = 'date_time'