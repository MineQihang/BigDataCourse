from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^handwrittenBoard/', views.handwrittenBoard),
]
