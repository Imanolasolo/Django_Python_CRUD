# Django-Python based full stack CRUD Tool


![image](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR34KcgkFGz7FjnKPBjfb2VZd2oy4M11esFMg&usqp=CAU)

## Introduction

I created this CRUD tool basing myself on a note creating app and use it as personal notes store, but the project is easily customizable to build any kind of CRUD applications.

To build an application like this, we need a database table that stores a list notes consisting of Title, Content, and the last updated date and hour. So we need to create some functions to make the different CRUD tasks:
* Creating a new note with empty title and content.
* Update the newly created note.
* Read the note and it´s diverse fields.
* Partially update the note.
* List all of notes includes in our database.
* Delete a note from app (not from database).

I used a Django-Phyton framework to build this database to show the power of the framework in crating, modifying and storing data for different purposes.

## Step 1, Set the Django project.

Run these commands on your preferred command line.
* Create a python3 virtual environment to isolate the project from your system.
```
python3 -m venv django_env
```
* Activate the virtual environment.
```
source django_env/bin/activate/
```
* Install all the dependencies (line by line)
```
pip install django
pip install djangorestframework
```
* Create a new django project called "notesapp" and create the initial database tables.
```
django-admin startproject notesapp
cd notesapp
python3 manage.py migrate
```
**Note**: This action creates a sqlite3 file in the folder who will act as database, but if you want to use a different database, feel free to change it like i did in the settings.py file where I used a Postgres database.

* Create a new appplication into the project called "notes".

```
python3 manage.py startapp notes
```

## Step 2, creating database models

I will create a database model on which we will perform the CRUD operations.

In `notes/models.py` file created earlier with django change and write:

```
from django.db import models

class Note(models.Model):
    # both these fields can be empty when you create a new note for the first time
    title = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    # notes will be sorted using this field
    last_udpated_on = models.DateTimeField(auto_now=True)

    # to delete a note, we will simply set is_active to False
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

```
Here I created the different fields which will complete the tables on the database.

Now we need to update the schema because we made changes on the database.

So in the command line perform these tasks one by one.
```
python3 manage.py makemigrations
python3 manage.py migrate
```
## Step 3, creating the CRUD APIs.

We will use `Django Rest Framework` to ceate the APIs who will give the sense to CRUD operations, and a nice to watch interface to view them.

The first step to make it is to `define a serializer` who will validate and allow request if the fields are OK, and will convert a database table entry in a JSON object to work with.

So let us create a serializer in `notes/serializers.py` as follows.
```
from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'title', 'content', 'last_udpated_on', 'is_active')
```
**DEFINING AN API VIEW SET**

In Django, the APIs are written in views.py and each API that does some operation on a certain database resource is a view. In our case we will be performing multiple operations on the database model and hence what we need is a viewset. Here is how you define one in `notes/views.py`

```
from django.shortcuts import render, get_object_or_404

from rest_framework.viewsets import ModelViewSet
from .models import Note
from .serializers import NoteSerializer


class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer

    def get_object(self):
        return get_object_or_404(Note, id=self.request.query_params.get("id"))

    def get_queryset(self):
        return Note.objects.filter(is_active=True).order_by('-last_udpated_on')

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
```
This viewset is now capable of performing all the CRUD operations and it will use the NoteSerializer to determine how the data will be received and how it will be sent back to the requesting client.

**‍DEFINING THE URL PATH‍**

We just have one more step to complete before we can see our APIs in action and that is to determine what URL path will invoke the above viewset. This can be done in `notesapp/urls.py` as follows.

```
from django.contrib import admin
from django.urls import path
from notes.views import NoteViewSet
from django.urls import re_path as url

urlpatterns = [
    # the admin path is present by default when you create the Django profject. It is used to access the Django admin panel.
    path('admin/', admin.site.urls),

    # the URLs for your APIs start from here
    url(r'^note$', NoteViewSet.as_view(
        {
            'get': 'retrieve',
            'post': 'create',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }
    )),
    url(r'^note/all$', NoteViewSet.as_view(
        {
            'get': 'list',
        }
    )),
]
```
To explain what is going on here, we are basically saying that if the url /note is called, no matter what the HTTP method is, we will be invoking the NoteViewSet and based on what the HTTP method is we will call a particular method within this viewset.‍

* A POST call will result in a create operation of the Note model.
* A GET call will result in retrieving a single Note model object using the id query parameter.
* A PUT call will result in replacing an existing Note model with a new Note and the existing Note model will be fetched using the id query parameter.
* A PATCH call will result in modifying only a certain field inside an existing Note model instead of entirely replacing it and the existing Note model will be fetched using the id query parameter.
* A DELETE call will result in calling a destroy function which internally calls the perform_destroy method defined above in views.py.
* In case you haven't noticed, there is one thing missing in this url PATH and that is the ability to list all the existing Note model objects.

* To solve this I created another URL path /note/all where I am invoking the same viewset as the above one with the difference being the GET call will now invoke a list method on the viewset instead of a retrieve method which means that the get_queryset method defined earlier will be invoked.

## Step 4, watch your APIs in action

Let us now run the server and view the APIs in action. You can run the Django development server using the below command and it will expose your server on the 8000 port on localhost.

Before of it do not forget to include `rest_framework` in the **INSTALLED_APPS** section of `notesapp/settings.py` or you will end up seeing weird errors.

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
     
    #include rest_framework here
    'rest_framework',
    'notes'
]
```
Now let´s watch the result:

In command line type:
```
python3 manage.py runserver
```
With this command you will run the app in your server.

In your preferred browser just open:

```
http://localhost:8000/note?id=1
```
And *voilá*, your app is running in your remote environment!

![image](https://uploads-ssl.webflow.com/5e0b01877436086c8beecd1a/5fb0aa5cedd5312372841411_PifgKlWKfMnLscQGtVyh4PRIymvcnottdrIMNU_qzK6y2A_vhKDABVeGsYnImHw7rRpJodXHFIhNqiplt7eHW3yKURDsFVTJDf2HDZOsuGbo29L6i-uRQFAeRry-VAXZ4Npy2t-W.png)

Pretty cool right? Since there is no Note that currently exists in the database the response says "Not Found" but you can now use this same interface to create a new Note in the database.

* Use POST button to show and create your first note in database.

* Use PUT button to add content to the note.

* Use PATCH buttton to add partial content to the note.

* With DELETE button you can delete the note from app, not from database as early related.

*If you want new notes, just play with POST button.

