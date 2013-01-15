'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import xbmc
import xbmcaddon
from time import sleep


ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
FOLDER = ADDON.getSetting('autoresume.save.folder')
FREQUENCY = int(ADDON.getSetting('autoresume.frequency'))
PATH = os.path.join(FOLDER.encode('utf-8', 'ignore'), 'autoresume.txt')

def resume():
  if os.path.exists(PATH):
    # Read from autoresume.txt.
    f = open(PATH, 'r')
    mediaFile = f.readline().rstrip('\n')
    position = float(f.readline())
    f.close()
    # Play file.
    xbmc.Player().play(mediaFile)
    # Seek to last recorded position.
    xbmc.Player().seekTime(position)

def recordPosition():
  if xbmc.Player().isPlaying():
    mediaFile = xbmc.Player().getPlayingFile()
    position = xbmc.Player().getTime()
    # Write info to file
    f = open(PATH, 'w')
    f.write(mediaFile)
    f.write('\n')
    f.write(repr(position))
    f.close()
  else:
    if os.path.exists(PATH):
      os.remove(PATH)

def log(msg):
  xbmc.log("%s: %s" % (ADDON_ID, msg), xbmc.LOGDEBUG)


if __name__ == "__main__":
  resume()
  while (not xbmc.abortRequested):
    recordPosition()
    sleep(FREQUENCY)
