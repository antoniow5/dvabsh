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
from app.serializers import LoginSerializer, RegisterSerializer 



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
                    token.created = datetime.datetime.utcnow()
                    token.save()
                return Response({"token": token.key})
            else:
                return Response(status=401)
    else:
        return Response(serializer.errors, status = 400)


@api_view(['POST'])
def users_list(request): 
    if request.method == "POST": 
        username = request.data['username']
        email = request.data['email']
        duplicates = check_duplicates(username, email)
        if duplicates is not None: return Response({duplicates: ''}, status = 401)
        else: 
            serializer = RegisterSerializer(data = request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status = 400)
            else: 
                user = serializer.save()
                tkn = Token.objects.create(user=user)
                return Response({"token": tkn.key}, status = 201)

# ну вроде должно работать, проверь            


def check_duplicates(username, email):
    if User.objects.filter(username=username).exists(): return Response(status=401)
    elif User.objects.filter(email=email).exists(): return Response(status=401)
    else: return None