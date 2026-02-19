from mercury import __version__
from mercury.metadata import AUTHOR, CONTACT_EMAIL, PROJECT_VERSION_TAG, summary_line


def test_version_is_v3_series():
    assert __version__.startswith("3.")
    assert PROJECT_VERSION_TAG == "v3.0"


def test_metadata_contains_author_and_contact():
    line = summary_line().lower()
    assert AUTHOR in line
    assert CONTACT_EMAIL in line
