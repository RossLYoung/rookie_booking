from django.core.urlresolvers import reverse

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter


# class UserProfileAccountAdapter(DefaultAccountAdapter):
#     def get_login_redirect_url(self, request):
#         # get the next parameter from request object and return the url
#         pass


class UserProfileSocialAccountAdapter(DefaultSocialAccountAdapter):

    def get_connect_redirect_url(self, request, socialaccount):
        """
        Returns the default URL to redirect to after successfully
        connecting a social account.
        """
        assert request.user.is_authenticated()
        url = reverse('userprofile:profile-social')
        return url