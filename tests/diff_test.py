import allib.diff

def test_diff():
	a = 'foo\nbar\n'
	b = 'foobar\nbarbaz\n'
	diff = allib.diff.get_diff_string(a, b)
	assert '''--- 
+++ 
@@ -1,2 +1,2 @@
-foo
-bar
+foobar
+barbaz
''' == diff
