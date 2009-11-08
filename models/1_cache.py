# coding: utf-8
# Hans Christian v. Stockhausen, hc@vst.io, 2009-11-05

from gluon.contrib.memdb import *
from gluon.contrib.gae_memcache import MemcacheClient
from google.appengine.api.memcache import Client

cache.ram=cache.disk=MemcacheClient(request) 
session.connect(request,response,db=MEMDB(Client())) 