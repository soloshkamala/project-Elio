from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calendar/', include('ELIO.calendar_app.urls')),
    path('profile/', include('ELIO.user_page.urls')),
    path('advice/', include('advice.urls')),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]



