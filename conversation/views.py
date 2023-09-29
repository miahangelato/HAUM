from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from conversation.forms import ConversationMessageForm
from conversation.models import Conversation
from item.models import Item


# Create your views here.
@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('conversation:detail_conversation', pk=item_pk)

    conversations = Conversation.objects.filter(members=request.user).filter(item=item)

    if conversations:
        pass

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.sender = request.user
            conversation_message.save()
            return redirect('conversation:detail_conversation', pk=conversation.pk)

    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new_conversation.html', {
        'form': form,
    })

@login_required
def inbox (request):
    conversations = Conversation.objects.filter(members=request.user)
    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,
    })

@login_required
def detail_conversation(request, pk):
    conversation = Conversation.objects.filter(members=request.user).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.sender = request.user
            conversation_message.save()

            conversation.save()
            return redirect('conversation:detail_conversation', pk=conversation.pk)

    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail_conversation.html', {
        'conversation': conversation,
        'form': form,
    })