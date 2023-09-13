from flatmark.flatmark import Document

def proc_text(data, linklen):
	clist = [ch for ch in data]
	if clist[0] == "*" and clist[1] == " ":
		clist[0] = "\u25AA"
	state_code = False
	state_emph = False
	state_url = None
	links = []
	idx = 0
	while True:
		if idx >= len(clist):
			break
		ch = clist[idx]
		if ch == "`":
			if state_code:
				clist[idx] = "</code>"
			else:
				clist[idx] = "<code>"
			state_code = not state_code
		elif ch == "*":
			if not state_code:
				if state_emph:
					clist[idx] = "</b>"
				else:
					clist[idx] = "<b>"
				state_emph = not state_emph
		elif ch == "<" or ch == ">":
			if not state_code:
				if state_url != None:
					clist[idx] = f'">[{linklen + len(links)}]</a>'
					links.append(state_url)
					state_url = None
				else:
					state_url = ""
					clist[idx] = '<a href="'
			else:
				if ch == "<":
					clist[idx] = "&lt;"
				else:
					clist[idx] = "&gt;"
		elif state_url != None:
			state_url += clist[idx]
		elif ch == "\\":
			clist[idx] = ""
			idx += 1
			if clist[idx] == "<":
				clist[idx] = "&lt;"
			elif clist[idx] == ">":
				clist[idx] = "&gt;"
			elif clist[idx] == "n":
				clist[idx] = "<br>"
		idx += 1
	result = "".join(clist)
	# print(result)
	return (result, links)

class Docman():
	def __init__(self, data = None):
		if data == None:
			self.doc = None
			self.pagelen = 0
		else:
			lines = data.decode().split("\n")
			self.doc = Document(lines)
			self.pagelen = len(self.doc.sects)
