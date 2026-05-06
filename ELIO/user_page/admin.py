from django.contrib import admin
from .models import MoodEntry, UserProfile

admin.site.register(MoodEntry)
admin.site.register(UserProfile)