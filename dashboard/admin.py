from django.contrib import admin
from .models import Notes,Homework
# Register your models here.

class NotesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notes)

class HomeworkAdmin(admin.ModelAdmin):
    pass
admin.site.register(Homework)
