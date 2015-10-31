class NotEnoughFundingException(Exception):
    pass


class ProjectNotCompleteException(Exception):
    pass

class NotInUserReinvestmentPeriod(Exception):
    pass

class NotInAdminReinvestmentPeriod(Exception):
    pass