# coding: utf-8
# Hans Christian v. Stockhausen, hc@vst.io, 2009-11-05
import binascii
from urllib import quote_plus as qp

@cache(request.env.path_info,time_expire=C_CACHE_WWW,cache_model=cache.ram)
def index():
    try:
        order_by = request.args[0]
    except IndexError:
        order_by = C_DEFAULT_ORDER
    try:
        index = request.args[1]
    except IndexError:
        index = None

    waves, next_index = get_waves(order_by, index=index)
    next_page = URL(r=request, args=[order_by, next_index]) if \
                next_index else None
    d = dict(hexlify=binascii.hexlify, waves=waves,
             next_page=next_page, order_by=order_by)
    return response.render(d)

@cache(request.env.path_info,time_expire=C_CACHE_WWW,cache_model=cache.ram)
def wave():
    try:
        waveid = binascii.unhexlify(request.args[0])
    except IndexError:
        #?w= old query string method supported
        waveid = urllib.unquote_plus(request.vars.get('w'))
    if not waveid:
        return 'No waveid specified'
    return dict(waveid=waveid,
                quoted_waveid=qp(qp((waveid)))) # no idea why i need to quote twice

# create some testdata
#def testdata():
    #import random
    #import re
    #for i in range(20):
        #x = str(i)
        #w = Wave(key_name = x)
        #w.str_title = "Hallo " + x
        #w.str_votes = random.randint(0,100)
        #w.str_participants = random.randint(0,100)
        #w.str_timestamp = re.sub(r'[^0-9]', '',str(datetime.now()))
        #w.put()