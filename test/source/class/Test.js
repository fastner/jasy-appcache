
window.upstart = function() {
  /** #asset(qunit.css) */
  uri = jasy.Asset.toUri("qunit.css");
  core.io.StyleSheet.load(uri);
}

QUnit.test("Test 1", function() {
  QUnit.ok(true, "Test test");
});

window.appcacheTest = {
	Test: {
		boot: function() {}
	}
};