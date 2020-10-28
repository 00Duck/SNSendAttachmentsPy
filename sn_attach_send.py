"""
ServiceNow Attachment Sender in Python

Purpose:
    Sends attachments to ServiceNow. The name of the attachment must correspond to a unique value on the record.

Example Prerequisites:
    Attachment names in example must contain the number of a corresponding record. EX: INC12345.html
    Attachments are all contained in the same folder
    Attachments are all .html
    dir_loc, instance, and Authorization header are populated along with table and query in getRecInfo

Output:
    Each send or failure to send is logged to the console in a format that can be easily grep'd
    An attachment magically appears on the record founds in ServiceNow. Ex: INC12345

Execution:
    - Ensure Python3 is installed
    - Clone project to a folder on your computer
    - Activate the virtual environment by navigating to the top folder and typing source bin/activate
    - Deactivate the environment when you are finished by typing deactivate
"""

import os, requests, json, datetime

#provide filepath to attachments
dir_loc = r"./example"
#provide hostname without "service-now.com" domain
instance = 'instancename'
#provide Authorization format: Basic 123456
header = {'Authorization': '', 'Accept': 'application/json'}

def logMsg(level, msg):
    ts = datetime.datetime.now()
    print('{}\t{}\t{}'.format(ts, level, msg))

def sendFile(table, sys_id, file_name):
    file_header = header
    file_header['Content-Type'] = "text/html"
    path = os.path.join(dir_loc, file_name)
    base_url = 'https://{}.service-now.com/api/now/attachment/file'.format(instance)
    uri = base_url + '?table_name={}&table_sys_id={}&file_name={}'.format(table, sys_id, file_name)

    try:
        with open(path, 'rb') as f:
            logMsg('INFO', 'Sending {} to {} in {}'.format(file_name, sys_id, table))
            r = requests.post(uri, headers = file_header, data = f.read())
    except:
        logMsg('ERROR', 'Error sending {}'.format(file_name))


def getRecInfo(name):
    #modify this to be the base table you need to get info from. Pulling sys_class_name gets us the extended table name if there is one
    table = ''
    query = 'number={}&sysparm_limit=1'.format(name)
    uri = 'https://{}.service-now.com/api/now/table/{}?sysparm_query={}&sysparm_fields=sys_id,sys_class_name'.format(instance, table, query)
    r = requests.get(uri, headers = header)
    if r.status_code == 200:
        resp = json.loads(r.text)
        if len(resp['result']) >= 1:
            sys_id = resp['result'][0]['sys_id']
            table = resp['result'][0]['sys_class_name']
            sendFile(table, sys_id, name + '.html') #add back the file extension. Obviously, change this if we use for more than .html
        else:
            logMsg('ERROR', 'No SN record found for {}'.format(file_name))
    else:
        logMsg('ERROR', 'Status {}: Failed to retrieve SN record for {}'.format(r.status_code, name))
    return ''

for file_name in os.listdir(dir_loc):
    html_inx = file_name.find('.html')
    if html_inx != -1:
        getRecInfo(file_name[0:html_inx])

