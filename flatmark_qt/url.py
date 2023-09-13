from urllib.request import urlopen
from urllib.parse import urlunparse

class Url:
	def __init__(self, basedir, srcfile):
		self.basedir = basedir
		self.srcfile = srcfile
	def genurl(self, file = None, strip = False):
		if file == None:
			file = self.srcfile
		url = self.basedir._replace(path = f"{self.basedir.path}/{file}")
		if strip:
			url = url._replace(fragment = "", query = "")
		return urlunparse(url)
	def openurl(self, file = None):
		url = self.genurl(file)
		print("opening", url)
		data = urlopen(url).read()
		return data
