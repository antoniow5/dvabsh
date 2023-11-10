from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from forum.serializers import TopicListCategoryAllSerializer, TopicListCategorySpecifiedSerializer, TopicCreateSerializer, TopicDetailSerializer, TopicCommentsDetailSerializer, TopicEditSerializer
from ..models import Category, Topic
from rest_framework.exceptions import PermissionDenied
from django.http import Http404
from django.db.models import Max, Count, Prefetch
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
from model_bakery import baker
from itertools import cycle

@api_view(['GET','POST'])
def topics_list(request):
    if request.method == 'GET':
        params = dict(request.query_params)
        print(params)
        if 'cat' in params:
            try:
                category = Category.objects.get(slug = params['cat'][0])
            except Exception:
                raise Http404
            topics = Topic.objects.filter(category = category)
            if not topics.exists():
                content = {"message": "Опубликованных тем еще нет. Стантьте первым!"}
                return Response(content, status = status.HTTP_204_NO_CONTENT)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        topics_count = topics.count()
        if 'order' in params and (params['order'][0] == 'created' or params['order'][0] == 'comment'): 
            if params['order'][0] == 'created':
                topics = topics.order_by('-created_at')
            if params['order'][0] == 'comment':

                topics = topics.order_by('-bump')
        else:
            topics = topics.order_by('-bump')
        page = 1
        limit = 20
        try:
            if 'page' in params and int(params['page'][0]) > 0: 
                page = int(params['page'][0])
        except Exception as e:
            return Response( status = status.HTTP_400_BAD_REQUEST)
        try:
            if 'offset' in params and int(params['offset'][0]) > 0:
                limit = int(params['offset'][0])
        except Exception as e:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        try:
            topics = topics[(page-1)*limit:page*limit]
        except Exception as e:
            raise Http404  
     
        topics = topics.values_list('id', flat = True)
        # topics = topics.reverse()
        topics = Topic.objects.filter(id__in = topics)
        topics = topics.annotate(comments_count=Count('comments'))
        topics = topics.select_related('author')
        topics = topics.order_by('-bump')
    
        

        return_dict = { 
                'pages_num' : (topics_count + limit - 1) // limit,
                'topics_num': topics_count,
                'results': topics.values('id', 'author__username', 'author_id', 'comments_count', 'bump', 'text', 'title')
            }

        return Response(return_dict)

    elif(request.method == 'POST'):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                serializer = TopicCreateSerializer(data = request.data, context = {'request':request})
            else:
                if not Category.objects.get(slug=request.data['category']).can_post:
                    raise PermissionDenied
                if request.data['is_pinned'] == True:
                    raise PermissionDenied
                serializer = TopicCreateSerializer(data = request.data, context = {'request':request})
            if serializer.is_valid():
                serializer.save()
                return Response(status= status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied({"message":"You don't have permission"})


@api_view(['GET','DELETE'])
def topics_detail(request, id):
    if request.method == 'GET':
        topic = Topic.objects.get(id = id)
        return_dict = {"title": topic.title,
                       "text": topic.text,
                       "author": topic.author.username,
                       "created_at": topic.created_at,
                       "category": topic.category.slug,
                       "bump": topic.bump}
        comments = topic.comments.order_by('-created_at')
        comments = comments.select_related('author').prefetch_related('answer_to')
        return_dict['comments'] =  comments.values('id', 'author', 'text', 'created_at', 'answer_to')
        return Response(return_dict)



