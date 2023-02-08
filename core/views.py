from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permission import IsAuthor

# Create your views here.
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'
    # If we used these two clasess in settings.py then these settings are applied globally
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsAuthor]

    def perform_create(self, serializer):
        # return super().perform_create(serializer)
        serializer.save(author = self.request.user)

'''
class BookViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'slug' 
'''


# creating the class viewset
'''
class BookViewSet(viewsets.ViewSet):

    def list(self, request):
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class BookdetailsViewSet(viewsets.ViewSet):
        
    def retrieve(self, request, slug):
        book = Book.objects.get(slug=slug)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def update(self, request, slug):
        book = Book.objects.get(slug=slug)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug):
        book = Book.objects.get(slug=slug)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''
'''

# generic class apiview
class Booklist(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class Bookdetails(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Book.objects.all()
    serializer_class = BookSerializer
'''

'''
#This is the class based views using the mixins
# This is also very short in lines

class Booklist(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class Bookdetails(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
'''

# Here we are creating the class based API views
# It is more usefull than function based views. It requires less code
'''
class Booklist(APIView):

    def get(self, request):
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Bookdetails(APIView):
    def get_object(self, slug):
        try:
            return Book.objects.get(slug=slug)
        except Book.DoesNotExist:
            raise Http404
        
    def get(self, request, slug):
        book = self.get_object(slug)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def post(self, request, slug):
        book = self.get_object(slug)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        book = self.get_object(slug)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''
'''
@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def single_book(request, slug):
    try:
        book = Book.objects.get(slug=slug)
    except Book.DoesNotExist:
        return Response("NOT FOUND" ,status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        book.delete()
        return Response("DELETION SUCCESSFULL" ,status=status.HTTP_204_NO_CONTENT)
'''
'''
@csrf_exempt
def book_list(request):

    # get all the books list
    if request.method == 'GET':
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)

        return JsonResponse(serializer.data, safe=False)

    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def single_book(request, slug):

    try:
        book = Book.objects.get(slug=slug)
    except Book.DoesNotExist:
        return HttpResponse(status = 404)

    if request.method == 'GET':
        serializers = BookSerializer(book)
        return JsonResponse(serializers.data, status=200)
   
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=404)

    elif request.method == 'DELETE':
        book.delete()
        return HttpResponse(status=204)
'''