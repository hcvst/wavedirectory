# coding: utf-8
# Hans Christian v. Stockhausen, hc@vst.io, 2009-11-05

# NOTE: This bot uses a modified waveapi - one that
# calls the handlers with 'event' instead of 'properties'
# to gain access to the event.modifiedBy attribute
# see Wiki at Github for details
# It also uses a slightly modified version of web2py to
# deal with a wsgi bug.

import logging
import urllib
from google.appengine.ext import webapp
robot = local_import('waveapihcvst.robot')
document = local_import('waveapihcvst.document')

class MyRobot(robot.Robot):

    def __init__(self, controller_path):
        self.controller_path = controller_path
        robot.Robot.__init__(self, C_BOT_NAME,
            version = C_BOT_VERSION,
            image_url = C_BOT_AVATAR,
            profile_url = C_BOT_PROFILE)
        self.RegisterListener(self)
            
    def _get_wsgi_app(self):
        p = self.controller_path
        return webapp.WSGIApplication([
            ('%s/capabilities.xml' % p,
             lambda: robot.RobotCapabilitiesHandler(self)),
            ('%s/robot/profile' % p,
             lambda: robot.RobotProfileHandler(self)),
            ('%s/robot/jsonrpc' % p,
            lambda: robot.RobotEventHandler(self)),
            ], debug=False)
    
    app = property(_get_wsgi_app)    
        
    def _reply(self, blip, message):
        inline_bp = blip.GetDocument().AppendInlineBlip()
        inline_bp.GetDocument().SetText(message)
    
    def _install(self, context, wl):
        blip = context.GetBlipById(wl.GetRootBlipId())
        url = '%s?w=%s&c=%s' % (C_GADGET_URL,
                                urllib.quote_plus(blip.GetWaveId()),
                                blip.GetCreator())
        gadget = document.Gadget(url=url)
        blip.GetDocument().AppendElement(gadget)
    
    def OnWaveletSelfAdded(self, event, context):
        pp = event.properties
        bp_id = pp['blipId']
        bp = context.GetBlipById(bp_id)
        root_wl = context.GetRootWavelet()
        if root_wl:
            wl = root_wl
            if wl.GetCreator() == event.modifiedBy:
                wave = Wave(key_name = wl.GetWaveId())
                if wl.GetTitle(): wave.str_title = wl.GetTitle()
                wave.str_creator = wl.GetCreator()
                wave.str_participants = len(wl.GetParticipants())-1
                wave.put()
                wl.AddParticipant(C_PUBLIC_ADDRESS)
                self._install(context, wl)
            else:
                self._reply(bp, T_ONLY_OWNER)
                #wl.RemoveSelf() not yet implemented by Google 2009-10-31
        else:
            wl_id = bp.GetWaveletId()
            wl = context.GetWaveletById(wl_id)
            self._reply(bp, T_ONLY_ROOT_WAVELET)
            #wl.RemoveSelf()
     
    def OnWaveletParticipantsChanged(self, event, context):
        wl = context.GetRootWavelet()
        wave_id = wl.GetWaveId()
        wave = Wave.get_by_key_name(wave_id)
        if not wave:
            if C_RECOVERY_MODE:
                wave = Wave(key_name = wave_id)
            else:
                return
        if wl.GetTitle(): wave.str_title = wl.GetTitle()
        wave.str_participants = len(wl.GetParticipants())-2
        wave.put()

        
#web2py controller function
# change web2py/routes.py to redirect http://.../_wave to process()
def process():
    bot = MyRobot(controller_path = URL(r=request))
    bot.app(request.wsgi.environ, request.wsgi.start_response)
    return response.body.getvalue()