#!/usr/bin/env python 
# -*- coding: iso-8859-1 -*-

import sublime_plugin, time
import Sun

"""
Simple Sublime Text 2 plug-in that automatically toggles color 
schemes by the availability of ambient light, as estimated by calculating current times of sunrise and sunset
at the preconfigured location.

Sunrise/set calculation is done by the 'Sun' class (see Sun.py), which has been developed by others 
(Paul Schlyter, Sean Russell, Henrik Härkönen, Miguel Tremblay) and is in the public domain.

The plugin is pre-configured for the dark and light Solarized color schemes (http://ethanschoonover.com/solarized)
and the location of Rostock, Germany.

Take care: this was just a playground project to learn a bit about Sublime Text plugins (and Python), 
so it's likely to be buggy, it's not very elegant etc.

@author: Roland Ewlad
@license: public domain
"""

# Color schemes
schemes = {
  "night" : "Packages/Color Scheme - Default/Solarized (Dark).tmTheme", 
  "day" : "Packages/Color Scheme - Default/Solarized (Light).tmTheme"
}

# Time - change this to match your timezone (GMT +/- x)
gmt_offset = 2 

# Location
lon = 12.133333 #Change these to match you location: Eastern long positive, Western long. negative ...
lat = 54.083333 # ... Northern lat. positive, Southern lat. negative (see Sun.py)

class AutoToggleColorScheme(sublime_plugin.EventListener):
  def on_activated(self, view):
    """
    Checking to toggle color schemes is done after every view activation, which is not very efficient but ensures switches both at runtime and at startup.
    """
    curr_time = time.localtime(time.time())
    times = Sun.Sun().sunRiseSet(curr_time.tm_year, curr_time.tm_mon, curr_time.tm_mday, lon, lat)
    daylight = map(lambda x: (x + gmt_offset) * 60, times)
    current_min = (curr_time.tm_hour * 60 + curr_time.tm_min)
    color_scheme = "day" if(current_min >= daylight[0] and current_min <= daylight[1]) else "night"
    view.settings().set('color_scheme', schemes[color_scheme])