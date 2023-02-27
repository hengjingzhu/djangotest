from django.urls import path
from app01.views import testview,test_render

urlpatterns = [
    path('01/', testview),
    path('index/',test_render)
]
