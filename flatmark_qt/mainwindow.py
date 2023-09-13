from qtpy.QtWidgets import QLabel, QMainWindow
from qtpy.QtCore import Qt
from urllib.request import url2pathname
from urllib.parse import urlparse, urlunparse, urljoin
from pathlib import Path

from . import mainview, config as C
from .url import Url
from .qtutils import set_bc
from .docman import Docman

class Mainwindow(QMainWindow):
	def __init__(self, parent = None):
		super(Mainwindow, self).__init__(parent)
		# child widgets
		self.info_r = QLabel("?/?", self)
		self.info_r.adjustSize()
		self.info_height = self.info_r.rect().height()
		self.info_r.setAlignment(Qt.AlignmentFlag.AlignRight)
		self.info_r.show()
		self.info_l = QLabel("?", self)
		self.info_l.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
		self.slides = dict()
		self.current_slide = None
		set_bc(self, "#f0f0f0")
		set_bc(self.info_r)
		self.resize(C.main_width, C.main_height)
		self.show()
		self.docman = Docman()
	def navi(self, offset):
		C.curl().sect_idx += offset
		if C.curl().sect_idx < 0:
			C.curl().sect_idx = 0
		elif C.curl().sect_idx >= self.docman.pagelen:
			C.curl().sect_idx = self.docman.pagelen - 1
	def seturl(self, url):
		parsed = urlparse(url)
		if parsed.scheme == "": # relative
			path = urljoin(C.curl().basedir.path, parsed.path)
			parsed = C.curl().basedir._replace(path = path)
		if "/" in parsed.path:
			[parent, srcname] = parsed.path.rsplit("/", 1)
		else:
			srcname = parsed.path
			parent = ""
		basedir = parsed._replace(path = parent, fragment = "", query = "")
		C.update_hurl(Url(basedir, srcname))
		C.curl().sect_idx = int(parsed.fragment or 1) - 1
	def clicked(self, url):
		self.seturl(url)
		self.load()
	def load(self):
		self.slides = dict()
		data = C.curl().openurl()
		self.docman = Docman(data)
		self.info_l.setText(C.curl().genurl(strip = True))
		self.update()
	def update(self):
		if self.docman.pagelen == 0:
			return
		if self.current_slide != None:
			self.current_slide.hide()
		idx = C.curl().sect_idx
		self.info_r.setText(f"P:{idx + 1}/{self.docman.pagelen}")
		if idx not in self.slides:
			sect = self.docman.doc.sects[idx]
			mv = mainview.Mainview(sect, self)
			self.slides[idx] = mv
		self.current_slide = self.slides[idx]
		self.current_slide.show()
		self.current_slide.locate()
	def resizeEvent(self, e):
		w = self.rect().width()
		self.info_l.resize(w, self.info_height)
		self.info_r.resize(w, self.info_height)
		if self.current_slide != None:
			self.current_slide.locate()
	def keyPressEvent(self, e):
		match e.text():
			case "k":
				self.navi(-1)
				self.update()
			case "j":
				self.navi(1)
				self.update()
			case "r":
				self.load()
			case "q":
				self.close()
			case "H":
				if C.hidx > 0:
					C.hidx -= 1
					self.load()
				else:
					print("invalid H")
			case "L":
				if C.hidx < len(C.hurl) - 1:
					C.hidx += 1
					self.load()
				else:
					print("invalid L")
			case "q":
				self.close()
			case x:
				if x.isdigit():
					num = ord(x) - ord("0")
					if num >= len(self.current_slide.links):
						print(f"invalid jump {num}")
					else:
						url = self.current_slide.links[num]
						self.clicked(url)
