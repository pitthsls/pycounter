"""Exception classes for pycounter."""


class PycounterException(Exception):
    """Base class for all module exceptions."""


class UnknownReportTypeError(PycounterException):
    """We can't parse this kind of report yet."""


class SushiException(PycounterException):
    """Base class for SUSHI-related exceptions."""

    def __init__(self, message, raw=None, xml=None):
        super().__init__(message)
        self.raw = raw
        self.xml = xml


class ServiceNotAvailableError(SushiException):
    """Fatal error: service failed due to internal error."""


class ServiceBusyError(SushiException):
    """Fatal error: server is too busy; try again later."""


class TooManyRequestsError(SushiException):
    """Fatal error: The client has made too many requests to the service."""


class RequestorNotAuthorizedError(SushiException):
    """
    Requestor is not authorized.

    Requestor ID or CustomerReference are not recognized as giving
    authorization to retrieve statistics.
    """


class Sushi5Error(SushiException):
    """Error from SUSHI release 5.

    Attributes:
        message: error message from the server
    """

    def __init__(self, message, severity, code):
        super().__init__(message)
        self.message = message
        self.severity = severity
        self.code = code


class ReportNotSupportedError(SushiException):
    """Server cannot serve the requested report name or version."""


class InvalidDateError(SushiException):
    """Dates are formatted incorrectly or illogical."""


class NoUsageAvailableError(SushiException):
    """Service has no data for requested date range."""


class PycounterWarning(Warning, PycounterException):
    """Warnings from pycounter."""


class SushiWarning(Warning, SushiException):
    """Base class for SUSHI_related warnings."""


class PartialDataWarning(SushiWarning):
    """Request not completely fulfilled, but available data was returned."""


class FilterNotSupportedWarning(SushiWarning):
    """a filter was ignored, because it was unsupported.

    Data is returned without that filter applied
    """


class ReportAttributeNotSupportedWarning(SushiWarning):
    """a report attribute was ignored because it was unsupported.

    Data is returned without that attribute applied
    """


class InvalidFilterValueWarning(SushiWarning):
    """a filter was ignored, because its value was unsupported.

    Data is returned without that filter applied
    """


class InvalidReportAttributeWarning(SushiWarning):
    """a report attribute was ignored because its value was unsupported.

    Data is returned without that attribute applied
    """
