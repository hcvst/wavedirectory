# coding: utf-8
from gluon.serializers import json
from urllib import quote_plus as qp

@cache(request.env.path_info,time_expire=C_CACHE_WWW,cache_model=cache.ram)
def index():
    return dict()

@cache(request.env.path_info+request.env.query_string,
       time_expire=C_CACHE_API,cache_model=cache.ram)
def waves():
    try:
        version = int(request.vars.get(C_API_QS_VERSION))
        index = request.vars.get(C_API_QS_INDEX)
        order_by = request.vars.get(C_API_QS_ORDER, C_API_DEFAULT_ORDER)
        pagesize = int(request.vars.get(C_API_QS_PAGESIZE, C_API_DEFAULT_PAGESIZE))
    except:
        return T_API_INVALID_REQUEST
    if not version: return T_API_VERSION_REQUIRED 
    if version != C_API_VERSION: return T_API_UNKNOWN_VERSION
    if pagesize < 0: return T_API_PAGESIZE_TOO_SMALL
    if pagesize > C_API_MAX_SIZE: return T_API_PAGESIZE_TOO_LARGE
    waves, next_index = get_waves(order_by=order_by,
                                  pagesize=pagesize,
                                  index=index)
    if next_index:
        vars = request.vars
        vars[C_API_QS_INDEX] = next_index
        next_url = C_SERVER+URL(r=request, vars=vars)
    else:
        next_url = None
    d = dict()
    d['api'] = dict(api_name=C_API_NAME,
                    api_version=C_API_VERSION,
                    api_author='Hans Christian v. Stockhausen',
                    contact='http://xri.net/=hc',
                    twitter='http://twitter.com/wavedirectory',
                    wave_robot=C_BOT_ADDRESS)
    d['results'] = dict(next_url=next_url,
                        waves=[dict(waveid=w.key().name(),
                                    title=w.str_title,
                                    avatar=w.str_avatar,
                                    votes=w.str_votes,
                                    participants=w.str_participants,
                                    wave_url=C_WAVEBROWSER+\
                                    qp(qp(w.key().name())))
                               for w in waves])
    response.write(json(d),escape=False)
    response.headers['Content-Type']='text/json'
    response.body.seek(0)
    return response.body.read()
   
