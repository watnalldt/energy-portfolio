from django import template

from clients.models import Client
from contracts.models import Contract

register = template.Library()


@register.simple_tag
def total_clients(user):
    """Returns total number of clients for the given user"""
    clients = Client.objects.filter(account_manager=user).count()
    return clients


@register.simple_tag
def total_contracts(user):
    """Returns total number of contracts for the given client"""
    contracts = Contract.objects.filter(client__account_manager=user).count()
    return contracts


@register.simple_tag
def total_electricity_contracts(user):
    """Returns most 5 most recent events"""
    contracts = (
        Contract.objects.filter(client__account_manager=user)
        .filter(utility__utility="Electricity")
        .count()
    )
    return contracts


@register.simple_tag
def total_gas_contracts(user):
    """Returns most 5 most recent events"""
    contracts = (
        Contract.objects.filter(client__account_manager=user).filter(utility__utility="Gas").count()
    )
    return contracts


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
def total_contracts_end_dates(user):
    """Returns most 5 most recent events"""
    contracts = (
        Contract.objects.filter(client__account_manager=user)
        .filter(contract_end_date__lte="2023-12-31")
        .count()
    )
    return contracts


@register.simple_tag
def total_contracts_ooc(user):
    """Returns most 5 most recent events"""
    contracts = Contract.objects.filter(client__account_manager=user).filter(is_ooc="YES").count()
    return contracts
