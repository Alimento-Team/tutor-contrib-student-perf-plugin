Chalix Student Performance Tutor Plugin
======================================

Deploys MLA and Emotion score APIs as internal-only Kubernetes services for Tutor.

Services are exposed as ClusterIP only:

- ``mla-score.<namespace>.svc.cluster.local:9010``
- ``emotion-score.<namespace>.svc.cluster.local:9011``

No ingress or Caddy route is created by this plugin.

Quick Start
-----------

1. Install the plugin:

.. code-block:: bash

	cd tutor-contrib-chalix-student-performance
	pip install -e .
	tutor plugins enable chalix_student_performance

2. Set image tags and runtime settings:

.. code-block:: bash

	tutor config save --set CHALIX_SP_MLA_IMAGE=docker.io/<org>/chalix-mla-prediction:<tag>
	tutor config save --set CHALIX_SP_EMOTION_IMAGE=docker.io/<org>/chalix-emotion-prediction:<tag>
	tutor config save --set CHALIX_SP_MINIO_ENDPOINT=minio.openedx.svc.cluster.local:9000
	tutor config save --set CHALIX_SP_MINIO_ACCESS_KEY=<access_key>
	tutor config save --set CHALIX_SP_MINIO_SECRET_KEY=<secret_key>

3. Render and apply Kubernetes manifests:

.. code-block:: bash

	tutor config save
	tutor k8s start

4. Verify services are internal-only:

.. code-block:: bash

	kubectl get svc -n openedx | grep -E 'mla-score|emotion-score'
	kubectl exec -it -n openedx deploy/lms -- \
	  curl -sS http://emotion-score.openedx.svc.cluster.local:9011/docs >/dev/null

Configuration
-------------

- ``CHALIX_SP_MLA_SERVICE_NAME`` default: ``mla-score``
- ``CHALIX_SP_EMOTION_SERVICE_NAME`` default: ``emotion-score``
- ``CHALIX_SP_MLA_PORT`` default: ``9010``
- ``CHALIX_SP_EMOTION_PORT`` default: ``9011``
- ``CHALIX_SP_MLA_IMAGE`` default: ``docker.io/alimento/chalix-mla-prediction:latest``
- ``CHALIX_SP_EMOTION_IMAGE`` default: ``docker.io/alimento/chalix-emotion-prediction:latest``
- ``CHALIX_SP_MINIO_ENDPOINT`` default: ``minio.openedx.svc.cluster.local:9000``

Notes
-----

- The plugin patches Kubernetes services/deployments and LMS settings only.
- There is no Caddy patch in this plugin, so the APIs are not externally routed.
