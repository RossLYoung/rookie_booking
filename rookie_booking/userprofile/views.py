import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _
from django.views.generic import UpdateView

from allauth.account.views import EmailView, PasswordChangeView, PasswordSetView, sensitive_post_parameters_m
from allauth.account import signals
from allauth.account.views import _ajax_response

from allauth.socialaccount.views import ConnectionsView


from .forms import CustomUserForm


class UserEditView(UpdateView):

    form_class = CustomUserForm
    template_name = "userprofile/details.html"
    success_url = reverse_lazy('userprofile:profile-details')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserEditView, self).get_context_data(**kwargs)
        # context['address_book'] = self.request.user.address_book.all()
        return context

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.INFO, 'User profile updated')
        return super(UserEditView, self).form_valid(form)


profile_details = login_required(UserEditView.as_view())


class ProfileEmail(EmailView):
    template_name = 'userprofile/email.html'
    success_url = reverse_lazy('userprofile:profile-email')

    def post(self, request, *args, **kwargs):
        res = None
        if "action_add" in request.POST:
            res = super(EmailView, self).post(request, *args, **kwargs)
        elif request.POST.get("email"):
            if "action_send" in request.POST:
                res = self._action_send(request)
            elif "action_remove" in request.POST:
                res = self._action_remove(request)
            elif "action_primary" in request.POST:
                res = self._action_primary(request)
            res = res or HttpResponseRedirect(reverse('userprofile:profile-email'))
            # Given that we bypassed AjaxCapableProcessFormViewMixin,
            # we'll have to call invoke it manually...
            res = _ajax_response(request, res)
        return res

profile_email = login_required(ProfileEmail.as_view())


class ProfileSocial(ConnectionsView):
    template_name = 'userprofile/social.html'
    success_url = reverse_lazy('userprofile:profile-social')

profile_social = login_required(ProfileSocial.as_view())


class ProfilePasswordChange(PasswordChangeView):
    template_name = 'userprofile/password.html'
    success_url = reverse_lazy('userprofile:profile-password')

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_usable_password():
            return HttpResponseRedirect(reverse('userprofile:profile-password-set'))
        return super(ProfilePasswordChange, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        #get_adapter().add_message(self.request, messages.SUCCESS, 'account/messages/password_changed.txt')
        signals.password_changed.send(sender=self.request.user.__class__,
                                      request=self.request,
                                      user=self.request.user)
        return super(ProfilePasswordChange, self).form_valid(form)


profile_passsword = login_required(ProfilePasswordChange.as_view())


class ProfilePasswordSet(PasswordSetView):
    template_name = 'userprofile/password_set.html'
    success_url   = reverse_lazy('userprofile:profile-password-set')

profile_password_set = login_required(ProfilePasswordSet.as_view())
