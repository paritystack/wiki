#!/usr/bin/python
# -*- coding: utf-8  -*-

import wikipedia # Import the wikipedia module
 
site = wikipedia.getSite('ml','malayalam') # Taking the default site
site1 = wikipedia.getSite('ml','wikipedia') # Taking the default site
page = wikipedia.Page(site, u'Image:P77d.png') # Calling the constructor
# print page.get()
#wikipedia.stopme()



