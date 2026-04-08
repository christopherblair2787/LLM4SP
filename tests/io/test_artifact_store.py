from pathlib import Path

from signal_agent.io.artifact_store import ArtifactStore


def test_artifact_store_creates_json_artifact(tmp_path: Path) -> None:
    store = ArtifactStore(tmp_path)
    artifact = store.write_json_artifact(
        artifact_id="artifact-001",
        kind="signal_summary",
        payload={"snr_estimate_db": 12.5},
    )

    assert artifact.uri.endswith("artifact-001.json")
    assert (tmp_path / "artifact-001.json").exists()
