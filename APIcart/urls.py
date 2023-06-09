from django.urls import path
from APIcart import views
urlpatterns = [
    path("", views.Cart),
    # path("text_input", views.text_input),

]
