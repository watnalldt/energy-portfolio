from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    # client manager registration
    path("register-user/", views.client_manager_registration, name="client_manager_registration"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("reset_password/", views.reset_password, name="reset_password"),
    path(
        "reset_password_validate/<uidb64>/<token>/",
        views.reset_password_validate,
        name="reset_password_validate",
    ),
    # Dashboards
    path("my_account/", views.my_account, name="my_account"),
    path(
        "account_managers_dashboard/",
        views.AccountManagerView.as_view(),
        name="account_managers_dashboard",
    ),
    path(
        "client_managers_dashboard/",
        views.ClientManagerDashBoard.as_view(),
        name="client_managers_dashboard",
    ),
    # Client List
    path(
        "account_managers_client_list/",
        views.AccountManagerClientList.as_view(),
        name="client_list",
    ),
]
