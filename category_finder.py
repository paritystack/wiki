#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import catlib
import pagegenerators
import wikipedia
site = wikipedia.getSite()
cat = catlib.Category(site,'Category:Malayalam-language_films')
gen = pagegenerators.CategorizedPageGenerator(cat,True)
for page in gen:
  #Do something with the page object, for example:
  print page.title()

