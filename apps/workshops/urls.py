from django.urls import path
from . import views

app_name = 'workshops'

urlpatterns = [
    path('', views.WorkshopListView.as_view(), name='list'),
    path('<slug:slug>/', views.WorkshopDetailView.as_view(), name='detail'),
    path('<slug:slug>/enroll/', views.EnrollView.as_view(), name='enroll'),
    path('<slug:slug>/cancel/', views.CancelEnrollmentView.as_view(), name='cancel'),
]