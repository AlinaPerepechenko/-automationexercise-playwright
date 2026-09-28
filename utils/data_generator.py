"""Random-but-valid data for account/checkout flows, so parallel test runs
never collide on the same email/user and every run is independent/repeatable
in isolation."""
from dataclasses import dataclass, field
from faker import Faker

fake = Faker()


@dataclass
class UserData:
    name: str
    email: str
    password: str
    title: str = "Mr"
    day: str = "10"
    month: str = "5"
    year: str = "1990"
    first_name: str = ""
    last_name: str = ""
    company: str = "QA Corp"
    address1: str = ""
    address2: str = ""
    country: str = "United States"
    state: str = ""
    city: str = ""
    zipcode: str = ""
    mobile_number: str = ""

    def __post_init__(self):
        self.first_name = self.first_name or self.name.split(" ")[0]
        self.last_name = self.last_name or (fake.last_name())
        self.address1 = self.address1 or fake.street_address()
        self.address2 = self.address2 or fake.secondary_address()
        self.state = self.state or fake.state()
        self.city = self.city or fake.city()
        self.zipcode = self.zipcode or fake.postcode()
        self.mobile_number = self.mobile_number or fake.numerify("##########")


@dataclass
class CardData:
    name_on_card: str = field(default_factory=lambda: fake.name())
    card_number: str = field(default_factory=lambda: fake.credit_card_number(card_type="visa"))
    cvc: str = field(default_factory=lambda: fake.numerify("###"))
    expiry_month: str = "12"
    expiry_year: str = "2028"


def random_user() -> UserData:
    unique = fake.unique.user_name()
    return UserData(
        name=fake.first_name(),
        email=f"qa.{unique}.{fake.random_int(1000, 9999)}@mailinator.com",
        password=fake.password(length=12),
    )


def random_card() -> CardData:
    return CardData()
