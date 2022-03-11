FROM python:3.8.10

COPY idm_lp /opt/idm_lp
RUN python -m pip install -U idm_lp
CMD python -m idm_lp --config_path /opt/idm_lp/config.json