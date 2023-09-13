from qtpy.QtGui import QFont

margin_pp = 20 # vertical para - para
margin_tp = 30 # vertical title - para
margin_tt = 30 # vertical title - top
margin_tl = 25 # horizontal title - left
margin_pl = 50 # horizontal para - left
margin_r = 25 # horizontal right
mainview_width = 800 # slide width
main_width = 900 # slide width
main_height = 600 # slide width
paragraph_width = mainview_width - margin_pl - margin_r
title_width = mainview_width - margin_tl - margin_r
image_maxheight = 320
image_minsize = 0.5 # at least k times max size
scale = 1.0

font = "sans"
body_font = QFont(font, 14)
mono_font = QFont("monospace", 12)
title_font = QFont(font, 24)
title_font.setBold(True)

hurl = []
hidx = -1
def update_hurl(url):
	global hurl, hidx
	hurl = hurl[:hidx + 1]
	hurl.append(url)
	hidx += 1
def curl():
	return hurl[hidx]
