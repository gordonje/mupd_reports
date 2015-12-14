import requests
from bs4 import BeautifulSoup
from time import sleep

# base url and initial page
base_url = 'http://mupolice.missouri.edu/blotter/'

# set up a requests session
with requests.session() as requests_session:

	r = None
	# until we have a response...
	while r == None:
		# try requesting the initial page
		try:
			r = requests.get(base_url)
		except:
			print "Request failed."
			# if the request fails, reset the session before trying again
			requests = requests.session()

	# create a Beautiful soup object from the response content, html5lib is the parser
	soup = BeautifulSoup(r.content, 'html5lib')

	# set up an array for all the links to the pdfs
	pdf_urls = []

	# iterate over each "font" tag in the soup with specified attributes
	for font_tag in soup.find_all('font', attrs = {'face': "Arial", 'size':"-2"}):
		# try finding an "a" tag in the font_tag, and tag's the href attribute with the base_url
		try:
			pdf_url = base_url + font_tag.find("a")['href']
		except TypeError:
			# ignore if there's no "a" tag
			pass
		finally:
			# if there is, append the full pdf_url to the arrary
			pdf_urls.append(pdf_url)

	# iterate over the array of pdf_urls
	for pdf_url in pdf_urls:

		print pdf_url
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
				requests = requests.session()

		print r

		# split the pdf_url at '/' and take the last item, which is the date
		date = pdf_url.split('/')[-1]

		month = date[0:2]
		day = date[2:4]
		year = '20{}'.format(date[4:6])

		# store the files in the "pdf/" directory, name format "YYYY-MM-DD"
		file_name = 'pdfs/{0}-{1}-{2}.pdf'.format(year, month, day)
		
		with open(file_name, 'w') as f:
			f.write(r.content)
		