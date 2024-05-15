# Embedded file name: ./lsr.py
import BigWorld
import ResMgr, Keys
from PlayerEvents import g_playerEvents
from helpers import getClientLanguage
import sys, os
curTime = None
LaserModActive = True
ColoredLaserModActive = True

def CheckVersion():
    import Account
    funcs = dir(Account.PlayerAccount)
    import re
    for s in funcs:
        if not str(s).find('version') == -1:
            return int(re.sub('[^\\d-]+', '', s))


if not hasattr(BigWorld, 'Version'):
    BigWorld.Version = CheckVersion()

def DebugMsg087(textRU, textEN = '', doHighlight = False):
    from helpers import getClientLanguage
    if getClientLanguage() == 'ru':
        text = textRU
    else:
        text = textEN
    player = BigWorld.player()
    import Avatar, Account
    if player is not None:
        if type(BigWorld.player()) is Account.PlayerAccount:
            from gui import SystemMessages
            SystemMessages.pushI18nMessage(text, type=SystemMessages.SM_TYPE.Information)
        elif type(BigWorld.player()) is Avatar.PlayerAvatar:
            from messenger.gui import MessengerDispatcher
            MessengerDispatcher.g_instance.battleMessenger.addFormattedMessage(text, doHighlight, False)
    return


def DebugMsg088(textRU, textEN = '', color = '#00cdcd'):
    from helpers import getClientLanguage
    if getClientLanguage() == 'ru':
        text = textRU
    else:
        text = textEN
    player = BigWorld.player()
    htmlMessage = "<font color='{color}'>{text}</font>".format(color=color, text=text)
    import Avatar, Account
    if player is not None:
        if type(BigWorld.player()) is Account.PlayerAccount:
            from gui import SystemMessages
            SystemMessages.pushI18nMessage(htmlMessage, type=SystemMessages.SM_TYPE.Information)
        elif type(BigWorld.player()) is Avatar.PlayerAvatar:
            from messenger import MessengerEntry
            MessengerEntry.g_instance.gui.addClientMessage(htmlMessage)
    return


if not hasattr(BigWorld, 'DebugMsg'):
    if BigWorld.Version == 8701:
        BigWorld.DebugMsg = DebugMsg087
    else:
        BigWorld.DebugMsg = DebugMsg088
entries = {}

def initLasers():
    global ColoredLaserModActive
    global curTime
    global entries
    global LaserModActive
    import Account
    if hasattr(BigWorld.player(), 'isOnArena'):
        if BigWorld.player().isOnArena:
            if curTime is None or curTime + 1 < BigWorld.time():
                if BigWorld.isKeyDown(Keys.KEY_NUMPAD8):
                    curTime = BigWorld.time()
                    if LaserModActive:
                        LaserModActive = False
                        BigWorld.DebugMsg('\xd0\x9b\xd0\xb0\xd0\xb7\xd0\xb5\xd1\x80\xd0\xbd\xd0\xb0\xd1\x8f \xd1\x83\xd0\xba\xd0\xb0\xd0\xb7\xd0\xba\xd0\xb0 \xd0\xb2\xd1\x8b\xd0\xba\xd0\xbb\xd1\x8e\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb0', 'Laser Sight Mod ON')
                    else:
                        LaserModActive = True
                        BigWorld.DebugMsg('\xd0\x9b\xd0\xb0\xd0\xb7\xd0\xb5\xd1\x80\xd0\xbd\xd0\xb0\xd1\x8f \xd1\x83\xd0\xba\xd0\xb0\xd0\xb7\xd0\xba\xd0\xb0 \xd0\xb2\xd0\xba\xd0\xbb\xd1\x8e\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb0', 'Laser Sight Mod OFF')
                if BigWorld.isKeyDown(Keys.KEY_NUMPAD7):
                    curTime = BigWorld.time()
                    if ColoredLaserModActive:
                        ColoredLaserModActive = False
                        BigWorld.DebugMsg('\xd0\xa6\xd0\xb2\xd0\xb5\xd1\x82\xd0\xbd\xd0\xb0\xd1\x8f \xd1\x83\xd0\xba\xd0\xb0\xd0\xb7\xd0\xba\xd0\xb0 \xd0\xb2\xd1\x8b\xd0\xba\xd0\xbb\xd1\x8e\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb0', 'Colored Laser ON')
                    else:
                        ColoredLaserModActive = True
                        BigWorld.DebugMsg('\xd0\xa6\xd0\xb2\xd0\xb5\xd1\x82\xd0\xbd\xd0\xb0\xd1\x8f \xd1\x83\xd0\xba\xd0\xb0\xd0\xb7\xd0\xba\xd0\xb0 \xd0\xb2\xd0\xba\xd0\xbb\xd1\x8e\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb0', 'Colored Laser OFF')
            import Vehicle
            if LaserModActive:
                playerHealth = BigWorld.player().vehicleTypeDescriptor.maxHealth
                for v in BigWorld.entities.values():
                    if type(v) is Vehicle.Vehicle:
                        if v.isAlive():
                            if v.publicInfo['team'] is not BigWorld.player().team:
                                if not entries.has_key(v.id):
                                    if ColoredLaserModActive:
                                        shotsToKill = playerHealth / v.typeDescriptor.gun['shots'][0]['shell']['damage'][0]
                                        if shotsToKill < 3.0:
                                            laserColor = 'red'
                                        elif shotsToKill > 8.0:
                                            laserColor = 'green'
                                        else:
                                            laserColor = 'yellow'
                                    else:
                                        laserColor = 'red'
                                    listi = v.appearance
                                    newModel = BigWorld.Model('objects/%sgun.model' % laserColor)
                                    servo = BigWorld.Servo(listi.modelsDesc['gun']['model'].matrix)
                                    newModel.addMotor(servo)
                                    entries[v.id] = dict({'model': newModel,
                                     'vehicle': v,
                                     'lasttime': BigWorld.time()})
                                    v.addModel(newModel)
                                else:
                                    entries[v.id]['lasttime'] = BigWorld.time()

            currentTime = BigWorld.time()
            for k in entries.keys():
                if entries[k]['lasttime'] + 0.5 < currentTime or not LaserModActive:
                    ModelToDel = entries[k]
                    try:
                        ModelToDel['vehicle'].delModel(ModelToDel['model'])
                    except:
                        pass

                    del entries[k]

    if type(BigWorld.player()) is not Account.PlayerAccount:
        BigWorld.callback(0.1, lambda : initLasers())
    return


def reloadLasers():
    global entries
    aih = BigWorld.player().inputHandler
    if not hasattr(aih, 'ctrl'):
        BigWorld.callback(0.1, lambda : reloadLasers())
    else:
        entries = {}
        initLasers()


g_playerEvents.onAvatarReady += reloadLasers