#!/usr/bin/python3

import urllib.request
from pathlib import Path
from lxml import etree
from datetime import datetime

def to_balanced_path(number: str, extension: str, depth: int = 3) -> Path:
    # credit for this idea: https://www.linkedin.com/in/martijnschiedon
    parts = list(number[-depth:][::-1])
    path = Path(*parts).joinpath(number).with_suffix(extension)

    return path


def oai_request(endpoint: str, payload: dict):
    url = endpoint
    first = True
    for key in payload:
        if first: 
            url = url + "?"
            first = False
        else: 
            url = url + "&"
        url = url + key + "=" + payload[key]
    
    print(url)

    result = urllib.request.urlopen(url)
    response = result.read()
#    response = result.read().decode() # sometimes this is needed. Don't know why yet.

    return response


def find_youngest_file_date(path: Path):
    last_mod_date = None
    if path.exists():
        for file in path.glob("**/*.xml"):
            mtime = file.stat().st_mtime
            file_last_mod_date = str(datetime.fromtimestamp(mtime).isoformat().split('T')[0])
            if last_mod_date < file_last_mod_date: last_mod_date = file_last_mod_date

    return last_mod_date


# initialize
# https://webservices.memorix.nl/a2a/20a181d4-c896-489f-9d16-20a3b7306b15?verb=ListRecords&metadataPrefix=a2a&set=dtb_trouwen

oai_endpoint          = "https://webservices.memorix.nl/a2a/20a181d4-c896-489f-9d16-20a3b7306b15"
oai_identifier_prefix = None
oai_payload           = { 'verb': 'ListRecords',
                            'metadataPrefix': 'a2a',
                            'set': 'dtb_trouwen' }
ext_path              = Path("extracted")
NS                    = { "oai": "http://www.openarchives.org/OAI/2.0/",
                          "a2a": "http://Mindbus.nl/A2A" }

# break after 'amount' requests, amounts = 0 means the script will run until resumptionTokens run out
amount = 0

# only request new records
# (that is: records that are available on the endpoint after the last file_date of the target directory)
from_date = find_youngest_file_date(ext_path)
if from_date is not None:
    oai_payload["from"] = from_date

while True:

    try:
        response = oai_request(oai_endpoint, oai_payload)
    except:
        print("OAI error")
        break

    try: 
        root = etree.XML(response)
    except etree.XMLSyntaxError as e:
        print(f"Parse error XML: {e}")
        break

    resources = root.xpath('/oai:OAI-PMH/oai:ListRecords/oai:record', namespaces=NS)
    for resource in resources:
        status = resource.find("oai:header", namespaces=NS).get('status')
        if status == 'deleted': continue
        record = resource.find("oai:metadata//a2a:A2A", namespaces=NS)
        oai_identifier = resource.find("oai:header/oai:identifier", namespaces=NS).text
        if oai_identifier_prefix is not None:
            identifier = oai_identifier.partition(oai_identifier_prefix)[2]
        else: identifier = oai_identifier
        file = ext_path.joinpath(to_balanced_path(identifier, '.xml'))
        file.parent.mkdir(exist_ok=True, parents=True)
        with open(file, "w") as xmlfile:
            xmlfile.write(etree.tostring(record, pretty_print=True).decode('utf-8'))
        print("written: " + str(file))

    resumption_token_element = root.find(".//oai:resumptionToken", namespaces=NS)
    amount = amount - 1
    if amount == 0: resumption_token_element = None
    if resumption_token_element is not None:
        oai_payload = {'verb': 'ListRecords'}
        oai_payload["resumptionToken"] = resumption_token_element.text
    else: break

print('done')
