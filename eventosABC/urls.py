'''This is a docstring'''
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .api import (registration_view,
                  api_detail_event_view,
                  api_create_event,)
from .views import create_user, api_auth, create_event, event_detail, event_update, get_events

app_name = 'eventosABC'

urlpatterns = [
    path('api/create-user/', registration_view, name="create-user"),
    path('api/api-auth/', obtain_auth_token, name="login"),
    path('api/events/', api_create_event, name="event_create"),
    path('api/events/<str:event_id>/', api_detail_event_view, name="event_detail"),
    path('signup/', create_user, name="singup"),
    path('login/', api_auth, name="login"),
    path('create-event/', create_event, name='create-event'),
    path('event-detail/<str:event_id>/', event_detail, name="event-detail"),
    path('event-update/<str:event_id>/', event_update, name="event-update"),
    path('', get_events, name="get-events")
]
