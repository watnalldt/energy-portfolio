from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from core.decorators import admin_changelist_link

from .models import Client

User = get_user_model()


class ClientResource(resources.ModelResource):
    account_manager = fields.Field(
        column_name="account_manager",
        attribute="account_manager",
        widget=ForeignKeyWidget(User, "email"),
    )

    class Meta:
        model = Client
        skip_unchanged = True
        report_skipped = True
        fields = [
            "id",
            "client",
            "account_manager",
        ]
        import_id_fields = ["id"]

        export_order = [
            "client",
            "account_manager",
        ]


class ClientAdmin(ImportExportModelAdmin):
    show_full_result_count = False
    resource_class = ClientResource
    list_display = (
        "client",
        "link_to_account_managers",
        "id",
        "contracts_link",
    )
    list_filter = (
        "client",
        "account_manager",
    )
    list_select_related = ("account_manager",)
    autocomplete_fields = ("account_manager",)
    search_fields = ("client", "account_manager__email")
    list_per_page = 25
    search_help_text = "Search by Client Name"
    ordering = ("client",)

    @admin_changelist_link(
        "client_contracts", _("All Contracts"), query_string=lambda c: f"client_id={c.pk}"
    )
    def contracts_link(self, client_contracts):
        return _("All Contracts")

    def link_to_account_managers(self, obj):
        link = reverse("admin:users_accountmanager_change", args=[obj.account_manager.id])
        return format_html(
            '<a href="{}">{}</a>',
            link,
            obj.account_manager,
        )

    link_to_account_managers.short_description = "Account Managers"


admin.site.register(Client, ClientAdmin)
