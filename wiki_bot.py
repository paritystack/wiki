#!/usr/bin/python
# -*- coding: utf-8  -*-

#import Transliterate
import wikipedia # Import the wikipedia module
import re
import pagegenerators
import catlib
import codecs
import sqlite3

info_box_dict = {}
page_to_add = []
current_page = u''
data = u''
conn = ''
curs = ''
lang_code = 3
def getInfobox(film):
	info_box_data = []
	if type(film).__name__ == 'str' or type(film).__name__ == 'unicode':
		site = wikipedia.getSite('en','wikipedia') # Taking the default site
		page = wikipedia.Page(site, film) # Calling the constructor
		if page.isRedirectPage():
			page = page.getRedirectTarget()	
	else:
		page = film
	page_data = page.get()
	#print page_data
	page_data = page_data.split(u'\n')
	info_box = 0
	#remove the |
	r = re.compile(r'^\s*\|\s*',re.UNICODE)

	info_re = re.compile(r'\s*{{\s*Infobox\s*film\s*',re.IGNORECASE|re.UNICODE)
	#remove spaces
	r1 = re.compile(r'\s*=\s*',re.UNICODE)
	#remove comments
	#r2 = re.compile(r'<!--.*-->')


	#Get the info box data
	for line in page_data:
		if len(line) == 0:
			continue
		if info_re.search(line) and info_box == 0:
			print 'Found infobox'
			info_box = 1
		elif line == u'}}' or line == u'|}}' and info_box ==1:
			info_box = 0
			break
		elif info_box == 1:
		#remove unnecessary data
			line = r.sub('',line)
			#line = r2.sub('',line) 
			line = r1.sub('=',line)
			print line
			info_box_data.append(line)
		else:
			pass

	#update in dictionary 
	for i in info_box_data:
		info_box_dict[i.split(u'=',1)[0].strip()] = i.split(u'=',1)[1].strip()
			
	#print info_box_data
	#print info_box_dict
	wikipedia.stopme()

	
def getInterwiki(input_page,lang = 'ml',string = True):
	#print type(input_page)
	#print (input_page)

	r = re.compile(r'\[\[ml:(.*)\]\]',re.UNICODE)
	site = wikipedia.getSite('en','wikipedia') # Taking the default site
	try:
		if string:
			page = wikipedia.Page(site, input_page) # Calling the constructor
		else:
			page = input_page
		if page.isRedirectPage():
			page = page.getRedirectTarget()
	except NoPage:
		print 'getInterwiki: No Page to open'
		pass
	for i in page.interwiki():
		#print i.aslink()
		m = r.search(i.aslink())
		if m:
			iwiki = m.group(1)
			#print iwiki
			return iwiki

#for url = 0 the function returns the url links of the page,if 1 it returns the name.
def getMyLinks(stringdata,url=0):
	links = []
	r = re.compile(r'\[\[(.*?)\]\]',re.UNICODE)
	for i in r.findall(stringdata):
		try:
			i = i.split(u'|')[url]
		except IndexError:
			i = i.split(u'|')[0]
		i = i.strip()
		links.append(i)
	return links

def updateFilmDetails():
	global data
	if info_box_dict.has_key('name'):
		data+= u'\n\'\'\'\'\''
		data+=info_box_dict['name']
		data+=u'\'\'\'\'\' '
	if info_box_dict.has_key('director'):	
		data+=getMyLinks(info_box_dict['director'],1)[0]
		data+=u' സംവിധാനം നിര്‍വഹിച്ച് '
	if info_box_dict.has_key('released'):			
		data+=info_box_dict['released']
		data+=u'പുറത്തിറങ്ങിയ '
	if info_box_dict.has_key('language'):			
		data+=info_box_dict['language']
	data+=u'ചലച്ചിത്രമാണ്.'		

def updateInfobox():
	global data
	data+=u'{{Infobox Film\n'
	for i,j in info_box_dict.iteritems():
		data+=u'| '
		data+=i
		data+=u'='
		data+=j
		data+=u'\n'
	data+=u'''}}'''		
def updateActortable():
	global data
	data+=u'''
== അഭിനേതാക്കൾ ==
{| class="wikitable"
|-
! അഭിനേതാവ് !! കഥാപാത്രം
|-
'''
	for i in getMyLinks(info_box_dict['starring'],1):
		data+=u'|'
		data+=i
		data+=u'||\n'
		data+=u'|-\n'
	data+=u'''|}'''

def updateIwikis():
	global data
	site = wikipedia.getSite('en','wikipedia')
	page = wikipedia.Page(site,current_page)
	data+=u'[['
	data+=u'en:'
	data+=current_page
	data+=u']]'
	for i in page.interwiki():
		data+=i

def update_music():
	global data
	temp = data
	data+=u'''	
== സംഗീതം ==
'''

	if info_box_dict.has_key('music') and info_box_dict.has_key('lyrics'):
		data+=u'ഇതിലെ ഗാനങ്ങൾ രചിച്ചത് '
		data+=info_box_dict['lyrics']
		data+=u' ആണ്.ഈണം പകർന്നിരുന്നത്  '
		data+=info_box_dict['music']
		data+=u' ആണ്.'
	elif info_box_dict.has_key('music'):
		data+=u'ഇതിലെ ഗാനങ്ങൾക്ക് ഈണം പകർന്നിരുന്നത് '
		data+=info_box_dict['music']
		data+=u' ആണ്.'
	elif info_box_dict.has_key('lyrics'):
		data+=u'ഇതിലെ ഗാനങ്ങൾ രചിച്ചത്  '
		data+=info_box_dict['lyrics']
		data+=u' ആണ്.'
	else:
		data = temp


def update_aniyara():
	global data
	flag = False
	temp = data
	data+=u'''

== അണിയറ പ്രവർത്തകർ ==
{| class="wikitable"
|-
! അണിയറപ്രവർത്തനം !! നിർ‌വ്വഹിച്ചത്
|-
'''
	if info_box_dict.has_key('cinematography'):
		flag = True
		data+=u'''
| ഛായാഗ്രഹണം || '''
		data+=info_box_dict['cinematography']
		data+=u'\n|-'
	elif info_box_dict.has_key('editing'):
		flag = True
		data+=u'''
| ചിത്രസം‌യോജനം || '''
		data+=info_box_dict['editing']
		data+=u'\n|-'

	if flag == True:
		data+=u'\n|}'
	else:
		data = temp



def update_others():
	global data
	data+=u'''

== അവലംബം ==
<references />

== പുറത്തേക്കുള്ള കണ്ണികൾ ==

{{film-stub}}

'''
			
def udate2wiki(pagename=u'',towiki=True):
	global data
	if towiki:
		myuserpage = u"ഉപയോക്താവ്:" + 'Manubot'
		mypage = myuserpage + "/BotLabs/" + (pagename)
		 
		# doing the job
		site = wikipedia.getSite('ml','wikipedia')
		page = wikipedia.Page(site,mypage)
		page.put(data,u'ബോട്ടിന്റെ കൂന്തി വിളയാട്ടം')		
		wikipedia.stopme()
	else:
		f = codecs.open(pagename+u'.txt',encoding='utf-8', mode='w')
		f.write(data)
		f.close()
def savePage(pagename):
	
	updateInfobox()
	updateFilmDetails()
	updateActortable()
	update_music()
	update_aniyara()
	update_others()
	updateIwikis()
	udate2wiki(pagename,towiki = False)

def delTestPage(pagename):
	myuserpage = u"ഉപയോക്താവ്:" + 'Manubot'
	mypage = myuserpage + "/BotLabs/test" + pagename
	 
	 
	# doing the job
	site = wikipedia.getSite('ml','wikipedia')
	page = wikipedia.Page(site,mypage)
	page.delete(reason='Deleting Test pages', prompt=False, throttle=True, mark=True)	
	wikipedia.stopme()	
	
def processDict():
	info_box_dict['country'] = u'ഇന്ത്യ'
	info_box_dict['language'] = u'മലയാളം'
	convert2native()
	link2name()
	#unknown2ml()

def convert2native():
	for i,j in info_box_dict.iteritems():
		temp = u''
		for k in getMyLinks(j):
			int_wiki = getInterwiki(k)
			if int_wiki:
				#replace the data in the dictionary
				temp+=u'[['
				temp+=int_wiki
				temp+=u']]<br/>'
			else:
				temp+=u'[['
				temp+=k
				temp+=u']]<br/>'
			info_box_dict[i] = temp		
	#print info_box_dict
def link2name():
	r = re.compile(r'\s*\(.*?\)',re.UNICODE)
	for i,j in info_box_dict.iteritems():
		for k in getMyLinks(j):
			x = u''
			y = u''
			x = r.sub('',k)
			#print x,k
			if x != k:
				#y+=u'[['
				y+=k
				y+=u' | '
				y+=x
				#y+=u']]'
				info_box_dict[i] = info_box_dict[i].replace(k,y,1)

	#print info_box_dict				

	
def unknown2ml():
	for i,j in info_box_dict.iteritems():
		for k in getMyLinks(j,1):
			if ord(k[0]) < 255:
				y = translate2ml(k)
				info_box_dict[i] = info_box_dict[i].replace(k,y)
	info_box_dict['name'] = translate2ml(info_box_dict['name'])
	#print info_box_dict	
	
	
def translate2ml(string):

		ml = Transliterate.Transliteration()
		return ml.getTransliteration(string)
		
		
def listfilms(cat,iscat=False):
	global conn,curs,lang_code
	site = wikipedia.getSite('en','wikipedia')
	if iscat:
		cat = catlib.Category(site, cat)
		gen = pagegenerators.CategorizedPageGenerator(cat,True)
	else:
		page = wikipedia.Page(site,cat)
		if page.isRedirectPage():
			page = page.getRedirectTarget()
		for i in pagegenerators.LinkedPageGenerator(page):
			if i.exists():
				if i.isRedirectPage():
					i = i.getRedirectTarget()
				res1 = curs.execute('select pages from crawled_db').fetchall()
				if (i.title(),) not in res1:					
					curs.execute('INSERT INTO crawled_db VALUES (?)',(i.title(),))
					conn.commit()	
					#print i.templates()
					res = curs.execute('select en_link from wiki_db').fetchall()

					#print res
					if (i.title(),) not in res:
						print "listfilms(): not in db " + i.title().encode('utf-8')
						if u'Infobox film'.lower() in [hh.lower() for hh in i.templates()]:
							x = getInterwiki(i,string = False)
							# print 'listfilms():',x.encode('utf-8')
							if x == None:
								print 'listfilms():',i.title().encode('utf-8')
								#appending only thye names
								#page_to_add.append(i.title())
								page_to_add.append(i)
								curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(i.title(),None,1,1,lang_code))
								conn.commit()
							else:
								curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(i.title(),x,1,0,lang_code))
								conn.commit()						
						
						elif (u'Infobox person'.lower() in [hh.lower() for hh in i.templates()]) or (u'Infobox actor'.lower() in [hh.lower() for hh in i.templates()]):
							print 'listfilms():','Got actor page'
							x = getInterwiki(i,string = False)
							# print 'listfilms():',x.encode('utf-8')
							if x == None:
								print 'listfilms():',i.title().encode('utf-8')
								#appending only thye names
								#page_to_add.append(i.title())
								curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(i.title(),None,2,1,lang_code))
								conn.commit()
							else:
								curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(i.title(),x,2,0,lang_code))
								conn.commit()						
						else:
							print 'listfilms():',"Skipping junk "+i.title().encode('utf-8')
							x = getInterwiki(i,string = False)
							if x is None:
								curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(i.title(),None,255,1,lang_code))
							else:
								curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(i.title(),x,255,0,lang_code))
							conn.commit()	
					else:
						print 'listfilms():',"Skipping as in db "+i.title().encode('utf-8')
						
def updatedb(cat):
	global conn,curs,lang_code
	site = wikipedia.getSite('en','wikipedia')

	cat = catlib.Category(site, cat)
	gen = pagegenerators.CategorizedPageGenerator(cat,True)
	for page in gen:
		if page.isRedirectPage():
			page = page.getRedirectTarget()
		print 'updatedb()',page.title().encode('utf-8')
		res1 = curs.execute('select pages from crawled_db').fetchall()
		if (page.title(),) not in res1:
			curs.execute('INSERT INTO crawled_db VALUES (?)',(page.title(),))
			conn.commit()
			res = curs.execute('select en_link from wiki_db').fetchall()

			
			if (page.title(),) not in res:
				print 'updatedb() not in db '+page.title().encode('utf-8')

				if u'Infobox film'.lower() in [hh.lower() for hh in page.templates()]:
					print 'updatedb()',"Got Film"
					x = getInterwiki(page,string = False)
					# print 'updatedb()',x.encode('utf-8')
					if x == None:
						print 'updatedb()',page.title().encode('utf-8')
						#appending only thye names
						#page_to_add.append(page.title())
						curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(page.title(),None,1,1,lang_code))
						conn.commit()
					else:
						curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(page.title(),x,1,0,lang_code))
						conn.commit()	

				elif (u'Infobox person'.lower() in [hh.lower() for hh in page.templates()]) or (u'Infobox actor'.lower() in [hh.lower() for hh in page.templates()]):
					print 'updatedb()','Got actor page'
					x = getInterwiki(page,string = False)
					# print 'updatedb()',x.encode('utf-8')
					if x == None:
						print 'updatedb()',page.title().encode('utf-8')
						#appending only thye names
						#page_to_add.append(page.title())
						curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(page.title(),None,2,1,lang_code))
						conn.commit()
					else:
						curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(page.title(),x,2,0,lang_code))
						conn.commit()					
				else:
					print 'updatedb()',"List page"
					listfilms(page.title())

			else:
				print 'updatedb()',"Skipping as in db ",page.title().encode('utf-8')

						
if __name__ == '__main__':
	global conn,curs
	conn = sqlite3.connect('wiki_db.db')
	curs = conn.cursor()
	try:

		curs.execute('''CREATE TABLE wiki_db (
						en_link TEXT UNIQUE,
						ml_link TEXT,
						type INT,
						missing INT,
						lang INT)''')
		curs.execute('''CREATE TABLE crawled_db (
						pages TEXT UNIQUE)''')						
	except sqlite3.OperationalError:
		print "Database present already"
		pass	
	#ml = Transliterate.Transliteration() 
	updatedb('Category:Hindi-language_films')
	#page_to_add.append('Makalkku')
	# for i in page_to_add:
		# print i
		# j= ml.getTransliteration(i.title())		
		# j= i.title()
		# current_page = i.title()
		# getInfobox(i)
		# processDict()
		# savePage(j)
		# data = u''
		# info_box_dict = {}

	conn.commit()
	conn.close()		
		


	