Changes made from the original Weboob distribution :

- weboob\tools\parsers\__init__.py
		def get_parser(preference_order=('lxml', 'lxmlsoup')):
			return load_lxml()
			
- weboob\tools\borwer\browser.py
		delete import ssl
    