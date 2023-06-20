from django.db import models

class Chatbot(models.Model):
    user_input = models.CharField(max_length=100)
    bot_response = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_input
    