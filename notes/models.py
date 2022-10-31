from django.db import models

class Note(models.Model):
    #both these fields can be empty when you create a new note for the first time
    title = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    # Notes will be sorted using this field
    last_updated_on = models.DateTimeField(auto_now=True)

    # To delete a note, we wil simply set is_active to False
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
