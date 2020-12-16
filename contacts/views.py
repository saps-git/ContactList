from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
"""
The create/retrieve/update/delete operations that we will be using are going to be pretty similar
for any model-backed API views we create. Those bits of common behaviour are implemented in REST framework's 
mixin classes. (generics)
 
ListCreateAPIView = Will handle creation and listing

RetrieveUpdateDestroyAPIView = Will handle update and deletion

"""
from .models import Contact
from .serializers import ContactSerializer
from rest_framework import permissions
# Create your views here.

class ContactList(ListCreateAPIView): 
    serializer_class = ContactSerializer
    permission_classes = (permissions.IsAuthenticated, )

    """
    (default example)
    class SnippetList(generics.ListCreateAPIView):
        queryset = Snippet.objects.all()
        serializer_class = SnippetSerializer
    """

    def perform_create(self, serializer): #overwritting this method to tell it how to create an instance (adding extra)
        serializer.save(owner = self.request.user) #since every user will have its own contact list, hence making the owner the user himself

    def get_queryset(self): #overwritting this method to tell it how to return an instance (adding extra)
        return Contact.objects.filter(owner=self.request.user)

class ContactDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ContactSerializer
    permission_classes = (permissions.IsAuthenticated,)
    """
    (default example)
    class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
        queryset = Snippet.objects.all()
        serializer_class = SnippetSerializer
    """
    lookup_field = "id" #adding a lookup field, to help to lookup the instance we need

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)

