
import BigWorld
from debug_utils import LOG_DEBUG, LOG_NOTE
import SoundGroups

from gui.wgfm.data import g_dataHolder
from gui.wgfm.events import g_eventsManager
from gui.wgfm.controllers import g_controllers
from gui.wgfm.wgfm_constants import VOLUME_STEP, VOLUME_STEP_LOW, VOLUME_STEP_VERY_LOW

__all__ = ('VolumeController', )

class VolumeController(object):
	
	volume = property(lambda self: round(float(self.__volume), 2))
	muted = property(lambda self: self.__muted)
	
	def __init__(self):
		self.__volume = 1.0
		self.__volumeVOIP = None
		self.__voipActive = False
		self.__isAudioPlaying = False
		self.__isWindowVisible = True
		self.__mutedCallbackID = None
		self.__muted = False
	
	def init(self):
		
		g_eventsManager.onSetVoipActive += self.__onSetVoipActive
		
		if g_dataHolder.settings.get('saveVolume', True):
			self.__volume = g_dataHolder.settings.get('lastVolume', 1.0)
		
		self.__mutedByWindowVisibility()
	
	def fini(self):
		
		g_eventsManager.onSetVoipActive -= self.__onSetVoipActive
		
		if self.__mutedCallbackID:
			BigWorld.cancelCallback(self.__mutedCallbackID)
			self.__mutedCallbackID = None
	
	
	def setVolume(self, volume):
		if g_dataHolder.settings.get('saveVolume', True):
			g_dataHolder.settings['lastVolume'] = volume
		
		if self.__voipActive and g_dataHolder.settings.get('muteOnVoip', False):
			return self.setVolumeVOIP(volume)
		
		volume = round(volume, 2)
		
		if self.__volumeVOIP is not None:
			if volume == self.__volumeVOIP:
				self.__volumeVOIP = None
				return False
			self.__volumeVOIP = None
		elif volume == self.__volume:
			return False
		
		self.__volume = volume 
		
		g_eventsManager.onVolumeChanged(self.volume)
		
		return True
	
	def setVolumeVOIP(self, volumeVOIP):
		self.__volume = round(volumeVOIP, 2)
		volumeVOIP = max(0.0, min(round(round(SoundGroups.g_instance.getVolume('masterFadeVivox'), 1) * float(volumeVOIP), 1), 1.0))
		if self.__volumeVOIP == volumeVOIP:
			return
		self.__volumeVOIP = volumeVOIP
		g_eventsManager.onVolumeChanged(round(float(volumeVOIP), 2))
		return True
	
	def volumeUp(self):
		if self.__volume < 0.2:
			volumeStep = VOLUME_STEP_LOW
		elif self.__volume < 0.1:
			volumeStep = VOLUME_STEP_VERY_LOW
		else:
			volumeStep = VOLUME_STEP
		
		newVolume = round(self.__volume + volumeStep, 2)

		if newVolume >= 1.0:
			self.setVolume(1)
			return False
		else:
			return self.setVolume(newVolume)			 
		
	def volumeDown(self):
		if self.__volume <= 0.2:
			volumeStep = VOLUME_STEP_LOW
		elif self.__volume <= 0.1:
			volumeStep = VOLUME_STEP_VERY_LOW
		else:
			volumeStep = VOLUME_STEP
		
		newVolume = round(self.__volume - volumeStep, 2)

		if newVolume <= 0.0:
			self.setVolume(0)
			return False
		else:
			return self.setVolume(newVolume)
	
	

	
	def __mutedByWindowVisibility(self):
		isWindowVisible = BigWorld.isWindowVisible()
		if self.__isWindowVisible != isWindowVisible:
			self.__isWindowVisible = isWindowVisible
					
			def volumeByWindowVisibility(self, volume, timeout=0.0):
				callback = lambda : g_eventsManager.onVolumeChangedHidden(round(float(volume), 2))
				BigWorld.callback(timeout, callback)
				
			if isWindowVisible:
				volumeByWindowVisibility(0, 0.2)
				volumeByWindowVisibility(self.__volume / 10.0, 0.3)
				volumeByWindowVisibility(self.__volume / 5.0, 0.4)
				volumeByWindowVisibility(self.__volume / 2.0, 0.5)
				volumeByWindowVisibility(self.__volume, 0.6)
			else:
				volumeByWindowVisibility(self.__volume, 0.2)
				volumeByWindowVisibility(self.__volume / 2.0, 0.3)
				volumeByWindowVisibility(self.__volume / 5.0, 0.4)
				volumeByWindowVisibility(self.__volume / 10.0, 0.5)
				volumeByWindowVisibility(0, 0.6)
		
		self.__mutedCallbackID = BigWorld.callback(0.1, self.__mutedByWindowVisibility)
	
	def __onSetVoipActive(self, isActive):
		self.__voipActive = isActive
		self.setVolume(self.__volume)
	
	def setMuted(self):
		self.__muted = not self.__muted
		g_eventsManager.onVolumeChanged(self.volume)