import sys
from unittest.mock import MagicMock

# The tests don't need a real VLC install: replace the vlc module with a stand-in.
sys.modules["vlc"] = MagicMock()
