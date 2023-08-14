from django.db import models
from django.contrib.auth.models import AbstractUser

from openunited.mixins import TimeStampMixin, UUIDMixin
from talent.models import Person
from .managers import UserManager


# This model will be used for advanced authentication methods
class User(AbstractUser, TimeStampMixin):
    full_name = models.CharField(max_length=256)
    preferred_name = models.CharField(max_length=128)
    remaining_budget_for_failed_logins = models.PositiveSmallIntegerField(default=3)
    password_reset_required = models.BooleanField(default=False)

    objects = UserManager()

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.preferred_name


class SignUpRequest(TimeStampMixin):
    full_name = models.CharField(max_length=256)
    preferred_name = models.CharField(max_length=128)
    email = models.EmailField()
    verification_code = models.CharField(max_length=6)
    username = models.CharField(max_length=128)
    password = models.CharField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.username}"


class SignInAttempt(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_hash = models.CharField(max_length=64, null=True, blank=True)
    country = models.CharField(max_length=64, null=True, blank=True)
    region_code = models.CharField(max_length=8, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    successful = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.region_code} - {self.city} - {self.country}"


class ProductPerson(TimeStampMixin, UUIDMixin):
    CONTRIBUTOR = 0
    PRODUCT_MANAGER = 1
    PRODUCT_ADMIN = 2

    ROLES = (
        (CONTRIBUTOR, "Contributor"),
        (PRODUCT_MANAGER, "Manager"),
        (PRODUCT_ADMIN, "Admin"),
    )
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    product = models.ForeignKey("product_management.Product", on_delete=models.CASCADE)
    role = models.IntegerField(choices=ROLES, default=0)
    organisation = models.ForeignKey(
        "commerce.Organisation", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.person} {self.get_role_display()} {self.product}"

    def clean(self):
        from security.services import ProductPersonService

        ProductPersonService.is_organisation_provided(self)


class BlacklistedUsernames(models.Model):
    username = models.CharField(max_length=30, unique=True, blank=False)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "black_listed_usernames"
