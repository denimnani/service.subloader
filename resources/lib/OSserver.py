#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, xbmc
from resources.lib.utils import name, version, setting, boolsetting

try:
    import xmlrpc.client as xc
except:
    import xmlrpclib
    xc = xmlrpclib



OpenSubtitles = xc.Server('http://api.opensubtitles.org/xml-rpc', verbose=0)




#OpenSubtilte.org functions*******************************************************************************************************************************

def OSserver():
        user = ""
        password = ""
        ua = "kodi_%s_v%s" % (name().lower(), version())
        if boolsetting('OScustomuser'):
                if setting ('OSuser') != '' or setting('OSpassword') != '':
                        user = setting('OSuser')
                        password = setting('OSpassword')
                else:
                        user = "error"
                        password = "error"
        return OpenSubtitles.LogIn(user, password, 'en', ua)


def OSinfo():
        return OpenSubtitles.ServerInfo()['website_url']


def OStoken():
        return OSserver()['token']


def OSuser():
        return OSserver()['status'] == "200 OK"


def OSusersetting():
        if boolsetting('OScustomuser') and (setting('OSuser') != setting('OSusercheck') or setting('OSpassword') != setting('OSpasswordcheck')):
                return True
        return False

#*********************************************************************************************************************************************************
