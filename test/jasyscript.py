
profile = Profile(session)
profile.registerPart("kernel", className="appcacheTest.Test")


@task("Clean")
def clean():
	core.clean()


@task("Distclean")
def distclean():
	core.distclean()


@task("Build")
def build():
	"""Generate deployable and combined build version"""

	# Enable both debugging and final
	profile.permutateField("debug")

	# Enable copying and hashing of assets
	profile.setHashAssets(True)
	profile.setCopyAssets(True)

	# Start actual build
	Build.run(profile)

	profile.getFileManager().copyFile("source/index.html", "{{destination}}/index.html")

	appcache.cacheManifest(profile)


@task("Source")
def source():
	# Force debug enabled
	profile.setField("debug", True)

	# Load all scripts/assets from source folder
	profile.setUseSource(True)

	# Start actual build
	Build.run(profile)

	import fileinput
	textToSearch = "((function(){return this})())"
	textToReplace = ")(window"
	for line in fileinput.input("source/js/kernel.js", inplace=True):
		print(line.replace(textToSearch, textToReplace), end='')
	
	

@task
def run():
	session.pause()
	Server().start()
	session.resume()
