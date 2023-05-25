from split_settings.tools import include
from decouple import config


base_settings = ['base.py',
                 'social.py',
                 ]
   
   
include(*base_settings)
