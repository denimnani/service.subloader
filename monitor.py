#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, xbmc, time
from resources.lib.loadsub import loadsub
from resources.lib.exclusions import globalexclusion
from resources.lib.OSserver import OSusersetting, OSuser
from resources.lib.utils import setting, boolsetting, setsetting, localize, debug, debugsetting


#Main Monitor********************************************************************************************************************************************

class SubLoaderMonitor(xbmc.Monitor):


	def __init__(self):
		xbmc.Monitor.__init__(self)
		debug("Initalized main monitor")
		self.run = True

	def onSettingsChanged(self):

		if self.run:	

			if debugsetting():
				self.run = False
				debug('Debug settings changed')
				setsetting('debugcheck', value=setting('debug'))
				global closedebug
				closedebug = boolsetting('debug')
				debug('Debug initalized')
				if not closedebug:
					debug('Debug stopped', force = True)

			if OSusersetting():
				self.run = False
				debug('OS User settings changed')
				if OSuser():
					xbmc.executebuiltin('Notification("SubLoader", "%s", "%s",)' % (localize(32033), 4000))
					setsetting('OSusercheck', value=setting('OSuser'))
					setsetting('OSpasswordcheck', value=setting('OSpassword'))
					debug('OS Login: successful')
				else:
					xbmc.executebuiltin('Notification("SubLoader", "%s", "%s",)' % (localize(32034), 4000))
					setsetting('OSusercheck', value='nouser')
					setsetting('OSpasswordcheck', value='nopassword')
					debug('OS Login: unsuccessful')

		else:
			xbmc.sleep(1000)
			self.run = True


monitor = SubLoaderMonitor()


#Player monitor******************************************************************************************************************************************

class SubLoaderPlayer(xbmc.Player):

	def __init__(self, *args, **kwargs):
		xbmc.Player.__init__(self)
		debug('Initalized player monitor')
		self.run = True

	def onPlayBackStopped(self):
		debug('Playback stopped')
		self.run = True

	def onPlayBackEnded(self):
		debug('Playback ended')
		self.run = True

	def onAVStarted(self):
		self.run = True
		delay = int(setting('delay'))*1000

		if self.run:
			xbmc.sleep(delay)		
			if xbmc.Player().isPlayingVideo() and globalexclusion():
				self.run = False	
				if setting('default') == '0':
					debug('Default: automatic subtitles')
					loadsub()
				elif setting('default') == '1':
					debug('Default: opening search dialog')
					xbmc.executebuiltin('ActivateWindow(SubtitleSearch)')
				else:
					debug('Default: do nothing...')
			else:
				self.run = False


player = SubLoaderPlayer()


#Abort request*******************************************************************************************************************************************

closedebug = boolsetting('debug')

while not xbmc.Monitor().abortRequested():
	
	if xbmc.Monitor().waitForAbort(10):
		if closedebug:
			debug('Shutdown requested', force = True)
			debug('Player monitor stopped', force = True)
			debug('Main monitor stopped', force = True)
		del player
		del monitor
		break

#********************************************************************************************************************************************************
