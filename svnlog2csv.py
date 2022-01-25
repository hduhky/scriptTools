import csv
import subprocess
import sys
import xml.etree.cElementTree as etree
import time

log_text = subprocess.Popen(['svn', 'log', '--xml'] + sys.argv[1:], stdout=subprocess.PIPE).communicate()[0]
log_xml = etree.XML(log_text)

csv_writer = csv.writer(sys.stdout)

def format_date(date_string):
	date = date_string.split('.')[0]
	time_struct = time.strptime(date, "%Y-%m-%dT%H:%M:%S")
	timestamp = time.mktime(time_struct) + 8 * 3600
	formatted_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
	return formatted_date

csv_writer.writerow([
	'revision',
	'date', 
	'author',
	'msg',
	])

for child in log_xml.getchildren():
	csv_writer.writerow([
		child.attrib['revision'],
		format_date(child.findtext('date')), 
		child.findtext('author').encode('utf-8'),
		child.findtext('msg').encode('utf-8'),
		])
