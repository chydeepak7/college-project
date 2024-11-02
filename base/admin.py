from django.contrib import admin
from .models import *
# Register your models here.

class ChatMessageAdmin(admin.ModelAdmin):
    list_editable = ['is_read']
    list_display = ['sender','receiver','message','is_read']

admin.site.register(Room)
admin.site.register(UserType)
admin.site.register(Profile)
admin.site.register(ChatMessage,ChatMessageAdmin)
admin.site.register(RegistrationDetails)
admin.site.register(RoomDetails)