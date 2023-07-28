from django.contrib import admin
from .models import Post
# Register your models here.
class Postadmin(admin.ModelAdmin):
    list_display = ('title','name','desc','date')
    list_filter = ("date",)
    search_fields = ['title', 'name']
admin.site.register(Post,Postadmin)
