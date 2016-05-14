#!/usr/bin/env python
import os
import random
from traceback import print_exc
from suds.client import Client
from suds.client import Client, sys
from suds.sax.element import Element
from suds.sax.attribute import Attribute
from suds.xsd.sxbasic import Import
from suds.wsse import UsernameToken, Security, Token, Timestamp
import logging


def payuMeaSetTransactionApiCall(args):
    urlToQuery = 'https://secure.payu.co.za/service/PayUAPI?wsdl'
    if args['store']['environment'] == 'staging':
        urlToQuery = 'https://staging.payu.co.za/service/PayUAPI?wsdl'

    client = Client(urlToQuery, faults=False)

    #------------------------------------- CREATING CUSTOM HEADER--------------------------------------

    wsse = ('wsse','http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd')

    mustAttributeSecurity = Attribute('SOAP-ENV:mustUnderstand', '1')
    addressAttributeSecurity = Attribute('xmlns:wsse', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd')
    AttributeUsernameToken1 = Attribute('wsu:Id','UsernameToken-9')
    addressAttributeUsernameToken = Attribute('xmlns:wsu','http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd')
    addressAttributePassword = Attribute('Type','http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText')

    msgUsername = Element('Username', ns=wsse).setText(args['store']['soapUsername'])
    msgPassword = Element('Password', ns=wsse).setText(args['store']['soapPassword']).append(addressAttributePassword)

    msgUsernameToken = Element('UsernameToken', ns=wsse)
    msgUsernameToken.append(AttributeUsernameToken1)
    msgUsernameToken.append(addressAttributeUsernameToken)
    msgUsernameToken.insert(msgPassword).insert(msgUsername)

    msgSecurity = Element('Security', ns=wsse).addPrefix(p='SOAP-ENC', u='http://www.w3.org/2003/05/soap-encoding')
    msgSecurity.append(mustAttributeSecurity)
    msgSecurity.append(addressAttributeSecurity)
    msgSecurity.insert(msgUsernameToken)

    client.set_options(soapheaders=[msgSecurity])

    #------------------------------------- CREATING SOAP CALL DETAILS HERE--------------------------------------
    transaction = {}
    transaction['Api'] = 'ONE_ZERO';
    transaction['Safekey'] = args['store']['safekey'];
    transaction['TransactionType'] = 'PAYMENT';
    transaction['AdditionalInformation'] = args['additionalInformation']
    transaction['Basket'] = args['basket']
    transaction['Customer'] = args['customer']

    #------------------------------------- DOING SOAP CALL HERE--------------------------------------
    setTransaction = client.service.setTransaction(** transaction)
    print(setTransaction)


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
        'additionalInformation': additional_info,
        'customer': customer,
    })
