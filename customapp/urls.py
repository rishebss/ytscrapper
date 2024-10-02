from django.urls import path
from . import views
app_name="customapp"

urlpatterns = [
path('',views.fetch_youtube_videos, name='youtube_arts'),

]
