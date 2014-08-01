import os
import time
import json
import zipfile
from urllib import request as url
from urllib import error as urlError

base_path = '/Users/jonnagel/Documents/Personal Projects/manga-downloader/tmp/'
# base_url = 'http://s9.eatmanga.com/mangas/Manga-Scan/'
base_url = 'http://r1.goodmanga.net/images/manga/'
data = json.loads(open(base_path + 'manga.json').read())

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

for manga in data['series']:
	if not os.path.exists(base_path + manga['name']):
		os.makedirs(base_path + manga['name'])

#	name = manga['name'].replace(' ', '-')
	name = manga['name'].replace(' ', '_').lower()
	last_ch = manga['last']
	print (name + '\t' + str(last_ch))
	last_ch += 1
	
#	ch = ch_formatter(last_ch)
	
#	print (ch)
#	url_no_pg = base_url + name + '/' + name + '-' + ch + '/'
	url_no_pg = base_url + name + '/' + str(last_ch) + '/'
	print (url_no_pg)
	
	more_ch = 1
	
	while more_ch == 1:
		if not os.path.exists(base_path + manga['name'] + '/' + str(last_ch)):
			os.makedirs(base_path + manga['name'] + '/' + str(last_ch))
			
		pg_num = 1
		
		try:
			while pg_num != 0:
#				pg = pg_formatter(pg_num)
				pg = str(pg_num)
			
				try:
#					print (url_no_pg + pg + '.jpg')
#					url.urlretrieve(url_no_pg + pg + '.jpg', base_path + pg+ '.jpg')
					url.urlretrieve(url_no_pg + pg + '.jpg', base_path + manga['name'] + '/' + str(last_ch) + '/' + pg+ '.jpg')
					print ('downloaded ' + pg + '.jpg')
					pg_num += 1
					time.sleep(15)
				except urlError.HTTPError:
					print ('CHAPTER DONE')
					pg_num = 0
					time.sleep(60)
						
			last_ch += 1
			print (name + '\t' + str(last_ch))
#			ch = ch_formatter(last_ch)
#			print (ch)
#			url_no_pg = base_url + name + '/' + name + '-' + ch + '/'
			url_no_pg = base_url + name + '/' + str(last_ch) + '/'
			print (url_no_pg)
			url.urlopen(url_no_pg + '1.jpg')
		
		except urlError.HTTPError:
			print ('no more chapters')
			last_ch -= 2
			more_ch = 0
			time.sleep(90)
			
	manga['last'] = last_ch
	print (name + '\t' + str(last_ch))

print ('done downloading')

jsonfile = open(base_path + 'manga.json', 'w+')
jsonfile.write(json.dumps(data, sort_keys=True,indent=3, separators=(',',':')))
print ('json updated')
				
dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
print (dirs)

for dir in dirs:
	chapters = [c for c in os.listdir(base_path + dir + '/') if os.path.isdir(os.path.join(base_path + dir + '/', c))]
	print (chapters)
	
	for ch in chapters:
		pgs = [p for p in os.listdir(base_path + dir + '/' + ch + '/') if os.path.isfile(os.path.join(base_path + dir + '/' + ch + '/', p))]
		print (pgs)
				
		for pg in pgs:
			zip = zipfile.ZipFile(base_path + dir + '/' + ch + '.zip', 'w')
			if len(pgs) != 0:
				
				print (os.path.join(base_path, dir, ch, pg))
				zip.write(os.path.join(base_path, dir, ch, pg))
			else:
				break
				
			zip.close()
print ('FINISHED')