#!/usr/bin/python
# -*- coding: utf-8 -*-
import imagetransfer
import wikipedia
site = wikipedia.getSite()
page = wikipedia.Page(site,'File:Police (2005 film).jpg')

bot = imagetransfer.ImageTransferBot(iter([page]),targetSite = 'ml')
bot.run()