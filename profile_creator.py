#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import wikipedia

lan = ('de', 'fr', 'pl', 'it', 'ja', 'es', 'nl','pt', 'ru', 'zh', 'ca', 'no', 'fi', 'uk', 'hu', 'cs', 'ro', 'tr', 'ko', 'vi', 'da', 'ar', 'eo', 'sr', 'id', 'lt', 'vo', 'sk', 'he', 'fa', 'bg', 'sl', 'war','hr', 'ms', 'et', 'new','simple',  'gl', 'th', 'roa-rup', 'nn', 'eu', 'hi', 'el', 'ht', 'la', 'te', 'tl', 'ka', 'ceb','mk', 'az', 'br', 'sh', 'mr', 'lb', 'lv', 'jv', 'is', 'cy', 'be-x-old','pms','sq', 'be', 'bpy','an', 'oc', 'bn', 'sw', 'io', 'ksh','fy', 'lmo','gu', 'nds','af', 'qu', 'scn','ku', 'ur', 'su', 'zh-yue',  'ast','nap','bat-smg', 'wa', 'ga', 'cv', 'hy', 'yo', 'ne', 'kn', 'tg', 'pnb','roa-tara','vec','gd', 'yi', 'zh-min-nan',      'tt', 'uz', 'pam','os', 'sah','als','arz','mi', 'kk', 'nah','li', 'hsb','glk','co', 'gan','am', 'mn', 'ia', 'bcl','sco','fo', 'fiu-vro', 'nds-nl',  'tk', 'si', 'vls','sa', 'my',  'bar', 'gv',  'dv',  'ilo', 'nrm', 'mg',  'rm',  'pag', 'map-bms',     'diq', 'ckb', 'se',  'mzn', 'wuu', 'ug',  'fur', 'lij', 'mt',  'bh',  'nov', 'ang', 'csb', 'sc',  'zh-classical','km',  'lad', 'cbk-zam',     'pi',  'bo',  'hif', 'frp', 'hak', 'kw',  'ps',  'pa',  'szl', 'xal', 'pdc', 'haw', 'nv',  'stq', 'ie',  'kv',  'fj',  'crh', 'so',  'to',  'ace', 'myv', 'mhr', 'gn',  'krc', 'ext', 'ln',  'ky',  'eml', 'pcd', 'arc', 'jbo', 'ay',  'wo',  'bjn', 'ba',  'frr', 'kab', 'pap', 'tpi', 'ty',  'srn', 'zea', 'kl',  'udm', 'koi', 'ce',  'ig',  'dsb', 'or',  'mrj', 'kg',  'lo',  'ab',  'mdf', 'rmy', 'mwl', 'cu',  'kaa', 'sm',  'mo',  'tet', 'av',  'ks',  'got', 'bm',  'sd',  'na',  'ik',  'pih', 'pnt', 'iu',  'chr', 'bi',  'as',  'cdo', 'ss',  'ee',  'om',  'za',  'zu',  'ti',  'ts',  've',  'ha',  'dz',  'sg',  'ch',  'cr',  'ak',  'xh',  'rw',  'st',  'bug', 'tn',  'ki',  'bxr', 'ny',  'lbe', 'tw',  'sn',  'rn',  'ff',  'chy', 'tum', 'lg',  'ng',  'ii',  'cho', 'mh',  'aa',  'kj',  'ho',  'mus', 'kr',  'hz')

myuserpage = u"User:Manumg"
myuserpage1 = u"User:Manubot"
data1 = u'''Bot operated by [[User:Manumg]].

Proud Wikipedian from India.

[[en:User:Manumg]]
[[ml:ഉപയോക്താവ്:Manumg]]
'''
data2 = u'''Bot operated by [[User:Manumg]].
Home wiki is Malayalam Wikipedia.

Used for updating interwiki links using pywikipedia/interwiki.py.
[[en:User:Manubot]]
[[ml:ഉപയോക്താവ്:Manubot]]
'''  
for i in lan:
	site = wikipedia.getSite(i,'wikipedia')
	page1 = wikipedia.Page(site,myuserpage)
	page2 = wikipedia.Page(site,myuserpage1)
	page1.put(data1,u'Creating User page')		
	page2.put(data2,u'Creating Bot page')		
wikipedia.stopme()
