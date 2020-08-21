from error_handlers import rps
from error_handlers import captha


error_handlers_bp = (
    rps.user,
    captha.user,
)