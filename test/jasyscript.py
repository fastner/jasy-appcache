
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
	session.getAssetManager().addBuildProfile()
	session.getAssetManager().deploy(Resolver().addClassName(NAMESPACE).getIncludedClasses())
	kernelClasses = storeKernel("script/kernel.js")

	sortedClasses = Resolver().addClassName(NAMESPACE).excludeClasses(kernelClasses).getSortedClasses()
	storeCompressed(sortedClasses, "script/main.js")
	copyFile("source/index.html", "index.html")


@task("Source")
def source():
	jsFormatting.enable("comma")
	jsFormatting.enable("semicolon")
	jsOptimization.disable("privates")
	jsOptimization.disable("variables")
	jsOptimization.disable("declarations")
	jsOptimization.disable("blocks")
	
	session.getAssetManager().addSourceProfile()
	resolver = Resolver().addClassName(NAMESPACE)
	
	kernelClasses = storeKernel("script/kernel.js")

	sortedClasses = Resolver().addClassName(NAMESPACE).excludeClasses(kernelClasses).getSortedClasses()
	storeLoader(sortedClasses, "script/main.js")

@task
def run():
	serve()	
