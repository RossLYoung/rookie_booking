#Dirty dirty hack if I want to bury the fabric package away in projectname/conf
#If fab is invoked from it's directory, parent imports (..) don't work.
#Is this cleaner than just having the fabfile directory on the top level??

from rosslyoung.config.fabfile import *