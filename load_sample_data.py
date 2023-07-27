import os
import datetime
import django
from random import choice, sample, randint
from django.apps import apps
import json
from utility.utils import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openunited.settings")
django.setup()

from commerce.services import (
    OrganisationService,
    OrganisationAccountService,
    OrganisationAccountCreditService,
    CartService,
    PointPriceConfigurationService,
)
from product_management.models import Capability
from talent.services import PersonService, SkillService, ExpertiseService
from product_management.services import (
    InitiativeService,
    TagService,
    ProductService,
    ChallengeService,
)


def load_reference_data(classname):
    klass = eval(classname.capitalize())
    klass.objects.all().delete()
    file = os.path.abspath("utility/reference_data/" + classname + ".json")
    with open(file) as json_file:
        data_set = json.load(json_file)
        for data in data_set:
            obj = klass(**data)
            obj.save()


def clear_rows_by_model_name(model_names_mapping: dict) -> None:
    for model_name, app_name in model_names_mapping.items():
        model = apps.get_model(app_name, model_name)
        model.objects.all().delete()


def create_capabilities():
    fancy_out("Create Capability records")
    get = lambda node_id: Capability.objects.get(pk=node_id)
    root = Capability.add_root(
        name="Capability 1", description="Description of Capability 1"
    )
    node = get(root.pk).add_child(
        name="Capability 2", description="Description of Capability 2"
    )
    get(node.pk).add_sibling(
        name="Capability 3", description="Description of Capability 3"
    )
    get(node.pk).add_sibling(
        name="Capability 4", description="Description of Capability 4"
    )
    get(node.pk).add_child(
        name="Capability 5", description="Description of Capability 5"
    )
    get(node.pk).add_child(
        name="Capability 6", description="Description of Capability 6"
    )
    get(node.pk).add_child(
        name="Capability 7", description="Description of Capability 7"
    )

    return Capability.objects.all()


def read_json_data(file_name, model_name=None):
    if model_name:
        fancy_out(f"Create {model_name.title()} records")
    with open(file_name, "r") as json_file:
        return json.load(json_file)


proceed = input(
    "Running this script will replace all your current data. Ok? (Y/N)"
).lower()

if len(proceed) == 0:
    fancy_out("Execution Abandoned")
    exit()

if proceed[0] != "y":
    fancy_out("Stopped at your request")
    exit()
else:
    model_app_mapping = read_json_data("sample_data/model_app_mapping.json")

    print(f"Delete all the records of the following models: {model_app_mapping.keys()}")
    # Deletes all the existing records before populating sample data according to the dictionary
    clear_rows_by_model_name(model_app_mapping)

    person_data = read_json_data("sample_data/person.json", "person")

    people = []
    for pd in person_data:
        people.append(PersonService.create(**pd))

    product_data = read_json_data("sample_data/product.json", "product")

    products = []
    for pd in product_data:
        products.append(ProductService.create(**pd))

    initiative_data = read_json_data("sample_data/initiative.json", "initiative")

    for elem in initiative_data:
        elem["product"] = choice(products)

    initiatives = []
    for i_data in initiative_data:
        initiatives.append(InitiativeService.create(**i_data))

    capabilities = create_capabilities()

    skill_data = read_json_data("sample_data/skill.json", "skill")

    skills = []
    for sk in skill_data:
        skills.append(SkillService.create(**sk))

    expertise_data = read_json_data("sample_data/expertise.json", "expertise")

    expertise = []
    for exp in expertise_data:
        expertise.append(ExpertiseService.create(**exp))

    tag_data = read_json_data("sample_data/tag.json", "tag")

    tags = []
    for tag in tag_data:
        tags.append(TagService.create(**tag))

    challenge_data = read_json_data("sample_data/challenge.json", "challenge")

    for elem in challenge_data:
        elem["initiative"] = choice(initiatives)
        elem["capability"] = choice(capabilities)
        elem["created_by"] = choice(people)
        elem["updated_by"] = choice(people)
        elem["reviewer"] = choice(people)
        elem["product"] = choice(products)
        elem["skill"] = choice(skills)

    challenges = []
    for cd in challenge_data:
        challenge = ChallengeService.create(**cd)
        challenge.expertise.set(sample(expertise, k=randint(1, 3)))
        challenges.append(challenge)

    organisation_data = read_json_data("sample_data/organisation.json", "organisation")

    organisations = []
    for org_data in organisation_data:
        organisations.append(OrganisationService.create(**org_data))

    organisation_account_data = read_json_data(
        "sample_data/organisation_account.json", "organisation account"
    )

    for index, oad in enumerate(organisation_account_data):
        oad["organisation"] = organisations[index]

    organisation_accounts = []
    for oad in organisation_account_data:
        organisation_accounts.append(OrganisationAccountService.create(**oad))

    organisation_account_credit_data = read_json_data(
        "sample_data/organisation_account_credit.json", "organisation account credit"
    )

    for index, oac in enumerate(organisation_account_credit_data):
        oac["organisation_account"] = organisation_accounts[index]

    organisation_account_credits = []
    for oacd in organisation_account_credit_data:
        organisation_account_credits.append(
            OrganisationAccountCreditService.create(**oacd)
        )

    fancy_out("Create a PointPriceConfiguration record")

    point_price_conf_service = PointPriceConfigurationService()
    point_price_conf_service.create(
        applicable_from_date=datetime.date.today(),
        usd_point_inbound_price_in_cents=2,
        eur_point_inbound_price_in_cents=2,
        gbp_point_inbound_price_in_cents=2,
        usd_point_outbound_price_in_cents=1,
        eur_point_outbound_price_in_cents=1,
        gbp_point_outbound_price_in_cents=1,
    )

    cart_data = read_json_data("sample_data/cart.json", "cart")

    for index, cd in enumerate(cart_data):
        cd["creator"] = choice(people)
        cd["organisation_account"] = organisation_accounts[index]

    carts = []
    for cd in cart_data:
        carts.append(CartService.create(**cd))

    fancy_out("Complete!")
