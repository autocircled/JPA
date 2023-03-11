from urllib.request import urlopen, Request
from urllib.error import HTTPError
# pip install beautifulsoup4
from bs4 import BeautifulSoup as soup
from pathlib import Path
import json
import time
# pip install python-dateutil --user
import dateutil.parser
import random
from random import seed
from random import choice
from datetime import datetime, timedelta
import os
import io
import sys
from wp import Custom_WP_XMLRPC
from indexing import Instant_Indexing
# install below command to solve SSL error
# pip install pyopenssl ndg-httpsclient pyasn1 urllib3

# get redirected URL from LinkedIn
import re
from urllib.parse import unquote

# to create a backup of progress.txt
import shutil

def check_my_ip():
	# needtochange
	proxy = "http://username:password@proxy:port/"
	if proxy != None:
		script_host = 'Proxy Server IP: '
		os.environ['http_proxy'] = proxy 
		os.environ['HTTP_PROXY'] = proxy
		os.environ['https_proxy'] = proxy
		os.environ['HTTPS_PROXY'] = proxy
	else:
		script_host = 'Local PC IP: '

	# print current IP
	external_ip = urlopen('https://ipv4.webshare.io/').read().decode('utf8')
	print(script_host + external_ip)

seed(1)
suffle_mins = [(i+7) for i in range(10)]
# needtochange
domain = 'example.com'
# user input
def entrance( argv = None ):
    Label = """
    Step 1: Select the appropiate country code from below list
    ---------- \t---------------------- \t----------------
    Codes \tCountries \t\tDomains
    ---------- \t---------------------- \t----------------
    au  \t=> Australia \t\t> au.domainname
    be  \t=> Belgium \t\t> be.domainname
    br  \t=> Brazil \t\t> br.domainname
    ca  \t=> Canada \t\t> ca.domainname
    ch  \t=> Switzerland \t\t> ch.domainname
    co  \t=> Colombia \t\t> co.domainname
    de  \t=> Germany \t\t> de.domainname
    es  \t=> Spain \t\t> es.domainname
    fr  \t=> France \t\t> fr.domainname
    in  \t=> India \t\t> in.domainname
    it  \t=> Italy \t\t> it.domainname
    mx  \t=> Mexico \t\t> mx.domainname
    nl  \t=> Netherlands \t\t> nl.domainname
    ph  \t=> Philippines \t\t> ph.domainname
    pl  \t=> Poland \t\t> pl.domainname
    se  \t=> Sweden \t\t> se.domainname
    sg  \t=> Singapore \t\t> sg.domainname
    us1 \t=> United States (US) \t> usa-jobs.domainname
    us \t\t=> United States (US) \t> domainname
    uk  \t=> United Kingdom (UK) \t> uk.domainname
    """.replace("domainname", str(domain))
    
    keys = {
        'be' : {
            'site'              : 'https://be.'+ str(domain) +'/',
        },
        'br' : {
            'site'              : 'https://br.'+ str(domain) +'/',
        },
        'ca' : {
            'site'              : 'https://ca.'+ str(domain) +'/',
        },
        'ch' : {
            'site'              : 'https://ch.'+ str(domain) +'/',
        },
        'co' : {
            'site'              : 'https://co.'+ str(domain) +'/',
        },
        'de' : {
            'site'              : 'https://de.'+ str(domain) +'/',
        },
        'es' : {
            'site'              : 'https://es.'+ str(domain) +'/',
        },
        'fr' : {
            'site'              : 'https://fr.'+ str(domain) +'/',
        },
        'it' : {
            'site'              : 'https://it.'+ str(domain) +'/',
        },
        'nl' : {
            'site'              : 'https://nl.'+ str(domain) +'/',
        },
        'ph' : {
            'site'              : 'https://ph.'+ str(domain) +'/',
        },
        'pl' : {
            'site'              : 'https://pl.'+ str(domain) +'/',
        },
        'se' : {
            'site'              : 'https://se.'+ str(domain) +'/',
        },
        'sg' : {
            'site'              : 'https://sg.'+ str(domain) +'/',
        },
        'us' : {
            'site'              : 'https://'+ str(domain) +'/',
        },
        'us1' : {
            'site'              : 'https://usa-jobs.'+ str(domain) +'/',
        },
        'uk' : {
            'site'              : 'https://uk.'+ str(domain) +'/',
        }
    }

    site = input(Label)

    if site in keys:
        print("\tYou have selected ", keys[site]['site'])
        return keys[site]['site']
    else:
        print("\tYou have selected ", "Nothing")
        return None

# upload jobs
def upload( site_link ):
	raw_file = "append.xml"
	read_file = open(raw_file, 'r', encoding="utf8")
	copied_all_text = read_file.read()

	# Now write all the job items into another file
	with open("ready-for-automation.xml", "w", encoding="utf-8") as new_file:
		new_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		new_file.write('<jobs>\n')
		new_file.write("%s" % (copied_all_text))
		new_file.write('</jobs>')
		new_file.close()

	# Now start the automation
	ready_for_upload = 'ready-for-automation.xml'
	xmlUrl = site_link + 'xmlrpc.php'
	obj = Custom_WP_XMLRPC()
	with open(ready_for_upload, "r", encoding="utf8") as f:
		contents = f.read()
		data = soup(contents, "xml")

		items = data.findAll("item")

		if( len(items) > 0 ):
			for item in items:
				title = item.title.text
				# pubDate = item.pubDate.text
				wp_post_date = item.wp_post_date.text
				content_encoded = item.content_encoded.text
				excerpt_encoded = item.excerpt_encoded.text
				wp_post_name = item.wp_post_name.text
				wp_post_status = item.wp_status.text
				# wp_post_type = item.wp_post_type.text
				categories = item.find_all("category")
				company = []
				all_locations = []
				job_natures = []
				job_industries = []
				job_type = []
				job_location_type = []
				for category in categories:
					if category.get('domain') == 'company':
						company.append(category.get('nicename'))
					
					if category.get('domain') == 'location':
						all_locations.append(category.get('nicename'))
					
					if category.get('domain') == 'job_nature':
						job_natures.append(category.get('nicename'))
					
					if category.get('domain') == 'job_industry':
						job_industries.append(category.get('nicename'))
					
					if category.get('domain') == 'job_type':
						job_type.append(category.get('nicename'))

					if category.get('domain') == 'job_location_type':
						job_location_type.append(category.get('nicename'))

					# pprint(category.get('domain') == 'location')
					# pprint(type(category))


				wp_postmetas = item.find_all("wp_postmeta")
				post_meta = []
				for wp_postmeta in wp_postmetas:
					post_meta.append({'key':wp_postmeta.wp_meta_key.text, 'value':wp_postmeta.wp_meta_value.text})
				
				# pprint(post_meta)

				jobExcerpt = excerpt_encoded
				jobDescription = content_encoded
				# needtochange
				wp_n = 'username'
				wp_p = 'password'
				post_id = obj.post_article( xmlUrl, wp_n, wp_p, title, wp_post_name, wp_post_date, jobExcerpt, jobDescription, wp_post_status, company, all_locations, job_natures, job_industries, job_type, job_location_type, post_meta )
				# print(post_id)
				if post_id != None:
					instant_indexing( site_link, post_id )
				# clean files
				open(raw_file, 'w').close()
				open(ready_for_upload, 'w').close()


def instant_indexing( site_link, post_id ):
	indexing = Instant_Indexing()
	indexing.indexURL( str(site_link) + '?p=' + str(post_id) )

# open HTTP connection
def openConnection(url):
	import ssl
	# This restores the same behavior as before.
	context = ssl._create_unverified_context()

	time.sleep(0.3)
	# open connection and grabbing the page
	request = Request(url)
	request.add_header('User-agent', 'saccah 0.1')

	# with urlopen(url) as uClient:

	with urlopen(request, context=context) as uClient:
		# print(uClient.status)
		page_html = uClient.read()
		uClient.close()
	return page_html


def scrap(url, automation ):
	error_count = 0
	# global random_mins
	# random_mins += choice(suffle_mins)
	now = datetime.now() + timedelta(hours= -6)
	# now =  datetime.now() + timedelta(hours= -6, minutes=random_mins)

	try:
		page_html = openConnection(url)

	
		# html parsing
		page_soup = soup(page_html, "html.parser")

		# job container
		job_container = page_soup.find('section', attrs = {'class':'core-rail'})

		# Job informations
		#Title
		title = job_container.h1.text

		#link
		link = url
		link_found = 'no'
		link_source = job_container.findAll("a", class_='apply-button apply-button--link', attrs={'data-tracking-control-name':'public_jobs_apply-link-offsite'})
		# print(link_source)
		# print(len(link_source))
		if len(link_source) > 0:
			# print("Link found")
			link_found = 'yes'
			raw_link = link_source[0].get('href')
			filter_link = re.findall('url=\s*([a-zA-Z0-9%-]+)', raw_link)
			if not filter_link[0]:
				error_count = 1
			else:
				link = unquote(filter_link[0])
			
		else:
			print("Link not found")
		
		
		# Company
		company_container = job_container.find('a', attrs = {'class':'topcard__org-name-link'})
		if company_container == None:
			company_container = job_container.find('span', attrs={'class':'topcard__flavor'})

		company = company_container.text.strip()

		# Location
		span_list = page_soup.findAll('span', attrs = {'class':'topcard__flavor'})
		locations = span_list[1].text.split(",")

		# Contents
		# Container
		content_container = page_soup.find('section', attrs = {'class':'description'})

		# description container
		description_container = content_container.find('div', attrs = {'class':'show-more-less-html__markup'})
		description_container = str(description_container).lstrip('<div class="show-more-less-html__markup show-more-less-html__markup--clamp-after-5">')
		description_container = description_container.rstrip('</div>')
		
		# Job Description
		# description = description_container.p.text

		#Job Excerpt
		excerpt_container = description_container.replace('<p>', '')
		excerpt_container = excerpt_container.replace('</p>', ' ')
		excerpt_container = excerpt_container.replace('<em>', '')
		excerpt_container = excerpt_container.replace('<u>', '')
		excerpt_container = excerpt_container.replace('</u>', '')
		excerpt_container = excerpt_container.replace('<i>', '')
		excerpt_container = excerpt_container.replace('</i>', '')
		excerpt_container = excerpt_container.replace('<b>', '')
		excerpt_container = excerpt_container.replace('</b>', '')
		excerpt_container = excerpt_container.replace('</em>', '')
		excerpt_container = excerpt_container.replace('<strong>', '')
		excerpt_container = excerpt_container.replace('</strong>', '')
		excerpt_container = excerpt_container.replace('<span>', '')
		excerpt_container = excerpt_container.replace('</span>', '')
		excerpt_container = excerpt_container.replace('<br/>', ' ')
		excerpt_container = excerpt_container.replace('<ul>', '')
		excerpt_container = excerpt_container.replace('</ul>', '')
		excerpt_container = excerpt_container.replace('<ol>', '')
		excerpt_container = excerpt_container.replace('</ol>', '')
		excerpt_container = excerpt_container.replace('<li>', '')
		excerpt_container = excerpt_container.replace('</li>', ' ')
		excerpt_container = excerpt_container.replace('\n', ' ')
		excerpt_container = excerpt_container.replace('\r', ' ')
		excerpt_container = excerpt_container.replace('\t', ' ')
		excerpt_container = excerpt_container.lstrip()
		excerpt_container = excerpt_container[0:120]
		excerpt_container = excerpt_container + '...See this and similar jobs on ' + str(domain)

		# Job criteria container
		criteria_container = content_container.find('ul', attrs = {'class':'description__job-criteria-list'})			
		# print(criteria_container)
		# exit
		seniority = ''
		job_type = ''
		job_functions_container = []
		job_industies_container = []
		
		#								  ['English', 			'Filipino', 			'Switzerland', 				'Sweden',			'Spanish-columbia-spain',	'Brazil',				'Netherlands',			'Poland',				'Italiano', 			'french' ]
		probable_seniority_headings 	= ['Seniority level', 	'Antas ng seniority', 	'Karrierestufe', 			'Yrkesnivå',		'Nivel de antigüedad',		'Nível de experiência',	'Senioriteitsniveau',	'Poziom w hierarchii',	'Livello di anzianità', 'Niveau hiérarchique' ]
		probable_job_type_headings 		= ['Employment type', 	'Uri ng trabaho', 		'Beschäftigungsverhältnis', 'Anställningstyp',	'Tipo de empleo', 			'Tipo de emprego',		'Soort baan',			'Forma zatrudnienia',	'Tipo di impiego', 		'Type d’emploi' ]
		probable_job_function_headings 	= ['Job function', 		'Function sa trabaho', 	'Tätigkeitsbereich', 		'Befattning',		'Función laboral',			'Função',				'Functie',				'Funkcja',				'Funzione lavorativa',	'Fonction' ]
		probable_job_industry_headings 	= ['Industries', 		'Mga Industriya', 		'Branchen', 				'Branscher',		'Sectores',					'Setores',				'Bedrijfstakken',		'Branże',				'Settori',				'Secteurs' ]
		try:
			all_criterias = criteria_container.findAll('li')
			for criteria in all_criterias:
				criteria_heading = criteria.find('h3').text.strip()
				if criteria_heading in probable_seniority_headings:
					seniority = criteria.span.text
				elif criteria_heading in probable_job_type_headings:
					job_type = criteria.span.text
				elif criteria_heading in probable_job_function_headings:
					job_functions_container = criteria.span.text
				elif criteria_heading in probable_job_industry_headings:
					job_industies_container = criteria.span.text
		except:
			print("problem in job criteria")
				
			
		seniority = seniority.strip()
		job_type = job_type.strip()
		if not job_functions_container:
			job_functions = job_functions_container
		else:
			job_functions = job_functions_container.strip().split(',')
		
		if not job_industies_container:
			job_industies = job_industies_container
		else:
			job_industies = job_industies_container.strip().split(',')

		# get json data
		try:
			json_data = "".join(page_soup.find('script', {'type':'application/ld+json'}).contents)
			j = json.loads(json_data)
		except:
			error_count = 2
			print("JSON data not found")
	except HTTPError as err:
		error_count = 1
		print(err)
		if str(err) == "HTTP Error 429: Request denied":
			print("Waiting for 4 secs")
			time.sleep(10)

	if error_count < 1:
		# random_mins minutes after published all posts
		# modified_dateposted = now + timedelta( minutes = random_mins )
		modified_dateposted = now + timedelta(minutes=-(30 + choice(suffle_mins)))
		future_time = modified_dateposted.strftime('%Y-%m-%d %H:%M:%S+00:00')
		j['datePosted'] = str(future_time)
		d = dateutil.parser.parse(j['validThrough'])
		
		# new formatted date
		dl = d.strftime('%Y%m%d') # deadline of job
		st = modified_dateposted.strftime("%Y-%m-%d %H:%M:%S")
		ft = modified_dateposted.strftime('%A, %d %b %Y %H:%M:%S')
		rt = modified_dateposted.strftime('%Y%m%d-%H%M%S')
		ct = now.strftime('%Y%m%d') # Current year/month/day
		
		# check if deadline is over
		if ct > dl :
			print('Deadline is over!!!!!!!!!!!!')
			exit() # exit script execution

		# open file for writing
		filename = Path("append.xml")
		with io.open(filename, "a+", encoding="utf-8") as f:

			# writing job info
			f.write("<item>\r")
			f.write("\t<title>%s</title>\r" % (title) )
			f.write("\t<pubDate>%s</pubDate>\r" % (ft) )
			f.write("\t<!--[[%s]]-->\r" % ( url ))

			# company
			f.write("\t<category domain=\"company\" nicename=\"%s\"><![CDATA[%s]]></category>\r" % (company, company) )

			# locations as location
			for location in locations:
				location = location.strip()
				f.write("\t<category domain=\"location\" nicename=\"%s\"><![CDATA[%s]]></category>\r" % (location, location) )

			# job_functions
			# count = 0
			substring = ''
			if 'ph.linkedin' in url:
				substring = 'at'
			elif 'ch.linkedin' in url:
				substring = 'und'
			elif 'de.linkedin' in url:
				substring = 'und'
			elif 'se.linkedin' in url:
				substring = 'och'
			elif 'co.linkedin' in url:
				substring = 'y'
			elif 'es.linkedin' in url:
				substring = 'y'
			elif 'mx.linkedin' in url:
				substring = 'y'
			elif 'br.linkedin' in url:
				substring = 'e'
			elif 'nl.linkedin' in url:
				substring = 'en'
			elif 'pl.linkedin' in url:
				substring = 'i'
			elif 'fr.linkedin' in url:
				substring = 'et'
			else:
				substring = 'and'
			
			for job_function in job_functions:
				job_function = job_function.strip()

				if substring in job_function:
					if job_function.index(substring) == 0:
						job_function = job_function.replace( substring + ' ', '' )
				f.write("\t<category domain=\"job_nature\" nicename=\"%s\"><![CDATA[%s]]></category>\r" % (job_function, job_function) )

			# job_industies
			for job_industry in job_industies:
				job_industry = job_industry.strip()

				if substring in job_industry:
					if job_industry.index(substring) == 0:
						job_industry = job_industry.replace( substring + ' ', '' )
				f.write("\t<category domain=\"job_industry\" nicename=\"%s\"><![CDATA[%s]]></category>\r" % (job_industry, job_industry) )

			# Job Type
			FULL_TIME  = [ 'Full-time', 'Fulltime', 'Vollzeit', 'Heltid', 'Jornada completa', 'Tempo integral', 'Pełny etat', 'A tempo pieno', 'Temps plein'  ]
			PART_TIME  = [ 'Part-time', 'Teilzeit', 'Deltid', 'Media jornada', 'Meio período', 'Parttime', 'Niepełny etat', 'Part-time', 'Temps partiel' ]
			CONTRACTOR = [ 'Contract', 'Befristete Beschäftigung', 'Kontrakt', 'Contrato por obra', 'Contrato', 'Zlecenie', 'Contratto', 'CDD ou mission ponctuelle' ]
			TEMPORARY  = [ 'Temporary', 'Zeitarbeit', 'Tillfälligt', 'Temporal', 'Temporário', 'Tijdelijk', 'Praca tymczasowa', 'Temporaneo', 'Travail temporaire' ]
			VOLUNTEER  = [ 'Volunteer', 'Volontär', 'Voluntario', 'Voluntário', 'Vrijwilliger', 'Wolontariusz', 'Volontario', 'Bénévole' ]
			INTERN     = [ 'Intern', 'Internship', 'Praktikum', 'Praktikplats', 'Prácticas', 'Estágio', 'Stageplek', 'Staż', 'Stage', 'Stagiaire / Alternant' ]

			if job_type in FULL_TIME:
				job_type_value = 'FULL_TIME'
			elif job_type in PART_TIME:
				job_type_value = 'PART_TIME'
			elif job_type in CONTRACTOR:
				job_type_value = 'CONTRACTOR'
			elif job_type in TEMPORARY:
				job_type_value = 'TEMPORARY'
			elif job_type in INTERN:
				job_type_value = 'INTERN'
			elif job_type in VOLUNTEER:
				job_type_value = 'VOLUNTEER'
			else:
				job_type_value = 'OTHER'
			f.write("\t<category domain=\"job_type\" nicename=\"%s\"><![CDATA[%s]]></category>\r" % (job_type_value, job_type_value) )
			
			# JobLocationType : TELECOMMUTE
			if j.get('jobLocationType'):
				f.write("\t<category domain=\"job_location_type\" nicename=\"%s\"><![CDATA[%s]]></category>\r" % (j['jobLocationType'], j['jobLocationType']) )

			if automation:
				f.write("\t<wp_post_date><![CDATA[%s]]></wp_post_date>\r" % (st) )
				f.write("\t<content_encoded><![CDATA[%s]]></content_encoded>\r" % (description_container) )
				f.write("\t<excerpt_encoded><![CDATA[%s]]></excerpt_encoded>\r" % (excerpt_container) )
				f.write("\t<wp_post_name><![CDATA[%s - %s - f]]></wp_post_name>\r" % (title, rt))
				f.write("\t<wp_status><![CDATA[future]]></wp_status>\r")
				f.write("\t<wp_post_type><![CDATA[jobs]]></wp_post_type>\r")

				# JSON DATA
				f.write("\t<wp_postmeta>\r\t\t<wp_meta_key><![CDATA[json_from_linkedin]]></wp_meta_key>\r\t\t<wp_meta_value><![CDATA[<script type=\"application/ld+json\">%s</script>]]></wp_meta_value>\r\t</wp_postmeta>\r" % (json.dumps(j)) )
				
				# Deadline 
				f.write("\t<wp_postmeta>\r\t\t<wp_meta_key><![CDATA[deadline_job]]></wp_meta_key>\r\t\t<wp_meta_value><![CDATA[%s]]></wp_meta_value>\r\t</wp_postmeta>\r" % (dl))
				
				if link_found == 'yes':
					f.write("\t<wp_postmeta>\r\t\t<wp_meta_key><![CDATA[platform]]></wp_meta_key>\r\t\t<wp_meta_value><![CDATA[other]]></wp_meta_value>\r\t</wp_postmeta>\r")
				else:
					f.write("\t<wp_postmeta>\r\t\t<wp_meta_key><![CDATA[platform]]></wp_meta_key>\r\t\t<wp_meta_value><![CDATA[linkedin]]></wp_meta_value>\r\t</wp_postmeta>\r")
				
										
					
				# Apply Now
				f.write("\t<wp_postmeta>\r\t\t<wp_meta_key><![CDATA[apply_now]]></wp_meta_key>\r\t\t<wp_meta_value><![CDATA[%s]]></wp_meta_value>\r\t</wp_postmeta>\r" % (link))
			else:
				f.write("\t<wp:post_date><![CDATA[%s]]></wp:post_date>\r" % (st) )
				f.write("\t<content:encoded><![CDATA[%s]]></content:encoded>\r" % (description_container) )
				f.write("\t<excerpt:encoded><![CDATA[%s]]></excerpt:encoded>\r" % (excerpt_container) )
				f.write("\t<wp:post_name><![CDATA[%s - %s - f]]></wp:post_name>\r" % (title, rt))
				f.write("\t<wp:status><![CDATA[future]]></wp:status>\r")
				f.write("\t<wp:post_type><![CDATA[jobs]]></wp:post_type>\r")

				# JSON DATA
				f.write("\t<wp:postmeta>\r\t\t<wp:meta_key><![CDATA[json_from_linkedin]]></wp:meta_key>\r\t\t<wp:meta_value><![CDATA[<script type=\"application/ld+json\">%s</script>]]></wp:meta_value>\r\t</wp:postmeta>\r" % (json.dumps(j)) )
				
				# Deadline 
				f.write("\t<wp:postmeta>\r\t\t<wp:meta_key><![CDATA[deadline_job]]></wp:meta_key>\r\t\t<wp:meta_value><![CDATA[%s]]></wp:meta_value>\r\t</wp:postmeta>\r" % (dl))
				
				if link_found == 'yes':
					f.write("\t<wp:postmeta>\r\t\t<wp:meta_key><![CDATA[platform]]></wp:meta_key>\r\t\t<wp:meta_value><![CDATA[other]]></wp:meta_value>\r\t</wp:postmeta>\r")
				else:
					f.write("\t<wp:postmeta>\r\t\t<wp:meta_key><![CDATA[platform]]></wp:meta_key>\r\t\t<wp:meta_value><![CDATA[linkedin]]></wp:meta_value>\r\t</wp:postmeta>\r")
				
										
					
				# Apply Now
				f.write("\t<wp:postmeta>\r\t\t<wp:meta_key><![CDATA[apply_now]]></wp:meta_key>\r\t\t<wp:meta_value><![CDATA[%s]]></wp:meta_value>\r\t</wp:postmeta>\r" % (link))

			f.write("</item>\r")
		
			f.close()

	return error_count


def main( args ):
	if '-start' in args:

		# check my IP Address
		check_my_ip()
		whois_site = entrance()
		links = []
		progress_path = Path("progress.txt")
		# progress_failed_path = Path("progress-failed.txt")

		progress_bkp_path = Path("progress-bkp.txt")
		shutil.copyfile(progress_path, progress_bkp_path)

		ready_links = []
		with open(progress_path, 'r') as links:
			#URLs = opp.readlines()
			for link in links:
				currentPlace = link[:-1]
				ready_links.append(currentPlace)
		total_link = len(ready_links)
		valid = 0
		while len(ready_links) > 0:

			# print linkedin job link
			print(ready_links[len(ready_links)-1])
			if '-a' in args:
				result = scrap(ready_links[len(ready_links)-1], automation = True )
			else:
				result = scrap(ready_links[len(ready_links)-1], automation = False )

			if result == 0:

				# upload jobs
				upload( whois_site )
				valid = valid + 1
				ready_links.pop(len(ready_links)-1)
			elif result == 2:
				ready_links.pop(len(ready_links)-1)

			print(str(valid) + ' of ' + str(len(ready_links)-1) + ' of ' + str(total_link))
			
			with io.open(progress_path, "w", encoding="utf-8") as dff1:
				for link in ready_links:
					dff1.write("%s\n" % (link))
				dff1.close()
	else:
		print("Nothing to do here. See readme file to learn how to use this repl.")

if __name__ == "__main__":

    #calling the main function
    main(sys.argv)