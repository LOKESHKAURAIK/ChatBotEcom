from django.contrib import admin
from .models import Chatbot


# admin.site.register(Chatbot)

@admin.register(Chatbot)
class ChatbotAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_input', "bot_response", "created_at"]
    
