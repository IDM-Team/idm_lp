FROM python:3.8.10

RUN python -m pip install -U idm_lp
CMD ["python", "-m", "idm_lp"]