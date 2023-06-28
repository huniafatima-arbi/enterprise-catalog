import datetime
from uuid import uuid4

import factory
from factory.fuzzy import FuzzyText
from faker import Faker

from enterprise_catalog.apps.catalog.constants import (
    COURSE,
    COURSE_RUN,
    LEARNER_PATHWAY,
    PROGRAM,
    json_serialized_course_modes,
)
from enterprise_catalog.apps.catalog.models import (
    CatalogQuery,
    ContentMetadata,
    EnterpriseCatalog,
    EnterpriseCatalogFeatureRole,
    EnterpriseCatalogRoleAssignment,
)
from enterprise_catalog.apps.core.models import User


USER_PASSWORD = 'password'
FAKE_ADVERTISED_COURSE_RUN_UUID = uuid4()
FAKE_CONTENT_AUTHOR_NAME = 'Partner Name'
FAKE_CONTENT_AUTHOR_UUID = uuid4()
FAKE_CONTENT_TITLE_PREFIX = 'Fake Content Title'

fake = Faker()


class CatalogQueryFactory(factory.django.DjangoModelFactory):
    """
    Test factory for the `CatalogQuery` model
    """
    class Meta:
        model = CatalogQuery

    content_filter = factory.Dict({'content_type': factory.Faker('words', nb=3)})
    title = FuzzyText(length=100)


class EnterpriseCatalogFactory(factory.django.DjangoModelFactory):
    """
    Test factory for the `EnterpriseCatalog` model
    """
    class Meta:
        model = EnterpriseCatalog

    uuid = factory.LazyFunction(uuid4)
    title = FuzzyText(length=255)
    enterprise_uuid = factory.LazyFunction(uuid4)
    enterprise_name = factory.Faker('company')
    catalog_query = factory.SubFactory(CatalogQueryFactory)
    enabled_course_modes = json_serialized_course_modes()
    publish_audit_enrollment_urls = False   # Default to False


class ContentMetadataFactory(factory.django.DjangoModelFactory):
    """
    Test factory for the `ContentMetadata` model
    """
    class Meta:
        model = ContentMetadata
        # Exclude certain factory fields from being used as model fields during mode.save().  If these were not
        # specified here, the test SQL server would throw an error that the field does not exist on the table.
        exclude = ('card_image_url_prefix', 'card_image_url', 'title')

    # factory fields
    card_image_url_prefix = factory.Faker('image_url')
    card_image_url = factory.LazyAttribute(lambda p: f'{p.card_image_url_prefix}.jpg')
    title = factory.Faker('lexify', text=f'{FAKE_CONTENT_TITLE_PREFIX} ??????????')

    # model fields
    content_key = factory.Sequence(lambda n: f'{str(n).zfill(5)}_metadata_item')
    content_type = factory.Iterator([COURSE_RUN, COURSE, PROGRAM, LEARNER_PATHWAY])
    parent_content_key = None

    @factory.lazy_attribute
    def json_metadata(self):
        json_metadata = {
            'key': self.content_key,
            'aggregation_key': f'{self.content_type}:{self.content_key}',
            'uuid': str(uuid4()),
            'title': self.title,
        }
        if self.content_type == COURSE:
            owners = [{
                'uuid': str(FAKE_CONTENT_AUTHOR_UUID),
                'name': FAKE_CONTENT_AUTHOR_NAME,
                'logo_image_url': fake.image_url() + '.jpg',
            }]
            course_runs = [{
                'key': 'course-v1:edX+DemoX',
                'uuid': str(FAKE_ADVERTISED_COURSE_RUN_UUID),
                'content_language': 'en-us',
                'status': 'published',
                'is_enrollable': True,
                'is_marketable': True,
                'availability': 'current',
            }]
            json_metadata.update({
                'content_type': COURSE,
                'marketing_url': f'https://marketing.url/{self.content_key}',
                'image_url': self.card_image_url,
                'owners': owners,
                'advertised_course_run_uuid': str(FAKE_ADVERTISED_COURSE_RUN_UUID),
                'course_runs': course_runs,
            })
        elif self.content_type == COURSE_RUN:
            json_metadata.update({
                'content_type': COURSE_RUN,
                'content_language': 'en-us',
                'status': 'published',
                'is_enrollable': True,
                'is_marketable': True,
                'availability': 'current',
                'image_url': self.card_image_url,
            })
        elif self.content_type == PROGRAM:
            # programs in the wild do not have a key
            json_metadata.pop('key')
            authoring_organizations = [{
                'uuid': str(FAKE_CONTENT_AUTHOR_UUID),
                'name': FAKE_CONTENT_AUTHOR_NAME,
                'logo_image_url': fake.image_url() + '.jpg',
            }]
            json_metadata.update({
                'uuid': self.content_key,
                'content_type': PROGRAM,
                'type': 'MicroMasters',
                'hidden': True,
                'marketing_url': f'https://marketing.url/{self.content_key}',
                'authoring_organizations': authoring_organizations,
                'card_image_url': self.card_image_url,
            })
        elif self.content_type == LEARNER_PATHWAY:
            json_metadata.update({
                'content_type': LEARNER_PATHWAY,
                'name': 'Data Engineer',
                'status': 'active',
                'overview': 'Pathway for a data engineer.',
                'published': True,
                'visible_via_association': True,
                'created': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                'card_image': {
                    'card': {
                        'url': self.card_image_url,
                        'width': 378,
                        'height': 225,
                    },
                },
            })
        return json_metadata


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.PostGenerationMethodCall('set_password', USER_PASSWORD)
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_staff = False
    is_superuser = False

    class Meta:
        model = User


class EnterpriseCatalogFeatureRoleFactory(factory.django.DjangoModelFactory):
    """
    Test factory for the `EnterpriseCatalogFeatureRole` model.
    """
    name = FuzzyText(length=32)

    class Meta:
        model = EnterpriseCatalogFeatureRole


class EnterpriseCatalogRoleAssignmentFactory(factory.django.DjangoModelFactory):
    """
    Test factory for the `EnterpriseCatalogRoleAssignment` model.
    """
    role = factory.SubFactory(EnterpriseCatalogFeatureRoleFactory)
    enterprise_id = factory.LazyFunction(uuid4)

    class Meta:
        model = EnterpriseCatalogRoleAssignment
