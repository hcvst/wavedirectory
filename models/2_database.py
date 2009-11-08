# coding: utf8
# Hans Christian v. Stockhausen, hc@vst.io, 2009-11-05
# Using GAE's db directly instead of w2p's excellent DBA to store
# a wave's id direclty in key_name

# Badly hacked somebody please help sort this out :)

import re
from datetime import datetime
from functools import partial
from google.appengine.ext import db



class Wave(db.Model):
    
    ts = re.sub(r'[^0-9]', '',str(datetime.now())) # timestamp
    str_title = db.StringProperty(required=True, default=C_NOTITLE)
    str_snippet = db.StringProperty()
    str_creator = db.StringProperty()
    str_avatar = db.StringProperty(required=True, default=C_NOAVATAR)
    _str_participants = db.StringProperty(required=True, default='00000000-'+ts)
    _str_votes = db.StringProperty(required=True, default='00000000-'+ts)
    dt_added = db.DateTimeProperty(auto_now_add=True)
    dt_activity = db.DateTimeProperty(auto_now=True)
    bool_show = db.BooleanProperty(required=True, default=True)
    str_timestamp = db.StringProperty(default=ts)
    
    # Participants and votes are stored as "hex|timestamp" where hex 
    # is the vote count as hex. This setup is needed (at least I could not
    # find a better method) to sort and page through data.
    
    def _set_participants(self, value):
        self._str_participants = '%08X-%s' % (int(value), self.str_timestamp)
        
    def _get_participants(self):
        return str(int(self._str_participants.split('-')[0],16))
    
    # votes can be negative
    def _set_votes(self, value):
        v = int(value)
        if v < 0:
            v = 0xFFFFFFF + v
            self._str_votes = '-%07X-%s' % (v, self.str_timestamp)
        else:
            self._str_votes = '%08X-%s' % (v, self.str_timestamp)
        
    def _get_votes(self):
        votes = self._str_votes 
        if votes.startswith('-'):
            _, v, _ = votes.split('-')
            value = -(0xFFFFFFF - int(v,16))
        else:
            value = int(votes.split('-')[0],16)
        return str(value)
        
    str_participants = property(_get_participants, _set_participants) 
    str_votes = property(_get_votes, _set_votes)
    

    
def get_waves(order_by, descending=True, pagesize=C_PAGESIZE, index=None):
    order_prefix = '-' if descending else ''
    order_field = C_ORDERING[order_by]
    query = Wave.all().order(order_prefix+order_field)
    if index:
        query.filter(order_field +
                     ' <=' if descending else ' >', 
                     index)
    waves = query.fetch(pagesize+1)
    if len(waves) == pagesize+1:
        next_index = waves[-1].__getattribute__(order_field)
        waves = waves[:pagesize]
    else:
        next_index = None
    return waves, next_index   