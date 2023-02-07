from django.shortcuts import render,redirect
from .models import Homework, Notes
import requests,wikipedia,random
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request,'dashboard/home.html')

@login_required(login_url='login')
def todo(request):
    return render(request,'dashboard/todo.html')

def do_logout(request):
    logout(request)
    return render(request,'dashboard/register.html',{'error_msg': 'User has been successfully logged out'})

def do_login(request):
    error_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        auth_ = authenticate(request,username=username,password=password)
        if auth_ is not None:
            print("User logging") 
            print(auth_)
            login(request,auth_)
            return redirect('render_homepage') 
        else:
            print("user not logging")
            error_msg = 'Username or Password is Incorrect! Please try again!'
            return render(request,'dashboard/login.html',{'error_msg': error_msg})
    else:                                                                         
        return render(request,'dashboard/login.html',{'error_msg': error_msg})

def do_register(request):
    error_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            error_msg = 'Password and Confirm Password are not same!!!!!!'
            return redirect(request,'dashboard/register.html',{'error_msg': error_msg})
        user_ = User.objects.create_user(username,email,password1)
        user_.save()
        
        return redirect('login')   
    else:
        return render(request,'dashboard/register.html',{'error_msg': error_msg})

def books(request):
    books_list = []
    list_exist = False
    if request.method == 'POST':
        search = request.POST['search']
        url = 'https://www.googleapis.com/books/v1/volumes'        
        x = requests.get(url, params = {"q":search,"maxResults": 40})
        json_data = x.json()
        for item in json_data['items']:
            if item['volumeInfo'].get('imageLinks') == None:
                continue
            d = {}
            d['title'] = item['volumeInfo']['title']
            d['subtitle'] = item['volumeInfo'].get('subtitle','No Subtitle Avaiable for this...')
            author_list = ''
            check_author = item['volumeInfo'].get('authors','')
            if check_author != '':
                for author in item['volumeInfo']['authors']:
                    author_list += str(author) + ','
            d['authors'] = author_list
            d['desc'] = item['volumeInfo'].get('description','No Desciption Available for this...')
            d['thumbnail'] = item['volumeInfo']['imageLinks']['thumbnail']
            d['infoLink'] = item['volumeInfo']['infoLink'] 
            books_list.append(d)
        if len(books_list) > 0:
            list_exist = True
    return render(request,'dashboard/books.html',{'list': books_list,'exist': list_exist})

def wiki(request):
    content_ = ''
    if request.method == 'POST':
        search = request.POST['search']
        content_ = str(content_)
        try:
            content_ = wikipedia.page(search).content
        except wikipedia.DisambiguationError as e:
            s = random.choice(e.options)
            content_ = wikipedia.page(s).content
        except wikipedia.PageError as e:
            content_ = "No information found for the word: "+str(search)+" on wikipedia!!"
        except wikipedia.exceptions as e:
            l = wikipedia.search(search)
            if l and content_ == '':
                content_ = wikipedia.page(l[0]).content
    return render(request,'dashboard/wiki.html',{'content': content_})

def youtube(request):
    youtube_data = []
    if request.method == 'POST':
        search = request.POST['search']
        url = 'https://www.googleapis.com/youtube/v3/search'
        #demonstrate how to use the 'params' parameter:
        x = requests.get(url, params = {"part": "snippet","q":search,"maxResults": 100,"key":"AIzaSyDr1EsC02ozytQG0mncb1mpmY5eMZIWEPE"})
        json_data = x.json()
        
        for data in json_data['items']:
            d = {}
            temp = data['snippet']
            d['title'] = temp['title']
            d['description'] = temp['description']
            d['thumb_url'] = temp['thumbnails']['medium']['url']
            d['link'] = '#'
            if('videoId' in data['id'] != None):
                d['link'] = 'https://www.youtube.com/watch?v='+data['id']['videoId']
            else:
                continue
            # d['thumb_width'] = temp['thumbnails']['medium']['width']
            # d['thumb_height'] = temp['thumbnails']['medium']['height']
            d['channel_title'] = temp['channelTitle']
            youtube_data.append(d)
        return render(request,'dashboard/youtube.html',{'data': youtube_data,'token':json_data['nextPageToken']})
    else:
        return render(request,'dashboard/youtube.html',{'data': youtube_data})

def homework(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        title = request.POST['title']
        desc = request.POST['description']
        date_ = request.POST['duedate']
        finish = request.POST.get('finished',False)
        if finish is not None and finish == 'on':
            finish = True
        else:
            finish = False
        new_homework = Homework(subject=subject,title=title,description=desc,homework_date=date_,finish=finish)
        new_homework.save()
    homeworks = Homework.objects.all()
    return render(request,'dashboard/homework.html',{'homework': homeworks})

def homework_delete(request,pk):
    homework = Homework.objects.get(id=pk)
    homework.delete()
    return redirect('homework_page')

def homework_update(request,pk,status):
    homework = Homework.objects.filter(id=pk)
    b = False
    if status == 1:
        b = True
    else:
        b = False
    homework.update(finish=b)
    return redirect('homework_page')
def notes(request):
    notes = []
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['description']
        new_note = Notes(title=title,description=desc)
        new_note.save()
    notes = Notes.objects.all()
    return render(request,'dashboard/notes.html',{'notes': notes})

def notes_delete(request,pk):
    note = Notes.objects.get(id=pk)
    note.delete()
    return redirect('notes_page')

def dictionary(request):
    if request.method == 'POST':
        q = request.POST['search']
        api_str = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
        api_str += str(q)
        x = requests.get(api_str)
        json_data = x.json()
        audio_arr = []
        text_arr = []
        synonyms = []
        antonyms = []
        defination_arr = []
        example_arr = []
        word = q
        exist = False
        if type(json_data) == dict:
            return render(request,'dashboard/dictionary.html',{'exist': False})
        internal_data = json_data[0]
        if 'word' in internal_data.keys():
            exist = True
        else:
            return render(request,'dashboard/dictionary.html',{'exist': exist})
        for internal_data in json_data:
            if 'phonetic' in internal_data.keys():
                text_arr.append(internal_data['phonetic'])
            for item in internal_data['phonetics']:
                if 'audio' in item.keys():
                    audio_arr.append(item['audio'])
                if 'text' in item.keys():
                    text_arr.append(item['text'])
            for item in internal_data['meanings']:
                if 'definitions' in item.keys():
                    for d in item['definitions']:
                        if 'definition' in d.keys():
                            defination_arr.append(d['definition'])
                        if 'example' in d.keys():
                            example_arr.append(d['example'])
                        if 'synonyms' in d.keys():
                            for word in d['synonyms']:
                                synonyms.append(word)
                        if 'antonyms' in d.keys():
                            for word in d['antonyms']:
                                antonyms.append(word)
                if 'synonyms' in item.keys():
                    for sy in item['synonyms']:
                        synonyms.append(sy)
                if 'antonyms' in item.keys():
                    for ay in item['antonyms']:
                        antonyms.append(ay)

        context = {}
        if len(defination_arr) == 0:
            exist = False
        else:
            context['definition'] = defination_arr[0]
            if len(example_arr) == 0:
                context['example'] = 'No Examples found for this word'
            else:
                context['example']  = example_arr[0]
        if len(text_arr) > 0:
            context['text'] = text_arr[0]
        else:
            context['text'] = q
        if len(synonyms) > 0:
            context['synonym'] = synonyms[0]
        else:
            context['synonym'] = 'No Synonym Found'
        if len(antonyms) > 0:
            context['antonym'] = antonyms[0]
        else:
            context['antonym'] = 'No Antonym Found'
        context['exist'] = exist
        audio_arr = [ele for ele in audio_arr if ele.strip()]
        if len(audio_arr) > 0:
            context['audio'] = audio_arr[0]
        else:
            context['audio'] = '#'
        context['word'] = q
        return render(request,'dashboard/dictionary.html',context)
    return render(request,'dashboard/dictionary.html',{'exist': False})
