from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from app.models import Category, Topic, Comment
from django.db.models.functions import Coalesce
from django.db.models import Max, Count, Prefetch
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.response import Response
import datetime
from app.serializers import LoginSerializer


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data = request.data)
    if serializer.is_valid():
        if not User.objects.filter(email = request.data['email']).exists():
            return Response(status = 404)
        else:
            username = User.objects.get(email = request.data['email']).username
            user = authenticate(username=username, password=request.data['password'])
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                if not created:
                    # update the created time of the token to keep it valid
                    token.created = datetime.datetime.utcnow()
                    token.save()
                return Response({"token": token.key})
            else:
                return Response(status=401)
    else:
        return Response(serializer.errors, status = 400)


@api_view(['POST'])
def register(request):
    if User.objects.filter(username = request.data['username']).exists:
        return Response({'username-exists':''}, status = 401)
    elif User.objects.filter(email = request.data['email']).exists:
        return Response({'email-exists':''}, status = 401)
    else:
        token = Token.objects.create(user = serializer.save())
        return Response({"token": token.key}, status= status.HTTP_201_CREATED)
