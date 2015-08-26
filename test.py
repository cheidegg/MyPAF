

import ROOT, array

super = ROOT.TH1F("super", "super", 5, array.array('d', [0, 5, 6, 7, 8, 9]))
print super.GetXaxis().GetXbins().GetArray()
heico = ROOT.TH1F("supeC", "supeC", super.GetNbinsX(), super.GetXaxis().GetXbins().GetArray())


selstring = "filter1 == 1 && SEL[othersel] && filter2"
repstring = "my && new && selection"
print selstring[selstring.find("SEL[")+4:]
print selstring[selstring.find("SEL[")+4:selstring.find("SEL[")+4+selstring[selstring.find("SEL[")+4:].find("]")]
print selstring[0:selstring.find("SEL[")] + repstring + selstring[selstring.find("SEL[")+4+selstring[selstring.find("SEL[")+4:].find("]")+1:]

s = "iswithalongword"
path = "my/super/prod/path/this/iswithalongword/"
print path[0:len(path)-len(s)-1]

binlist = [0, 5, 10, 11, 16, 21]
#binlist = [0, 5, 10, 15, 20, 25]
v = 0 % 5
print v
print [elm % binlist[1] == 0 for elm in binlist]
if all([elm % binlist[1] == 0 for elm in binlist]):
	print "equal stuff"
else:
	print "non equal stuff"

print next((i for i, x in enumerate(binlist) if x != 0), None)

##help('modules')
#from PIL import Image, PngImagePlugin
#
#meta = PngImagePlugin.PngInfo()
#meta.add_text("kMDItemFinderComment", "my super test value")
#
#im = Image.open("test.png")
#im.save("test2.png", "PNG", pnginfo = meta)
#
#im2 = Image.open("test3.png")
#print im2.info
