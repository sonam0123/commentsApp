from dateutil.parser import parse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required


from .models import Comment, Conversation



def home(request):
    return render(request, "comments/home.html")


@login_required
def comment(request):
    print request.method
    if request.method == 'POST':
        selectedtext = request.POST.get('text')
        comment = request.POST.get('comment')
        if selectedtext and comment:
            try:
                conversation = Conversation.objects.get(text=selectedtext)
            except Conversation.DoesNotExist:
                conversation = Conversation(text=selectedtext)
                conversation.save()
            comment = Comment(user=request.user, conversation=conversation, comment=comment)
            comment.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False}, status=400)
    else:
        text = request.GET.get('text')
        timestamp = request.GET.get('timestamp')
        conversation = get_object_or_404(Conversation, text=text)
        try:
            comment_after = parse(timestamp)
            comments = conversation.comment_set.filter(created__lt=comment_after).order_by('created')
        except ValueError:
            comments = conversation.comment_set.all().order_by('created')
        comment_list = []
        for comment in comments:
            comment_list.append({
                'user': comment.user.username,
                'comment': comment.comment,
                'created': comment.created.strftime('%c'),
            })
        data = {
            'text': conversation.text,
            'comments': comment_list,
        }
        return JsonResponse(data)
