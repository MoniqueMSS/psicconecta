from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class MinimumLengthValidatorPTBR:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("Sua senha deve ter no mínimo %(min_length)d caracteres."),
                params={'min_length': self.min_length},
                code='password_too_short',
            )

    def get_help_text(self):
        return _(
            "Sua senha deve ter no mínimo %(min_length)d caracteres." % {'min_length': self.min_length}
        )