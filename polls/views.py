from django.db.models import F
from django.http import (
    # HttpResponse,
    # Http404,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404, render

# from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from polls.models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        """
    Return the last five published questions (not including those set to be
    published in the future).
    """
        # return Question.objects.order_by("-pub_date")[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


# def index(request):
#     # return HttpResponse("Hello, World! You're at the polls index.")
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     # template = loader.get_template("polls/index.html")
#     context = {"latest_question_list": latest_question_list}
#     # output = ", ".join([q.question_text for q in latest_question_list])
#     # return HttpResponse(template.render(context, request))
#     return render(request, "polls/index.html", context)


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


# def detail(request, question_id):
#     # return HttpResponse("You're looking at the question %s." % question_id)
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


# def results(request, question_id):
#     # response = "You're looking at the results of question %s."
#     # return HttpResponse(response % question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     return render(
#         request=request,
#         template_name="polls/results.html",
#         context={"question": question},
#     )


def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request=request,
            template_name="polls/detail.html",
            context={
                "question": question,
                "error_message": "You didn't select a choice",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse("polls:results", args=(question.id,))
        )
