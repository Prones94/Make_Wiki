from django.urls import path
from .views import PageListView, PageDetailView, PageCreateView


urlpatterns = [
    path('', PageListView.as_view(), name='wiki-list-page'),
    path('<str:slug>/', PageDetailView.as_view(), name='wiki-details-page'),
    path('create/', PageCreateView.as_view(), name='wiki-create-page')
]
