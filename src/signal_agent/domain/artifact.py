from typing import Any

from pydantic import BaseModel, Field


class ArtifactRef(BaseModel):
    """持久化工件引用。"""

    artifact_id: str
    uri: str
    kind: str
    metadata: dict[str, Any] = Field(default_factory=dict)
