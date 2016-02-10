from decimal import Decimal

from django.conf import settings
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView
from django.views.generic.edit import FormView
from django.views.decorators.http import require_http_methods
from revolv.base.users import UserDataMixin
from revolv.base.utils import is_user_reinvestment_period
from revolv.lib.mailer import send_revolv_email
from revolv.payments.forms import CreditCardDonationForm
from revolv.payments.models import UserReinvestment, Payment, PaymentType, Tip
from revolv.payments.services import PaymentService
from revolv.project import forms
from revolv.project.models import Category, Project, ProjectUpdate, DonationLevel
from revolv.tasks.sfdc import send_donation_info

def stripe_callback(request, pk):
    import stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY
    token = stripe.Token.retrieve(request.POST['stripeToken'])

    project = get_object_or_404(Project, pk=pk)

    tip_cents = int(request.POST['metadata'])
    amount_cents = int(request.POST['amount_cents'])
    donation_cents = amount_cents - tip_cents

    try:
        charge = stripe.Charge.create(source=request.POST['stripeToken'], currency="usd", amount=amount_cents)
        print request.POST
    except stripe.error.CardError, e:
        msg = body['error']['message']
    except stripe.error.APIConnectionError, e:
        msg = body['error']['message']
    except Exception, e:
        #log it
        msg = "Payment error. Re-volv has been notified."
        return render(request, "project/project_donate_error.html", {"msg": msg, "project": project})
        pass

    payment = Payment.objects.create(
        user=request.user.revolvuserprofile,
        entrant=request.user.revolvuserprofile,
        amount=donation_cents/100.0,
        project=project,
        payment_type=PaymentType.objects.get_stripe(),
    )
    print payment
    tip = Tip.objects.create(
        amount=tip_cents/100.0,
        user=request.user.revolvuserprofile,
    )
    print tip.amount
    print tip.user
    return redirect('project:view', pk=project.pk)


class DonationLevelFormSetMixin(object):
    """
    Mixin that gets the ProjectDonationLeveLFormSet for a page, specifically
    the Create Project and Update Project page.
    """

    def get_donation_level_formset(self, extra=2):
        """ Checks if the request is a POST, and populates the formset with current object as the instance
        """
        ProjectDonationLevelFormSet = forms.make_donation_level_formset(extra)

        if self.request.POST:
            return ProjectDonationLevelFormSet(self.request.POST, instance=self.object)
        else:
            return ProjectDonationLevelFormSet(instance=self.object)


class CreateProjectView(DonationLevelFormSetMixin, CreateView):
    """
    The view to create a new project. Redirects to the homepage upon success.

    Accessed through /project/create
    """
    model = Project
    template_name = 'project/edit_project.html'
    form_class = forms.ProjectForm

    def get_success_url(self):
        return reverse('project:view', kwargs={'pk': self.object.id})

    # validates project, formset of donation levels, and adds categories as well
    def form_valid(self, form):

        formset = self.get_donation_level_formset()
        if formset.is_valid():
            new_project = Project.objects.create_from_form(form, self.request.user.revolvuserprofile)
            new_project.update_categories(form.cleaned_data['categories_select'])
            formset.instance = new_project
            formset.save()
            messages.success(self.request, new_project.title + ' has been created!')
        else:
            return self.render_to_response(self.get_context_data(form=form))

        return super(CreateProjectView, self).form_valid(form)

    # sets context to be the create view, doesn't pass in the id
    def get_context_data(self, **kwargs):
        context = super(CreateProjectView, self).get_context_data(**kwargs)
        context['valid_categories'] = Category.valid_categories
        context['GOOGLEMAPS_API_KEY'] = settings.GOOGLEMAPS_API_KEY
        context['donation_level_formset'] = self.get_donation_level_formset()
        return context


class UpdateProjectView(DonationLevelFormSetMixin, UpdateView):
    """
    The view to update a project. It is the same view as creating a new
    project, though it prepopulates the existing field and passes in the
    project id. Redirects to the project page upon success.

    Accessed through /project/{project_id}/edit
    """
    model = Project
    template_name = 'project/edit_project.html'
    form_class = forms.ProjectForm

    def get_initial(self):
        """
        Initializes the already selected categories for a given project.
        """
        return {'categories_select': self.get_object().categories}

    def get_success_url(self):
        messages.success(self.request, 'Project details updated')
        return reverse('project:view', kwargs={'pk': self.get_object().id})

    def form_valid(self, form):
        """
        Validates project, formset of donation levels, and adds categories as well
        """
        formset = self.get_donation_level_formset()

        if formset.is_valid():
            project = self.get_object()
            project.update_categories(form.cleaned_data['categories_select'])
            formset.instance = project
            formset.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))
        return super(UpdateProjectView, self).form_valid(form)

    # sets context to be the edit view by providing in the model id
    def get_context_data(self, **kwargs):
        context = super(UpdateProjectView, self).get_context_data(**kwargs)
        context['valid_categories'] = Category.valid_categories
        context['donation_level_formset'] = self.get_donation_level_formset()
        return context


class ReviewProjectView(UserDataMixin, UpdateView):
    """
    The view to review a project. Shows the same view as ProjectView, but at
    the top, has a button group through which an ambassador or admin can
    update the project status.

    Accessed through /project/{project_id}/review
    """
    model = Project
    form_class = forms.ProjectStatusForm
    http_method_names = [u'post']

    def get_success_url(self):
        if self.is_administrator:
            return "%s?active_project=%d" % (reverse('administrator:dashboard'), self.get_object().id)
        else:
            return reverse('project:view', kwargs={'pk': self.get_object().id})

    # Checks the post request and updates the project_status
    def form_valid(self, form):
        project = self.object
        if '_approve' in self.request.POST:
            messages.success(self.request, project.title + ' has been approved and is live.')
            project.approve_project()
        elif '_stage' in self.request.POST:
            messages.success(self.request, project.title + ' has been staged to go live.')
            project.stage_project()
        elif '_unapprove' in self.request.POST:
            messages.success(self.request, project.title + ' is no longer live.')
            project.unapprove_project()
        elif '_propose' in self.request.POST:
            messages.success(self.request, project.title + ' is now pending approval.')
            project.propose_project()
        elif '_deny' in self.request.POST:
            messages.info(self.request, project.title + ' has been denied.')
            project.deny_project()
        elif '_complete' in self.request.POST:
            messages.success(self.request, project.title + ' has been completed.')
            project.complete_project()
        elif '_incomplete' in self.request.POST:
            messages.info(self.request, project.title + ' has been marked as active again (not yet completed).')
            project.mark_as_incomplete_project()
        elif '_repayment' in self.request.POST:
            repayment_amount = Decimal(self.request.POST['_repayment_amount'])
            PaymentService.create_repayment(self.user_profile, repayment_amount, project)
            messages.success(self.request, '$' + str(repayment_amount) + ' repaid by ' + project.org_name)
        return redirect(self.get_success_url())

    # pass in Project Categories and Maps API key
    def get_context_data(self, **kwargs):
        context = super(ReviewProjectView, self).get_context_data(**kwargs)
        context['GOOGLEMAPS_API_KEY'] = settings.GOOGLEMAPS_API_KEY
        return context


class TemplateProjectUpdateView(UserDataMixin, UpdateView):
    form_class = forms.EditProjectUpdateForm
    template_name = 'project/edit_project_update.html'

    def dispatch(self, request, *args, **kwargs):
        response = super(TemplateProjectUpdateView, self).dispatch(request, args, kwargs)
        if not self.is_ambassador:
            return self.deny_access()
        return response


class PostProjectUpdateView(TemplateProjectUpdateView):
    model = Project

    def get_success_url(self):
        return reverse('project:view', kwargs={'pk': self.get_object().id})

    def form_valid(self, form):
        text = form.cleaned_data['update_text']
        project = self.get_object()
        project.add_update(text)
        return super(PostProjectUpdateView, self).form_valid(form)


class EditProjectUpdateView(TemplateProjectUpdateView):
    model = ProjectUpdate

    def get_success_url(self):
        return reverse('project:view', kwargs={'pk': self.get_object().project_id})

    def form_valid(self, form):
        text = form.cleaned_data['update_text']
        update = self.get_object()
        update.update_text = text
        return super(EditProjectUpdateView, self).form_valid(form)


class ProjectView(UserDataMixin, DetailView):
    """
    The project view. Displays project details and allows for editing.

    Accessed through /project/{project_id}
    """
    model = Project
    template_name = 'project/project.html'

    # pass in Project Categories and Maps API key
    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE
        context['GOOGLEMAPS_API_KEY'] = settings.GOOGLEMAPS_API_KEY
        context['updates'] = self.get_object().updates.order_by('date').reverse()
        context['donor_count'] = self.get_object().donors.count()
        context['project_donation_levels'] = self.get_object().donation_levels.order_by('amount')
        context["is_draft_mode"] = self.get_object().project_status == self.get_object().DRAFTED
        if self.user_profile and self.user_profile.reinvest_pool > 0.0 \
                and self.get_object().monthly_reinvestment_cap > 0.0 \
                and self.get_object().amount_left > 0.0:
            context["is_reinvestment"] = True
            context["reinvestment_amount"] = min(self.get_object().reinvest_amount_left,
                                                 self.user_profile.reinvest_pool)
            context["reinvestment_url"] = reverse('project:reinvest', kwargs={'pk': self.get_object().id})
        else:
            context["is_reinvestment"] = False
            context["reinvestment_amount"] = 0.0
            context["reinvestment_url"] = ''
        return context

    def dispatch(self, request, *args, **kwargs):
        # always populate self.user, etc
        super_response = super(ProjectView, self).dispatch(request, *args, **kwargs)
        project = self.get_object()
        if (project.is_active or project.is_completed or
                (self.user.is_authenticated() and (project.has_owner(self.user_profile) or self.is_administrator or self.is_ambassador))):
            return super_response
        else:
            return self.deny_access()


class SubmitDonationView(UserDataMixin, FormView):
    form_class = CreditCardDonationForm
    model = Project
    http_method_names = [u'post']

    def form_valid(self, form):
        project = Project.objects.get(pk=self.kwargs.get('pk'))
        form.process_payment(project, self.user)
        context = {}
        context['user'] = self.user
        context['project'] = project
        context['amount'] = form.cleaned_data.get('amount')

        send_revolv_email(
            'post_donation',
            context, [self.user.email]
        )
        try:
            amount = form.cleaned_data.get('amount')
            send_donation_info.delay(self.user_profile.get_full_name(), float(amount),
                                     project.title, self.user_profile.address)
        except:
            pass

        return JsonResponse({
            'amount': form.data['amount'],
        })

    def form_invalid(self, form):
        return JsonResponse({
            'error': form.errors,
        }, status=400)


class ProjectListReinvestmentView(UserDataMixin, TemplateView):
    """
    View List Project that are eligible to receive reinvestment funds.
    """
    template_name = 'base/projects-list.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectListReinvestmentView, self).get_context_data(**kwargs)
        context["is_reinvestment"] = True
        if not is_user_reinvestment_period():
            if self.user_profile.reinvest_pool > 0.0:
                    context["error_msg"] = "You have ${0} to reinvest, " \
                                           "but the reinvestment period has ended for this month. " \
                                           "Please come back next month!" \
                        .format(self.user_profile.reinvest_pool)
            else:
                context["error_msg"] = "The reinvestment period has ended for this month. " \
                                       "Please come back next month!"
        else:
            active = Project.objects.get_eligible_projects_for_reinvestment()
            context["active_projects"] = filter(lambda p: p.amount_left > 0.0, active)
            if self.user_profile.reinvest_pool > 0.0:
                context["reinvestment_amount"] = self.user_profile.reinvest_pool
            else:
                context["error_msg"] = "You don't have funds to reinvest."
        return context


@login_required
@require_http_methods(['POST'])
def reinvest(request, pk):
    """View handle reinvestment action
    """
    amount = request.POST.get('amount')
    if not amount:
        return HttpResponseBadRequest()
    try:
        project = Project.objects.get(pk=pk)
    except (Project.DoesNotExist, Project.MultipleObjectsReturned):
        return HttpResponseBadRequest()

    UserReinvestment.objects.create(user=request.user.revolvuserprofile,
                                        amount=amount,
                                        project=project)
    res = {'amount_donated': project.amount_donated,
           'partial_completeness': project.partial_completeness_as_js(),
           'num_donors': project.donors.count()}
    return JsonResponse({'success': True, 'project': res})
