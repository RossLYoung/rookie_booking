from django.core.urlresolvers import reverse



def get_model():
    from models import MPTTComment
    return MPTTComment


def get_form():
    from forms import MPTTCommentForm
    return MPTTCommentForm

#
# def get_form_target():
#     return reverse("commentry.views.post_comment")