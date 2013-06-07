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

import time, json
from jasy.asset.Manager import AssetManager
from jasy.core.FileManager import FileManager
from jasy.core.OutputManager import OutputManager
from jasy.js.Resolver import Resolver


def filenamesFromAsset(prefix, section, profiles, entries=None):
	if (entries == None):
		entries = []
	
	if section:
		for filename in section:
			entry = section[filename]
			if (len(prefix) > 0):
				id = prefix + "/" + filename
			else:
				id = filename
			
			if "p" in entry:
				entries.append(profiles[entry["p"]]["root"] + id)
			else:
				filenamesFromAsset(id, entry, profiles, entries)
		
	return entries
		

@share
def cacheManifest(session, startClassName, scripts = ["script/application-%s.js"], htmlfile = "index.html", kernel = "script/kernel.js", ignoreAssets=False):
	# Check for new jasy replacement system (1.1.0-rc4)                                                                                                                                  
	if session.expandFileName("{{id}}") != "{{id}}":
		PREFIX = "{{prefix}}"
		HASH = "{{id}}"
	else:
		PREFIX = "$prefix"
		HASH = "$permutation"

	timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
	appcache = """CACHE MANIFEST

# Jasy AppCache Manifest file
# Version: {version}

CACHE:
{htmlfile}
{kernel}
{scripts}
{assets}

NETWORK:
*"""

	htmlcache = '<!DOCTYPE html><html manifest="%s"></html>'
	assetManager = AssetManager(session).addBuildProfile()
	outputManager = OutputManager(session, assetManager)
	fileManager = FileManager(session)

	# Create an application cache file for each permutation
	for permutation in session.permutate():
		if ignoreAssets:
			assets = []
		else:
			classes = Resolver(session).addClassName(startClassName).getSortedClasses()
			assetConfig = json.loads(assetManager.export(classes))
			assets = filenamesFromAsset("", assetConfig["assets"], assetConfig["profiles"])

		# Set options
		if hasattr(permutation, "getId"):
			checksum = permutation.getId()
		else:
			checksum = permutation.getChecksum()
		
		scriptFiles = []
		for script in scripts:
			scriptFiles.append(script % checksum)
		
		manifestFilename = "appcache-%s.manifest" % (checksum)
		fileManager.writeFile(PREFIX + "/" + manifestFilename, appcache.format(version=timestamp, htmlfile=htmlfile, kernel=kernel, scripts="\n".join(scriptFiles), assets="\n".join(assets)))
		
		fileManager.writeFile(PREFIX + "/index-%s.html" % (checksum), htmlcache % manifestFilename)

