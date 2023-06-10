from split_settings.tools import include
import os


base_settings = ["base.py",               # standard django settings
                 "social_settings.py",    # social_auth
                 "email_settings.py",     # smpt
                 ]
   
include(*base_settings)
