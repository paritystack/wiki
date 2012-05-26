#!/usr/bin/python
# -*- coding: utf-8  -*-

import wikipedia 
import re
import pagegenerators
import catlib
import codecs
import sqlite3

gtemplates = (
			u'Infobox film'.lower(),
			u'Imdb title'.lower(),
			u'Amg title'.lower())
gremoval_re = (
				(r'\n',''),
				(r'\s*=\s*','=')
)
gdictInfobox = {}
gpageData = u''
gcurrent_page = u''
def getInfobox(film):
	info_box_dict = {}
	site = wikipedia.getSite('en','wikipedia') 
	page = wikipedia.Page(site, film) 
	if page.isRedirectPage():
		page = page.getRedirectTarget()	

	for template in page.templatesWithParams():
		x = template[0].lower()
		if x in gtemplates:
			info_box_dict[x] = template[1]

	#print info_box_dict
	try:
		#Populate the global dictionary
		for i in info_box_dict[gtemplates[0]]:
			#Cleanup the data
			for regex,removal in gremoval_re:
				r = re.compile(regex,re.UNICODE)
				r.sub(removal,i)
			#split
			#Strip not req
			split_val = i.split(u'=',1)
			key = split_val[0].strip()
			val = split_val[1].strip()
			if val:
				gdictInfobox[key] = val

	except KeyError:
		print "info_box_dict update failure in getInfobox()"
	except IndexError:
		print "Can be bug in pywiki.= not present.Wrong index in getInfobox()",i		
	try:
		gdictInfobox['imdb_id'] = info_box_dict[gtemplates[1]]
		gdictInfobox['amg_id'] = info_box_dict[gtemplates[2]]
	except KeyError:
		pass
	
	print gdictInfobox


def getInterwiki(input_page,lang = 'ml',string = True):
	#print type(input_page)
	#print (input_page)

	regex = r'\[\[%s:(.*)\]\]' % lang
	r = re.compile(regex,re.UNICODE)
	
	try:
		if string:
			site = wikipedia.getSite('en','wikipedia') 
			page = wikipedia.Page(site, input_page) 
		else:
			page = input_page
		if page.isRedirectPage():
			page = page.getRedirectTarget()

		for i in page.interwiki():
			#print i.aslink().encode('utf-8')
			m = r.search(i.aslink())
			if m:
				iwiki = m.group(1)
				#print iwiki
				return iwiki
	except wikipedia.NoPage:
		print 'getInterwiki: No Page to open',input_page.encode('utf-8')
		return None
	
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

#{{ubl|Harikrishnan|P. F. Mathews}}	
#Christopher Nolan<br />[[Emma Thomas]]
def getItems(stringdata):
	if stringdata.find('{{ubl|') != -1:
		stringdata = stringdata.replace('{{ubl|','')
		stringdata = stringdata.replace('}}','')
	elif stringdata.find('<br />') != -1:
		stringdata = stringdata.replace('<br />','|')
	return 	[i.strip() for i in stringdata.split('|')]
	
def updateInfobox():
	global gpageData
	gpageData+=u'{{Infobox Film\n'
	for i,j in gdictInfobox.iteritems():
		gpageData+=u'| '
		gpageData+=i
		gpageData+=u'='
		gpageData+=j
		gpageData+=u'\n'
	gpageData+=u'''}}'''	
	


def updateFilmDetails():
	global gpageData
	if gdictInfobox.has_key('name'):
		gpageData+= u'\n\'\'\'\'\''
		gpageData+=gdictInfobox['name']
		gpageData+=u'\'\'\'\'\' '
	if gdictInfobox.has_key('director'):	
		try:
			gpageData+= getMyLinks(gdictInfobox['director'],1)[0]
		except IndexError:
			gpageData+= gdictInfobox['director']
		gpageData+=u' സംവിധാനം നിര്‍വഹിച്ച് '
	if gdictInfobox.has_key('released'):			
		gpageData+=gdictInfobox['released']
		gpageData+=u'പുറത്തിറങ്ങിയ '
	if gdictInfobox.has_key('language'):			
		gpageData+=gdictInfobox['language']
	gpageData+=u'ചലച്ചിത്രമാണ്.'		

		
def updateActortable():
	global gpageData
	gpageData+=u'''
== അഭിനേതാക്കൾ ==
{| class="wikitable"
|-
! അഭിനേതാവ് !! കഥാപാത്രം
|-
'''
	for i in getMyLinks(gdictInfobox['starring'],1):
		gpageData+=u'|'
		gpageData+=i
		gpageData+=u'||\n'
		gpageData+=u'|-\n'
	gpageData+=u'''|}'''

def updateIwikis():
	global gpageData
	site = wikipedia.getSite('en','wikipedia')
	page = wikipedia.Page(site,gcurrent_page)
	gpageData+=u'[['
	gpageData+=u'en:'
	gpageData+=gcurrent_page
	gpageData+=u']]'
	for i in page.interwiki():
		gpageData+=i

def update_music():
	global gpageData
	temp = gpageData
	gpageData+=u'''	
== സംഗീതം ==
'''

	if gdictInfobox.has_key('music') and gdictInfobox.has_key('lyrics'):
		gpageData+=u'ഇതിലെ ഗാനങ്ങൾ രചിച്ചത് '
		gpageData+=gdictInfobox['lyrics']
		gpageData+=u' ആണ്.ഈണം പകർന്നിരുന്നത്  '
		gpageData+=gdictInfobox['music']
		gpageData+=u' ആണ്.'
	elif gdictInfobox.has_key('music'):
		gpageData+=u'ഇതിലെ ഗാനങ്ങൾക്ക് ഈണം പകർന്നിരുന്നത് '
		gpageData+=gdictInfobox['music']
		gpageData+=u' ആണ്.'
	elif gdictInfobox.has_key('lyrics'):
		gpageData+=u'ഇതിലെ ഗാനങ്ങൾ രചിച്ചത്  '
		gpageData+=gdictInfobox['lyrics']
		gpageData+=u' ആണ്.'
	else:
		gpageData = temp


def update_aniyara():
	global gpageData
	flag = False
	temp = gpageData
	gpageData+=u'''

== അണിയറ പ്രവർത്തകർ ==
{| class="wikitable"
|-
! അണിയറപ്രവർത്തനം !! നിർ‌വ്വഹിച്ചത്
|-
'''
	if gdictInfobox.has_key('cinematography'):
		flag = True
		gpageData+=u'''
| ഛായാഗ്രഹണം || '''
		gpageData+=gdictInfobox['cinematography']
		gpageData+=u'\n|-'
	elif gdictInfobox.has_key('editing'):
		flag = True
		gpageData+=u'''
| ചിത്രസം‌യോജനം || '''
		gpageData+=gdictInfobox['editing']
		gpageData+=u'\n|-'

	if flag == True:
		gpageData+=u'\n|}'
	else:
		gpageData = temp



def update_others():
	global gpageData
	gpageData+=u'''

== അവലംബം ==
<references />

== പുറത്തേക്കുള്ള കണ്ണികൾ ==

{{film-stub}}

'''
			
def udate2wiki(pagename=u'ഉപയോക്താവ്:Manubot/sandbox',towiki=True):
	global gpageData
	if towiki:
		site = wikipedia.getSite('ml','wikipedia')
		page = wikipedia.Page(site,pagename)
		page.put(gpageData,u'ബോട്ടിന്റെ കൂന്തി വിളയാട്ടം')		
		wikipedia.stopme()
	else:
		f = codecs.open(pagename+u'.txt',encoding='utf-8', mode='w')
		f.write(gpageData)
		f.close()	
	
	
def savePage(pagename):
	
	updateInfobox()
	updateFilmDetails()
	updateActortable()
	update_music()
	update_aniyara()
	update_others()
	updateIwikis()
	udate2wiki(pagename)

def delTestPage(pagename):
	myuserpage = u"ഉപയോക്താവ്:" + 'Manubot'
	mypage = myuserpage + "/BotLabs/test" + pagename
	 
	 
	# doing the job
	site = wikipedia.getSite('ml','wikipedia')
	page = wikipedia.Page(site,mypage)
	page.delete(reason='Deleting Test pages', prompt=False, throttle=True, mark=True)	
	wikipedia.stopme()	

def processDict():
	gdictInfobox['country'] = u'{{ഫലകം:Film India}}'
	gdictInfobox['language'] = u'മലയാളം'
	try:
		gdictInfobox['preceded_by'] = gdictInfobox['preceded by']
		del gdictInfobox['preceded by']
		gdictInfobox['followed_by'] =gdictInfobox['followed by']
		del gdictInfobox['followed by']
	except KeyError:
		pass
	convert2native()
	link2name()
	#unknown2ml()

def convert2native():
	for i,j in gdictInfobox.iteritems():
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
			gdictInfobox[i] = temp		
	#print gdictInfobox
def link2name():
	r = re.compile(r'\s*\(.*?\)',re.UNICODE)
	for i,j in gdictInfobox.iteritems():
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
				gdictInfobox[i] = gdictInfobox[i].replace(k,y,1)

	#print gdictInfobox				

	
def unknown2ml():
	for i,j in gdictInfobox.iteritems():
		for k in getMyLinks(j,1):
			if ord(k[0]) < 255:
				y = translate2ml(k)
				gdictInfobox[i] = gdictInfobox[i].replace(k,y)
	gdictInfobox['name'] = translate2ml(gdictInfobox['name'])
	#print gdictInfobox	
	
	
def translate2ml(string):

		ml = Transliterate.Transliteration()
		return ml.getTransliteration(string)


def processPage(page):
	outpage = u'ഉപയോക്താവ്:Manubot/sandbox'
	getInfobox(page)
	processDict()
	savePage(outpage)
	gdata = u''
	gdictInfobox = {}
	
if __name__ == '__main__':	
	gcurrent_page = 'Elektra (2010 film)'
	processPage(gcurrent_page)




	


	


	
		
		
# def listfilms(cat,iscat=False):
	# global conn,curs,lang_code
	# site = wikipedia.getSite('en','wikipedia')
	# if iscat:
		# cat = catlib.Category(site, cat)
		# gen = pagegenerators.CategorizedPageGenerator(cat,True)
	# else:
		# page = wikipedia.Page(site,cat)
		# if page.isRedirectPage():
			# page = page.getRedirectTarget()
		# for i in pagegenerators.LinkedPageGenerator(page):
			# if i.exists():
				# if i.isRedirectPage():
					# i = i.getRedirectTarget()
				# res1 = curs.execute('select pages from crawled_db').fetchall()
				# if (i.title(),) not in res1:					
					# curs.execute('INSERT INTO crawled_db VALUES (?)',(i.title(),))
					# conn.commit()	
					# #print i.templates()
					# res = curs.execute('select en_link from wiki_db').fetchall()

					# #print res
					# if (i.title(),) not in res:
						# print "listfilms(): not in db " + i.title().encode('utf-8')
						# if u'Infobox film'.lower() in [hh.lower() for hh in i.templates()]:
							# x = getInterwiki(i,string = False)
							# # print 'listfilms():',x.encode('utf-8')
							# if x == None:
								# print 'listfilms():',i.title().encode('utf-8')
								# #appending only thye names
								# #page_to_add.append(i.title())
								# page_to_add.append(i)
								# curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(i.title(),None,1,1,lang_code))
								# conn.commit()
							# else:
								# curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(i.title(),x,1,0,lang_code))
								# conn.commit()						
						
						# elif (u'Infobox person'.lower() in [hh.lower() for hh in i.templates()]) or (u'Infobox actor'.lower() in [hh.lower() for hh in i.templates()]):
							# print 'listfilms():','Got actor page'
							# x = getInterwiki(i,string = False)
							# # print 'listfilms():',x.encode('utf-8')
							# if x == None:
								# print 'listfilms():',i.title().encode('utf-8')
								# #appending only thye names
								# #page_to_add.append(i.title())
								# curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(i.title(),None,2,1,lang_code))
								# conn.commit()
							# else:
								# curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(i.title(),x,2,0,lang_code))
								# conn.commit()						
						# else:
							# print 'listfilms():',"Skipping junk "+i.title().encode('utf-8')
							# x = getInterwiki(i,string = False)
							# if x is None:
								# curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(i.title(),None,255,1,lang_code))
							# else:
								# curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(i.title(),x,255,0,lang_code))
							# conn.commit()	
					# else:
						# print 'listfilms():',"Skipping as in db "+i.title().encode('utf-8')
						
# def updatedb(cat):
	# global conn,curs,lang_code
	# site = wikipedia.getSite('en','wikipedia')

	# cat = catlib.Category(site, cat)
	# gen = pagegenerators.CategorizedPageGenerator(cat,True)
	# for page in gen:
		# if page.isRedirectPage():
			# page = page.getRedirectTarget()
		# print 'updatedb()',page.title().encode('utf-8')
		# res1 = curs.execute('select pages from crawled_db').fetchall()
		# if (page.title(),) not in res1:
			# curs.execute('INSERT INTO crawled_db VALUES (?)',(page.title(),))
			# conn.commit()
			# res = curs.execute('select en_link from wiki_db').fetchall()

			
			# if (page.title(),) not in res:
				# print 'updatedb() not in db '+page.title().encode('utf-8')

				# if u'Infobox film'.lower() in [hh.lower() for hh in page.templates()]:
					# print 'updatedb()',"Got Film"
					# x = getInterwiki(page,string = False)
					# # print 'updatedb()',x.encode('utf-8')
					# if x == None:
						# print 'updatedb()',page.title().encode('utf-8')
						# #appending only thye names
						# #page_to_add.append(page.title())
						# curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(page.title(),None,1,1,lang_code))
						# conn.commit()
					# else:
						# curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(page.title(),x,1,0,lang_code))
						# conn.commit()	

				# elif (u'Infobox person'.lower() in [hh.lower() for hh in page.templates()]) or (u'Infobox actor'.lower() in [hh.lower() for hh in page.templates()]):
					# print 'updatedb()','Got actor page'
					# x = getInterwiki(page,string = False)
					# # print 'updatedb()',x.encode('utf-8')
					# if x == None:
						# print 'updatedb()',page.title().encode('utf-8')
						# #appending only thye names
						# #page_to_add.append(page.title())
						# curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(page.title(),None,2,1,lang_code))
						# conn.commit()
					# else:
						# curs.execute('INSERT INTO wiki_db VALUES (?,?,?,?,?)',(page.title(),x,2,0,lang_code))
						# conn.commit()					
				# else:
					# print 'updatedb()',"List page"
					# listfilms(page.title())

			# else:
				# print 'updatedb()',"Skipping as in db ",page.title().encode('utf-8')

						
# if __name__ == '__main__':
	# global conn,curs
	# conn = sqlite3.connect('wiki_db.db')
	# curs = conn.cursor()
	# try:

		# curs.execute('''CREATE TABLE wiki_db (
						# en_link TEXT UNIQUE,
						# ml_link TEXT,
						# type INT,
						# missing INT,
						# lang INT)''')
		# curs.execute('''CREATE TABLE crawled_db (
						# pages TEXT UNIQUE)''')						
	# except sqlite3.OperationalError:
		# print "Database present already"
		# pass	
	# #ml = Transliterate.Transliteration() 
	# updatedb('Category:Hindi-language_films')
	# #page_to_add.append('Makalkku')
	# # for i in page_to_add:
		# # print i
		# # j= ml.getTransliteration(i.title())		
		# # j= i.title()
		# # gcurrent_page = i.title()
		# # getInfobox(i)
		# # processDict()
		# # savePage(j)
		# # data = u''
		# # gdictInfobox = {}

	# conn.commit()
	# conn.close()		
		


	