from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from app.organization.models import Organization
from app.position.models import Position
from app.role.models import Role
from app.icd_10.models import Icd_10
from app.icd_03.models import Icd_03
from app.employee.models import Employee
from app.scanning.models import Scanning
from app.histological_scanners.models import HistologicalScanners
from app.research.models import Research
from app.series.models import Series
from app.slide.models import Slide
from app.external_upload_file.models import ExternalUploadFile


admin.site.site_header = 'Административная часть'
admin.site.index_title = 'База данных гистологических стёкол'


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'

# Define a new User admin


class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


admin.site.register(Position)
admin.site.register(Role)
admin.site.register(Icd_10)
admin.site.register(Icd_03)
admin.site.register(Employee)
admin.site.register(Research)
admin.site.register(Series)
admin.site.register(Slide)
admin.site.register(Scanning)
admin.site.register(HistologicalScanners)
admin.site.register(Organization)
