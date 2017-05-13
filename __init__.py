# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.


import time
from os.path import dirname
import json
import requests

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'ruggedy'

LOGGER = getLogger(__name__)


class RandomBibleSkill(MycroftSkill):
    def __init__(self):
        super(RandomBibleSkill, self).__init__(name="RandomBibleSkill")
        self.process = None

    def initialize(self):
        intent = IntentBuilder("RandomBibleIntent").require(
            "RandomBibleKeyword").build()
        self.register_intent(intent, self.handle_intent)

    def handle_intent(self, message):
        try:
            response = requests.get('http://www.ourmanna.com/verses/api/get/?format=json&order=random')
            data = response.json()
            self.speak_dialog('bible')
            time.sleep(1)
	    self.speak(data["verse"]["details"]["reference"])	
            self.speak(data["verse"]["details"]["text"])   

        except Exception as e:
            LOGGER.error("Error: {0}".format(e))

    def stop(self):
        if self.process and self.process.poll() is None:
            self.speak_dialog('bilbe.stop')
            self.process.terminate()
            self.process.wait()


def create_skill():
    return RandomBibleSkill()
