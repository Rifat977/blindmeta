from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(PersonalMessage)
admin.site.register(Book)
admin.site.register(Room)