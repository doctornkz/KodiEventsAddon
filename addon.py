# -*- coding: utf-8 -*-
# Licence: GPL v.3 http://www.gnu.org/licenses/gpl.html

# Импортируем нужные модули
import xbmcgui

import datetime
import time
import urllib2
import os
import xbmcaddon

# Коды клавиатурных действий
ACTION_PREVIOUS_MENU = 10 # По умолчанию - ESC
ACTION_NAV_BACK = 92 # По умолчанию - Backspace

# Ссылка напубличный гугл календарь. Формат:
# "https://calendar.google.com/calendar/ical/******/basic.ics"
URL = ""

# Главный класс-контейнер

class MyAddon(xbmcgui.WindowDialog):

    def __init__(self):
        self.retval=0
        self.w=1280
        self.h=720

        self.background=xbmcgui.ControlImage(0,0,self.w,self.h,os.path.join(settings_addon.getAddonInfo('path'),'resources','media','background.jpg'),colorDiffuse='0xff777777')
        self.addControl(self.background)

        # Создаем текстовую надпись.
        self.label = xbmcgui.ControlLabel(780,200,1024,900, self.read_ical(), textColor='0xFFFFFFFF', font='Font_Neon_200')
        # Добавляем надпись в контейнер
        self.addControl(self.label)
        # Background
        self.buttonok=xbmcgui.ControlButton(self.w/2-100,self.h-80,200,30,settings_addon.getLocalizedString(id=30003),alignment=6)
        self.addControl(self.buttonok)


    def onControl(self, controlID):
        if controlID == self.buttonok:
            self.retval=0
            self.close()

    def onAction(self, action):
        # Если нажали ESC или Backspace...
        if action == ACTION_NAV_BACK or action == ACTION_PREVIOUS_MENU:
            # ...закрываем плагин.
            self.retval=0
            self.close()

    def cal_requested(self):
        url = URL
        try:
            p = urllib2.urlopen(url) #file
            return (p.read())
        except:
            print("Google Cal unreacheable!")
            return 0

    def read_ical(self):
        self.ical = Calendar.from_ical(self.cal_requested())
        self.status = ""
        self.array = []
        for component in self.ical.walk():
            if component.name == "VEVENT" and str(component.decoded('dtstart')) >= str(datetime.datetime.now()).split(" ")[0]:
                self.dt = component.get('dtstart').to_ical()
                self.summary = component.get('summary').to_ical()
                self.array.append([self.dt, self.summary])
        self.array.sort()

        for items in self.array:
            try: #Strange Bug In KODI http://forum.kodi.tv/showthread.php?pid=964973
                self.items_dt = (datetime.datetime.strptime(items[0].split("T")[0], '%Y%m%d')) #str -> date
            except TypeError:
                self.items_dt = datetime.datetime.fromtimestamp(time.mktime(time.strptime(items[0].split("T")[0], '%Y%m%d')))

            self.str_dt = (datetime.datetime.strftime(self.items_dt, '%d   %B')) # date -> str
            self.status = self.status + self.str_dt + "........." + items[1] + "\r\n"

        return self.status
settings_addon = xbmcaddon.Addon(id='plugin.program.events')
sys.path.append(os.path.join(settings_addon.getAddonInfo('path'), 'resources', 'lib' ))
sys.path.append(os.path.join(settings_addon.getAddonInfo('path')))

from icalendar import Calendar, Event

finished=0
while finished == 0:
    # Создаем экземпляр класса-контейнера.
    addon = MyAddon()
    # Выводим контейнер на экран.
    addon.doModal()
    if addon.retval == 0:
        finished = 1
    del addon
del settings_addon
