"""NISO SUSHI support."""
from __future__ import absolute_import

import collections
import datetime
import logging
import time
import uuid


from lxml import etree
from lxml import objectify
import pendulum
import requests
import six

from pycounter import sushi5
import pycounter.constants
import pycounter.exceptions
from pycounter.helpers import convert_date_run
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

    response = requests.post(url=wsdl_url, headers=headers, data=payload, verify=verify)

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

    no_delay = kwargs.pop("no_delay", False)
    delay_amount = 0 if no_delay else 60
    while True:
        try:
            raw_report = gssr(*args, **kwargs)
            return rtf(raw_report)
        except pycounter.exceptions.ServiceBusyError:
            print("Service busy, retrying in %d seconds" % delay_amount)
            time.sleep(delay_amount)


def ns(namespace, name):
    """Convenience function to make a namespaced XML name.

    :param namespace: one of 'SOAP-ENV', 'sushi', 'sushicounter', 'counter'
    :param name: tag name within the given namespace
    """
    return "{" + NS[namespace] + "}" + name


def raw_to_full(raw_report):
    """Convert a raw report to CounterReport.

    :param raw_report: raw XML report
    :return: a :class:`pycounter.report.CounterReport`
    """
    # pylint: disable=too-many-statements,too-many-branches,too-many-locals
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
            else:
                logger.error("report not found in XML: %s", raw_report)
                raise pycounter.exceptions.SushiException(
                    message="report not found in XML", raw=raw_report, xml=o_root
                )
    logger.debug("COUNTER report: %s", etree.tostring(c_report))
    start_date = datetime.datetime.strptime(
        root.find(".//%s" % ns("sushi", "Begin")).text, "%Y-%m-%d"
    ).date()

    end_date = datetime.datetime.strptime(
        root.find(".//%s" % ns("sushi", "End")).text, "%Y-%m-%d"
    ).date()

    report_data = {"period": (start_date, end_date)}

    rep_def = root.find(".//%s" % ns("sushi", "ReportDefinition"))
    report_data["report_version"] = int(rep_def.get("Release"))

    report_data["report_type"] = rep_def.get("Name")

    customer = root.find(".//%s" % ns("counter", "Customer"))
    try:
        report_data["customer"] = customer.find(".//%s" % ns("counter", "Name")).text
    except AttributeError:
        report_data["customer"] = ""

    try:
        inst_id = customer.find(".//%s" % ns("counter", "ID")).text
    except AttributeError:
        inst_id = u""
    report_data["institutional_identifier"] = inst_id

    rep_root = root.find(".//%s" % ns("counter", "Report"))
    created_string = rep_root.get("Created")
    if created_string is not None:
        report_data["date_run"] = pendulum.parse(created_string)
    else:
        report_data["date_run"] = datetime.datetime.now()

    report = pycounter.report.CounterReport(**report_data)

    report.metric = pycounter.constants.METRICS.get(report_data["report_type"])

    for item in c_report.Customer.ReportItems:
        try:
            publisher_name = item.ItemPublisher.text
        except AttributeError:
            publisher_name = ""
        title = item.ItemName.text
        platform = item.ItemPlatform.text

        eissn = issn = ""
        print_isbn = None
        online_isbn = None
        doi = ""
        prop_id = ""

        try:
            for identifier in item.ItemIdentifier:
                if identifier.Type == "Print_ISSN":
                    issn = identifier.Value.text
                    if issn is None:
                        issn = ""
                elif identifier.Type == "Online_ISSN":
                    eissn = identifier.Value.text
                    if eissn is None:
                        eissn = ""
                elif identifier.Type == "Online_ISBN":
                    online_isbn = identifier.Value.text
                elif identifier.Type == "Print_ISBN":
                    print_isbn = identifier.Value.text
                elif identifier.Type == "DOI":
                    doi = identifier.Value.text
                elif identifier.Type == "Proprietary":
                    prop_id = identifier.Value.text

        except AttributeError:
            pass

        month_data = []
        html_usage = 0
        pdf_usage = 0

        metrics_for_db = collections.defaultdict(list)

        for perform_item in item.ItemPerformance:
            item_date = convert_date_run(perform_item.Period.Begin.text)
            logger.debug("perform_item date: %r", item_date)
            usage = None
            if hasattr(perform_item, "Instance"):
                for inst in perform_item.Instance:
                    if inst.MetricType == "ft_total":
                        usage = str(inst.Count)
                    elif inst.MetricType == "ft_pdf":
                        pdf_usage += int(inst.Count)
                    elif inst.MetricType == "ft_html":
                        html_usage += int(inst.Count)
                    elif report.report_type.startswith("DB"):
                        metrics_for_db[inst.MetricType].append(
                            (item_date, int(inst.Count))
                        )
            if usage is not None:
                month_data.append((item_date, int(usage)))

        if report.report_type:
            if report.report_type.startswith("JR"):
                report.pubs.append(
                    pycounter.report.CounterJournal(
                        title=title,
                        platform=platform,
                        publisher=publisher_name,
                        period=report.period,
                        metric=report.metric,
                        issn=issn,
                        eissn=eissn,
                        doi=doi,
                        proprietary_id=prop_id,
                        month_data=month_data,
                        html_total=html_usage,
                        pdf_total=pdf_usage,
                    )
                )
            elif report.report_type.startswith("BR"):
                report.pubs.append(
                    pycounter.report.CounterBook(
                        title=title,
                        platform=platform,
                        publisher=publisher_name,
                        period=report.period,
                        metric=report.metric,
                        issn=issn,
                        doi=doi,
                        proprietary_id=prop_id,
                        print_isbn=print_isbn,
                        online_isbn=online_isbn,
                        month_data=month_data,
                    )
                )
            elif report.report_type.startswith("DB"):
                for metric_code, month_data in six.iteritems(metrics_for_db):
                    metric = pycounter.constants.DB_METRIC_MAP[metric_code]
                    report.pubs.append(
                        pycounter.report.CounterDatabase(
                            title=title,
                            platform=platform,
                            publisher=publisher_name,
                            period=report.period,
                            metric=metric,
                            month_data=month_data,
                        )
                    )

    return report
