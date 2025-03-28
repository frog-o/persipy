"""
Start up of the wrangler dev server in the direcory of that script

IMPORTANT: To not mess if running other python scripts if usung VSC for example use the option **<Run the Python File in Dedicated Terminal>**

[wrangler configuration](https://developers.cloudflare.com/workers/wrangler/configuration/)
[wrangler commands](https://developers.cloudflare.com/workers/wrangler/commands/#dev)
"""

import os
import subprocess

# Get the directory of the current script
tests_directory = os.path.dirname(os.path.abspath(__file__))

#prep symlyncs - first remove old then add new

# Define the symlink to be removed
ASSETS = os.path.abspath('./tests/wrangler/assets')
SRC = os.path.abspath('./src')
SRC_ASSETS = os.path.abspath('./tests/wrangler/assets/src')
DIST = os.path.abspath('./dist')
DIST_ASSETS = os.path.abspath('./tests/wrangler/assets/dist')
# Remove the symlinks
try:
    os.unlink(SRC_ASSETS)
    print(f'Symlink {SRC_ASSETS} has been removed.')
except:
    pass
try:
    os.unlink(DIST_ASSETS)
    print(f'Symlink {DIST_ASSETS} has been removed.')
except:
    pass

# Create the symlink
os.symlink(SRC, SRC_ASSETS)
print(f'Symlink created from {SRC} to {SRC_ASSETS}')
os.symlink(DIST, DIST_ASSETS)
print(f'Symlink created from {DIST} to {DIST_ASSETS}')


#running with secure context with local ip (not just localhost)
#that way can be accesed from test devices in the network
#and all js stuff which need secure context will work
command = "npx wrangler dev --ip 0.0.0.0 --port 443 --local-protocol https"

# Execute the command in the terminal
print('executing wrangler in:', tests_directory)
subprocess.run(command, shell=True, check=True, cwd=tests_directory)
