import csv
import subprocess
import sys
import xml.etree.cElementTree as etree

log_text = subprocess.Popen(['svn', 'log', '--xml'] + sys.argv[1:], stdout=subprocess.PIPE).communicate()[0]
log_xml = etree.XML(log_text)

csv_writer = csv.writer(sys.stdout)

csv_writer.writerow([
                'revision',
                'date', 
                'author',
                'msg',
        ])
for child in log_xml.getchildren():
        csv_writer.writerow([
                child.attrib['revision'],
                child.findtext('date'), 
                child.findtext('author').encode('utf-8'),
                child.findtext('msg').encode('utf-8'),
        ])
