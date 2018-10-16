import logging
import time
import warnings

import requests

import pycounter.exceptions


logger = logging.getLogger(__name__)


def _raw_to_full(raw_report):
    """Convert a raw report to CounterReport.

    :param raw_report: raw report as dict decoded from JSON
    :return: a :class:`pycounter.report.CounterReport`
    """
    #  FIXME


def get_sushi_stats_raw(
    wsdl_url=None,
    start_date=None,
    end_date=None,
    requestor_id=None,
    requestor_email=None,
    requestor_name=None,
    customer_reference=None,
    customer_name=None,
    report="TR_J1",
    release=5,
    sushi_dump=False,
    verify=True,
    url=None,
):
    """Get SUSHI stats for a given site in dict (decoded from JSON) format.

    :param wsdl_url: (Deprecated; for backward compatibility with COUNTER 4 SUSHI
    code. Use `url` instead.) URL to API endpoint for this provider

    :param start_date: start date for report (must be first day of a month)

    :param end_date: end date for report (must be last day of a month)

    :param requestor_id: requestor ID as defined by SUSHI protocol

    :param requestor_email: requestor email address, if required by provider

    :param requestor_name: Internationally recognized organization name

    :param customer_reference: customer reference number as defined by SUSHI
        protocol

    :param customer_name: Internationally recognized organization name

    :param report: report type, values defined by SUSHI protocol

    :param release: report release number (should generally be `4`.)

    :param sushi_dump: produces dump of XML to DEBUG logger

    :param verify: bool: whether to verify SSL certificates

    :param url: str: URL to endpoint for this provider

    """
    if url is None and wsdl_url:
        warnings.warn(
            DeprecationWarning(
                "wsdl_url argument to get_sushi_stats"
                "_raw is deprecated; use url instead"
            )
        )
        url = wsdl_url
    url_params = {"url": url, "report": report}
    req_params = {
        "customer_id": customer_reference,
        "begin_date": start_date,
        "end_date": end_date,
        "requestor_id": requestor_id,
    }

    response = requests.get(
        "{url}/reports/{report}".format(**url_params),
        params=req_params,
        headers={"User-Agent": "pycounter/%s" % pycounter.__version__},
    )

    if sushi_dump:
        logger.debug(
            "SUSHI DUMP: request: %s \n\n response: %s",
            vars(response.request),
            response.content,
        )

    return response.json()


def get_report(*args, **kwargs):
    """Get a usage report from a COUNTER 5 (RESTful) SUSHI server.

    returns a :class:`pycounter.report.CounterReport` object.

    parameters: see get_sushi_stats_raw

    :param no_delay: don't delay in retrying Report Queued
    """
    no_delay = kwargs.pop("no_delay", False)
    delay_amount = 0 if no_delay else 60
    while True:
        try:
            raw_report = get_sushi_stats_raw(*args, **kwargs)
            return _raw_to_full(raw_report)
        except pycounter.exceptions.ServiceBusyError:
            print("Service busy, retrying in %d seconds" % delay_amount)
            time.sleep(delay_amount)