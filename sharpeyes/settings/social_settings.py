SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_EMAIL_FORM_URL = '/login-form/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '948248851315-fligescr1aqrbsiudief96o9kujt8itp.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
SOCIAL_AUTH_TELEGRAM_BOT_TOKEN = '5777561664:AAEM6PVmJ689eUbSQXtHO4z502u0HDNCc5M'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',       #user attributes(description)
    #'social_core.pipeline.social_auth.social_uid',
    'mainapp.pipeline.social_uid_lower',
    #'social_core.pipeline.social_auth.auth_allowed',        #this is where emails and domains whitelists are applied (if defined).
    'social_core.pipeline.social_auth.social_user',          #checking an existing user
    #'social_core.pipeline.user.get_username',
    #'social_core.pipeline.social_auth.associate_by_email',  #social accounts association 
    'mainapp.pipeline.custom_associate_by_email',            #custom social accounts association 
    'mainapp.pipeline.email_preparation',                    #custom pipeline for telegram email field
    'social_core.pipeline.user.create_user',
    'mainapp.pipeline.user_social_activate',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'social.pipeline.disconnect.allowed_to_disconnect',
    'social.pipeline.disconnect.get_entries',
    'social.pipeline.disconnect.revoke_tokens',
    'social.pipeline.disconnect.disconnect',
    'mainapp.pipeline.stay', 
)