#
# AppCache for Jasy - App cache supporting library
#
#
# Copyright (C) 2012-2014 Sebastian Fastner, Mainz, Germany
# Copyright (C) 2015 Sebastian Software GmbH, Mainz, Germany
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
import os.path

from jasy.asset.Manager import AssetManager
from jasy.core.FileManager import FileManager

import jasy.core.Console as Console

import jasy.build.Asset as AssetBuilder
import jasy.build.Script as ScriptBuilder
import jasy.build.Style as StyleBuilder

KERNEL_NAME = "kernel"

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
def cacheManifest(profile):
	PREFIX = "{{prefix}}"
	HASH = "{{id}}"

	timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
	appcache = """CACHE MANIFEST

# Jasy AppCache Manifest file
# Version: {version}

CACHE:
{htmlfile}
{scripts}
{assets}

NETWORK:
*"""

	htmlcache = '<!DOCTYPE html><html manifest="{manifestfile}"></html>'

	destinationPath = profile.getDestinationPath()

	fileManager = FileManager(profile)
	session = profile.getSession()
	parts = profile.getParts()

	assetBuilder = AssetBuilder.AssetBuilder(profile)
	scriptBuilder = ScriptBuilder.ScriptBuilder(profile)
	styleBuilder = StyleBuilder.StyleBuilder(profile)

	assetManager = profile.getAssetManager()
	
	htmlfile = "index.html"

	for permutation in profile.permutate():
		scripts = []
		assets = []

		if KERNEL_NAME in parts:
			scripts.append("js/kernel.js")

		for part in parts:
			if part != KERNEL_NAME:
				scripts.append(profile.expandFileName("js/%s-{{id}}.js" % part))
				assets.append(profile.expandFileName("css/%s-{{id}}.css" % part))

		# TODO: How to get permutated asset list?
		for (srcFile, dstFile) in assetManager.getAssetList():
			assets.append(os.path.relpath(dstFile, profile.getDestinationPath()))

		appcacheFilename = "appcache-{{id}}.manifest"
		fileManager.writeFile(
			"{{destination}}/" + appcacheFilename,
			appcache.format(version=timestamp, htmlfile=htmlfile, scripts="\n".join(scripts), assets="\n".join(assets))
		)
		fileManager.writeFile("{{destination}}/index-{{id}}.html", htmlcache.format(manifestfile=profile.expandFileName(appcacheFilename)))
		Console.info("Generate manifest file...")



"""


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
			checksum = session.expandFileName(HASH) #instead of permutation.getChecksum()
		
		scriptFiles = []
		for script in scripts:
			scriptFiles.append(script % checksum)
		
		manifestFilename = "appcache-%s.manifest" % (checksum)
		fileManager.writeFile(PREFIX + "/" + manifestFilename, appcache.format(version=timestamp, htmlfile=htmlfile, kernel=kernel, scripts="\n".join(scriptFiles), assets="\n".join(assets)))
		
		fileManager.writeFile(PREFIX + "/index-%s.html" % (checksum), htmlcache % manifestFilename)

"""