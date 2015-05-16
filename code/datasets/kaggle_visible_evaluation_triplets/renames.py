import os

for filename in os.listdir("."):
	if "cosine_binary" in filename:
		continue
	newname = filename
	if filename.startswith("MAP_cosine"):
		newname = newname.replace("MAP_cosine", "MAP_ucf_cosine")
	if not "_mnn=" in filename:
		newname = newname.replace("_q=", "_mnn=9999_q=")
	if newname != filename:
		print filename, "-->", newname
		os.rename(filename, newname)
		