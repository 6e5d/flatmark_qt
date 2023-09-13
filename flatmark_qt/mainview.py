from qtpy.QtWidgets import QWidget, QLabel
from qtpy.QtCore import Qt
from qtpy.QtGui import QPixmap

from . import qtutils, config as C
from flatmark.flatmark import Multimedia, Code, Paragraph
from flatmark_qt.docman import proc_text

class Mainview(QWidget):
	def label(self, text):
		l = QLabel("", self)
		l.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction);
		l.linkActivated.connect(self.parent().clicked)
		# set_bc(l, "lime")
		l.setWordWrap(True);
		l.setText(text)
		return l

	def build_block(self, block):
		if isinstance(block, Multimedia):
			data = C.curl().openurl(block.url)
			try:
				w = QLabel("", self)
				w.setMaximumSize(C.paragraph_width, C.image_maxheight)
				pixmap = QPixmap()
				pixmap.loadFromData(data)
				pixmap = qtutils.scale_pixmap(pixmap)
				w.resize(pixmap.size())
				w.setPixmap(pixmap)
				return w
			except Exception as e:
				print(e)
				w = QLabel(f"Bad url: {block.url}", self)
				return w
		elif isinstance(block, Paragraph):
			data, links = proc_text(block.data, len(self.links))
			self.links += links
			w = self.label(data)
			w.setMinimumSize(C.paragraph_width, 1)
			w.setFont(C.body_font)
			return w
		elif isinstance(block, Code):
			data = "\n".join(block.lines)
			w = self.label(data)
			w.setFont(C.mono_font)
			w.setMinimumSize(C.paragraph_width, 1)
			return w
		raise Exception(type(block))

	def __init__(self, sect, parent = None):
		super(Mainview, self).__init__(parent)
		qtutils.set_bc(self, "white")
		# render title
		line = sect.title.data
		l = self.label(line)
		l.setMinimumSize(C.title_width, 1)
		l.move(C.margin_tl, C.margin_tt)
		l.setFont(C.title_font)
		l.adjustSize()
		prev_y = l.geometry().bottom() + C.margin_tp
		self.links = []

		for block in sect.blocks:
			w = self.build_block(block)
			w.adjustSize()
			left = C.margin_pl
			if w.rect().width() < C.paragraph_width:
				left += (C.paragraph_width - w.rect().width()) // 2
			w.move(left, prev_y)
			w.show()
			prev_y = w.geometry().bottom() + C.margin_pp
	def locate(self):
		b = self.parent().info_l.geometry().bottom()
		self.resize(C.mainview_width, self.parent().height() - b)
		pos = self.parent().rect().center() - self.rect().center()
		pos = pos.x()
		if pos < 0:
			pos = 0
		self.move(pos, b)
