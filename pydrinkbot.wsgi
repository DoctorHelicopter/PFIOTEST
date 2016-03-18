import sys,os,logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,'/var/www/pydrinkbot')
os.chdir('/var/www/pydrinkbot')
from RunServer import app as application
