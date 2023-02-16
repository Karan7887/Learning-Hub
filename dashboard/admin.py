from django.contrib import admin
from .models import Notes,Homework,Todos
# Register your models here.

class NotesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notes)

class HomeworkAdmin(admin.ModelAdmin):
    pass
admin.site.register(Homework)

class TodosAdmin(admin.ModelAdmin):
    pass
admin.site.register(Todos)
