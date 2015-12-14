# mupd_reports

Scraping, parsing and re-publishing University of Missouri Police Department Incident Reports

## Intro

The University of Missour Police Department publishes data on it's website about their cases. They doing a great job keeping the data up-to-date, but there are a couple of problems:

1.	The [incident page](http://vco.missouri.edu/mupdcfs/) has filter options to find specific kinds of incidents within a date range and/or at a specific address, which is nice. But some of the less common charges, like making a terrotist threat, aren't categorized under an incident type. Furthermore, not all cases originate from an incident report, so you won't even find those cases on this list.

2.	The [daily clery reports](http://mupolice.missouri.edu/blotter/) include every cases and more information about each cases, including the exact charges and the current disposition of the case. But, the daily reports are [published as pdfs](http://mupolice.missouri.edu/blotter/November/111115.pdf), which prevents any searching or analysis.

We can do better. Here's how:
1.	Download the daily clery reports;
2.	Extract the text from the pdf pages;
3.	Parse that text into a database;
4.	Build a web app for users to interact with this improved data.

## Dependencies

*	[Python 2.7 +](https://www.python.org/ "Python 2.7"): An interpreted, object-oriented, high-level programming language;
*	[requests](http://docs.python-requests.org/en/latest/ "requests"): For handling HTTP request;
*	[html5lib](https://pypi.python.org/pypi/html5lib/1.0b3): For parsing HTML the same way any major browser would;
*	[beautifulsoup 4](http://www.crummy.com/software/BeautifulSoup/ "BeautifulSoup4"): For conveniently manipulating the parsed HTML.
