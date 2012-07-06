def cacheManifest(scripts = ["script/application-%s.js"], htmlfile = "index.html", kernel = "script/kernel.js"):
	timestamp = time.time()
	appcache = """
CACHE MANIFEST

# Jasy AppCache Manifest file
# Version: %(version)

CACHE:
%(htmlfile)
%(kernel)
%(scripts)
"""
	htmlcache = """
<!DOCTYPE html>
<html manifest="%(manifest)"></html>
"""

	# Create an application cache file for each permutation
	for permutation in session.permutate():
		# Set options
		checksum = permutation.getChecksum()
		
		manifestFilename = "appcache-%s.manifest" % (checksum)
		writeFile(manifestFilename, appcache % {
			"version" : str(timestamp),
			"htmlfile" : htmlfile,
			"kernel" : kernel,
			"scripts" : "\n".join(scripts)
		})
		
		writeFile("index-%s.html" % (checksum), htmlcache % {
			"manifest" : manifestFilename
		});

