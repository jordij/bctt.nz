from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.helpers import PermissionHelper

from .models import Team, CompPageResult


class TeamModelAdmin(ModelAdmin):
    model = Team
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', )
    list_filter = ('region', )
    search_fields = ('name', )


class MyPermissionHelper(PermissionHelper):
    def user_can_create(self, user):
        return False


class CompPageResultModelAdmin(ModelAdmin):
    model = CompPageResult
    permission_helper_class = MyPermissionHelper
    menu_icon = 'table'
    menu_label = 'Results'
    label = 'Results'
    menu_order = 201
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title', 'page', 'date', 'team_one_name', 'team_two_name', )
    list_filter = ('page', 'date', 'team_one', 'team_two', 'is_final', )
    search_fields = ()
    list_display_add_buttons = False


modeladmin_register(TeamModelAdmin)
modeladmin_register(CompPageResultModelAdmin)
