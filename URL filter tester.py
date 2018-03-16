import tkinter as tk
import urllib.request
import requests
import os
import xml.etree.ElementTree as et
import os
import datetime

def setup():
    now = datetime.datetime.now()

    year = str(now.year)
    month = str(now.month)
    date = str(now.day)
    hour = str(now.hour)
    min = str(now.minute)
    sec = str(now.second)
    time = 'on %s %s %s @ %sH %sM %sS' % (year, month, date, hour, min, sec)
    global file_name
    file_name = 'Shield results %s' % time

    print(os.curdir)
    os.mkdir(file_name)
    current_dir = os.getcwd()

    global path
    path = current_dir + '/' + file_name + '/'

def input_verification(test_url, path, test_case):
    test = "https://"
    if test not in test_url:
        error_report = path + '/' + test_case + '_error_erport.txt'
        with open(error_report, 'a+') as f:
            f.write(test_url)
        return 0
    else:
        return 1

def URL_filter():

    setup()
    URLoutputfile = path+'/URLreport.txt'

    with open(URLoutputfile, 'w') as resultFile:
        resultFile.write('URL test results are*******************************************************************************\n')
        with open('website_list.txt', 'r') as f:
            while (True):
                url = f.readline()
                if url == "":
                    break

                elif (input_verification(url, path, 'URL_filter')):
                    try:
                        urllib.request.urlopen(url)
                        out = str(url)
                        result = ("Gained access to %s \n" % out)
                        resultFile.write(result)
                    except Exception as e:
                        error = "%s \n" % e
                        resultFile.write(str(error))

        f.close()

        getting_key = ""

        response = requests.get(getting_key, verify=False)

        URL_log_num = path+'URL_log_job_number.xml'
        with open(URL_log_num, 'wb') as file:
            file.write(response.content)

        file.close()

        tree = et.parse(URL_log_num)
        root = tree.getroot()

        for check in root.iter('job'):
            job_number = check.text

        the_key = "" + job_number + ""

        response = requests.get(the_key, verify=False)
        XML_log_report = path+'Job_report.xml'
        with open(XML_log_report, 'wb') as file:
            file.write(response.content)

        base_path = os.path.dirname(os.path.realpath(__file__))
        xml_file = os.path.join(base_path, XML_log_report)
        tree = et.parse(xml_file)
        root = tree.getroot()

        resultFile.write("Firewall log outputs are:"
                         "**********************************************************************************************\n")
        for entry in root.iter('entry'):
            cat = entry.find('category').text
            website = entry.find('url_domain').text
            action = entry.find('action').text
            reps = entry.find('repeatcnt').text
            days = entry.find('day-of-receive_time').text

            output = '* %s %s was %s repeated block %s on %s\n' % (website, cat, action, reps, days)
            resultFile.write(output)

URL_filter()