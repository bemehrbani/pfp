#!/usr/bin/env python3
"""
Minab Incident Unified Data Model & Registry Validator
======================================================
People for Peace & Justice ry (PFPJ ry)
Campaign: Justice for Minab Children & Mothers
Incident: Shajareh Tayyebeh School Strike (February 28, 2026)

This script validates Minab incident datasets against the formal JSON schema,
enforces relational foreign key integrity, cross-validates bidirectional
parent-child relationships, verifies casualty counts in family clusters, and
exports clean CSV tables for platform & legal dissemination.

Usage:
    python3 validate_minab_data.py [--data PATH] [--schema PATH] [--export-csv DIR] [--strict] [--json]
"""

import os
import sys
import json
import re
import csv
import argparse
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime

# ANSI Color codes for formatted terminal output
class TermColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

@dataclass
class ValidationIssue:
    severity: str  # "ERROR", "WARNING", "INFO"
    code: str
    entity_type: str  # "victim", "mother", "family_cluster", "source", "metadata", "schema"
    entity_id: Optional[str]
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "severity": self.severity,
            "code": self.code,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "field": self.field,
            "message": self.message,
            "details": self.details
        }

@dataclass
class ValidationReport:
    is_valid: bool = True
    total_errors: int = 0
    total_warnings: int = 0
    total_info: int = 0
    total_victims: int = 0
    total_mothers: int = 0
    total_family_clusters: int = 0
    total_sources: int = 0
    issues: List[ValidationIssue] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)

    def add_issue(self, issue: ValidationIssue):
        self.issues.append(issue)
        if issue.severity == "ERROR":
            self.total_errors += 1
            self.is_valid = False
        elif issue.severity == "WARNING":
            self.total_warnings += 1
        elif issue.severity == "INFO":
            self.total_info += 1


class MinabDataValidator:
    """Validates the structure and relational integrity of the Minab incident dataset."""

    VALID_ROLES = {"student", "teacher", "staff", "parent", "community", "unborn_fetus"}
    VALID_STATUSES = {"killed", "injured", "missing"}
    VALID_MOTHER_STATUSES = {"killed", "injured", "survived"}
    VALID_ID_METHODS = {"visual", "dna", "personal_belongings", "unrecovered", "official_records", "eyewitness"}
    VALID_GENDERS = {"female", "male", "unknown", "other"}

    def __init__(self, data_path: str, schema_path: Optional[str] = None, strict: bool = False):
        self.data_path = os.path.abspath(data_path)
        self.schema_path = os.path.abspath(schema_path) if schema_path else None
        self.strict = strict
        self.data: Dict[str, Any] = {}
        self.schema: Optional[Dict[str, Any]] = None
        self.report = ValidationReport()

        # Lookup caches
        self.victims_by_id: Dict[str, Dict[str, Any]] = {}
        self.mothers_by_id: Dict[str, Dict[str, Any]] = {}
        self.clusters_by_id: Dict[str, Dict[str, Any]] = {}
        self.sources_by_id: Dict[str, Dict[str, Any]] = {}

    def load_files(self) -> bool:
        """Loads data and schema JSON files."""
        if not os.path.exists(self.data_path):
            self.report.add_issue(ValidationIssue(
                severity="ERROR",
                code="FILE_NOT_FOUND",
                entity_type="general",
                entity_id=None,
                field="data_path",
                message=f"Data file not found at: {self.data_path}"
            ))
            return False

        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except json.JSONDecodeError as e:
            self.report.add_issue(ValidationIssue(
                severity="ERROR",
                code="INVALID_JSON",
                entity_type="general",
                entity_id=None,
                field="data_file",
                message=f"Invalid JSON syntax in data file: {str(e)}",
                details={"line": e.lineno, "col": e.colno}
            ))
            return False

        if self.schema_path and os.path.exists(self.schema_path):
            try:
                with open(self.schema_path, "r", encoding="utf-8") as f:
                    self.schema = json.load(f)
            except Exception as e:
                self.report.add_issue(ValidationIssue(
                    severity="WARNING",
                    code="SCHEMA_LOAD_FAIL",
                    entity_type="schema",
                    entity_id=None,
                    field="schema_path",
                    message=f"Could not parse schema JSON: {str(e)}"
                ))

        return True

    def validate_with_jsonschema(self):
        """Validates data against JSON schema using jsonschema if available."""
        if not self.schema:
            return

        try:
            import jsonschema
            validator = jsonschema.Draft7Validator(self.schema)
            errors = sorted(validator.iter_errors(self.data), key=lambda e: e.path)
            for err in errors:
                path_str = " -> ".join([str(p) for p in err.path]) if err.path else "root"
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="SCHEMA_VALIDATION_ERROR",
                    entity_type="schema",
                    entity_id=path_str,
                    field=err.json_path if hasattr(err, "json_path") else path_str,
                    message=f"Schema violation at '{path_str}': {err.message}"
                ))
        except ImportError:
            self.report.add_issue(ValidationIssue(
                severity="INFO",
                code="JSONSCHEMA_LIB_UNAVAILABLE",
                entity_type="schema",
                entity_id=None,
                field=None,
                message="jsonschema Python package is not installed; executing internal rigorous structural validation."
            ))
            self._fallback_schema_validation()

    def _fallback_schema_validation(self):
        """Built-in deep structural validator when jsonschema library is absent."""
        required_top_level = ["incident_metadata", "sources", "victims", "mothers", "family_clusters"]
        for key in required_top_level:
            if key not in self.data:
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="MISSING_TOP_LEVEL_KEY",
                    entity_type="metadata",
                    entity_id=None,
                    field=key,
                    message=f"Missing required top-level key '{key}' in dataset."
                ))

    def build_indexes(self):
        """Indexes entities and detects duplicate IDs."""
        # 1. Sources
        sources = self.data.get("sources", [])
        self.report.total_sources = len(sources)
        for idx, src in enumerate(sources):
            if not isinstance(src, dict):
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="MALFORMED_ENTITY",
                    entity_type="source",
                    entity_id=f"index-{idx}",
                    field=None,
                    message="Source entry is not a JSON object."
                ))
                continue
            src_id = src.get("id")
            if not src_id:
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="MISSING_ID",
                    entity_type="source",
                    entity_id=f"index-{idx}",
                    field="id",
                    message=f"Source at index {idx} has no ID."
                ))
                continue
            if src_id in self.sources_by_id:
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="DUPLICATE_ID",
                    entity_type="source",
                    entity_id=src_id,
                    field="id",
                    message=f"Duplicate Source ID '{src_id}' detected."
                ))
            else:
                self.sources_by_id[src_id] = src

        # 2. Victims
        victims = self.data.get("victims", [])
        self.report.total_victims = len(victims)
        for idx, vic in enumerate(victims):
            if not isinstance(vic, dict):
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="MALFORMED_ENTITY",
                    entity_type="victim",
                    entity_id=f"index-{idx}",
                    field=None,
                    message="Victim entry is not a JSON object."
                ))
                continue
            vic_id = vic.get("id")
            if not vic_id:
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="MISSING_ID",
                    entity_type="victim",
                    entity_id=f"index-{idx}",
                    field="id",
                    message=f"Victim at index {idx} has no ID."
                ))
                continue
            if vic_id in self.victims_by_id:
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="DUPLICATE_ID",
                    entity_type="victim",
                    entity_id=vic_id,
                    field="id",
                    message=f"Duplicate Victim ID '{vic_id}' detected."
                ))
            else:
                self.victims_by_id[vic_id] = vic

        # 3. Mothers
        mothers = self.data.get("mothers", [])
        self.report.total_mothers = len(mothers)
        for idx, mom in enumerate(mothers):
            if not isinstance(mom, dict):
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="MALFORMED_ENTITY",
                    entity_type="mother",
                    entity_id=f"index-{idx}",
                    field=None,
                    message="MotherProfile entry is not a JSON object."
                ))
                continue
            mom_id = mom.get("id")
            if not mom_id:
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="MISSING_ID",
                    entity_type="mother",
                    entity_id=f"index-{idx}",
                    field="id",
                    message=f"Mother at index {idx} has no ID."
                ))
                continue
            if mom_id in self.mothers_by_id:
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="DUPLICATE_ID",
                    entity_type="mother",
                    entity_id=mom_id,
                    field="id",
                    message=f"Duplicate Mother ID '{mom_id}' detected."
                ))
            else:
                self.mothers_by_id[mom_id] = mom

        # 4. Family Clusters
        clusters = self.data.get("family_clusters", [])
        self.report.total_family_clusters = len(clusters)
        for idx, fc in enumerate(clusters):
            if not isinstance(fc, dict):
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="MALFORMED_ENTITY",
                    entity_type="family_cluster",
                    entity_id=f"index-{idx}",
                    field=None,
                    message="FamilyCluster entry is not a JSON object."
                ))
                continue
            cid = fc.get("cluster_id")
            if not cid:
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="MISSING_ID",
                    entity_type="family_cluster",
                    entity_id=f"index-{idx}",
                    field="cluster_id",
                    message=f"FamilyCluster at index {idx} has no cluster_id."
                ))
                continue
            if cid in self.clusters_by_id:
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="DUPLICATE_ID",
                    entity_type="family_cluster",
                    entity_id=cid,
                    field="cluster_id",
                    message=f"Duplicate FamilyCluster ID '{cid}' detected."
                ))
            else:
                self.clusters_by_id[cid] = fc

    def validate_entities_and_relationships(self):
        """Performs comprehensive relational and logical checks across all entities."""
        self._validate_sources()
        self._validate_victims()
        self._validate_mothers()
        self._validate_family_clusters()
        self._validate_metadata()

    def _validate_sources(self):
        """Validates sources attributes and scores."""
        for src_id, src in self.sources_by_id.items():
            if not src.get("title"):
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="EMPTY_TITLE",
                    entity_type="source",
                    entity_id=src_id,
                    field="title",
                    message=f"Source '{src_id}' is missing a title."
                ))
            if not src.get("outlet"):
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="EMPTY_OUTLET",
                    entity_type="source",
                    entity_id=src_id,
                    field="outlet",
                    message=f"Source '{src_id}' is missing an outlet organization."
                ))
            score = src.get("reliability_score")
            if score is None or not isinstance(score, (int, float)) or score < 0.0 or score > 1.0:
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="INVALID_RELIABILITY_SCORE",
                    entity_type="source",
                    entity_id=src_id,
                    field="reliability_score",
                    message=f"Source '{src_id}' has invalid reliability_score ({score}). Must be between 0.0 and 1.0."
                ))

    def _validate_victims(self):
        """Validates individual victim records and their foreign keys."""
        for vic_id, vic in self.victims_by_id.items():
            # Required names
            if not vic.get("full_name_en"):
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="MISSING_NAME_EN",
                    entity_type="victim",
                    entity_id=vic_id,
                    field="full_name_en",
                    message=f"Victim '{vic_id}' missing full_name_en."
                ))
            if not vic.get("full_name_fa"):
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="MISSING_NAME_FA",
                    entity_type="victim",
                    entity_id=vic_id,
                    field="full_name_fa",
                    message=f"Victim '{vic_id}' missing full_name_fa."
                ))

            # Role & Status & Identification Method enums
            role = vic.get("role")
            if role not in self.VALID_ROLES:
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="INVALID_ROLE",
                    entity_type="victim",
                    entity_id=vic_id,
                    field="role",
                    message=f"Victim '{vic_id}' has invalid role '{role}'. Allowed: {sorted(self.VALID_ROLES)}"
                ))

            status = vic.get("status")
            if status not in self.VALID_STATUSES:
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="INVALID_STATUS",
                    entity_type="victim",
                    entity_id=vic_id,
                    field="status",
                    message=f"Victim '{vic_id}' has invalid status '{status}'. Allowed: {sorted(self.VALID_STATUSES)}"
                ))

            id_method = vic.get("identification_method")
            if id_method not in self.VALID_ID_METHODS:
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="INVALID_IDENTIFICATION_METHOD",
                    entity_type="victim",
                    entity_id=vic_id,
                    field="identification_method",
                    message=f"Victim '{vic_id}' has invalid identification_method '{id_method}'. Allowed: {sorted(self.VALID_ID_METHODS)}"
                ))

            # Age validation
            age = vic.get("age")
            if age is not None:
                if not isinstance(age, (int, float)) or age < 0 or age > 120:
                    self.report.add_issue(ValidationIssue(
                        severity="ERROR",
                        code="INVALID_AGE",
                        entity_type="victim",
                        entity_id=vic_id,
                        field="age",
                        message=f"Victim '{vic_id}' has out-of-range age ({age})."
                    ))
            elif role != "unborn_fetus":
                self.report.add_issue(ValidationIssue(
                    severity="WARNING",
                    code="MISSING_AGE",
                    entity_type="victim",
                    entity_id=vic_id,
                    field="age",
                    message=f"Victim '{vic_id}' has no documented age."
                ))

            # Foreign Key: mother_id -> MotherProfile
            mother_id = vic.get("mother_id")
            if mother_id:
                if mother_id not in self.mothers_by_id:
                    self.report.add_issue(ValidationIssue(
                        severity="ERROR",
                        code="ORPHAN_MOTHER_REF",
                        entity_type="victim",
                        entity_id=vic_id,
                        field="mother_id",
                        message=f"Victim '{vic_id}' references non-existent mother_id '{mother_id}'."
                    ))
                else:
                    # Bidirectional check: Mother.children_ids must include this victim
                    mother_children = self.mothers_by_id[mother_id].get("children_ids", [])
                    if vic_id not in mother_children:
                        self.report.add_issue(ValidationIssue(
                            severity="WARNING",
                            code="BIDIRECTIONAL_RELATION_MISMATCH",
                            entity_type="victim",
                            entity_id=vic_id,
                            field="mother_id",
                            message=f"Victim '{vic_id}' links to mother '{mother_id}', but mother's children_ids list does not contain '{vic_id}'."
                        ))

            # Foreign Key: family_cluster_id -> FamilyCluster
            cluster_id = vic.get("family_cluster_id")
            if cluster_id:
                if cluster_id not in self.clusters_by_id:
                    self.report.add_issue(ValidationIssue(
                        severity="ERROR",
                        code="ORPHAN_CLUSTER_REF",
                        entity_type="victim",
                        entity_id=vic_id,
                        field="family_cluster_id",
                        message=f"Victim '{vic_id}' references non-existent family_cluster_id '{cluster_id}'."
                    ))
                else:
                    cluster_members = self.clusters_by_id[cluster_id].get("member_ids", [])
                    if vic_id not in cluster_members:
                        self.report.add_issue(ValidationIssue(
                            severity="WARNING",
                            code="CLUSTER_MEMBER_OMISSION",
                            entity_type="victim",
                            entity_id=vic_id,
                            field="family_cluster_id",
                            message=f"Victim '{vic_id}' is tagged with cluster '{cluster_id}', but cluster's member_ids does not list this victim."
                        ))

            # Sources resolution
            sources = vic.get("sources", [])
            if not sources:
                self.report.add_issue(ValidationIssue(
                    severity="WARNING",
                    code="UNSOURCED_RECORD",
                    entity_type="victim",
                    entity_id=vic_id,
                    field="sources",
                    message=f"Victim '{vic_id}' has no evidentiary sources cited."
                ))
            else:
                for s_id in sources:
                    if s_id not in self.sources_by_id:
                        self.report.add_issue(ValidationIssue(
                            severity="ERROR",
                            code="UNRESOLVED_SOURCE_REF",
                            entity_type="victim",
                            entity_id=vic_id,
                            field="sources",
                            message=f"Victim '{vic_id}' references unknown source ID '{s_id}'."
                        ))

    def _validate_mothers(self):
        """Validates mother profiles and their children links."""
        for mom_id, mom in self.mothers_by_id.items():
            if not mom.get("full_name_en"):
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="MISSING_NAME_EN",
                    entity_type="mother",
                    entity_id=mom_id,
                    field="full_name_en",
                    message=f"MotherProfile '{mom_id}' missing full_name_en."
                ))
            if not mom.get("full_name_fa"):
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="MISSING_NAME_FA",
                    entity_type="mother",
                    entity_id=mom_id,
                    field="full_name_fa",
                    message=f"MotherProfile '{mom_id}' missing full_name_fa."
                ))

            status = mom.get("status")
            if status not in self.VALID_MOTHER_STATUSES:
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="INVALID_STATUS",
                    entity_type="mother",
                    entity_id=mom_id,
                    field="status",
                    message=f"MotherProfile '{mom_id}' has invalid status '{status}'. Allowed: {sorted(self.VALID_MOTHER_STATUSES)}"
                ))

            # Check is_casualty flag consistency
            is_casualty = mom.get("is_casualty")
            if is_casualty is True and status == "survived":
                self.report.add_issue(ValidationIssue(
                    severity="WARNING",
                    code="STATUS_CASUALTY_INCONSISTENCY",
                    entity_type="mother",
                    entity_id=mom_id,
                    field="is_casualty",
                    message=f"MotherProfile '{mom_id}' has is_casualty=true but status='survived' (should be 'injured' or 'killed')."
                ))

            # Validate children_ids foreign keys
            children_ids = mom.get("children_ids", [])
            if not children_ids:
                self.report.add_issue(ValidationIssue(
                    severity="WARNING",
                    code="NO_CHILDREN_LINKED",
                    entity_type="mother",
                    entity_id=mom_id,
                    field="children_ids",
                    message=f"MotherProfile '{mom_id}' has empty children_ids list."
                ))
            else:
                for c_id in children_ids:
                    if c_id not in self.victims_by_id:
                        self.report.add_issue(ValidationIssue(
                            severity="ERROR",
                            code="ORPHAN_CHILD_REF",
                            entity_type="mother",
                            entity_id=mom_id,
                            field="children_ids",
                            message=f"MotherProfile '{mom_id}' references non-existent child victim ID '{c_id}'."
                        ))
                    else:
                        child_vic = self.victims_by_id[c_id]
                        if child_vic.get("mother_id") != mom_id:
                            self.report.add_issue(ValidationIssue(
                                severity="WARNING",
                                code="REVERSE_PARENT_MISMATCH",
                                entity_type="mother",
                                entity_id=mom_id,
                                field="children_ids",
                                message=f"MotherProfile '{mom_id}' claims child '{c_id}', but child's mother_id is set to '{child_vic.get('mother_id')}'."
                            ))

            # Validate other_family_member_ids
            other_members = mom.get("other_family_member_ids", [])
            for om_id in other_members:
                if om_id not in self.victims_by_id and om_id not in self.mothers_by_id:
                    self.report.add_issue(ValidationIssue(
                        severity="WARNING",
                        code="UNRESOLVED_OTHER_MEMBER_REF",
                        entity_type="mother",
                        entity_id=mom_id,
                        field="other_family_member_ids",
                        message=f"MotherProfile '{mom_id}' references other family member ID '{om_id}' not found in victims or mothers registry."
                    ))

            # Validate sources
            for s_id in mom.get("sources", []):
                if s_id not in self.sources_by_id:
                    self.report.add_issue(ValidationIssue(
                        severity="ERROR",
                        code="UNRESOLVED_SOURCE_REF",
                        entity_type="mother",
                        entity_id=mom_id,
                        field="sources",
                        message=f"MotherProfile '{mom_id}' references unknown source ID '{s_id}'."
                    ))

    def _validate_family_clusters(self):
        """Validates family clusters, member references, and casualty totals."""
        for cid, cluster in self.clusters_by_id.items():
            mother_id = cluster.get("mother_id")
            if mother_id and mother_id not in self.mothers_by_id:
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="ORPHAN_CLUSTER_MOTHER_REF",
                    entity_type="family_cluster",
                    entity_id=cid,
                    field="mother_id",
                    message=f"FamilyCluster '{cid}' references non-existent mother_id '{mother_id}'."
                ))

            member_ids = cluster.get("member_ids", [])
            if not member_ids:
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="EMPTY_CLUSTER_MEMBERS",
                    entity_type="family_cluster",
                    entity_id=cid,
                    field="member_ids",
                    message=f"FamilyCluster '{cid}' has no listed member_ids."
                ))

            actual_killed = 0
            actual_injured = 0
            for m_id in member_ids:
                if m_id in self.victims_by_id:
                    v_status = self.victims_by_id[m_id].get("status")
                    if v_status == "killed":
                        actual_killed += 1
                    elif v_status == "injured":
                        actual_injured += 1
                elif m_id in self.mothers_by_id:
                    m_status = self.mothers_by_id[m_id].get("status")
                    if m_status == "killed":
                        actual_killed += 1
                    elif m_status == "injured":
                        actual_injured += 1
                else:
                    self.report.add_issue(ValidationIssue(
                        severity="ERROR",
                        code="UNRESOLVED_CLUSTER_MEMBER",
                        entity_type="family_cluster",
                        entity_id=cid,
                        field="member_ids",
                        message=f"FamilyCluster '{cid}' member ID '{m_id}' does not exist in victims or mothers registry."
                    ))

            declared_killed = cluster.get("total_killed", 0)
            declared_injured = cluster.get("total_injured", 0)

            if declared_killed != actual_killed:
                self.report.add_issue(ValidationIssue(
                    severity="WARNING",
                    code="CLUSTER_KILLED_COUNT_MISMATCH",
                    entity_type="family_cluster",
                    entity_id=cid,
                    field="total_killed",
                    message=f"FamilyCluster '{cid}' declared total_killed={declared_killed}, but computed {actual_killed} from resolved members."
                ))

            if declared_injured != actual_injured:
                self.report.add_issue(ValidationIssue(
                    severity="WARNING",
                    code="CLUSTER_INJURED_COUNT_MISMATCH",
                    entity_type="family_cluster",
                    entity_id=cid,
                    field="total_injured",
                    message=f"FamilyCluster '{cid}' declared total_injured={declared_injured}, but computed {actual_injured} from resolved members."
                ))

    def _validate_metadata(self):
        """Validates incident metadata block."""
        meta = self.data.get("incident_metadata")
        if not meta or not isinstance(meta, dict):
            self.report.add_issue(ValidationIssue(
                severity="ERROR",
                code="MISSING_METADATA",
                entity_type="metadata",
                entity_id=None,
                field="incident_metadata",
                message="incident_metadata object is missing or invalid."
            ))
            return

        coords = meta.get("coordinates")
        if not coords or not isinstance(coords, dict):
            self.report.add_issue(ValidationIssue(
                severity="ERROR",
                code="INVALID_COORDINATES",
                entity_type="metadata",
                entity_id=None,
                field="coordinates",
                message="Metadata coordinates object missing or malformed."
            ))
        else:
            lat = coords.get("latitude")
            lng = coords.get("longitude")
            if lat is None or lng is None or not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                self.report.add_issue(ValidationIssue(
                    severity="ERROR",
                    code="OUT_OF_BOUNDS_COORDINATES",
                    entity_type="metadata",
                    entity_id=None,
                    field="coordinates",
                    message=f"Coordinates out of bounds: lat={lat}, lng={lng}."
                ))

    def run_validation(self) -> ValidationReport:
        """Executes full validation suite."""
        if not self.load_files():
            return self.report

        self.validate_with_jsonschema()
        self.build_indexes()
        self.validate_entities_and_relationships()

        # Compute summary statistics
        killed_students = sum(1 for v in self.victims_by_id.values() if v.get("role") == "student" and v.get("status") == "killed")
        killed_teachers = sum(1 for v in self.victims_by_id.values() if v.get("role") in {"teacher", "staff"} and v.get("status") == "killed")
        total_killed_all = sum(1 for v in self.victims_by_id.values() if v.get("status") == "killed")
        total_injured_all = sum(1 for v in self.victims_by_id.values() if v.get("status") == "injured")

        self.report.stats = {
            "total_victims": self.report.total_victims,
            "total_mothers": self.report.total_mothers,
            "total_family_clusters": self.report.total_family_clusters,
            "total_sources": self.report.total_sources,
            "killed_students": killed_students,
            "killed_teachers_and_staff": killed_teachers,
            "total_killed_documented": total_killed_all,
            "total_injured_documented": total_injured_all,
        }

        if self.strict and self.report.total_warnings > 0:
            self.report.is_valid = False

        return self.report

    def export_csvs(self, output_dir: str):
        """Exports clean flattened CSV files for platform integration and analytics."""
        os.makedirs(output_dir, exist_ok=True)

        # 1. Victims CSV
        victims_csv_path = os.path.join(output_dir, "minab_victims.csv")
        with open(victims_csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([
                "id", "full_name_en", "full_name_fa", "father_name", "mother_id",
                "age", "gender", "role", "grade_or_class", "status",
                "identification_method", "burial_location", "photo_url",
                "grid_index", "border_index", "biography_en", "biography_fa",
                "family_cluster_id", "sources", "injuries_description", "date_of_death"
            ])
            for vic in self.victims_by_id.values():
                grid = vic.get("photo_grid")
                grid_idx = ""
                border_idx = ""
                if isinstance(grid, dict):
                    grid_idx = grid.get("grid_index", "")
                    border_idx = grid.get("border_index", "")
                elif isinstance(grid, str):
                    grid_idx = grid

                bio = vic.get("biography")
                bio_en = ""
                bio_fa = ""
                if isinstance(bio, dict):
                    bio_en = bio.get("en", "")
                    bio_fa = bio.get("fa", "")
                elif isinstance(bio, str):
                    bio_en = bio

                writer.writerow([
                    vic.get("id", ""),
                    vic.get("full_name_en", ""),
                    vic.get("full_name_fa", ""),
                    vic.get("father_name", ""),
                    vic.get("mother_id", ""),
                    vic.get("age", ""),
                    vic.get("gender", ""),
                    vic.get("role", ""),
                    vic.get("grade_or_class", ""),
                    vic.get("status", ""),
                    vic.get("identification_method", ""),
                    vic.get("burial_location", ""),
                    vic.get("photo_url", ""),
                    grid_idx,
                    border_idx,
                    bio_en,
                    bio_fa,
                    vic.get("family_cluster_id", ""),
                    "; ".join(vic.get("sources", [])),
                    vic.get("injuries_description", ""),
                    vic.get("date_of_death", "2026-02-28")
                ])

        # 2. Mothers CSV
        mothers_csv_path = os.path.join(output_dir, "minab_mothers.csv")
        with open(mothers_csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([
                "id", "full_name_en", "full_name_fa", "spouse_name", "is_casualty",
                "status", "profession", "narrative_summary_en", "narrative_summary_fa",
                "children_count", "children_ids", "other_family_member_ids",
                "family_cluster_id", "sources"
            ])
            for mom in self.mothers_by_id.values():
                summary = mom.get("narrative_summary")
                sum_en = ""
                sum_fa = ""
                if isinstance(summary, dict):
                    sum_en = summary.get("en", "")
                    sum_fa = summary.get("fa", "")
                elif isinstance(summary, str):
                    sum_en = summary

                children = mom.get("children_ids", [])
                writer.writerow([
                    mom.get("id", ""),
                    mom.get("full_name_en", ""),
                    mom.get("full_name_fa", ""),
                    mom.get("spouse_name", ""),
                    "YES" if mom.get("is_casualty") else "NO",
                    mom.get("status", ""),
                    mom.get("profession", ""),
                    sum_en,
                    sum_fa,
                    len(children),
                    "; ".join(children),
                    "; ".join(mom.get("other_family_member_ids", [])),
                    mom.get("family_cluster_id", ""),
                    "; ".join(mom.get("sources", []))
                ])

        # 3. Family Clusters CSV
        clusters_csv_path = os.path.join(output_dir, "minab_family_clusters.csv")
        with open(clusters_csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([
                "cluster_id", "family_surname_en", "family_surname_fa", "mother_id",
                "total_killed", "total_injured", "member_count", "member_ids",
                "description_en", "description_fa", "neighborhood_or_residence", "sources"
            ])
            for fc in self.clusters_by_id.values():
                desc = fc.get("description")
                desc_en = ""
                desc_fa = ""
                if isinstance(desc, dict):
                    desc_en = desc.get("en", "")
                    desc_fa = desc.get("fa", "")
                elif isinstance(desc, str):
                    desc_en = desc

                members = fc.get("member_ids", [])
                writer.writerow([
                    fc.get("cluster_id", ""),
                    fc.get("family_surname_en", ""),
                    fc.get("family_surname_fa", ""),
                    fc.get("mother_id", ""),
                    fc.get("total_killed", 0),
                    fc.get("total_injured", 0),
                    len(members),
                    "; ".join(members),
                    desc_en,
                    desc_fa,
                    fc.get("neighborhood_or_residence", ""),
                    "; ".join(fc.get("sources", []))
                ])

        # 4. Sources CSV
        sources_csv_path = os.path.join(output_dir, "minab_sources.csv")
        with open(sources_csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([
                "id", "title", "outlet", "url", "publication_date",
                "tier", "reliability_score", "notes", "archive_hash"
            ])
            for src in self.sources_by_id.values():
                writer.writerow([
                    src.get("id", ""),
                    src.get("title", ""),
                    src.get("outlet", ""),
                    src.get("url", ""),
                    src.get("publication_date", ""),
                    src.get("tier", ""),
                    src.get("reliability_score", ""),
                    src.get("notes", ""),
                    src.get("archive_hash", "")
                ])

        return {
            "victims_csv": victims_csv_path,
            "mothers_csv": mothers_csv_path,
            "family_clusters_csv": clusters_csv_path,
            "sources_csv": sources_csv_path,
        }


def print_cli_report(report: ValidationReport, strict: bool = False):
    """Outputs a clean formatted terminal validation summary."""
    print("\n" + "="*80)
    print(f"{TermColors.BOLD}{TermColors.CYAN}MINAB INCIDENT DATA ARCHITECTURE VALIDATION REPORT{TermColors.RESET}")
    print("="*80)

    # Status Banner
    if report.is_valid:
        print(f"\n{TermColors.GREEN}{TermColors.BOLD}[PASSED] ALL DATA INTEGRITY & FOREIGN KEY CHECKS SUCCEEDED{TermColors.RESET}")
    else:
        print(f"\n{TermColors.RED}{TermColors.BOLD}[FAILED] VALIDATION FOUND INTEGRITY ERRORS{TermColors.RESET}")

    # Entity counts
    print(f"\n{TermColors.BOLD}Entity Counts:{TermColors.RESET}")
    print(f"  • Victims Documented:         {report.total_victims}")
    print(f"  • Mother Profiles:           {report.total_mothers}")
    print(f"  • Family Clusters:           {report.total_family_clusters}")
    print(f"  • Sources & Citations:       {report.total_sources}")

    if report.stats:
        print(f"\n{TermColors.BOLD}Casualty Summary:{TermColors.RESET}")
        print(f"  • Student Martyrs:           {report.stats.get('killed_students', 0)}")
        print(f"  • Staff / Teacher Martyrs:   {report.stats.get('killed_teachers_and_staff', 0)}")
        print(f"  • Total Documented Killed:   {report.stats.get('total_killed_documented', 0)}")
        print(f"  • Total Documented Injured:  {report.stats.get('total_injured_documented', 0)}")

    # Issues breakdown
    print(f"\n{TermColors.BOLD}Issues Breakdown:{TermColors.RESET}")
    print(f"  • Errors:   {TermColors.RED if report.total_errors else TermColors.GREEN}{report.total_errors}{TermColors.RESET}")
    print(f"  • Warnings: {TermColors.YELLOW if report.total_warnings else TermColors.GREEN}{report.total_warnings}{TermColors.RESET}")
    print(f"  • Info:     {report.total_info}")

    if report.issues:
        print(f"\n{TermColors.BOLD}Detailed Issues Log:{TermColors.RESET}")
        for idx, issue in enumerate(report.issues, 1):
            if issue.severity == "ERROR":
                color = TermColors.RED
            elif issue.severity == "WARNING":
                color = TermColors.YELLOW
            else:
                color = TermColors.BLUE

            prefix = f"{color}[{issue.severity}]{TermColors.RESET}"
            entity_tag = f"({issue.entity_type.upper()}:{issue.entity_id or 'global'})"
            print(f"  {idx:02d}. {prefix} {entity_tag} [{issue.code}] {issue.message}")

    print("\n" + "="*80 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Validate Minab Incident dataset integrity and export clean CSVs.")
    parser.add_argument("--data", "-d", default=os.path.join(os.path.dirname(__file__), "minab_incident_dataset.json"),
                        help="Path to minab_incident_dataset.json")
    parser.add_argument("--schema", "-s", default=os.path.join(os.path.dirname(__file__), "minab_data_model.json"),
                        help="Path to minab_data_model.json schema file")
    parser.add_argument("--export-csv", "-o", default=None,
                        help="Target directory to export flattened CSV files")
    parser.add_argument("--strict", action="store_true",
                        help="Strict mode: treat warnings as fatal validation errors")
    parser.add_argument("--json", action="store_true",
                        help="Output report formatted as JSON for CI/CD integration")

    args = parser.parse_args()

    validator = MinabDataValidator(data_path=args.data, schema_path=args.schema, strict=args.strict)
    report = validator.run_validation()

    if args.export_csv and report.is_valid:
        export_paths = validator.export_csvs(args.export_csv)
        if not args.json:
            print(f"{TermColors.GREEN}Successfully exported clean CSVs to {args.export_csv}:{TermColors.RESET}")
            for k, p in export_paths.items():
                print(f"  - {k}: {p}")

    if args.json:
        output_payload = {
            "isValid": report.is_valid,
            "totalErrors": report.total_errors,
            "totalWarnings": report.total_warnings,
            "stats": report.stats,
            "issues": [i.to_dict() for i in report.issues]
        }
        print(json.dumps(output_payload, indent=2))
    else:
        print_cli_report(report, strict=args.strict)

    sys.exit(0 if report.is_valid else 1)


if __name__ == "__main__":
    main()
