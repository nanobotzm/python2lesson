from django.contrib import admin
from .models import City, Language, Vacancy, Errors, URL

admin.site.register(City)
admin.site.register(Language)
admin.site.register(Vacancy)
admin.site.register(Errors)
admin.site.register(URL)
