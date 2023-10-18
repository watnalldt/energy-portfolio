from datetime import datetime, timedelta

from django import template
from django.utils import timezone

from clients.models import Client
from contracts.models import Contract

register = template.Library()

current_date = timezone.now()
end_date_30_days = current_date + timedelta(days=30)
end_date_60_days = current_date + timedelta(days=60)


@register.simple_tag
def total_clients(user):
    """Returns total number of clients for the given user"""
    clients = Client.objects.filter(account_manager=user).count()
    return clients


@register.simple_tag
def total_seamless_contracts(user):
    """Returns most 5 most recent events"""
    contracts = (
        Contract.objects.filter(client__account_manager=user)
        .filter(contract_type="SEAMLESS")
        .count()
    )
    return contracts


@register.simple_tag
def total_non_seamless_contracts(user):
    """Returns most 5 most recent events"""
    contracts = (
        Contract.objects.filter(client__account_manager=user)
        .filter(contract_type="NON_SEAMLESS")
        .count()
    )
    return contracts


@register.simple_tag
def total_contracts_directors_approval(user):
    """Returns most 5 most recent events"""
    contracts = (
        Contract.objects.filter(client__account_manager=user)
        .filter(is_directors_approval="YES")
        .count()
    )
    return contracts


@register.simple_tag
def total_contracts(user):
    """Returns total number of contracts for the given client"""
    contracts = Contract.objects.filter(client__account_manager=user).count()
    return contracts


@register.inclusion_tag("account_managers/contracts_expiry_pie_chart.html")
def contract_expiry_chart_inclusion(user_id):
    expiry_30_days = (
        Contract.objects.filter(client__account_manager=user_id)
        .filter(contract_end_date__lte=end_date_30_days)
        .count()
    )
    expiry_60_days = (
        Contract.objects.filter(client__account_manager=user_id)
        .filter(contract_end_date__lte=end_date_60_days)
        .filter(contract_end_date__lte=end_date_60_days)
        .count()
    )
    expiry_over_60_days = (
        Contract.objects.filter(client__account_manager=user_id)
        .filter(contract_end_date__gt=end_date_60_days)
        .count()
    )
    out_of_contract = (
        Contract.objects.filter(client__account_manager=user_id).filter(is_ooc="YES").count()
    )
    context = {
        "expiry_30_days": expiry_30_days,
        "expiry_60_days": expiry_60_days,
        "expiry_over_60_days": expiry_over_60_days,
        "out_of_contract": out_of_contract,
    }
    return context


@register.inclusion_tag("account_managers/contracts_pie_chart.html")
def utility_contract_chart_inclusion(user_id):
    gas_contracts = (
        Contract.objects.filter(client__account_manager=user_id)
        .filter(utility__utility="Gas")
        .count()
    )
    electricity_contracts = (
        Contract.objects.filter(client__account_manager=user_id)
        .filter(utility__utility="Electricity")
        .count()
    )
    electricity_hh_contracts = (
        Contract.objects.filter(client__account_manager=user_id)
        .filter(utility__utility="Electricity - HH")
        .count()
    )
    electricity_nhh_contracts = (
        Contract.objects.filter(client__account_manager=user_id)
        .filter(utility__utility="Electricity - NHH")
        .count()
    )
    electricity_ums_contracts = (
        Contract.objects.filter(client__account_manager=user_id)
        .filter(utility__utility="Electricity - UMS")
        .count()
    )
    context = {
        "gas_contracts": gas_contracts,
        "electricity_contracts": electricity_contracts,
        "electricity_hh_contracts": electricity_hh_contracts,
        "electricity_nhh_contracts": electricity_nhh_contracts,
        "electricity_ums_contracts": electricity_ums_contracts,
    }
    return context


@register.inclusion_tag("account_managers/suppliers_pie_chart.html")
def supplier_contract_chart_inclusion(user_id):
    corona_contracts = (
        Contract.objects.filter(client__account_manager=user_id)
        .filter(supplier__supplier="Crown")
        .count()
    )
    pozitive_contracts = (
        Contract.objects.filter(client__account_manager=user_id)
        .filter(supplier__supplier="Pozitive")
        .count()
    )
    crown_contracts = (
        Contract.objects.filter(client__account_manager=user_id)
        .filter(supplier__supplier="Crown")
        .count()
    )
    sse_contracts = (
        Contract.objects.filter(client__account_manager=user_id)
        .filter(supplier__supplier="SSE")
        .count()
    )
    eon_contracts = (
        Contract.objects.filter(client__account_manager=user_id)
        .filter(supplier__supplier="E.ON")
        .count()
    )
    context = {
        "corona_contracts": corona_contracts,
        "pozitive_contracts": pozitive_contracts,
        "crown_contracts": crown_contracts,
        "sse_contracts": sse_contracts,
        "eon_contracts": eon_contracts,
    }
    return context


@register.inclusion_tag("account_managers/contracts_by_year_pie_chart.html")
def contract_by_year_inclusion(user_id):
    # Calculate the number of contracts for the current year
    end_date = datetime.strptime("31-12-2023", "%d-%m-%Y")
    contracts_this_year = Contract.objects.filter(
        client__account_manager=user_id, contract_end_date__lte=end_date
    ).count()

    # Calculate the number of contracts for the next year
    next_year_start = datetime.strptime("01-01-2024", "%d-%m-%Y")
    next_year_end = datetime.strptime("31-12-2024", "%d-%m-%Y")
    contracts_next_year = Contract.objects.filter(
        client__account_manager=user_id,
        contract_end_date__lte=next_year_end,
        contract_end_date__gt=next_year_start,
    ).count()

    # Calculate the number of contracts for previous years
    previous_end_date = datetime.strptime("31-12-2022", "%d-%m-%Y")
    contracts_previous_years = Contract.objects.filter(
        client__account_manager=user_id, contract_end_date__lte=previous_end_date
    ).count()

    context = {
        "contracts_this_year": contracts_this_year,
        "contracts_next_year": contracts_next_year,
        "contracts_previous_years": contracts_previous_years,
    }
    return context
