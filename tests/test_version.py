import re
import blendertoolbox


def test_version_matches_setup():
    with open('setup.py') as f:
        m = re.search(r"version='([^']+)'", f.read())
    assert m
    assert blendertoolbox.__version__ == m.group(1)
