'''This is a docstring'''
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import Event
from .serializers import UserSerializer, EventSerializer

# Crear usuario
@api_view(['POST',])
@permission_classes(())
def registration_view(request):
    '''This is a docstring'''
    if request.method == 'POST':
        serilizer = UserSerializer(data=request.data)
        data = {}
        if serilizer.is_valid():
            user = serilizer.save()
            data['response'] = "El usuario se creo exitosamente."
            data['email'] = user.email
            data['username'] = user.username
            data['first_name'] = user.first_name
            data['last_name'] = user.last_name
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serilizer.errors
        return Response(data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def api_detail_event_view(request, event_id):
    '''This is a docstring'''
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if event.user != user:
        return Response({'response': "You don't have permission to do that."})


    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = "Update successful"
            return Response(serializer.data)
        else:
            data = serializer.errors
        return Response(data)

    if request.method == 'DELETE':
        operation = event.delete()
        data = {}
        if operation:
            data['success'] = "Delete successful"
        else:
            data["failure"] = "Delete failed"
        return Response(data=data)


@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated,))
def api_create_event(request):
    '''This is a docstring'''
    account = request.user

    event = Event(user=account)

    if request.method == 'POST':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        events = Event.objects.filter(user=request.user).order_by('id')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
