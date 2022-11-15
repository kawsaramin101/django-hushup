from django.shortcuts import render

from .models import Message 
from users.models import CustomUser


def messages_view(request):
    messages = Message.objects.filter(receiver=request.user, soft_deleted=False)
    
    return render(request, 'hush/messages.html', {"messages": messages})
    


def send_message(request, receiver_id):
    receiver = CustomUser.objects.get(secondary_id=receiver_id)
    
    #messageform = 
    pass

def unread_messages(request):
    messages = Message.unread_objs.filter(receiver=request.user)
    return render(request, 'unread_messages.html', {"context": messages})
    