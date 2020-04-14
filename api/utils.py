import random
from .models import *


def get_doctor():
    queryset = UserProfile.objects.filter(user_type=1)
    ids = [profile.user.id for profile in queryset]

    print(ids)

    selected = random.choice(ids)
    return selected
