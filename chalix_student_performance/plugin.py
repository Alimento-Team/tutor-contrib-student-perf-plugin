from __future__ import annotations

import os
from glob import glob

import importlib_resources
from tutor import hooks

from .__about__ import __version__

config = {
    "defaults": {
        "VERSION": __version__,
        "MLA_SERVICE_NAME": "mla-score",
        "EMOTION_SERVICE_NAME": "emotion-score",
        "MLA_PORT": 9010,
        "EMOTION_PORT": 9011,
        # Set these to registry-published images accessible from your cluster.
        "MLA_IMAGE": "docker.io/alimento/chalix-mla-prediction:latest",
        "EMOTION_IMAGE": "docker.io/alimento/chalix-emotion-prediction:latest",
        "MODEL_WEIGHTS_DIR": "/app/model_weights",
        "SHAPE_PREDICTOR_PATH": "/app/shape_predictor_68_face_landmarks.dat",
        "MINIO_ENDPOINT": "minio.openedx.svc.cluster.local:9000",
        "MINIO_SECURE": "false",
        # Use tutor config save --set ... in each environment.
        "MINIO_ACCESS_KEY": "",
        "MINIO_SECRET_KEY": "",
        "MLA_REPLICAS": 1,
        "EMOTION_REPLICAS": 1,
    },
    "unique": {},
    "overrides": {},
}

hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    str(importlib_resources.files("chalix_student_performance") / "templates")
)
hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("chalix_student_performance", "plugins"),
    ]
)

for path in glob(
    str(importlib_resources.files("chalix_student_performance") / "patches" / "*")
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (f"CHALIX_SP_{key}", value)
        for key, value in config["defaults"].items()
    ]
)
hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        (f"CHALIX_SP_{key}", value)
        for key, value in config["unique"].items()
    ]
)
hooks.Filters.CONFIG_OVERRIDES.add_items(list(config["overrides"].items()))
