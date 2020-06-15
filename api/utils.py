import random
from .models import *


def get_doctor(hospital):
    queryset = UserProfile.objects.filter(user_type=1, current_hospital=hospital)
    ids = [profile.user.id for profile in queryset]

    print(ids)

    selected = random.choice(ids)
    return selected
