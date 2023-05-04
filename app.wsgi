python_home = '/var/www/html/assignment/'

import sys
import site

# Calculate path to site-packages directory.

# python_version = '.'.join(map(str, sys.version_info[:2]))
python_version = '3.7'

site_packages = python_home + '/lib/python%s/site-packages' % python_version

# Add the site-packages directory.

site.addsitedir(site_packages)


sys.path.insert(0,"/var/www/html/cc-assignment/")

from EmpApp import app as application
