import random
import factory 

from ..models import User


class UserFactory(factory.Factory):
    
    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    email = factory.Faker('email')
    gender = random.choice(User.Gender.choices)

    class Meta:
        model = User
    