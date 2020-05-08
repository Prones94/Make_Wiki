from django.urls import path
from .views import PageListView, PageDetailView, PageCreateView


urlpatterns = [
    path('', PageListView.as_view(), name='wiki-list-page'),
    path('wiki/new/', PageCreateView.as_view(), name='create'),
    path('<str:slug>/', PageDetailView.as_view(), name='wiki-details-page'),
    
]
