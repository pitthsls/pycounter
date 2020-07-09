"""NISO SUSHI support."""
import datetime
import logging
import time
import uuid
import warnings

from lxml import etree
from lxml import objectify
import pendulum
import requests

from pycounter import sushi5
import pycounter.constants
import pycounter.exceptions
from pycounter.helpers import ns
import pycounter.report


logger = logging.getLogger(__name__)
NS = pycounter.constants.NS


def get_sushi_stats_raw(
    wsdl_url,
    start_date,
    end_date,
    requestor_id=None,
    requestor_email=None,
    requestor_name=None,
    customer_reference=None,
    customer_name=None,
    report="JR1",
    release=4,
    sushi_dump=False,
    verify=True,
    **extra_params
):
    """Get SUSHI stats for a given site in raw XML format.

    :param wsdl_url: URL to SOAP WSDL for this provider

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

    :param sushi_dump: produces dump of XML (or JSON, for COUNTER 5) to DEBUG logger

    :param verify: bool: whether to verify SSL certificates

    :param extra_params: extra params are passed to requests.post

    """
    # pylint: disable=too-many-locals
    root = etree.Element("{%(SOAP-ENV)s}Envelope" % NS, nsmap=NS)
    body = etree.SubElement(root, "{%(SOAP-ENV)s}Body" % NS)
    timestamp = pendulum.now("UTC").isoformat()
    report_req = etree.SubElement(
        body,
        "{%(sushicounter)s}ReportRequest" % NS,
        {"Created": timestamp, "ID": str(uuid.uuid4())},
    )

    req = etree.SubElement(report_req, "{%(sushi)s}Requestor" % NS)
    rid = etree.SubElement(req, "{%(sushi)s}ID" % NS)
    rid.text = requestor_id
    req_name_element = etree.SubElement(req, "{%(sushi)s}Name" % NS)
    req_name_element.text = requestor_name
    req_email_element = etree.SubElement(req, "{%(sushi)s}Email" % NS)
    req_email_element.text = requestor_email

    cust_ref_elem = etree.SubElement(report_req, "{%(sushi)s}CustomerReference" % NS)
    cid = etree.SubElement(cust_ref_elem, "{%(sushi)s}ID" % NS)
    cid.text = customer_reference
    cust_name_elem = etree.SubElement(cust_ref_elem, "{%(sushi)s}Name" % NS)
    cust_name_elem.text = customer_name

    report_def_elem = etree.SubElement(
        report_req,
        "{%(sushi)s}ReportDefinition" % NS,
        Name=report,
        Release=str(release),
    )
    filters = etree.SubElement(report_def_elem, "{%(sushi)s}Filters" % NS)
    udr = etree.SubElement(filters, "{%(sushi)s}UsageDateRange" % NS)
    beg = etree.SubElement(udr, "{%(sushi)s}Begin" % NS)
    beg.text = start_date.strftime("%Y-%m-%d")
    end = etree.SubElement(udr, "{%(sushi)s}End" % NS)
    end.text = end_date.strftime("%Y-%m-%d")

    payload = etree.tostring(
        root, pretty_print=True, xml_declaration=True, encoding="utf-8"
    )

    headers = {
        "SOAPAction": '"SushiService:GetReportIn"',
        "Content-Type": "text/xml; charset=UTF-8",
        "User-Agent": "pycounter/%s" % pycounter.__version__,
        "Content-Length": str(len(payload)),
    }

    response = requests.post(
        url=wsdl_url, headers=headers, data=payload, verify=verify, **extra_params
    )

    if sushi_dump:
        logger.debug(
            "SUSHI DUMP: request: %s \n\n response: %s", payload, response.content
        )
    return response.content


def get_report(*args, **kwargs):
    """Get a usage report from a SUSHI server.

    returns a :class:`pycounter.report.CounterReport` object.

    parameters: see get_sushi_stats_raw

    :param no_delay: don't delay in retrying Report Queued
    """
    if kwargs.get("release") == 5:
        gssr = sushi5.get_sushi_stats_raw
        rtf = sushi5.raw_to_full

    else:
        gssr = get_sushi_stats_raw
        rtf = raw_to_full
        if "api_key" in kwargs:
            if kwargs["api_key"] is not None:
                warnings.warn(
                    pycounter.exceptions.SushiWarning(
                        "api_key only supported in COUNTER 5"
                    )
                )
            kwargs.pop("api_key", None)

    no_delay = kwargs.pop("no_delay", False)
    delay_amount = 0 if no_delay else 60
    while True:
        try:
            raw_report = gssr(*args, **kwargs)
            return rtf(raw_report)
        except pycounter.exceptions.ServiceBusyError:
            print("Service busy, retrying in %d seconds" % delay_amount)
            time.sleep(delay_amount)


def raw_to_full(raw_report):
    """Convert a raw report to CounterReport.

    :param raw_report: raw XML report
    :return: a :class:`pycounter.report.CounterReport`
    """
    try:
        root = etree.fromstring(raw_report)
    except etree.XMLSyntaxError:
        logger.error("XML syntax error: %s", raw_report)
        raise pycounter.exceptions.SushiException(
            message="XML syntax error", raw=raw_report
        )
    o_root = objectify.fromstring(raw_report)
    rep = None
    try:
        rep = o_root.Body[ns("sushicounter", "ReportResponse")]
        c_report = rep.Report[ns("counter", "Report")]
    except AttributeError:
        try:
            c_report = rep.Report[ns("counter", "Reports")].Report
        except AttributeError:
            if b"Report Queued" in raw_report:
                raise pycounter.exceptions.ServiceBusyError("Report Queued")
            try:
                c_report = o_root[ns("counter", "Report")]
            except AttributeError:
                logger.error("report not found in XML: %s", raw_report)
                raise pycounter.exceptions.SushiException(
                    message="report not found in XML", raw=raw_report, xml=o_root
                )
    logger.debug("COUNTER report: %s", etree.tostring(c_report))
    try:
        start_date = datetime.datetime.strptime(
            root.find(".//%s" % ns("sushi", "Begin")).text, "%Y-%m-%d"
        ).date()
    except AttributeError:
        start_date = None
    try:
        end_date = datetime.datetime.strptime(
            root.find(".//%s" % ns("sushi", "End")).text, "%Y-%m-%d"
        ).date()
    except AttributeError:
        end_date = None

    period = (start_date, end_date)

    return pycounter.report.CounterReport.from_xml(
        etree.tostring(c_report.getparent()), period=period
    )
