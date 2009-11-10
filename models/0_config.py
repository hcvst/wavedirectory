# coding: utf-8
# Hans Christian v. Stockhausen, hc@vst.io, 2009-11-05

# Configuration constants
C_RECOVERY_MODE = False # insert waves into db outside robot.OnWaveletSelfAdded
                       # use after dropping DB to allow Gadget and OnParticipantsChanged
                       # to repopulate the DB. 

C_SERVER = 'http://wavedirectory.appspot.com'
C_NOTITLE = 'No title'
C_NOAVATAR = C_SERVER + URL(r=request, c='static', f='media/avatar_unknown.png')
C_PUBLIC_ADDRESS = 'public@a.gwave.com'
C_WAVEBROWSER = 'https://wave.google.com/wave/#restored:wave:'
C_BOT_NAME = 'Wavedirectory.net'
C_BOT_VERSION = '5'
C_BOT_AVATAR = C_SERVER + URL(r=request, c='static', f='media/avatar.png')
C_BOT_PROFILE = C_SERVER
C_BOT_ADDRESS = 'wavedirectory@appspot.com'

C_GADGET_URL = C_SERVER + URL(r=request, c='gadget', f='wavedirectory.xml')

# caching
C_CACHE_WWW = 30 #sec
C_CACHE_API = 30 #sec

# results and results ordering
C_PAGESIZE = 20
C_VOTES = 'v'
C_PARTICIPANTS = 'p'
C_ADDED = 'a'
C_ORDERING = {C_VOTES:'_str_votes',
              C_PARTICIPANTS:'_str_participants',
              C_ADDED:'str_timestamp'}
C_DEFAULT_ORDER = C_PARTICIPANTS

#API
C_API_NAME = 'wavedirectory.net'
C_API_VERSION = 1
C_API_QS_VERSION = 'v'
C_API_QS_INDEX = 'i'
C_API_QS_ORDER = 'o'
C_API_DEFAULT_ORDER = C_VOTES
C_API_QS_PAGESIZE = 's'
C_API_DEFAULT_PAGESIZE = 50
C_API_MAX_SIZE = 250


# Text constants
T_ONLY_OWNER = """Sorry, only the wave owner may add this robot. Could you please remove
this bot from the list of participants and ask the owner to add %s in order for this wave
to be listed at wavedirectory.net. Thank you.""" % C_BOT_ADDRESS
T_ONLY_ROOT_WAVELET = "Sorry, private replies cannot be added to wavedirectory.net."
T_API_VERSION_REQUIRED = "Error: Please specify an API version with ?%s." % C_API_QS_VERSION
T_API_PAGESIZE_TOO_SMALL = "The pagesize you requested is too small."
T_API_PAGESIZE_TOO_LARGE = "The pagesize you requested is too large (max: %s)." % C_API_MAX_SIZE 
T_API_UNKNOWN_VERSION = "The version you specified is unknown."
T_API_INVALID_REQUEST = "There is a problem with your request."