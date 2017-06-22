
from django import forms
from django.contrib import messages
from django.forms.widgets import Textarea

from django_comments.forms import CommentForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, Layout, Hidden, Field, HTML

from models import MPTTComment


class MPTTCommentForm(CommentForm):

    def __init__(self, *args, **kwargs):
        super(MPTTCommentForm, self).__init__(*args, **kwargs)
        # self.helper = FormHelper()
        # # self.helper.set_form_action('/comments/post/')
        # self.helper.form_tag = False
        # # self.helper.form = None
        # self.helper.layout = Layout(
        #     Fieldset(
        #         '', #legend
        #         'comment',
        #         'honeypot',
        #         'content_type',
        #         'object_pk',
        #         'timestamp',
        #         'security_hash'
        #     ),
        # )

        # self.fields['name'].hidden = "True"

        self.fields['comment'].label = ""
        self.fields['comment'].required = "True"
        self.fields['comment'].widget = Textarea(attrs={
            # 'class': 'form-control',
            'required': "required",
            'placeholder': 'I think that...',
            'rows': 5
        })

    parent = forms.ModelChoiceField(queryset=MPTTComment.objects.all(), required=False, widget=forms.HiddenInput)

    def get_comment_model(self):
        return MPTTComment

    def get_comment_create_data(self, site_id=None):
        data = super(MPTTCommentForm, self).get_comment_create_data(site_id=None)
        data['parent'] = self.cleaned_data['parent']
        return data