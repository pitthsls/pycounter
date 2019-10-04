"""Constants used by pycounter."""

NS = {
    "SOAP-ENV": "http://schemas.xmlsoap.org/soap/envelope/",
    "sushi": "http://www.niso.org/schemas/sushi",
    "sushicounter": "http://www.niso.org/schemas/sushi/counter",
    "counter": "http://www.niso.org/schemas/counter",
}

METRICS = {
    "JR1": "FT Article Requests",
    "JR1 GOA": "Gold Open Access Article Requests",
    "BR1": "Book Title Requests",
    "BR2": "Book Section Requests",
    "DB1": [
        "Regular Searches",
        "Searches-federated and automated",
        "Result Clicks",
        "Record Views",
    ],
    "DB2": [
        "Access denied: concurrent/simultaneous user license exceeded",
        "Access denied: content item not licensed",
    ],
}

DB_METRIC_MAP = {
    "search_reg": METRICS["DB1"][0],
    "search_fed": METRICS["DB1"][1],
    "result_click": METRICS["DB1"][2],
    "record_view": METRICS["DB1"][3],
    "turnaway": METRICS["DB2"][0],
    "no_license": METRICS["DB2"][1],
}

CODES = {
    "Database": "DB",
    "Journal": "JR",
    "Book": "BR",
    "Title": "TR",
    "Platform": "PR",
    "Multimedia": "MR",
    "Consortium": "CR",
}

# from http://www.niso.org/workrooms/sushi/registry/
# Not all of these are actually supported by pycounter
REPORT_DESCRIPTIONS = {
    "BR1": "Number of Successful Title Requests by Month and Title",
    "BR2": "Number of Successful Section Requests by Month and Title",
    "BR3": "Access Denied to Content Items by Month, Title, and Category",
    "BR4": "Access Denied to Content Items by Month, Platform, and Category",
    "BR5": "Total Searches by Month and Title",
    "CR1": "Number of Successful Full-text Journal Article or Book Chapter "
    "Requests by Month",
    "CR2": "Total Searches by Month and Database",
    "CR3": "Number of Successful Multimedia Full Content Unit Requests "
    "by Month and Collection",
    "DB1": "Total Searches, Result Clicks and Record Views by Month and " "Database",
    "DB2": "Access Denied by Month, Database and Category",
    "JR1": "Number of Successful Full-Text Article Requests by Month and " "Journal",
    "JR1 GOA": "Number of Successful Gold Open Access Full-Text Article "
    "Requests by Month and Journal",
    "JR1a": "Number of Successful Full-Text Article Requests from an "
    "Archive by Month and Journal",
    "JR2": "Access Denied to Full Text Articles by Month, Journal, and " "Category",
    "JR3": "Number of Successful Item Requests and Turnaways by Month, "
    "Journal, and Page-Type",
    "JR3mobile": "Number of Successful Item Requests by Month, Journal, "
    "and Page-Type for usage on a mobile device",
    "JR4": "Total Searches Run by Month and Collection",
    "JR5": "Number of Successful Full-Text Article Requests by "
    "Year-of-Publication (YOP) and Journal",
    "MR1": "Number of Successful Multimedia Full Content Unit Requests "
    "by Month and Collection",
    "MR2": "Number of Successful Multimedia Full Content Unit Requests by "
    "Month, Collection, and Item Type",
    "PR1": "Total Searches, Result Clicks, and Record Views by Month and " "Platform",
    "TR1": "Number of Successful Requests for Journal Full-Text Articles "
    "and Book Sections by Month and Title",
    "TR1mobile": "Number of Successful Requests for Journal Full-Text "
    "Articles and Book Sections by Month and Title "
    "(formatted for normal browsers/delivered to mobile "
    "devices AND formatted for mobile devices/delivered "
    "to mobile devices)",
    "TR2": "Access Denied to Full-Text Items by Month, Title, and Category",
    "TR3": "Number of Successful Item Requests by Month, Title, and " "Page-Type",
    "TR3mobile": "Number of Successful Item Requests by Month, Title, "
    "and Page-Type (formatted for normal browsers/delivered "
    "to mobile devices and for mobile devices/delivered to "
    "mobile devices)",
    "TR_J1": 'Journal Requests (Excluding "OA_Gold")',
}

HEADER_FIELDS = {
    "JR1": (
        "Journal",
        "Publisher",
        "Platform",
        "Journal DOI",
        "Proprietary Identifier",
        "Print ISSN",
        "Online ISSN",
        "Reporting Period Total",
        "Reporting Period HTML",
        "Reporting Period PDF",
    ),
    "JR1 GOA": (
        "Journal",
        "Publisher",
        "Platform",
        "Journal DOI",
        "Proprietary Identifier",
        "Print ISSN",
        "Online ISSN",
        "Reporting Period Total",
        "Reporting Period HTML",
        "Reporting Period PDF",
    ),
    "JR2": (
        "Journal",
        "Publisher",
        "Platform",
        "Journal DOI",
        "Proprietary Identifier",
        "Print ISSN",
        "Online ISSN",
        "Access Denied Category",
        "Reporting Period Total",
    ),
    "JR3": (
        "Journal",
        "Publisher",
        "Platform",
        "Journal DOI",
        "Proprietary Identifier",
        "Print ISSN",
        "Online ISSN",
        "Reporting Period Total",
        "Reporting Period HTML",
        "Reporting Period PDF",
    ),
    "BR1": (
        "",
        "Publisher",
        "Platform",
        "Book DOI",
        "Proprietary Identifier",
        "ISBN",
        "ISSN",
        "Reporting Period Total",
    ),
    "BR2": (
        "",
        "Publisher",
        "Platform",
        "Book DOI",
        "Proprietary Identifier",
        "ISBN",
        "ISSN",
        "Reporting Period Total",
    ),
    "BR3": (
        "",
        "Publisher",
        "Platform",
        "Book DOI",
        "Proprietary Identifier",
        "ISBN",
        "ISSN",
        "Access Denied Category",
        "Reporting Period Total",
    ),
    "DB1": (
        "Database",
        "Publisher",
        "Platform",
        "User Activity",
        "Reporting Period Total",
    ),
    "DB2": (
        "Database",
        "Publisher",
        "Platform",
        "Access denied category",
        "Reporting Period Total",
    ),
    "PR1": ("Platform", "Publisher", "User Activity", "Reporting Period Total"),
    # FIXME: this is outputting counter 5 reports in 4 format for... reasons.
    "TR_J1": (
        "Journal",
        "Publisher",
        "Platform",
        "Journal DOI",
        "Proprietary Identifier",
        "Print ISSN",
        "Online ISSN",
        "Reporting Period Total",
        "Reporting Period HTML",
        "Reporting Period PDF",
    ),
}

TOTAL_TEXT = {
    "JR1": "Total for all journals",
    "JR2": "Total for all journals",
    "BR1": "Total for all titles",
    "BR2": "Total for all titles",
    "BR3": "Total for all titles",
    "DB2": "Total for all databases",
}
