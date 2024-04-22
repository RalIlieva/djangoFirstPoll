from django.http import HttpResponse, Http404, HttpResponseRedirect
# from django.template import loader - not needed when render template is used
from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.urls import reverse
from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # template = loader.get_template('polls/index.html')
    context = {"latest_question_list": latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {"question": question})
    # Second version
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'polls/detail,html', {"question": question})

    # return HttpResponse("You are looking at question %s." % question_id) - initial version


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
    # Initial version:
    # response = "You are looking at question %s."
    # return HttpResponse(response % question_id)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
    #     Redisplay the question voting
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You did not select a choice.',
        },)
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
    #     Good practice to end with redirect to avoid posting twice
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    # return HttpResponse("You are voting on question %s." % question_id) - initial version
