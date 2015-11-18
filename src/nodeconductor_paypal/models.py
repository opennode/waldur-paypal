from django.db import models

from django_fsm import transition, FSMIntegerField
from model_utils.models import TimeStampedModel

from nodeconductor.core import models as core_models
from nodeconductor.structure.models import Customer
from nodeconductor.logging.log import LoggableMixin


class Payment(LoggableMixin, TimeStampedModel, core_models.UuidMixin):

    class Permissions(object):
        customer_path = 'customer'

    class States(object):
        INIT = 0
        CREATED = 1
        APPROVED = 2
        CANCELLED = 3
        ERRED = 4

    STATE_CHOICES = (
        (States.INIT, 'Initial'),
        (States.CREATED, 'Created'),
        (States.APPROVED, 'Approved'),
        (States.ERRED, 'Erred'),
    )

    state = FSMIntegerField(default=States.INIT, choices=STATE_CHOICES)

    customer = models.ForeignKey(Customer)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    # Payment ID is required and fetched from backend
    backend_id = models.CharField(max_length=255, null=True)

    # URL is fetched from backend
    approval_url = models.URLField()

    def __str__(self):
        return "%s %.2f %s" % (self.modified, self.amount, self.customer.name)

    def get_log_fields(self):
        return ('uuid', 'customer', 'amount', 'modified', 'status')

    @transition(field=state, source=States.INIT, target=States.CREATED)
    def set_created(self):
        pass

    @transition(field=state, source=States.CREATED, target=States.APPROVED)
    def set_approved(self):
        pass

    @transition(field=state, source=States.CREATED, target=States.CANCELLED)
    def set_cancelled(self):
        pass

    @transition(field=state, source='*', target=States.ERRED)
    def set_erred(self):
        pass
