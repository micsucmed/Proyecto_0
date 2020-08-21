'''This is a docstring'''
from rest_framework import serializers
from .models import User, Event

class UserSerializer(serializers.ModelSerializer):
    '''This is a docstring'''
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user

class EventSerializer(serializers.ModelSerializer):
    '''This is a docstring'''
    username = serializers.SerializerMethodField('get_event_user')
    id = serializers.ReadOnlyField()
    class Meta:
        model = Event
        fields = ['id',
                  'event_name',
                  'event_category',
                  'event_place',
                  'event_address',
                  'event_initial_date',
                  'event_final_date',
                  'event_type',
                  'username']

    def get_event_user(self, event):
        '''This is a docstring'''
        username = event.user.username
        return username
