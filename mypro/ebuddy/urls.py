from django.urls import path
from . import views

urlpatterns = [
    path('insert',views.makeCreate),
    path('view',views.makeList),
    path('page',views.makePage)
]
