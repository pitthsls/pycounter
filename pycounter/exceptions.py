"""Exception classes for pycounter"""


class PycounterException(Exception):
    """Base class for all module exceptions"""
    pass


class UnknownReportTypeError(PycounterException):
    """We can't parse this kind of report yet."""
    pass


class SushiException(PycounterException):
    """Base class for SUSHI-related exceptions"""
    def __init__(self, message, raw=None, xml=None):
        super(SushiException, self).__init__(message)
        self.raw = raw
        self.xml = xml


class ServiceNotAvailableError(SushiException):
    """Fatal error: service failed due to internal error"""
    pass


class ServiceBusyError(SushiException):
    """Fatal error: server is too busy; try again later"""
    pass


class TooManyRequestsError(SushiException):
    """Fatal error: The client has made too many requests to the service"""
    pass


class RequestorNotAuthorizedError(SushiException):
    """Requestor ID or CustomerReference are not recognized as giving
    authorization to retrieve statistics
    """
    pass


class ReportNotSupportedError(SushiException):
    """Server cannot serve the requested report name or version"""
    pass


class InvalidDateError(SushiException):
    """Dates are formatted incorrectly or illogical"""
    pass


class NoUsageAvailableError(SushiException):
    """Service has no data for requested date range"""
    pass


class SushiWarning(Warning, SushiException):
    """Base class for SUSHI_related warnings"""
    pass


class PartialDataWarning(SushiWarning):
    """Request not completely fulfilled, but available data was returned"""
    pass


class FilterNotSupportedWarning(SushiWarning):
    """a filter was ignored, because it was unsupported.

    Data is returned without that filter applied
    """
    pass


class ReportAttributeNotSupportedWarning(SushiWarning):
    """a report attribute was ignored because it was unsupported.

    Data is returned without that attribute applied
    """
    pass


class InvalidFilterValueWarning(SushiWarning):
    """a filter was ignored, because its value was unsupported.

    Data is returned without that filter applied
    """
    pass


class InvalidReportAttributeWarning(SushiWarning):
    """a report attribute was ignored because its value was unsupported.

    Data is returned without that attribute applied
    """
    pass
