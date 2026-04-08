from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from signal_agent.domain.artifact import ArtifactRef


class ArtifactStore:
    """负责将中间结果持久化成工件并返回引用"""

    def __init__(self, base_dir: Path) -> None:
        self._base_dir = base_dir
        self._base_dir.mkdir(parents=True, exist_ok=True)

    def write_json_artifact(
        self, artifact_id: str, kind: str, payload: dict[str, Any]
    ) -> ArtifactRef:
        target = self._base_dir / f"{artifact_id}.json"
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return ArtifactRef(
            artifact_id=artifact_id,
            uri=str(target),
            kind=kind,
            metadata={"path": str(target)},
        )
