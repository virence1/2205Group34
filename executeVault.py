import sys
from vault import *

vote = {}
vote['vote'] = sys.argv[1]
vote['user'] = sys.argv[2]
generatePath(vote)