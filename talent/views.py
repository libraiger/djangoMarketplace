import json
from django.shortcuts import render, HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from utility.utils import get_path_from_url
from .models import Person, Skill, Expertise, PersonSkill, BountyClaim, Feedback
from product_management.models import Challenge
from .forms import (
    PersonProfileForm,
    FeedbackForm,
)
from .services import FeedbackService


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Person
    template_name = "talent/profile.html"
    form_class = PersonProfileForm
    context_object_name = "person"
    slug_field = "username"
    slug_url_kwarg = "username"
    login_url = "sign_in"

    def get_queryset(self):
        # Restrict the queryset to the currently authenticated user
        queryset = super().get_queryset()
        return queryset.filter(user__pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        person = self.get_object()

        if "form" not in kwargs:
            context["form"] = self.form_class(initial=person.get_initial_data())

        context["pk"] = person.pk

        image_url, requires_upload = person.get_photo_url()
        context["photo_url"] = image_url
        context["requires_upload"] = requires_upload

        return context

    def _remove_picture(self, request):
        person = self.get_object()
        person.delete_photo()
        context = self.get_context_data()

        return render(request, "talent/profile_picture.html", context)

    def get_success_url(self):
        return reverse("profile", kwargs={"pk": self.request.user.pk})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        trigger = request.headers.get("Hx-Trigger")
        if trigger == "remove_picture_button":
            return self._remove_picture(request)

        return super().get(request, *args, **kwargs)

    def _get_skills_list(self, skill_ids: str) -> list:
        if skill_ids:
            json_skill_ids = json.loads(skill_ids)
            skills_queryset = Skill.objects.filter(id__in=json_skill_ids).values(
                "id", "name"
            )
            return list(skills_queryset)

    def _get_expertise_list(self, expertise_ids: str) -> list:
        if expertise_ids:
            json_expertise_ids = json.loads(expertise_ids)
            expertise_queryset = Expertise.objects.filter(
                id__in=json_expertise_ids
            ).values("id", "name")

            return list(expertise_queryset)

    # TODO: Add a success message under the photo upload field
    def post(self, request, *args, **kwargs):
        person = request.user.person

        form = PersonProfileForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            created_person_obj = form.save(commit=False)
            created_person_obj.completed_profile = True
            created_person_obj.save()

            skill_and_expertise, _ = PersonSkill.objects.get_or_create(person=person)
            skill_and_expertise.skill = self._get_skills_list(
                request.POST.get("selected_skill_ids")
            )
            skill_and_expertise.expertise = self._get_expertise_list(
                request.POST.get("selected_expertise_ids")
            )
            skill_and_expertise.save()

        return super().post(request, *args, **kwargs)


@login_required(login_url="sign_in")
def get_skills(request):
    skill_queryset = (
        Skill.objects.filter(active=True).order_by("-display_boost_factor").values()
    )
    skills = list(skill_queryset)
    return JsonResponse(skills, safe=False)


@login_required(login_url="sign_in")
def get_current_skills(request):
    person = request.user.person
    try:
        person_skill = PersonSkill.objects.get(person=person)
        skill_ids = [entry.get("id") for entry in person_skill.skill]
    except ObjectDoesNotExist:
        skill_ids = []

    return JsonResponse(skill_ids, safe=False)


@login_required(login_url="sign_in")
def get_expertise(request):
    selected_skills = request.GET.get("selected_skills")
    if selected_skills:
        selected_skill_ids = json.loads(selected_skills)
        expertise_queryset = Expertise.objects.filter(
            skill_id__in=selected_skill_ids
        ).values()

        person = request.user.person
        try:
            person_expertise = PersonSkill.objects.get(person=person)
            expertise_ids = [entry.get("id") for entry in person_expertise.expertise]
        except ObjectDoesNotExist:
            expertise_ids = []

        return JsonResponse(
            {
                "expertiseList": list(expertise_queryset),
                "expertiseIDList": expertise_ids,
            },
            safe=False,
        )

    return JsonResponse(
        {
            "expertiseList": [],
            "expertiseIDList": [],
        },
        safe=False,
    )


@login_required(login_url="sign_in")
def get_current_expertise(request):
    person = request.user.person
    try:
        person_skill = PersonSkill.objects.get(person=person)
        expertise_ids = [entry.get("id") for entry in person_skill.expertise]
        expertise = Expertise.objects.filter(id__in=expertise_ids).values()
    except:
        expertise_ids = []
        expertise = []

    return JsonResponse(
        {"expertiseList": list(expertise), "expertiseIDList": expertise_ids},
        safe=False,
    )


@login_required(login_url="sign_in")
def list_skill_and_expertise(request):
    skills = request.GET.get("skills")
    expertise = request.GET.get("expertise")

    if skills and expertise:
        expertise_ids = json.loads(expertise)
        expertise_queryset = Expertise.objects.filter(id__in=expertise_ids)

        skill_expertise_pairs = []
        for exp in expertise_queryset:
            pair = {
                "skill": exp.skill.name,
                "expertise": exp.name,
            }
            skill_expertise_pairs.append(pair)

        return JsonResponse(skill_expertise_pairs, safe=False)

    return JsonResponse([], safe=False)


# NOTE: The links in this view are not completed
class TalentPortfolio(TemplateView):
    User = get_user_model()
    template_name = "talent/portfolio.html"

    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(self.User, username=username)
        person = user.person
        photo_url, _ = person.get_photo_url()

        status = person.status
        person_skill = person.skills.all().first()
        bounty_claims = BountyClaim.objects.filter(
            person=person, bounty__challenge__status=Challenge.CHALLENGE_STATUS_DONE
        ).select_related("bounty__challenge")
        received_feedbacks = Feedback.objects.filter(recipient=person)

        if request.user == user or received_feedbacks.filter(
            provider=request.user.person
        ):
            can_leave_feedback = False
        else:
            can_leave_feedback = True

        context = {
            "user": user,
            "photo_url": photo_url,
            "person": person,
            "person_linkedin_link": get_path_from_url(person.linkedin_link),
            "person_twitter_link": get_path_from_url(person.twitter_link),
            "status": status,
            "skills": person_skill.skill,
            "expertise": person_skill.expertise,
            "bounty_claims": bounty_claims,
            "FeedbackService": FeedbackService,
            "received_feedbacks": received_feedbacks,
            "form": FeedbackForm(),
            "can_leave_feedback": can_leave_feedback,
        }
        return self.render_to_response(context)


def status_and_points(request):
    return HttpResponse("TODO")


def submit_feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            recipient_username = request.POST.get("feedback-recipient-username")
            recipient = Person.objects.get(user__username=recipient_username)
            feedback = Feedback(
                recipient=recipient,
                provider=request.user.person,
                message=form.cleaned_data.get("message"),
                stars=int(form.cleaned_data.get("stars")),
            )
            feedback.save()

            return redirect("portfolio", username=recipient_username)

    return HttpResponse("Something went wrong")
