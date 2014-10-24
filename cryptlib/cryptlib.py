

def hex_to_base64(hexval):
	""" Returns: base64 encoded value for a given
		hex value. """
	return hexval.decode('hex').encode('base64')

def test_hex_to_base64():
	results = hex_to_base64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d")
	assert results == "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t\n"

def runtests():
	import inspect
	thismodule = __import__(inspect.getmodulename(__file__))
	for name in dir(thismodule):
		obj = getattr(thismodule, name)
		if inspect.isfunction(obj) and name.startswith('test_'):
			obj()
			print name, "tests passed!"

if __name__ == "__main__":
	runtests()
