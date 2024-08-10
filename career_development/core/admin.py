from django.contrib import admin
from .models import Profile
from .models import Connection
from .models import Feedback
from .models import Badge


admin.site.register(Profile)
admin.site.register(Connection)
admin.site.register(Feedback)
admin.site.register(Badge)


