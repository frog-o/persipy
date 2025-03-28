"""
adding symlink if external/js to src/js
"""

import os

EXTERNAL_JS = os.path.abspath('external/js')
SRC_JS = os.path.abspath('src/js')

# Remove the symlinks if exists
try:
    os.unlink(SRC_JS)
    print(f'Symlink {SRC_JS} has been removed.')
except:
    pass

# Create the symlink
os.symlink(EXTERNAL_JS, SRC_JS)
print(f'Symlink created from {EXTERNAL_JS} to {SRC_JS}')
