from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
  # Call REST framework's default exception handler first,
  # to get the standard error response.
  response = exception_handler(exc, context)

  if response is not None:
    handlers = {
      'cooperative.create': create_cooperative_handler
    }
    error_view = context['view'].basename + "." + context['view'].action
    error_handler = handlers.get(error_view)
    if error_handler is not None:
      return error_handler(response)

  return response

def create_cooperative_handler(response):
  if 'recaptcha' in response.data.keys():
    response.data = {'ERROR_CODE': 'INVALID_RECAPTCHA'}

  if 'business_name' in response.data.keys():
    response.data = {'ERROR_CODE': 'COOPERATIVE_ALREADY_EXISTS'}

  if 'email' in response.data.keys():
    response.data = {'ERROR_CODE': 'EMAIL_ALREADY_EXISTS'}

  return response