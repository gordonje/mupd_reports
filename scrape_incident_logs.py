import requests
from bs4 import BeautifulSoup
from time import sleep
import os.path
import re

def extract_pdf_urls(url, html):
	""" Yields full urls of pdf reports.

	url -- url pointing to the page where the pdf_urls will be extracted (necessary for forming the full pdf_url)
	html -- html content from which the pdf_urls will be extracted	
	"""

	# create a Beautiful soup object from the response content, html5lib is the parser
	soup = BeautifulSoup(html, 'html5lib')

	# iterate over each "td" tag that has one of the two bgcolor values
	# note that sometimes (but not always) the bgcolor values include a leading '#', hence the use of regex
	for td in soup.find_all('td', attrs = {'bgcolor': re.compile(r"#?CAE1C1"), 'bgcolor': re.compile(r"#?F0FFC6")}):
		# try finding an "a" tag in the td, combine the provided url with the href attribute
		try:
			pdf_url = url + td.find("a")['href']
		except TypeError:
			# ignore if there's no "a" tag
			pass
		finally:
			# if there is, yield the full pdf_url to the array
			yield pdf_url


# url for the current year's reports
base_url = 'http://mupolice.missouri.edu/blotter/'

# set up an array for all the links to the pdfs
pdf_urls = []

# set up a requests session
with requests.session() as requests_session:

	# #### getting the current year's pdfs ####
	r = None
	# until we have a response...
	while r == None:
		# try requesting the initial page
		try:
			r = requests_session.get(base_url)
		except:
			print "Request failed."
			# if the request fails, reset the session before trying again
			requests_session = requests.session()
		finally:
			# iterate over the extracted pdf_urls
			for url in extract_pdf_urls(base_url, r.content):
				# append them to the global array
				pdf_urls.append(url)

	#### getting 2014's pdfs ####
	r = None
	# until we have a response...
	while r == None:
		# try requesting the initial page
		try:
			r = requests_session.get(base_url + 'archive/2014/')
		except:
			print "Request failed."
			# if the request fails, reset the session before trying again
			requests_session = requests.session()
		finally:
			# iterate over the extracted pdf_urls
			for url in extract_pdf_urls(base_url + 'archive/2014/', r.content):
				# append them to the global array
				pdf_urls.append(url)

	#### getting 2013's pdfs ####
	r = None
	# until we have a response...
	while r == None:
		# try requesting the initial page
		try:
			r = requests.get(base_url + 'archive/2013/')
		except:
			print "Request failed."
			# if the request fails, reset the session before trying again
			requests_session = requests.session()
		finally:
			# iterate over the extracted pdf_urls
			for url in extract_pdf_urls(base_url + 'archive/2013/', r.content):
				# append them to the global array
				pdf_urls.append(url)

# iterate over the array of pdf_urls
for pdf_url in pdf_urls:

	# split the pdf_url at '/' and take the last item, which is the date
	date = pdf_url.split('/')[-1]

	month = date[0:2]
	day = date[2:4]
	year = '20{}'.format(date[4:6])

	# store the files in the "pdf/" directory, name format "YYYY-MM-DD"
	file_name = 'pdfs/{0}-{1}-{2}.pdf'.format(year, month, day)

	# check to see if we've already downloaded the file
	if not os.path.isfile(file_name): 

		print '   Downloading to {}'.format(file_name)

		# pause three seconds between making requests
		sleep(3)

		r = None
		# until we have a response...
		while r == None:
			# try requesting the pdf
			try:
				r = requests.get(pdf_url)
			except:
				print "Request failed."
				# if the request fails, reset the session before trying again
				requests_session = requests.session()
			finally:
				# open the file...
				with open(file_name, 'w') as f:
					# write the contents of the file ()
					f.write(r.content)

print 'fin.'
		