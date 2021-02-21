#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, xbmc, xbmcaddon, xbmcgui
import base64, gzip, xbmcvfs
import re, hashlib, json
import codecs, urllib, xbmcplugin, time

try:
    import StringIO
    loglevel = xbmc.LOGNOTICE
    py2 = True
except:
    import io
    loglevel = xbmc.LOGINFO
    py2 = False

langdict = {
        'Afrikaans': 'afr', 'Albanian': 'alb', 'Arabic': 'ara', 'Armenian': 'arm', 'Basque': 'baq',
        'Bengali': 'ben', 'Bosnian': 'bos', 'Breton': 'bre', 'Bulgarian': 'bul', 'Burmese': 'bur',
        'Catalan': 'cat', 'Chinese': 'chi', 'Croatian': 'hrv', 'Czech': 'cze', 'Danish': 'dan', 'Dutch': 'dut',
        'English': 'eng', 'Esperanto': 'epo', 'Estonian': 'est', 'Finnish': 'fin', 'French': 'fre',
        'Galician': 'glg', 'Georgian': 'geo', 'German': 'ger', 'Greek': 'ell', 'Hebrew': 'heb', 'Hindi': 'hin',
        'Hungarian': 'hun', 'Icelandic': 'ice', 'Indonesian': 'ind', 'Italian': 'ita', 'Japanese': 'jpn',
        'Kazakh': 'kaz', 'Khmer': 'khm', 'Korean': 'kor', 'Latvian': 'lav', 'Lithuanian': 'lit',
        'Luxembourgish': 'ltz', 'Macedonian': 'mac', 'Malay': 'may', 'Malayalam': 'mal', 'Manipuri': 'mni',
        'Mongolian': 'mon', 'Montenegrin': 'mne', 'Norwegian': 'nor', 'Occitan': 'oci', 'Persian': 'per',
        'Polish': 'pol', 'Portuguese': 'por', 'Portuguese(Brazil)': 'pob', 'Romanian': 'rum',
        'Russian': 'rus', 'Serbian': 'scc', 'Sinhalese': 'sin', 'Slovak': 'slo', 'Slovenian': 'slv',
        'Spanish': 'spa', 'Swahili': 'swa', 'Swedish': 'swe', 'Syriac': 'syr', 'Tagalog': 'tgl', 'Tamil': 'tam',
        'Telugu': 'tel', 'Thai': 'tha', 'Turkish': 'tur', 'Ukrainian': 'ukr', 'Urdu': 'urd'}




def addon():
        addon = xbmcaddon.Addon().getAddonInfo('id')
        return xbmcaddon.Addon(addon)


def name():
        return xbmcaddon.Addon().getAddonInfo('name')


def version():
        return xbmcaddon.Addon().getAddonInfo('version')


def localize(id):
        if py2:
            return addon().getLocalizedString(id).encode('utf-8')
        else:
            return addon().getLocalizedString(id)


def setting(setting):
        return addon().getSetting(setting)


def boolsetting(setting):
        return addon().getSetting(setting).lower() == "true"


def setsetting(setting, value):
        return addon().setSetting(setting, value)


def setboolsetting(setting, value):
        return addon().setSettingBool(setting, value)


def debug(msg, force = False):

        if force or boolsetting('debug'):
                try:
                        xbmc.log("#####[SubLoader]##### " + msg, loglevel)
                except UnicodeEncodeError:
                        xbmc.log("#####[SubLoader]##### " + msg, loglevel).encode( "utf-8", "ignore" )

debug('Loading %s version %s' % (name(), version()))


def videopath():
        return xbmc.Player().getPlayingFile()


def videosource():
        return xbmc.getInfoLabel('Player.Folderpath')


def fullvideosource():
        return xbmc.getInfoLabel('Player.Filenameandpath')


def debugsetting():

        if boolsetting('debug') != boolsetting('debugcheck'):
                return True
        return False
