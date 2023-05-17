from .forms import UserAuthentication, UserRegistration, UserPasswordReset

def get_forms(request):
   forms = {
      "user_log_form": UserAuthentication(),
      "user_reg_form": UserRegistration(),
      "reset_pass_form": UserPasswordReset(),
   }
   return forms