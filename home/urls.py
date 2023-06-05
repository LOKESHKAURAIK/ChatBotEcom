from django.urls import path
from home import views
urlpatterns = [
    path("", views.index),
    path("text_input", views.text_input),

]
