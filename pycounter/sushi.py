"""NISO SUSHI support"""
from __future__ import absolute_import

import pycounter.report
import six
import os.path
import requests
from lxml import etree

NS = {
    'SOAP-ENV': "http://schemas.xmlsoap.org/soap/envelope/",
    'ns1': "http://www.niso.org/schemas/sushi",
    'ns2': "http://www.niso.org/schemas/sushi/counter",
    }

def get_sushi_stats_raw(wsdl_url, start_date, end_date, requestor_id=None,
                        requestor_email=None, customer_reference=None,
                        report="JR1", release=4):
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

    """
    root = etree.Element("{%(SOAP-ENV)s}Envelope" % NS, nsmap=NS)
    body = etree.SubElement(root, "{%(SOAP-ENV)s}Body" % NS)
    rr = etree.SubElement(body, "{%(ns2)s}ReportRequest" % NS)

    req = etree.SubElement(rr, "{%(ns1)s}Requestor" % NS)
    rid = etree.SubElement(req, "{%(ns1)s}ID" % NS)
    rid.text = requestor_id
    req.append(etree.Element("{%(ns1)s}Name" % NS))
    remail = etree.SubElement(req, "{%(ns1)s}Email" % NS)
    remail.text = requestor_email

    custref = etree.SubElement(rr, "{%(ns1)s}CustomerReference" % NS)
    cid = etree.SubElement(custref, "{%(ns1)s}ID" % NS)
    cid.text = requestor_id
    custref.append(etree.Element("{%(ns1)s}Name" % NS))

    repdef = etree.SubElement(rr, "{%(ns1)s}ReportDefinition" % NS,
                              Name=report, Release=str(release))
    filters = etree.SubElement(repdef, "{%(ns1)s}Filters" % NS)
    udr = etree.SubElement(filters, "{%(ns1)s}UsageDateRange" % NS)
    beg = etree.SubElement(udr, "{%(ns1)s}Begin" % NS)
    beg.text = start_date.strftime("%Y-%m-%d")
    end = etree.SubElement(udr, "{%(ns1)s}End" % NS)
    end.text = end_date.strftime("%Y-%m-%d")

    payload = etree.tostring(root, xml_declaration=True, encoding="utf-8")
    headers = {"SOAPAction": '"SushiService:GetReportIn"',
               "Content-Type": "text/xml; charset=UTF-8",
               "Content-Length": len(payload)}

    response = requests.post(url=wsdl_url,
                             headers=headers,
                             data=payload,
                             verify=False)

    return response.content


def get_report(*args, **kwargs):
    """Get a usage report from a SUSHI server

    returns a pycounter.report.CounterReport object.
    """
    raw_report = get_sushi_stats_raw(*args, **kwargs)
    return _raw_to_full(raw_report)


def _raw_to_full(raw_report):
    """Convert a raw report to a pycounter.report.CounterReport object"""
    startdate = raw_report.ReportDefinition.Filters.UsageDateRange.Begin
    enddate = raw_report.ReportDefinition.Filters.UsageDateRange.End
    report_data = {}
    report_data['period'] = (startdate, enddate)

    report_data['report_version'] = raw_report.ReportDefinition._Release
    report_data['report_type'] = raw_report.ReportDefinition._Name

    report_data['customer'] = raw_report.Report.Report[0].Customer[0].Name
    inst_id = raw_report.Report.Report[0].Customer[0].ID
    report_data['institutional_identifier'] = inst_id

    report_data['date_run'] = raw_report.Report.Report[0]._Created.date()

    report = pycounter.report.CounterReport()

    for key, value in six.iteritems(report_data):
        setattr(report, key, value)

    report.metric = pycounter.report.METRICS.get(report_data['report_type'])

    for item in raw_report.Report.Report[0].Customer[0].ReportItems:
        itemline = []
        itemline.append(item.ItemName)
        itemline.append(item.ItemPublisher)
        itemline.append(item.ItemPlatform)

        eissn = issn = ""
        for identifier in item.ItemIdentifier:
            if identifier.Type == "Print_ISSN":
                issn = identifier.Value
            elif identifier.Type == "Online_ISSN":
                eissn = identifier.Value
        itemline.append(issn)
        itemline.append(eissn)

        for perfitem in item.ItemPerformance:
            usage = 0
            for inst in perfitem.Instance:
                if inst.MetricType == "ft_total":
                    usage = str(inst.Count)
                    break
            itemline.append(usage)
        if report.report_type:
            if report.report_type.startswith('JR'):
                report.pubs.append(pycounter.report.CounterPublication(
                    itemline,
                    report.period,
                    report.metric))
            elif report.report_type.startswith('BR'):
                report.pubs.append(
                    pycounter.report.CounterBook(itemline,
                                                 report.period,
                                                 report.metric))

    return report
