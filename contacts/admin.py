from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    fields = ('id','first_name', 'last_name','initials','email','phone','color')
    list_display = ('id','first_name', 'last_name','email','phone',)
    search_fields = ('first_name', 'last_name','email',)

admin.site.register(Contact, ContactAdmin)