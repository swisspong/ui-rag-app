from .error import Error


class DomainError(Error):
    status_code = 400