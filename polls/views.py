''' views for the polls app '''

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.db.models import F
from django.utils import timezone
from django.views import generic

from django.contrib.auth import login, authenticate

from .models import Question, Choice #CreatePoll
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future, and also, each of the returned questions must have at least, one choice).
        """
        all_questions = Question.objects.all()
        has_choice = True
        questions_with_choices = []
        filtered_list = []
        for question in all_questions:
            if len(question.choice_set.all()) < 1:
                has_choice = False
            else:
                has_choice = True
                questions_with_choices.append(question)
        for question in questions_with_choices:
            if question.pub_date <= timezone.now():
                filtered_list.append(question)
            else:
                pass
        return filtered_list[:5]
            

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte = timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

def create_poll_index(request):
    return render(request, 'polls/create_poll.html', context={'user':request.user})

def create_poll(request):
    """Enables anonymous and authenticated users to create a poll """
    if request.method == 'POST':
        question_text = request.POST.get('poll_question')
        choice_text = request.POST.get('poll_choice')
        question = Question.objects.create(question_text=question_text,
        pub_date=timezone.now(),
        )
        question.save()
        choice = Choice.objects.create(choice_text = choice_text, votes=0, question=question)
        choice.save()
        context = {
                'question':question,
                }
        return render(request, 'polls/my_poll_detail.html', context)
    else:
        #return HttpResponse('Not created successfuly. Try again')
        return render(request, 'polls/create_poll.html')
        


def poll_detail(request):
    return HttpResponse('Done!')

    
       
def votes(request, question_id):
    question = get_object_or_404(Question, pk = question_id)

    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])

    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message':"You didn't select a choice", 
        })

    else:
        selected_choice.votes = F('votes') + 1 #Avoids error when multiple users vote at the same time
        selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,))) 

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user.save()
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             #return HttpResponseRedirect(reverse('polls:index'))
#             return redirect('polls:index')

#     else:
#         form = SignUpForm()
#     return render(request, 'polls/signup.html',{'form':form})

def contact(request):
    return HttpResponse('Contact template not yet available')

def faq(request):
    return HttpResponse('faq template not yet available')

def help_(request):
    return HttpResponse('help template not yet available')

def archives(request):
    return HttpResponse('Archives template not yet available')

def events(request):
    return HttpResponse('Events template not yet available')

def privacy_policy(request):
    return HttpResponse('Privacy policy not yet available')