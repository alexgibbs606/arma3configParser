from pprint import pformat
from json import dumps as jsonDumps

class ARMAConfig:
	def __init__(self, configPath:str, pathDelim:str='.'):
		self._pathDelim = pathDelim
		self.configPath = configPath
		self._loadConfig(self.configPath)

	def _loadConfig(self, configPath:str):
		self.config = {}
		path = []
		with open(configPath, encoding='utf-8') as configDump:
			configDump.readline()
			for index, line in enumerate(configDump.readlines()):
				line = line.strip()
				# Handling adding datat to the config
				if line.startswith('class'):
					classname = line.split(':')[0].split(' ')[-1]
					path.append(classname)
					self[self._pathDelim.join(path)] = {}

				# If it's the end of the class, we go up a level in the path
				elif line.startswith('};'):
					# Previous directory
					path = path[:-1]

				# elif line.startswith('{'):
				# 	# Don't need to do anything here expect move to the next line
				# 	continue

				elif '=' in line:
					# Now the fun part, lets start parsing all the values into their respective classes/locations
					# Finding the key for each value is easy, determining the datatype that the value should be stored is going to be harder.
					(key, value) = [_.strip() for _ in line[:-1].split('=', 1)]

					# Values with a leading and trailing " are strings
					if value[0] == '"' and value[-1] == '"':
						value = value[1:-1] # Trimming the ends off our string, and keeping the value as a string

					# Keys that have a trailing '[]' are going to be lists
					elif key[-2:] == '[]':
						# try:
						key = key[:-2] # Trimming the trailing [] off the key
						listVal = value.replace('{', '[').replace('}', ']')
						# To handle strings with backslashes, we'll replace them all with an escaped version
						value = eval(listVal.replace('\\', '\\\\'))
						# 	# Removing leading and trailing {}, then splitting on commas.
						# 	tempList = []
						# 	for item in value[1:-1].split(','):
						# 		item = item.strip()
						# 		if item[0] == '"' and item[-1] == '"':
						# 			tempList.append(item)

						# 		else:
						# 			tempList.append(float(item))
						# except ValueError:

					# Anything else we can just lazily say it's a float. This will handle integers and floating point numbers
					else:
						value = float(value)

					self[self._pathDelim.join(path + [key])] = value


	def __getitem__(self, key):
		if key == '':
			return self.config
		head = self.config
		for obj in key.split(self._pathDelim):
			head = head[obj]
		return head

	def __setitem__(self, key, value=None):
		if not value:
			value = {}
		head = self.config
		newKey = key.split(self._pathDelim)
		for obj in newKey[:-1]:
			head = head[obj]
		head[newKey[-1]] = value

	def __str__(self):
		return pformat(self.config)


	def _findCS(self, searchString, sourceString):
		return searchString in sourceString

	def _findNCS(self, searchString, sourceString):
		return searchString.lower() in sourceString.lower()

	def findPath(self, searchString, caseSensitive=True):
		with open(self.configPath, encoding='utf-8') as configDump:
			configDump.readline()
			path = []
			hits = []

			matchFunc = self._findCS if caseSensitive else self._findNCS
			for index, line in enumerate(configDump.readlines()):
				if line.strip().startswith('class'):
					classname = line.strip().split(':')[0].split(' ')[-1]
					path.append(classname)

				# If it's the end of the class, we go up a level in the path
				elif line.strip().startswith('};'):
					# Previous directory
					path = path[:-1]

				elif matchFunc(searchString, line):
					hits.append({
						'lineNumber': index,
						'line': line,
						'path': path,
						'pathStr': self._pathDelim.join(path),
					})
		return hits

	def asJson(self, file):
		with open(file, 'w', encoding='utf-8') as outFile:
			outFile.write(jsonDumps(self.config))


if __name__ == '__main__':
	from sys import argv

	config = ARMAConfig(argv[1])

	foo = config.findPath('wipeout', False)

	config.asJson('AiO.1.92.145639_CUP.json')

	pass