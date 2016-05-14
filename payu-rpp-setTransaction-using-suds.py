#!/usr/bin/env python

from suds.client import Client
from suds.sax.element import Element
from suds.sax.attribute import Attribute


wsse = ('wsse', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd')


def payuMeaSetTransactionApiCall(args):
    username_token = Element('UsernameToken', ns=wsse)
    username = Element('Username', ns=wsse).setText(args['store']['soapUsername'])
    password = Element('Password', ns=wsse).setText(args['store']['soapPassword'])
    password.append(
        Attribute('Type', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText')
    )
    username_token_things = [
        username,
        password,
        Attribute('wsu:Id', 'UsernameToken-9'),
        Attribute('xmlns:wsu', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd'),
    ]
    for thing in username_token_things:
        username_token.append(thing)

    security = Element('Security', ns=wsse).addPrefix(p='SOAP-ENC', u='http://www.w3.org/2003/05/soap-encoding')
    security_things = [
        username_token,
        Attribute('SOAP-ENV:mustUnderstand', '1'),
        Attribute('xmlns:wsse', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd')
    ]
    for thing in security_things:
        security.append(thing)

    transaction = {
        'Api': 'ONE_ZERO',
        'Safekey': args['store']['safekey'],
        'TransactionType': 'PAYMENT',
        'AdditionalInformation': args['additional_info'],
        'Basket': args['basket'],
        'Customer': args['customer']
    }

    url = 'https://secure.payu.co.za/service/PayUAPI?wsdl'
    if args['store']['environment'] == 'staging':
        url = 'https://staging.payu.co.za/service/PayUAPI?wsdl'

    client = Client(url, faults=False)
    client.set_options(soapheaders=[security])
    results = client.service.setTransaction(**transaction)
    print(results)


if __name__ == '__main__':
    store = {
        'soapUsername': 'Staging Integration Store 1',
        'soapPassword': '78cXrW1W',
        'safekey': '{45D5C765-16D2-45A4-8C41-8D6F84042F8C}',
        'environment': 'staging',
    }
    basket = {
        'description': 'Some basket description',
        'amountInCents': '100',
        'currencyCode': 'ZAR',
    }
    additional_info = {
        'merchantReference': 123,
        'returnUrl': 'http://eg.com/return',
        'cancelUrl': 'http://eg.com/cancel',
        'supportedPaymentMethods': 'CREDITCARD',
    }
    customer = {
        'merchantUserId': '7',
        'email': 'john@doe.com',
        'firstName': 'John',
        'lastName': 'Doe',
        'mobile': '123455666',
    }

    payuMeaSetTransactionApiCall({
        'store': store,
        'basket': basket,
        'additional_info': additional_info,
        'customer': customer,
    })
