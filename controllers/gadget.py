# coding: utf-8
# Hans Christian v. Stockhausen, hc@vst.io, 2009-11-05
import urllib


def wavedirectory():
    return dict(encoded_waveid = urllib.quote_plus(request.vars.get('w')),
                creator = request.vars.get('c'))

def update():
    wave_id = request.vars.get('w')
    wave = Wave.get_by_key_name(wave_id)
    if not wave:
        if C_RECOVERY_MODE:
            wave = Wave(key_name = wave_id)
        else:
            return
    if request.vars.get('t'):
        wave.str_avatar = request.vars.get('t')
    wave.str_votes = request.vars.get('v', '0')
    wave.put()