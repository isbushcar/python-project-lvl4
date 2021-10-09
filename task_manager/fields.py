from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _

class UsernameFieldWithPlaceholder(UsernameField):

    def widget_attrs(self, widget):
        return {
            **super(UsernameFieldWithPlaceholder, self).widget_attrs(widget),
            'placeholder': _("Username"),
            'class': 'form-control',
        }
