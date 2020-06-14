from . import views
from django.urls import path

app_name = 'polls'
urlpatterns = [
path('', views.IndexView.as_view(), name='index'),
path('<int:pk>/', views.DetailView.as_view(), name='detail'),
path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
path('<int:question_id>/votes/', views.votes, name='votes'),

path('create_poll/index/', views.create_poll_index, name='create_poll_index'),
path('create_poll/', views.create_poll, name='create_poll'),
path('create_poll/detail/', views.poll_detail, name='create_poll_detail'),

path('contact/', views.contact, name='contact'),
path('faq/', views.faq, name='faq'),
path('help/', views.help_, name='help_'),
path('archives/', views.archives, name='archives'),
path('events/', views.events, name='events'),
path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
]

#TO DO
#help, contact, 