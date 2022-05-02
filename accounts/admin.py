import datetime

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import EmailActivation, News


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to change and add user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'full_name', 'email', 'is_superuser')
    list_filter = ('is_superuser', 'staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        # would have data we had fields like 'full_name'
        ('Personal info', {'fields': ('full_name', 'cash', 'loan', 'coeff_of_variation')}),
        ('Permissions', {'fields': ('is_superuser', 'staff', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'full_name', 'cash', 'loan', 'coeff_of_variation', 'password1', 'password2'
            )}
         ),
    )
    search_fields = ('username', 'email', 'full_name')
    ordering = ('username', 'email')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)


class EmailActivationAdmin(admin.ModelAdmin):
    search_fields = ['email']   # Search guest users by email in admin panel

    class Meta:
        model = EmailActivation


admin.site.register(EmailActivation, EmailActivationAdmin)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'is_active')
    search_fields = ['title', 'content']   # Search guest users by email in admin panel

    actions = ['make_active', 'make_inactive']

    @admin.action(description='Mark selected news as active')
    def make_active(self, request, queryset):
        queryset.update(is_active = True)
        queryset.update(updated = datetime.datetime.now() )

    @admin.action(description='Mark selected news as inactive')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    class Meta:
        model = News
admin.site.register(News, NewsAdmin)