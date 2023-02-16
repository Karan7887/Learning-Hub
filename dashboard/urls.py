from django.contrib import admin
from django.urls import path,include
from dashboard import views
urlpatterns = [
    path('/',views.home,name='render_homepage'),
    path('/notes',views.notes,name='notes_page'),
    path('/homework',views.homework,name='homework_page'),
    path('/todo',views.todo,name='todo_page'),
    path('/wiki',views.wiki,name='wiki_page'),
    path('/books',views.books,name='books_page'),
    path('/youtube',views.youtube,name='youtube_page'),
    path('/todo',views.todo,name='conversion_page'),
    path('/dictionary',views.dictionary,name='dictionary_page'),
    path('/register',views.do_register,name='register'),
    path('/login',views.do_login,name='login'), 
    path('/logout',views.do_logout,name='logout'), 
    path('/notes/delete/<int:pk>', views.notes_delete, name='notes_delete'),
    path('/homework/delete/<int:pk>', views.homework_delete, name='homework_delete'),
    path('/homework/update/<int:pk>/<int:status>', views.homework_update, name='homework_update'),
    path('/todo/delete/<int:pk>', views.todo_delete, name='todo_delete'),
    path('/todo/update/<int:pk>/<int:status>', views.todo_update, name='todo_update')
]