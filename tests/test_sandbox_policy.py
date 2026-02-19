from mercury.sandbox import validate_manifest_local_only


def test_manifest_requires_explicit_local_only_policy():
    assert validate_manifest_local_only({"network_policy": "local-only"})
    assert not validate_manifest_local_only({})
    assert not validate_manifest_local_only({"network_policy": "internet"})
