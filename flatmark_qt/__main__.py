from qtpy.QtWidgets import QApplication
from flatmark_qt import mainwindow
from flatmark_qt import config as C
from pathlib import Path
import sys

url = sys.argv[1]
if url.startswith("."):
	url = Path(url).resolve()
	url = f"file://{url}"
app = QApplication([])
C.scale = app.primaryScreen().devicePixelRatio()
mw = mainwindow.Mainwindow()
mw.seturl(url)
mw.load()
app.exec()
