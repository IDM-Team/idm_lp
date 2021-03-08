from error_handlers import access_token
from error_handlers import captha
from error_handlers import rps

error_handlers_bp = (
    access_token.user,
    rps.user,
    captha.user,
)
