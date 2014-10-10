from mixpanel import Mixpanel

from alphatracker.settings import MIXPANEL_TOKEN, DEBUG


def mixpanel_track(username, event, properties={}):
    if not DEBUG:
        mp = Mixpanel(MIXPANEL_TOKEN)
        mp.track(username, event, properties)