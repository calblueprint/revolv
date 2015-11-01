"""
Some interesting exceptions
"""


class NotEnoughFundingException(Exception):
    pass


class ProjectNotCompleteException(Exception):
    pass


class NotInUserReinvestmentPeriodException(Exception):
    pass


class NotInAdminReinvestmentPeriodException(Exception):
    pass


class ProjectNotEligibleException(Exception):
    pass