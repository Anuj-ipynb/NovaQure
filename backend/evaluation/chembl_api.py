"""
NovaQure

ChEMBL API Client

Provides a thin service layer over the official ChEMBL REST API.

Responsibilities
----------------
- Search targets
- Retrieve bioactivity records
- Handle pagination
- Handle retries
- Provide typed models

Author:
    NovaQure Evaluation Team
"""

from __future__ import annotations

import logging
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from backend.configs.chembl_config import (
    CHEMBL_BASE_URL,
    DEFAULT_ACTIVITY_TYPE,
    DEFAULT_TIMEOUT,
    PAGE_SIZE,
)

from backend.evaluation.chembl_models import (
    ChEMBLActivity,
    ChEMBLTarget,
)

logger = logging.getLogger(__name__)

TARGET_TYPE_SINGLE_PROTEIN = "SINGLE PROTEIN"


class ChEMBLAPI:
    """
    Wrapper around the official ChEMBL REST API.
    """

    def __init__(self) -> None:

        self.session = requests.Session()

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[
                429,
                500,
                502,
                503,
                504,
            ],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy
        )

        self.session.mount(
            "https://",
            adapter,
        )

        self.session.headers.update(
            {
                "Accept": "application/json",
            }
        )

    # ---------------------------------------------------------
    # Internal HTTP Helper
    # ---------------------------------------------------------

    def _get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Execute a GET request against ChEMBL.
        """

        url = f"{CHEMBL_BASE_URL}/{endpoint}"

        logger.debug(
            "GET %s",
            url,
        )

        try:

            response = self.session.get(
                url,
                params=params,
                timeout=DEFAULT_TIMEOUT,
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as exc:

            logger.exception(
                "Failed ChEMBL request."
            )

            raise RuntimeError(
                f"Unable to communicate with ChEMBL: {exc}"
            ) from exc

    # ---------------------------------------------------------
    # Pagination Helper
    # ---------------------------------------------------------

    def _paginate(
        self,
        endpoint: str,
        params: dict[str, Any],
        result_key: str,
    ) -> list[dict[str, Any]]:
        """
        Retrieve all paginated records from ChEMBL.
        """

        records: list[dict[str, Any]] = []

        offset = 0

        while True:

            payload = {
                **params,
                "limit": PAGE_SIZE,
                "offset": offset,
            }

            response = self._get(
                endpoint,
                payload,
            )

            page = response.get(
                result_key,
                [],
            )

            if not page:
                break

            records.extend(page)

            if len(page) < PAGE_SIZE:
                break

            offset += PAGE_SIZE

        logger.info(
            "Retrieved %d records from %s.",
            len(records),
            endpoint,
        )

        return records

    # ---------------------------------------------------------
    # Target Search
    # ---------------------------------------------------------

    def search_target(
        self,
        protein_name: str,
    ) -> list[ChEMBLTarget]:
        """
        Search ChEMBL for target proteins.

        Parameters
        ----------
        protein_name : str
            Protein name (e.g. EGFR, KRAS).

        Returns
        -------
        list[ChEMBLTarget]
            Matching ChEMBL targets.
        """

        logger.info(
            "Searching ChEMBL target '%s'.",
            protein_name,
        )

        response = self._get(
            endpoint="target/search",
            params={
                "q": protein_name,
            },
        )

        targets: list[ChEMBLTarget] = []

        for item in response.get("targets", []):

            targets.append(

                ChEMBLTarget(

                    chembl_id=item.get(
                        "target_chembl_id",
                        "",
                    ),

                    name=item.get(
                        "pref_name",
                        "",
                    ),

                    organism=item.get(
                        "organism",
                        "",
                    ),

                    target_type=item.get(
                        "target_type",
                        "",
                    ),

                )

            )

        targets.sort(
            key=lambda target: (
                target.target_type != TARGET_TYPE_SINGLE_PROTEIN,
                target.organism != "Homo sapiens",
                target.name.lower() != protein_name.lower(),
            )
        )

        if targets:
            logger.info(
                "Selected target: %s (%s)",
                targets[0].chembl_id,
                targets[0].target_type,
            )

        logger.info(
            "Found %d matching targets.",
            len(targets),
        )

        return targets

    # ---------------------------------------------------------
    # Activity Retrieval
    # ---------------------------------------------------------

    def fetch_activities(
        self,
        target_chembl_id: str,
        activity_type: str = DEFAULT_ACTIVITY_TYPE,
    ) -> list[ChEMBLActivity]:
        """
        Retrieve bioactivity records for a target.

        Parameters
        ----------
        target_chembl_id : str
            ChEMBL target identifier.

        activity_type : str
            Activity type (default: IC50).

        Returns
        -------
        list[ChEMBLActivity]
        """

        logger.info(
            "Fetching %s activities for %s.",
            activity_type,
            target_chembl_id,
        )

        records = self.fetch_activity_records(target_chembl_id, activity_type)

        activities: list[ChEMBLActivity] = []
        seen: set[tuple[str, float]] = set()

        for item in records:

            smiles = item.get("canonical_smiles")
            value = item.get("standard_value")

            if not smiles or value is None:
                continue

            if item.get("standard_flag") != 1:
                continue

            try:

                key = (
                    smiles,
                    float(value),
                )

                if key in seen:
                    continue

                seen.add(key)

                activity = ChEMBLActivity(

                    smiles=smiles,

                    activity_type=item.get(
                        "standard_type",
                        "",
                    ),

                    value=float(value),

                    units=item.get(
                        "standard_units",
                        "",
                    ),

                    relation=item.get(
                        "standard_relation",
                        "=",
                    ),

                    pchembl_value=(
                        float(item["pchembl_value"])
                        if item.get("pchembl_value")
                        else None
                    ),

                )

                activities.append(activity)

            except (TypeError, ValueError):

                logger.warning(
                    "Skipping malformed activity record."
                )

                continue

        logger.info(
            "Collected %d activity records.",
            len(activities),
        )

        return activities

    def fetch_activity_records(
        self,
        target_chembl_id: str,
        activity_type: str = DEFAULT_ACTIVITY_TYPE,
    ) -> list[dict[str, Any]]:
        """
        Return raw ChEMBL activity records.
        """

        return self._paginate(
            endpoint="activity",
            params={
                "target_chembl_id": target_chembl_id,
                "standard_type": activity_type,
            },
            result_key="activities",
        )

    # ---------------------------------------------------------
    # Health Check
    # ---------------------------------------------------------

    def ping(self) -> bool:
        """
        Verify connectivity with the ChEMBL API.

        Returns
        -------
        bool
            True if the API is reachable.
        """

        try:

            self._get("status")

            logger.info(
                "ChEMBL API is reachable."
            )

            return True

        except RuntimeError:

            logger.error(
                "Unable to reach ChEMBL API."
            )

            return False

    # ---------------------------------------------------------
    # Session Cleanup
    # ---------------------------------------------------------

    def close(self) -> None:
        """
        Close the underlying HTTP session.
        """

        self.session.close()

    # ---------------------------------------------------------
    # Context Manager Support
    # ---------------------------------------------------------

    def __enter__(self) -> "ChEMBLAPI":

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:

        self.close()