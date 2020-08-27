from error_handlers import captha
from error_handlers import rps

error_handlers_bp = (
    rps.user,
    captha.user,
)
