#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, datetime
from resources.lib import utils
from resources.lib.utils import setting, videosource, debug, videopath, boolsetting


# Exclusions*********************************************************************************************************************************************

def addonexclusion():

	if setting('excludeaddon'):
		exaddon = setting('excludeaddon').split(',')
		if all(videosource().find (v) <= -1 for v in exaddon):
			return True
		else:
			debug('Excluded: the source addon is excluded %s' % exaddon)
			return False
	else:
		return True


def wordsexclusion():

	if setting('excludewords'):
		words = setting('excludewords').split(',')
		if all(videopath().find (v) <= -1 for v in words):
			return True
		else:
			debug('Excluded: the video path have excluded words %s' % words)
			return False
	else:
		return True


def timeexclusion():

	time = xbmc.Player().getTotalTime()
	debug('Total time: %s' % str(datetime.timedelta(seconds=round(time))))
	timeexcluded = int(setting('excludetime'))*60
	if time > timeexcluded:
		return True
	else:
		debug('Excluded: the content time is lower than the exclusion')
		return False


def audioexclusion():

	if boolsetting('excludeaudio'):
		langs = []
		langs.append(utils.langdict[setting('excludeaudiolang1')])
		if not setting('excludeaudiolang2') == "-----":
			langs.append(utils.langdict[setting('excludeaudiolang2')])
		if not setting('excludeaudiolang3') == "-----":
			langs.append(utils.langdict[setting('excludeaudiolang3')])
		availableaudio = xbmc.Player().getAvailableAudioStreams()
		debug('Available audio streams: %s' % availableaudio)
		availableaudio = " ".join(availableaudio)
		if any(x in availableaudio for x in langs):
			debug('Excluded: the audio language is excluded')
			return False
		if "und" in availableaudio and not boolsetting('audiound'):
			debug('Excluded: undertermined audio')
			return False
		return True
	return True


def subexclusion():

	if boolsetting('excludesub'):
		langs = []
		langs.append(utils.langdict[setting('excludesublang1')])
		if not setting('excludesublang2') == "-----":
			langs.append(utils.langdict[setting('excludesublang2')])
		if not setting('excludesublang3') == "-----":
			langs.append(utils.langdict[setting('excludesublang3')])
		availablesubs = xbmc.Player().getAvailableSubtitleStreams()
		debug('Available sub languages: %s' % availablesubs)
		availablesubs = " ".join(availablesubs)
		if any(x in availablesubs for x in langs):
			debug('Subtitle is already present')
			return False
		return True
	return True


def pathexclusion():

	debug('Content path: %s' % videopath())
	if videopath().find("http://") > -1 or videopath().find("https://") > -1:
		debug('Content source: %s' % videosource())

	if not videopath():
		return False

	if (videopath().find("pvr://") > -1) and boolsetting('excludelivetv'):
		debug('Video is playing via Live TV, which is currently set as excluded location.')
		return False

	if (videopath().find("http://") > -1 or videopath().find("https://") > -1) and boolsetting('excludehttp'):
		debug('Video is playing via HTTP or HTTPS source, which is currently set as excluded location.')
		return False

	path = setting('path')
	if path and boolsetting('excludepath'):
		if (videopath().find(path) > -1):
			debug('Video is playing from %s, which is currently set as excluded path 1.' % path)
			return False

	path2 = setting('path2')
	if path2 and boolsetting('excludepath2'):
		if (videopath().find(path2) > -1):
			debug('Video is playing from %s, which is currently set as excluded path 2.' % path2)
			return False

	path3 = setting('path3')
	if path3 and boolsetting('excludepath3'):
		if (videopath().find(path3) > -1):
			debug('Video is playing from %s, which is currently set as excluded path 3.' % path3)
			return False

	path4 = setting('path4')
	if path4 and boolsetting('excludepath4'):
		if (videopath().find(path4) > -1):
			debug('Video is playing from %s, which is currently set as excluded path 4.' % path4)
			return False

	path5 = setting('path5')
	if path5 and boolsetting('excludepath5'):
		if (videopath().find(path5) > -1):
			debug('Video is playing from %s, which is currently set as excluded path 5.' % path5)
			return False

	return True


def globalexclusion():

	if pathexclusion() and addonexclusion() and wordsexclusion() and timeexclusion() and subexclusion() and audioexclusion():
		return True
	return False

#********************************************************************************************************************************************************