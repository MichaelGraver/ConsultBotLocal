from django.conf.urls import url
from Bot import views

urlpatterns = [
    url(r'Consent/', views.Consent.as_view(), name='Consent'),
    url(r'Participant/', views.Participant.as_view(), name='Participant'),
    url(r'^$', views.Intro.as_view(), name='Intro'),
    url(r'index/', views.index.as_view(), name='index'),
    url(r'survey/', views.QuestionnaireView.as_view(), name='Questionnaire'),
    url(r'stats/', views.Statistics.as_view(), name='stats'),
]