from celery.task import task
from simple_salesforce import Salesforce

from revolv.settings import SFDC_ACCOUNT, SFDC_PASSWORD, SFDC_TOKEN, SFDC_REVOLV_DONATION, SFDC_REVOLV_SIGNUP
from django.utils import log

logger = log.getLogger(__name__)

INTERVAL = 10 * 60 #10 minutes
MAX_RETRIES = 100


class SFDCException(Exception):
    pass


@task
def send_signup_info( name, email, address=''):
    try:
        res = None
        payload = {'donorName': name, 'email': email, 'donorAddress': address}
        sf = Salesforce(username=SFDC_ACCOUNT, password=SFDC_PASSWORD, security_token=SFDC_TOKEN)
        logger.info('send sign-up to SFDC with data: %s', payload)
        res = sf.apexecute(SFDC_REVOLV_SIGNUP, method='POST', data=payload)
        if res.lower() != 'success':
            raise SFDCException(res)
        logger.info('SFDC sign-up: sucess.')
    except Exception as e:
        logger.error('SFDC sign-up: ERROR for name: %s and data: %s, res: %s', name, payload, res, exc_info=True)
        send_signup_info.retry(args=[name, email, address], countdown=INTERVAL, exc=e, max_retries=MAX_RETRIES)


@task
def send_donation_info(name, amount, project, address=''):
    try:
        res = None
        payload = {'donorName': name, 'projectName': project, 'donationAmount': amount, 'donorAddress': address}
        sf = Salesforce(username=SFDC_ACCOUNT, password=SFDC_PASSWORD, security_token=SFDC_TOKEN)
        logger.info('send donation to SFDC with data: %s', payload)
        res = sf.apexecute(SFDC_REVOLV_DONATION, method='POST', data=payload)
        if res.lower() != 'success':
            raise SFDCException(res)
        logger.info('SFDC donation: success.')
    except Exception as e:
        logger.error('SFDC donation: ERROR for name: %s and data: %s, res: %s', name, payload, res, exc_info=True)
        send_donation_info.retry(args=[name, amount, project, address], countdown=INTERVAL, exc=e,
                                 max_retries=MAX_RETRIES)