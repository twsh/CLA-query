#!/usr/bin/env python3

import argparse
import cla_data
import cla_functions
import datetime
import logging
import openpyxl
import os
import requests


code_to_licence_type = cla_data.code_to_licence_type
code_to_usage_type = cla_data.code_to_usage_type
headers_to_messages = cla_data.headers_to_messages

if __name__ == "__main__":
    logging.basicConfig(filename='cla.log', filemode='w', level=logging.DEBUG)
    parser = argparse.ArgumentParser(
        description="Lookup ISBNs using the CLA's API."
    )
    parser.add_argument(
        'excel',
        help='The Excel workbook'
    )
    parser.add_argument(
        '--LicenceType',
        '-L',
        dest='licence_type',
        action='store',
        default='136',
        choices=sorted([x for x in code_to_licence_type]),
        help='The licence type (defaults to 136)'
    )
    parser.add_argument(
        '--UsageType',
        '-U',
        dest='usage_type',
        action='store',
        default='2',
        choices=sorted([x for x in code_to_usage_type]),
        help='The licence type (defaults to 2)'
    )
    parser.add_argument(
        '--ISBNname',
        '-I',
        dest='ISBN_name',
        action='store',
        default='ISBN',
        help='The name of the ISBN column.'
    )
    parser.add_argument(
        '--key',
        '-K',
        dest='key',
        action='store',
        default='key.txt',
        help='The name of the key file.'
    )
    args = parser.parse_args()
    list_of_extensions = ['xlsx', 'xls']
    path = cla_functions.check_extensions(args.excel, list_of_extensions)
    excel = openpyxl.load_workbook(path)
    licence_type = args.licence_type
    usage_type = args.usage_type
    ISBN_name = args.ISBN_name
    if cla_functions.check_for_integers(excel, ISBN_name) is True:
        print(
            'The input workbook has ISBNs formatted as numbers. '
            'This can cause problems when ISBNs have leading zeros.'
        )
    with open(args.key, 'r') as key_file:
        key = key_file.read().strip()
    list_of_ISBNs = cla_functions.get_ISBNs(excel, ISBN_name)
    logging.info('list_of_ISBNs: ' + str(list_of_ISBNs))
    ISBNs_to_headers = {}
    for x in list_of_ISBNs:
        payload = """<?xml version="1.0" encoding="utf-8"?>
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
        <soap12:Body>
        <GetPermissionByIdentifier xmlns="http://titlelookup.cla.co.uk/public/lookupapi/v1/">
        <RequestParameters>
        <RequestParameters xmlns="">
        <RequestSystem>{}</RequestSystem>
        <Identifier>{}</Identifier>
        <LicenceType>{}</LicenceType>
        <UsageType>{}</UsageType>
        </RequestParameters>
        </RequestParameters>
        </GetPermissionByIdentifier>
        </soap12:Body>
        </soap12:Envelope>
        """.format(key, x, licence_type, usage_type)
        logging.info(payload)
        response = requests.post(
            url='http://titlelookup.cla.co.uk/Public/lookupapi/v1/lookup.asmx',
            data=payload,
            headers={
                'Content-type': 'application/soap+xml; charset=utf-8'
            }
        )
        logging.info(response.text)
        logging.info('Status code: ' + str(response.status_code))
        if response.status_code == requests.codes.ok:
            if 'PositiveHeader' in response.text:
                ISBNs_to_headers.update(
                    {x: headers_to_messages['PositiveHeader']}
                )
            elif 'NegativeHeader' in response.text:
                ISBNs_to_headers.update(
                    {x: headers_to_messages['NegativeHeader']}
                )
            elif 'WarningHeader' in response.text:
                ISBNs_to_headers.update(
                    {x: headers_to_messages['WarningHeader']}
                )
            elif 'NeutralHeader' in response.text:
                ISBNs_to_headers.update(
                    {x: headers_to_messages['NeutralHeader']}
                )
            else:
                ISBNs_to_headers.update({x: 'Null'})
            if '<StatusCode>SUCCESS</StatusCode>' in response.text:
                pass
            elif '<StatusCode>INVALID_REQUEST_SYSTEM</StatusCode>' in response.text:
                raise ResponseError('The database did not except your key!')
        else:
            print(
                'Something went wrong with request {}! '
                'The error code was: {}.'.format(
                    x,
                    response.status_code
                )
            )
    logging.info('ISBNs_to_headers: ' + str(ISBNs_to_headers))
    cla_functions.write_responses(
        excel,
        ISBNs_to_headers,
        ISBN_name
    ).save(
        os.path.splitext(path)[0]
        + '_'
        + datetime.date.today().isoformat()
        + os.path.splitext(path)[1]
    )
    print(
        "I checked licence type {}: '{}', and usage type {}: '{}'.".format(
            licence_type,
            code_to_licence_type[licence_type],
            usage_type,
            code_to_usage_type[usage_type]
        )
    )
