#
# AppCache for Jasy - App cache supporting library
#
#
# Copyright (C) 2012 Sebastian Fastner, Mainz, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

@share
def cacheManifest(scripts = ["script/application-%s.js"], htmlfile = "index.html", kernel = "script/kernel.js"):
	timestamp = time.time()
	appcache = """CACHE MANIFEST

# Jasy AppCache Manifest file
# Version: {version}

CACHE:
{htmlfile}
{kernel}
{scripts}

NETWORK:
*"""

	htmlcache = '<!DOCTYPE html><html manifest="%s"></html>'

	# Create an application cache file for each permutation
	for permutation in session.permutate():
		# Set options
		checksum = permutation.getChecksum()
		
		scriptFiles = ""
		for script in scripts:
			scriptFiles += (script % checksum) + "\n"
		
		manifestFilename = "appcache-%s.manifest" % (checksum)
		writeFile(manifestFilename, appcache.format(version=str(timestamp), htmlfile=htmlfile, kernel=kernel, scripts=scriptFiles))
		
		writeFile("index-%s.html" % (checksum), htmlcache % (manifestFilename))

