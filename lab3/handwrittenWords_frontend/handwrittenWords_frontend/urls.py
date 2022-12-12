from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from handwrittenWords_frontend.views import handwrittenBoard

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', handwrittenBoard, name='handwrittenBoard'),
    url(r'^', include('handwrittenBoard.urls')),
]
