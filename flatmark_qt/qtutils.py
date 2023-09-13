from qtpy.QtCore import Qt
from . import config as C

def set_bc(w, color = "beige"):
	w.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
	w.setStyleSheet(f"background-color: {color};")

def scale_pixmap(pixmap):
	pixmap.setDevicePixelRatio(C.scale)
	size = pixmap.size()
	width = size.width()
	height = size.height()
	if width > C.paragraph_width * C.scale or \
		height > C.image_maxheight * C.scale:
		pixmap = pixmap.scaled(
			int(C.paragraph_width * C.scale),
			int(C.image_maxheight * C.scale),
			Qt.AspectRatioMode.KeepAspectRatio,
			transformMode = Qt.TransformationMode.SmoothTransformation,
		)
	elif width < C.paragraph_width * C.scale * C.image_minsize or \
		height < C.image_maxheight * C.scale * C.image_minsize:
		pixmap = pixmap.scaled(
			int(C.paragraph_width * C.scale * C.image_minsize),
			int(C.image_maxheight * C.scale * C.image_minsize),
			Qt.AspectRatioMode.KeepAspectRatio,
			transformMode = Qt.TransformationMode.SmoothTransformation,
		)
	return pixmap
