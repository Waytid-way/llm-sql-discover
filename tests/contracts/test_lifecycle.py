from importlib import import_module


def test_contract_meta_module_exposes_lifecycle_envelopes() -> None:
    module = import_module("sqltrace.contracts.meta")
    assert hasattr(module, "ContractMeta")
    assert hasattr(module, "BootstrapEnvelope")
    assert hasattr(module, "RunEnvelope")
    assert hasattr(module, "SnapshotEnvelope")
