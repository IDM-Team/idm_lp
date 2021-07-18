from idm_lp.error_handlers import access_token, captha, rps

error_handlers_bp = (
    access_token.user,
    rps.user,
    captha.user,
)
