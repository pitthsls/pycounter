"""NISO SUSHI support"""
from __future__ import absolute_import
from pycounter.helpers import convert_date_run

import pycounter.report
import pycounter.exceptions
import logging
import six
import requests
import datetime
import dateutil.parser
from lxml import etree
from lxml import objectify

logger = logging.getLogger(__name__)

NS = {
    'SOAP-ENV': "http://schemas.xmlsoap.org/soap/envelope/",
    'sushi': "http://www.niso.org/schemas/sushi",
    'sushicounter': "http://www.niso.org/schemas/sushi/counter",
    'counter': "http://www.niso.org/schemas/counter",
    }


def get_sushi_stats_raw(wsdl_url, start_date, end_date, requestor_id=None,
                        requestor_email=None, customer_reference=None,
                        report="JR1", release=4, sushi_dump=False):
    """Get SUSHI stats for a given site in raw XML format.

    :param wsdl_url: URL to SOAP WSDL for this provider

    :param start_date: start date for report (must be first day of a month)

    :param end_date: end date for report (must be last day of a month)

    :param requestor_id: requestor ID as defined by SUSHI protocol

    :param requestor_email: requestor email address, if required by provider

    :param customer_reference: customer reference number as defined by SUSHI
        protocol

    :param report: report type, values defined by SUSHI protocol

    :param release: report release number (should generally be `4`.)

    :param sushi_dump: produces dump of XML to DEBUG logger

    """
    root = etree.Element("{%(SOAP-ENV)s}Envelope" % NS, nsmap=NS)
    body = etree.SubElement(root, "{%(SOAP-ENV)s}Body" % NS)
    rr = etree.SubElement(body, "{%(sushicounter)s}ReportRequest" % NS)

    req = etree.SubElement(rr, "{%(sushi)s}Requestor" % NS)
    rid = etree.SubElement(req, "{%(sushi)s}ID" % NS)
    rid.text = requestor_id
    req.append(etree.Element("{%(sushi)s}Name" % NS))
    remail = etree.SubElement(req, "{%(sushi)s}Email" % NS)
    remail.text = requestor_email

    custref = etree.SubElement(rr, "{%(sushi)s}CustomerReference" % NS)
    cid = etree.SubElement(custref, "{%(sushi)s}ID" % NS)
    cid.text = customer_reference
    custref.append(etree.Element("{%(sushi)s}Name" % NS))

    repdef = etree.SubElement(rr, "{%(sushi)s}ReportDefinition" % NS,
                              Name=report, Release=str(release))
    filters = etree.SubElement(repdef, "{%(sushi)s}Filters" % NS)
    udr = etree.SubElement(filters, "{%(sushi)s}UsageDateRange" % NS)
    beg = etree.SubElement(udr, "{%(sushi)s}Begin" % NS)
    beg.text = start_date.strftime("%Y-%m-%d")
    end = etree.SubElement(udr, "{%(sushi)s}End" % NS)
    end.text = end_date.strftime("%Y-%m-%d")

    payload = etree.tostring(root, pretty_print=True,
                             xml_declaration=True, encoding="utf-8")

    headers = {"SOAPAction": '"SushiService:GetReportIn"',
               "Content-Type": "text/xml; charset=UTF-8",
               "Content-Length": len(payload)}

    response = requests.post(url=wsdl_url,
                             headers=headers,
                             data=payload,
                             verify=False)

    if sushi_dump:
        logger.debug("SUSHI DUMP: request: %s \n\n response: %s",
                     payload,
                     response.content)
    return response.content


def get_report(*args, **kwargs):
    """Get a usage report from a SUSHI server

    returns a :class:`pycounter.report.CounterReport` object.

    :param wsdl_url: URL to SOAP WSDL for this provider

    :param start_date: start date for report (must be first day of a month)

    :param end_date: end date for report (must be last day of a month)

    :param requestor_id: requestor ID as defined by SUSHI protocol

    :param requestor_email: requestor email address, if required by provider

    :param customer_reference: customer reference number as defined by SUSHI
        protocol

    :param report: report type, values defined by SUSHI protocol

    :param release: report release number (should generally be `4`.)

    :param sushi_dump: produces dump of XML to DEBUG logger

    """
    raw_report = get_sushi_stats_raw(*args, **kwargs)
    return _raw_to_full(raw_report)


def _ns(namespace, name):
    """Convenience function to make a namespaced XML name.

    :param namespace: one of 'SOAP-ENV', 'sushi', 'sushicounter', 'counter'
    :param name: tag name within the given namespace
    """
    return "{" + NS[namespace] + "}" + name


def _raw_to_full(raw_report):
    """Convert a raw report to a :class:`pycounter.report.CounterReport` object
    """
    try:
        root = etree.fromstring(raw_report)
    except etree.XMLSyntaxError as e:
        logger.error("XML syntax error: %s", raw_report)
        raise pycounter.exceptions.SushiException(e)
    oroot = objectify.fromstring(raw_report)
    rep = None
    try:
        rep = oroot.Body[_ns('sushicounter', "ReportResponse")]
        creport = rep.Report[_ns('counter', 'Report')]
    except AttributeError:
        try:
            creport = rep.Report[_ns('counter', 'Reports')].Report
        except AttributeError:
            logger.error("report not found in XML: %s", raw_report)
            raise
    logger.debug("COUNTER report: %s", etree.tostring(creport))
    startdate = datetime.datetime.strptime(
        root.find('.//%s' % _ns('sushi', 'Begin')).text,
        "%Y-%m-%d").date()

    enddate = datetime.datetime.strptime(
        root.find('.//%s' % _ns('sushi', 'End')).text,
        "%Y-%m-%d").date()

    report_data = {'period': (startdate, enddate)}

    rdef = root.find('.//%s' % _ns('sushi', 'ReportDefinition'))
    report_data['report_version'] = int(rdef.get('Release'))

    report_data['report_type'] = rdef.get('Name')

    customer = root.find('.//%s' % _ns('counter', 'Customer'))
    try:
        report_data['customer'] = (customer.find('.//%s' %
                                                 _ns('counter', 'Name')).text)
    except AttributeError:
        report_data['customer'] = ""

    inst_id = customer.find('.//%s' % _ns('counter', 'ID')).text
    report_data['institutional_identifier'] = inst_id

    reproot = root.find('.//%s' % _ns('counter', 'Report'))
    created_string = reproot.get('Created')
    if created_string is not None:
        report_data['date_run'] = dateutil.parser.parse(created_string)
    else:
        report_data['date_run'] = datetime.datetime.now()

    report = pycounter.report.CounterReport()

    for key, value in six.iteritems(report_data):
        setattr(report, key, value)

    report.metric = pycounter.report.METRICS.get(report_data['report_type'])

    for item in creport.Customer.ReportItems:
        try:
            publisher_name = item.ItemPublisher.text
        except AttributeError:
            publisher_name = ""

        itemline = [item.ItemName.text, publisher_name, item.ItemPlatform.text]

        eissn = issn = ""
        for identifier in item.ItemIdentifier:
            if identifier.Type == "Print_ISSN":
                issn = identifier.Value.text
                if issn is None:
                    issn = ""
            elif identifier.Type == "Online_ISSN":
                eissn = identifier.Value.text
                if eissn is None:
                    eissn = ""
        itemline.append(issn)
        itemline.append(eissn)
        month_data = []

        for perfitem in item.ItemPerformance:
            logger.debug("Perfitem date: %r",
                         convert_date_run(perfitem.Period.Begin.text))
            item_date = convert_date_run(
                perfitem.Period.Begin.text)
            usage = None
            for inst in perfitem.Instance:
                if inst.MetricType == "ft_total":
                    usage = str(inst.Count)
                    break
            if usage is not None:
                month_data.append((item_date, usage))
                itemline.append(usage)

        if report.report_type:
            if report.report_type.startswith('JR'):
                report.pubs.append(pycounter.report.CounterJournal(
                    line=itemline,
                    period=report.period,
                    metric=report.metric,
                    issn=issn,
                    eissn=eissn,
                    month_data=month_data
                ))
            elif report.report_type.startswith('BR'):
                report.pubs.append(
                    pycounter.report.CounterBook(itemline,
                                                 report.period,
                                                 report.metric))

    return report
