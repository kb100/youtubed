from sys import argv, exit
from urllib.parse import urlparse

if len(argv) != 3:
    exit(1)

url = urlparse(argv[1])
if url.scheme not in ["https", "http"]:
   exit(2) 

whitelist = []
try:
    with open(argv[2]) as f:
        line = f.readline().strip()
        while line:
            if line[0] != "#":
                whitelist.append(line)
            line = f.readline().strip()
except IOError:
    exit(3)

if url.netloc not in whitelist:
    exit(4)

exit(0)
