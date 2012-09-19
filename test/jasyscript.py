
NAMESPACE = "appcacheTest.Test"

@task("Clean")
def clean():
	session.clean()


@task("Distclean")
def distclean():
	session.clean()
	removeDir("build")
	removeDir("source/script")


@task("Build")
def build():
	assetManager = AssetManager(session)
	fileManager = FileManager(session)
	outputManager = OutputManager(session, assetManager)
	
	assetManager.addBuildProfile()
	assetManager.deploy(Resolver(session).addClassName(NAMESPACE).getIncludedClasses())
	
	outputManager.storeKernel("$prefix/script/kernel.js")

	sortedClasses = Resolver(session).addClassName(NAMESPACE).getSortedClasses()
	outputManager.storeCompressed(sortedClasses, "$prefix/script/main.js")
	fileManager.copyFile("source/index.html", "$prefix/index.html")


@task("Source")
def source():
	assetManager = AssetManager(session)
	fileManager = FileManager(session)
	outputManager = OutputManager(session, assetManager, 0, 1)
	
	assetManager.addSourceProfile()
	resolver = Resolver(session).addClassName(NAMESPACE)
	
	kernelClasses = outputManager.storeKernel("$prefix/script/kernel.js", debug=True)

	sortedClasses = Resolver(session).addClassName(NAMESPACE).getSortedClasses()
	outputManager.storeLoader(sortedClasses, "$prefix/script/main.js", "window.upstart();")

@task
def run():
	Server().start()
