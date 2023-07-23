# Generated by Django 4.2.2 on 2023-07-22 10:31

import commerce.utils
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("number_of_points", models.IntegerField(default=500)),
                (
                    "currency_of_payment",
                    models.IntegerField(
                        choices=[(1, "USD"), (2, "EUR"), (3, "GBP")],
                        default=commerce.utils.CurrencyTypes["USD"],
                    ),
                ),
                ("price_per_point_in_cents", models.IntegerField()),
                ("subtotal_in_cents", models.PositiveBigIntegerField()),
                ("sales_tax_in_cents", models.PositiveBigIntegerField()),
                ("total_payable_in_cents", models.PositiveBigIntegerField()),
                (
                    "payment_type",
                    models.IntegerField(
                        choices=[(1, "NONE"), (2, "ONLINE"), (3, "OFFLINE")],
                        default=commerce.utils.PaymentTypes["ONLINE"],
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ContributorAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "community_status",
                    models.IntegerField(
                        choices=[
                            (1, "DRONE"),
                            (2, "HONEY_BEE"),
                            (3, "TRUSTED_BEE"),
                            (4, "QUEEN_BEE"),
                            (5, "BEE_KEEPER"),
                        ],
                        default=commerce.utils.CommunityStatusOptions["DRONE"],
                    ),
                ),
                ("liquid_points_balance", models.PositiveBigIntegerField(default=0)),
                ("nonliquid_points_balance", models.PositiveBigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="ContributorAccountCredit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "reason",
                    models.IntegerField(
                        choices=[(1, "BOUNTY"), (2, "LIQUIDATION"), (3, "REWARD")],
                        default=0,
                    ),
                ),
                ("number_of_points", models.PositiveIntegerField()),
                (
                    "type_of_points",
                    models.IntegerField(
                        choices=[(1, "NONLIQUID"), (2, "LIQUID")],
                        default=commerce.utils.PointTypes["NONLIQUID"],
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ContributorAccountDebit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "reason",
                    models.IntegerField(
                        choices=[(1, "LIQUIDATION"), (2, "PUNISHMENT")], default=0
                    ),
                ),
                ("number_of_points", models.PositiveIntegerField()),
                (
                    "type_of_points",
                    models.IntegerField(
                        choices=[(1, "NONLIQUID"), (2, "LIQUID")],
                        default=commerce.utils.PointTypes["NONLIQUID"],
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ContributorReward",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "action",
                    models.IntegerField(
                        choices=[(1, "INVITED FRIENDS"), (2, "VERIFIED IDENTITY")],
                        default=0,
                    ),
                ),
                ("points", models.IntegerField(default=10)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Grant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.TextField(max_length=1024)),
                ("number_of_points", models.IntegerField(default=500)),
                (
                    "status",
                    models.IntegerField(
                        choices=[(1, "NEW"), (2, "COMPLETE"), (3, "CANCELLED")],
                        default=commerce.utils.LifecycleStatusOptions["NEW"],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="InboundPayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "payment_type",
                    models.IntegerField(
                        choices=[(1, "NONE"), (2, "ONLINE"), (3, "OFFLINE")],
                        default=commerce.utils.PaymentTypes["ONLINE"],
                    ),
                ),
                (
                    "currency_of_payment",
                    models.IntegerField(
                        choices=[(1, "USD"), (2, "EUR"), (3, "GBP")],
                        default=commerce.utils.CurrencyTypes["USD"],
                    ),
                ),
                ("amount_paid_in_cents", models.PositiveBigIntegerField()),
                ("transaction_detail", models.TextField(max_length=1024)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Organisation",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        default="",
                        max_length=39,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_username",
                                message="Username may only contain letters and numbers",
                                regex="^[a-z0-9]*$",
                            )
                        ],
                    ),
                ),
                ("name", models.CharField(max_length=512, unique=True)),
                (
                    "photo",
                    models.ImageField(blank=True, null=True, upload_to="avatars/"),
                ),
            ],
            options={
                "verbose_name_plural": "Organisations",
            },
        ),
        migrations.CreateModel(
            name="OrganisationAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("liquid_points_balance", models.PositiveBigIntegerField()),
                ("nonliquid_points_balance", models.PositiveBigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="OrganisationAccountCredit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("number_of_points", models.PositiveIntegerField()),
                (
                    "type_of_points",
                    models.IntegerField(
                        choices=[(1, "NONLIQUID"), (2, "LIQUID")],
                        default=commerce.utils.PointTypes["NONLIQUID"],
                    ),
                ),
                (
                    "credit_reason",
                    models.IntegerField(
                        choices=[(1, "GRANT"), (2, "SALE")],
                        default=commerce.utils.OrganisationAccountCreditReasons[
                            "GRANT"
                        ],
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OrganisationAccountDebit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "type_of_points",
                    models.IntegerField(
                        choices=[(1, "NONLIQUID"), (2, "LIQUID")],
                        default=commerce.utils.PointTypes["NONLIQUID"],
                    ),
                ),
                (
                    "debit_reason",
                    models.IntegerField(
                        choices=[(1, "TRANSFER"), (2, "EXPIRY")], default=0
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OutboundPayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("details", models.TextField(max_length=1024)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PaymentOrder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "currency_of_payment",
                    models.IntegerField(
                        choices=[(1, "USD"), (2, "EUR"), (3, "GBP")],
                        default=commerce.utils.CurrencyTypes["USD"],
                    ),
                ),
                ("subtotal_in_cents", models.PositiveBigIntegerField()),
                ("sales_tax_in_cents", models.PositiveBigIntegerField()),
                ("total_payable_in_cents", models.PositiveBigIntegerField()),
                (
                    "payment_type",
                    models.IntegerField(
                        choices=[(1, "PARTNER"), (2, "BANK TRANSFER")], default=0
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[(1, "NEW"), (2, "COMPLETE"), (3, "CANCELLED")],
                        default=commerce.utils.LifecycleStatusOptions["NEW"],
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PointPriceConfiguration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("applicable_from_date", models.DateField()),
                ("usd_point_inbound_price_in_cents", models.IntegerField()),
                ("eur_point_inbound_price_in_cents", models.IntegerField()),
                ("gbp_point_inbound_price_in_cents", models.IntegerField()),
                ("usd_point_outbound_price_in_cents", models.IntegerField()),
                ("eur_point_outbound_price_in_cents", models.IntegerField()),
                ("gbp_point_outbound_price_in_cents", models.IntegerField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProductAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("liquid_points_balance", models.PositiveBigIntegerField()),
                ("nonliquid_points_balance", models.PositiveBigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="ProductAccountCredit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("number_of_points", models.PositiveIntegerField()),
                (
                    "type_of_points",
                    models.IntegerField(
                        choices=[(1, "NONLIQUID"), (2, "LIQUID")],
                        default=commerce.utils.PointTypes["NONLIQUID"],
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProductAccountDebit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("number_of_points", models.PositiveIntegerField()),
                (
                    "type_of_points",
                    models.IntegerField(
                        choices=[(1, "NONLIQUID"), (2, "LIQUID")],
                        default=commerce.utils.PointTypes["NONLIQUID"],
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProductAccountReservation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("number_of_points", models.PositiveIntegerField()),
                (
                    "type_of_points",
                    models.IntegerField(
                        choices=[(1, "NONLIQUID"), (2, "LIQUID")],
                        default=commerce.utils.PointTypes["NONLIQUID"],
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SalesOrder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("number_of_points", models.IntegerField()),
                (
                    "currency_of_payment",
                    models.IntegerField(
                        choices=[(1, "USD"), (2, "EUR"), (3, "GBP")],
                        default=commerce.utils.CurrencyTypes["USD"],
                    ),
                ),
                ("price_per_point_in_cents", models.IntegerField()),
                ("subtotal_in_cents", models.PositiveBigIntegerField()),
                ("sales_tax_in_cents", models.PositiveBigIntegerField()),
                ("total_payable_in_cents", models.PositiveBigIntegerField()),
                (
                    "payment_type",
                    models.IntegerField(
                        choices=[(1, "NONE"), (2, "ONLINE"), (3, "OFFLINE")],
                        default=commerce.utils.PaymentTypes["ONLINE"],
                    ),
                ),
                (
                    "payment_status",
                    models.IntegerField(
                        choices=[
                            (1, "PENDING"),
                            (2, "PAID"),
                            (3, "CANCELLED"),
                            (4, "REFUNDED"),
                        ],
                        default=commerce.utils.PaymentStatusOptions["PENDING"],
                    ),
                ),
                (
                    "process_status",
                    models.IntegerField(
                        choices=[(1, "NEW"), (2, "COMPLETE"), (3, "CANCELLED")],
                        default=commerce.utils.LifecycleStatusOptions["NEW"],
                    ),
                ),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="commerce.cart"
                    ),
                ),
                (
                    "organisation_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="commerce.organisationaccount",
                    ),
                ),
                (
                    "organisation_account_credit",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="commerce.organisationaccountcredit",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
