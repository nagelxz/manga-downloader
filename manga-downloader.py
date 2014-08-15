import alerter
import os
import time
import json
import zipfile
import shutil
import logging
import logging.handlers
from urllib import request as url
from urllib import error as urlError

def set_logging():
	serverlog = logging.FileHandler('/var/log/manga-downloader.log')
	serverlog.setLevel(logging.INFO)
	serverlog.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s %(message)s'))

	logger = logging.getLogger('manga-downloader-log')
	logger.setLevel(logging.INFO)
	logger.addHandler(serverlog)
	return logger

def ch_formatter(last_ch):
	ch = ''
	
	if len(str(last_ch)) == 2:
		ch = '0' + str(last_ch)
	elif len(str(last_ch)) == 1:
			ch = '00' + str(last_ch)
	else:
		ch = str(last_ch)
	
	return ch
	
def pg_formatter(pg_num):
	pg = ''

	if len(str(pg_num)) == 1:
		pg = '0' + str(pg_num)
	else:
		pg = str(pg_num)
		
	return pg

#base_path = '/Users/jonnagel/Documents/Personal Projects/manga-downloader/'
base_url = 'http://s9.eatmanga.com/mangas/Manga-Scan/'
# base_url = 'http://r1.goodmanga.net/images/manga/'
data = json.loads(open('manga.json').read())

base_path = data['base path']
downloaded = []

	
logger = set_logging()
logger.info('Starting a new week\'s download')

#print (json.dumps(data, sort_keys=True,indent=3, separators=(',',':')))
logger.info('Opening json')

for manga in data['series']:
	if not os.path.exists(os.path.join(base_path, 'tmp', manga['name'])):
		os.makedirs(os.path.join(base_path, 'tmp', manga['name']))
		logger.info('Creating place for ' + manga['name'] + ' to download')
	if not os.path.exists(os.path.join(base_path, 'done', manga['name'])):	
		os.makedirs(os.path.join(base_path, 'done', manga['name']))
		logger.info('This (' + manga['name'] + ') must be new. Creating place for it to be stored...')

	name = manga['name'].replace(' ', '-')
#	name = manga['name'].replace(' ', '_').lower()
	last_ch = manga['last']
	last_ch += 1
#	print (name + '\t' + str(last_ch))
	logger.info('getting ready for ' + name + '\t' + str(last_ch))
	
	ch = ch_formatter(last_ch)
	
	url_no_pg = base_url + name + '/' + name + '-' + ch + '/'
#	url_no_pg = base_url + name + '/' + str(last_ch) + '/'
	
	more_ch = 1
	
	while more_ch == 1:
		pg_num = 1
		
		try:
			url.urlopen(url_no_pg + '01.jpg')
			
			if not os.path.exists(os.path.join(base_path, 'tmp', manga['name'], ch)):
				os.makedirs(os.path.join(base_path, 'tmp', manga['name'], ch))
				logger.info('creating place for the chapter')
		
			while pg_num != 0:
				pg = pg_formatter(pg_num)
#				pg = str(pg_num)
			
				try:
#					print (url_no_pg + pg + '.jpg')
					url.urlretrieve(url_no_pg + pg + '.jpg', os.path.join(base_path, 'tmp', manga['name'], ch, pg + '.jpg'))
#					url.urlretrieve(url_no_pg + pg + '.jpg', base_path + manga['name'] + '/' + str(last_ch) + '/' + pg+ '.jpg')
#					print ('downloaded ' + pg + '.jpg')
					logger.info('downloaded ' + pg + '.jpg')
					pg_num += 1
					time.sleep(8)
				except urlError.HTTPError:
#					print ('CHAPTER DONE')
					logger.info('CHAPTER DONE')
					downloaded.append(manga['name'] + '   ' + str(last_ch))
					pg_num = 0
					time.sleep(15)
						
			last_ch += 1
#			print (name + '\t' + str(last_ch))
			logger.info('getting ready for ' + name + '\t' + str(last_ch))
	
			ch = ch_formatter(last_ch)
#			print (ch)
			url_no_pg = base_url + name + '/' + name + '-' + ch + '/'
#			url_no_pg = base_url + name + '/' + str(last_ch) + '/'
		
		except urlError.HTTPError:
#			print ('no more chapters')
			logger.info('Nothing more in this manga to download')
			last_ch -= 1
			more_ch = 0
			time.sleep(25)
			
	manga['last'] = last_ch
#	print (name + '\t' + str(last_ch))

#print ('done downloading')
logger.info('Finished required downloads...')

#print (json.dumps(data, sort_keys=True,indent=3, separators=(',',':')))

jsonfile = open('manga.json', 'w+') 
jsonfile.write(json.dumps(data, sort_keys=True,indent=3, separators=(',',':')))
#print ('json updated')
logger.info('Updating json')
logger.info('...')
logger.info('...')
logger.info('converting mass downloads to comic chapters')

dirs = [d for d in os.listdir(os.path.join(base_path, 'tmp')) if os.path.isdir(os.path.join(base_path, 'tmp', d))]

for dir in dirs:
	chapters = [c for c in os.listdir(os.path.join(base_path, 'tmp', dir)) if os.path.isdir(os.path.join(base_path, 'tmp', dir, c))]
	
	for ch in chapters:
		pgs = [p for p in os.listdir(os.path.join(base_path, 'tmp', dir, ch)) if os.path.isfile(os.path.join(base_path, 'tmp', dir, ch, p))]
			
		zip = zipfile.ZipFile(os.path.join(base_path, 'done', dir, ch + '.cbz'), 'w')	
		logger.info('Creating Zip file: ' + os.path.join(base_path, 'done', dir, ch + '.cbz'))
		for pg in pgs:
			if len(pgs) != 0:
				zip.write(os.path.join(base_path, 'tmp', dir, ch, pg))
			else:
				break
				
		zip.close()
		logger.info('chapter done')
		
shutil.rmtree(os.path.join(base_path, 'tmp'))
logger.info('Taking out the trash. Kicking it to the curb. Sending into the abyss of nothingness')

if len(downloaded) >= 1:
	message = alerter.build_message(downloaded)
	alerter.alert_of_downloads(message)

#print ('FINISHED')
logger.info('FINISHED....Until next week!')
