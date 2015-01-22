"""NISO SUSHI support"""
from __future__ import absolute_import

from suds.client import Client
from suds.xsd import doctor
import pycounter.report
import six
import os.path


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
    imp = doctor.Import("http://www.niso.org/schemas/sushi/counter",
                        'file://' +
                        os.path.dirname(__file__) +
                        '/schemas/counter_sushi4_1.xsd')
    doc = doctor.ImportDoctor(imp)

    client = Client(wsdl_url, doctor=doc)
    print client
    rdef = client.factory.create('ns1:ReportDefinition')

    rdef._Name = report
    rdef._Release = release
    rdef.Filters.UsageDateRange.Begin = start_date
    rdef.Filters.UsageDateRange.End = end_date

    cref = client.factory.create('ns1:CustomerReference')
    cref.ID = customer_reference

    reqr = client.factory.create('ns1:Requestor')
    reqr.ID = requestor_id
    if requestor_email is not None:
        reqr.Email = requestor_email

    report = client.service.GetReport(reqr, cref, rdef)

    return report


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
