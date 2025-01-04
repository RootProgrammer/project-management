from django.contrib import admin
from .models import Users, Projects, ProjectMembers, Tasks, Comments

# Register models
admin.site.register(Users)
admin.site.register(Projects)
admin.site.register(ProjectMembers)
admin.site.register(Tasks)
admin.site.register(Comments)
