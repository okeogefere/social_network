from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(FriendRequest)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)