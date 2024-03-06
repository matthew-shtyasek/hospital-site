from django.urls import path
from proposal import views

urlpatterns = [
    path('proposal/<int:doctor_id>/', views.proposal, name='proposal'),
]
