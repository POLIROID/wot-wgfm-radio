
BUILD_FLASH = True

import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--ignore_flash')
args = parser.parse_args()
if args.ignore_flash:
	BUILD_FLASH = False

import compileall
import datetime
import shutil
import zipfile
import imp
import marshal

ANIMATE_PATH = 'C:\\Program Files\\Adobe\\Adobe Animate CC 2015\\Animate.exe'
MODIFICATION_VERSION = '3.0.5'
GAME_VERSION = '0.9.17.1'
GAME_FOLDER = 'X:/wot'
BUILD_RESMODS = False
BUILD_PACKAGE = True
COPY_INTO_GAME_FOLDER = True

# use this bcs shutil.copytree sometimes throw error on folders create
def copytree(source, destination, ignore=None):
	for item in os.listdir(source):
		sourcePath = os.path.join(source, item)
		destinationPath = os.path.join(destination, item)
		if os.path.isfile(sourcePath):
			baseDir, fileName = os.path.split(destinationPath)
			if not os.path.isdir(baseDir):
				os.makedirs(baseDir)
			if ignore:
				ignored_names = ignore(source, os.listdir(source))
				if fileName in ignored_names:
					continue
			shutil.copy2(sourcePath, destinationPath)
		else:
			copytree(sourcePath, destinationPath, ignore)

# use this because zipfile by default dont create folders info in result zip
def zipFolder(source, destination, mode='w', compression=zipfile.ZIP_STORED):
	
	def dirInfo(dirPath):
		zi = zipfile.ZipInfo(dirPath, now)
		zi.filename = zi.filename.replace(source, "")
		if zi.filename:
			if not zi.filename.endswith('/'): 
				zi.filename += '/'
			if zi.filename.startswith('/'): 
				zi.filename = zi.filename[1:]
			zi.compress_type = compression
			return zi
	
	def fileInfo(filePath):
		st = os.stat(filePath)
		zi = zipfile.ZipInfo(filePath, now)
		zi.external_attr = 2176188416L
		zi.filename = zi.filename.replace(source, "")
		if zi.filename.startswith('/'): 
			zi.filename = zi.filename[1:]
		zi.compress_type = compression
		return zi
	
	with zipfile.ZipFile(destination, mode, compression) as zip:
		now = tuple(datetime.datetime.now().timetuple())[:6]
		for dirPath, _, files in os.walk(source):
			info = dirInfo(dirPath)
			if info:
				zip.writestr(info, '')
			for fileName in files:
				filePath = os.path.join(dirPath, fileName)
				info = fileInfo(filePath)
				zip.writestr(info, open(filePath, 'rb').read())

# clean up
if os.path.isdir('temp'):
	shutil.rmtree('temp')
os.mkdir('temp') 
if os.path.isdir('build'):
	shutil.rmtree('build')
os.mkdir('build') 


if BUILD_FLASH:
	# build flash
	with open('temp/build.jsfl', 'wb') as fh:
		for fileName in os.listdir('as3'):
			if fileName.endswith('fla'):
				fh.write('fl.publishDocument("file:///{path}/as3/{fileName}", "Default");\r\n'.format(path = os.getcwd().replace('\\', '/').replace(':', '|'), fileName = fileName))
		fh.write('fl.quit(false);')
	os.system('"{animate}" -e temp/build.jsfl'.format(animate = ANIMATE_PATH))


# build python
for dirName, _, files in os.walk('python'):
	for fileName in files:
		if fileName.endswith(".py"):
			filePath = os.path.join(dirName, fileName)
			compileall.compile_file(filePath)
			
# copy all staff
if BUILD_FLASH:
	copytree('as3/bin/', 'temp/standart/res_mods/{version}/gui/flash'.format(version = GAME_VERSION))
	copytree('as3/bin/', 'temp/wgpackage/res/gui/flash')
copytree('python', 'temp/standart/res_mods/{version}/scripts/client'.format(version = GAME_VERSION), ignore=shutil.ignore_patterns('*.py'))
copytree('python', 'temp/wgpackage/res/scripts/client', ignore=shutil.ignore_patterns('*.py'))
copytree('resources', 'temp/standart/res_mods/{version}'.format(version = GAME_VERSION))
copytree('resources', 'temp/wgpackage/res')

# build binaries

META = """<root>
	<!-- Techical MOD ID -->
	<id>{modID}</id>
	<!-- Package version -->
	<version>{version}</version>
	<!-- Human readable name -->
	<name>{modName}</name>
	<!-- Human readable description -->
	<description>{modDescription}</description>
</root>"""

if BUILD_PACKAGE:
	with open('temp/wgpackage/meta.xml', 'wb') as fh:
		fh.write(
			META.format(
				modID = "wgfmRadio",
				modName = "WarGaming.FM",
				modDescription = "Слушайте радио WarGaming.FM прямо в клиенте игры",
				version = MODIFICATION_VERSION
			)
		)
	zipFolder('temp/wgpackage', 'build/wgfmRadio.wotmod')

if BUILD_RESMODS:
	zipFolder('temp/standart', 'build/wgfmRadio.zip', compression=zipfile.ZIP_DEFLATED)

if COPY_INTO_GAME_FOLDER:
	if BUILD_PACKAGE:
		shutil.copy2('build/wgfmRadio.wotmod', '{wot}/mods/{version}/'.format(wot = GAME_FOLDER, version =GAME_VERSION))
	elif BUILD_RESMODS:
		copytree('temp/standart', GAME_FOLDER)
	
	
# clean up
shutil.rmtree('temp')


if BUILD_FLASH:
	for dirname, _, files in os.walk('as3'):
		for filename in files:
			if filename.endswith('.swf'):
				os.remove(os.path.join(dirname, filename))

for dirname, _, files in os.walk('python'):
	for filename in files:
		if filename.endswith('.pyc'):
			os.remove(os.path.join(dirname, filename))
