#!/usr/bin/python
# -*- coding: utf-8 -*-
import wikipedia # Import the wikipedia module
import pagegenerators
import codecs
import imagetransfer

def genNoInterwikidata(toSite = False):
	mypage = u"ഉപയോക്താവ്:Manubot/Nointerwiki"
	data = u''
	gen = pagegenerators.WithoutInterwikiPageGenerator(10000)
	f = codecs.open('Nointerwiki.txt',encoding='utf-8', mode='w')
	for page in gen:
		f.write(page.title()+'\n')
		data += u'#[['
		data += page.title()
		data += u']]\n'
		
	f.close()		 
	site = wikipedia.getSite('ml','wikipedia')
	out_page = wikipedia.Page(site,mypage)
	out_page.put(data,u'Pages with No interwiki.')

	# mypage = u"ഉപയോക്താവ്:Manubot/NoMalayalamLinkFilms"
# mypage = u"ഉപയോക്താവ്:Manubot/NoMalayalamLinkPerson"


def genNoInterwikiFilms(toSite = False):
	mypage = u"ഉപയോക്താവ്:Manubot/NointerwikiFilms"
	data = u''
	gen = pagegenerators.WithoutInterwikiPageGenerator(10000)
	f = codecs.open('NointerwikiFilms.txt',encoding='utf-8', mode='w')
	for page in gen:
		print page
		x= page.templates()
		if (u'Infobox film'.lower() in [hh.lower() for hh in x]) or (u'Cinema Infobox'.lower() in [hh.lower() for hh in x]):
			f.write(page.title()+'\n')
			if toSite:
				data += u'#[['
				data += page.title()
				data += u']]\n'
	f.close()	
	if toSite:				
		site = wikipedia.getSite('ml','wikipedia')
		out_page = wikipedia.Page(site,mypage)
		out_page.put(data,u'Films pages with No interwiki.')
	
def genNoInterwikiPerson(toSite = False):
	mypage = u"ഉപയോക്താവ്:Manubot/NointerwikiPerson"
	data = u''
	gen = pagegenerators.WithoutInterwikiPageGenerator(10000)
	f = codecs.open('NointerwikiPerson.txt',encoding='utf-8', mode='w')
	for page in gen:
		print page
		x= page.templates()
		if (u'Infobox person'.lower() in [hh.lower() for hh in x]) or (u'Infobox actor'.lower() in [hh.lower() for hh in x]):
			f.write(page.title()+'\n')
			if toSite:
				data += u'#[['
				data += page.title()
				data += u']]\n'
	f.close()	
	if toSite:				
		site = wikipedia.getSite('ml','wikipedia')
		out_page = wikipedia.Page(site,mypage)
		out_page.put(data,u'Person pages with No interwiki.')
	



def imageTransfer(pic):
	page = wikipedia.Page(wikipedia.getSite('en','wikipedia'), pic)
	gen = iter([page])
	targetSite = wikipedia.Site('ml', 'wikipedia')
	bot = imagetransfer.ImageTransferBot(gen, interwiki = False, targetSite = targetSite)
	bot.run()

def unicode2url(uni):
	bytestream = uni.encode('utf-8')
	bytestream = repr(bytestream)
	bytestream = bytestream.replace('\\x','%')
	bytestream = bytestream.replace('\'','')
	return bytestream

def addlog(txt):
	page = wikipedia.Page(wikipedia.getSite('ml','wikipedia'), u'ഉപയോക്താവ്:Manubot/logs')
	text = page.get() + '\n' + txt
	page.put(text,u'Log appened.')

def ChangeCinemaInfobox():
	mapping = {
		u"പേര്" : u"name",
	 u"ഭാഷ": u"language",
	 u"സംവിധായകൻ": u"director",
	 u"നിർമ്മാതാ‍വ്": u"producer",
	 u"കഥ": u"writer",
	 u"തിരക്കഥ": u"screenplay",
	 u"അഭിനേതാക്കൾ": u"starring",
	 u"സംഗീതം": u"music",
	 u"ഗാനരചന": u"lyrics",
	 u"ക്യാമറ": u"cinematography",
	 u"എഡിറ്റിംഗ്": u"editing",
	 u"വിതരണം": u"distributor",
	 u"വർഷം": u"released",
	 u"മുൻഗാമി" :u"preceded_by",
	u"പിൻഗാമി":u"followed_by",
	u"ഐഎംഡിബി താൾ" :u"imdb_id"
	}

	page = wikipedia.Page(wikipedia.getSite('ml','wikipedia'), u'ഫലകം:Cinema Infobox')
	gen = pagegenerators.ReferringPageGenerator(page)
	y = 0
	for i in gen:
		data_dic = {'country':u'{{ഫലകം:Film India}}'}
		gpageData = u''
		y+=1
		temp = dict(i.templatesWithParams())
		for i in temp['Cinema Infobox']:
			i.replace(u'\n',u'')
			x = i.split(u'=',1)
			try:
				key = x[0].strip()
				val = x[1].strip()
				mappi = mapping[key]
				print key,val
			except:
				mappi = key
				print "Wrong key"
			data_dic[mappi] = val
		
		# print data_dic
		f = codecs.open('tempp%d.txt' %y,encoding='utf-8', mode='w')
		gpageData+=u'{{Infobox Film\n'
		for i,j in data_dic.iteritems():
			gpageData+=u'| '
			gpageData+=i
			gpageData+=u'='
			gpageData+=j
			gpageData+=u'\n'
		gpageData+=u'}}'	
		# print 'data is ',gpageData
		f.write(gpageData)
		f.close()
		# break
			
if __name__ == '__main__':
	# imageTransfer('en:File:')
	genNoInterwikidata(True)
	genNoInterwikiFilms(True)
	genNoInterwikiPerson(True)
	# addlog("Testing")
	# ChangeCinemaInfobox()