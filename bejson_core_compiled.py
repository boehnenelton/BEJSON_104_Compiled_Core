"""
Library:         bejson_core_compiled.py
Family:          Compiled
Description:     Single-file stdlib-only compiled BEJSON+MFDB core for Python.
                 Merges errors/env/path_guard/core/validator/list_validator/
                 mfdb_validator/mfdb_core. No intra-package imports.
                 C-01 FIXED: path_guard v1.1.0 includes
                 2026-08-07 sibling-directory bypass fix in bejson_safe_join().
Version:         1.1.1
Library_Version: 226
Date:            2026-08-19
Author:          Elton Boehnen
Contact:         boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton
Schema_Name:     MFDB-132
RELATIONAL_ID:   d8011c25-dc40-4835-a938-ff727e6eb7a4

Merged sources:
  bejson_errors        v2.4.0
  bejson_env           v2.1.2
  bejson_path_guard    v1.1.0   (C-01 security fix)
  bejson_core          v2.0.5
  bejson_validator     v2.0.3
  bejson_list_validator v1.3.1  (surface parity)
  mfdb_validator       v2.2.0
  mfdb_core            v2.3.0
"""
from __future__ import annotations
import json,os,sys,time,shutil,tempfile,zipfile,hashlib,logging
from datetime import datetime,timezone
from dataclasses import dataclass,field as dc_field
from pathlib import Path
from typing import Any,Callable,Dict,List,NamedTuple,Optional,Set,Tuple,Union
VERSION="1.1.1"


# ==========================================================================
# SECTION 1 — ERROR REGISTRY
# Sources: bejson_errors v2.4.0
# ==========================================================================

# ---------------------------------------------------------------------------
# BEJSON Validation (1-16)
# ---------------------------------------------------------------------------
E_INVALID_JSON                       = 1
E_MISSING_MANDATORY_KEY              = 2
E_INVALID_FORMAT                     = 3
E_INVALID_VERSION                    = 4
E_INVALID_RECORDS_TYPE               = 5
E_INVALID_FIELDS                     = 6
E_INVALID_VALUES                     = 7
E_TYPE_MISMATCH                      = 8
E_RECORD_LENGTH_MISMATCH             = 9
E_RESERVED_KEY_COLLISION             = 10
E_INVALID_RECORD_TYPE_PARENT         = 11
E_NULL_VIOLATION                     = 12
E_FILE_NOT_FOUND                     = 13
E_PERMISSION_DENIED                  = 14
E_ATOMIC_WRITE_FAILED                = 15
E_INVALID_FORMAT_CREATOR             = 16

# BEJSON Core ops (17-29)
# Codes 17-19: parse/serialization layer — added v2.3.0 (parity with TS v2.3.0)
E_CORE_PARSE_ERROR                   = 17
E_CORE_SERIALIZATION_ERROR           = 18
E_CORE_NULL_DOCUMENT                 = 19
E_CORE_INVALID_VERSION               = 20
E_CORE_INVALID_OPERATION             = 21
E_CORE_INDEX_OUT_OF_BOUNDS           = 22
E_CORE_FIELD_NOT_FOUND               = 23
E_CORE_TYPE_CONVERSION_FAILED        = 24
E_CORE_BACKUP_FAILED                 = 25
E_CORE_WRITE_FAILED                  = 26
E_CORE_QUERY_FAILED                  = 27
E_CORE_ENCRYPTION_FAILED             = 28
E_CORE_DECRYPTION_FAILED             = 29

# Aliases — map TS BEJSON_CORE_CODES aliases to canonical codes above
E_CORE_UNSUPPORTED_OPERATION         = E_CORE_INVALID_OPERATION    # 21
E_CORE_WRITE_TYPE_MISMATCH           = E_TYPE_MISMATCH             # 8
E_CORE_WRITE_LENGTH_MISMATCH         = E_RECORD_LENGTH_MISMATCH    # 9

# ---------------------------------------------------------------------------
# MFDB Validation (30-42)
# ---------------------------------------------------------------------------
E_MFDB_NOT_MANIFEST                  = 30
E_MFDB_NOT_ENTITY_FILE               = 31
E_MFDB_MANIFEST_RECORDS_TYPE         = 32
E_MFDB_ENTITY_NOT_FOUND              = 33
E_MFDB_ENTITY_NAME_MISMATCH          = 34
E_MFDB_DUPLICATE_ENTRY               = 35
E_MFDB_NO_PARENT_HIERARCHY           = 36
E_MFDB_MANIFEST_NOT_FOUND            = 37
E_MFDB_BIDIRECTIONAL_FAIL            = 38
E_MFDB_FK_UNRESOLVED                 = 39
E_MFDB_MISSING_REQUIRED_FIELD        = 40
E_MFDB_NULL_REQUIRED                 = 41
E_MFDB_INVALID_ARCHIVE               = 42

# ---------------------------------------------------------------------------
# MFDB Core ops (50-72)
# Codes 57-60: added v2.3.0 (parity with TS MFDB_CORE_CODES v2.3.0)
# ---------------------------------------------------------------------------
E_MFDB_CORE_MANIFEST_NOT_FOUND       = 50
E_MFDB_CORE_ENTITY_NOT_FOUND         = 51
E_MFDB_CORE_WRITE_FAILED             = 52
E_MFDB_CORE_LOCK_FAILED              = 53
E_MFDB_CORE_INVALID_OPERATION        = 54
E_MFDB_CORE_INDEX_OUT_OF_BOUNDS      = 55
E_MFDB_CORE_JOIN_FAILED              = 56
E_MFDB_CORE_DUPLICATE_ENTITY_NAME    = 57
E_MFDB_CORE_RECORD_COUNT_SYNC_FAILED = 58
E_MFDB_CORE_NULL_MANIFEST            = 59
E_MFDB_CORE_ENTITY_NOT_IN_MANIFEST   = 60
E_MFDB_CORE_ARCHIVE_ERROR            = 70
E_MFDB_CORE_MOUNT_CONFLICT           = 71
E_MFDB_CORE_CREATE_FAILED            = 72

# Core_Nesting codes moved to lib_bejson_CoreNesting_bejson_errors.py (v2.4.0)
# Cognition codes moved to lib_bejson_Cognition_bejson_errors.py (v2.4.0)


# ==========================================================================
# SECTION 2 — ENV & PATH RESOLUTION
# Sources: bejson_env v2.1.2
# ==========================================================================

import os
import sys
from pathlib import Path

def source_env(override_path: str = None) -> bool:
    """
    Mandatory Environment Sourcing (Section 54).
    Priority: 1. override_path, 2. ENV_FILE_PATH, 3. Android Storage, 4. Home
    """
    env_path = override_path or os.environ.get("ENV_FILE_PATH")
    search_paths = [
        Path(env_path) if env_path else None,
        Path("/storage/emulated/0/env_file.py"),
        Path.home() / "env_file.py"
    ]
    for p in search_paths:
        if p and p.exists():
            try:
                exec(p.read_text(), globals())
                return True
            except Exception:
                continue
    return False

def resolve_path(path_str: str) -> str:
    """
    Resolves system placeholders and absolute paths to environment-relative paths.
    Prioritizes environment variables (ADMIN_ROOT, BEJSON_LIB_ROOT, etc).
    """
    if not path_str:
        return path_str
    
    # Define standard roots with defaults
    home = os.environ.get("HOME", os.path.expanduser("~"))
    
    # Storage and Admin Roots
    # Fallback to HOME if storage root is unset to avoid hardcodes.
    storage_root = os.environ.get("BEJSON_STORAGE_ROOT", home)
    admin_root   = os.environ.get("ADMIN_ROOT", os.path.join(storage_root, "Admin"))
    
    # Library Root Resolution (Admin/libraries fallback to ~/libraries)
    lib_root = os.environ.get("BEJSON_LIB_ROOT")
    if not lib_root:
        candidate_admin = os.path.join(admin_root, "libraries")
        candidate_home  = os.path.join(home, "libraries")
        lib_root = candidate_admin if os.path.exists(candidate_admin) else candidate_home
    
    mappings = {
        "{BEJSON_LIB_ROOT}": lib_root,
        "{ADMIN_ROOT}": admin_root,
        "{INTERNAL_STORAGE}": storage_root,
        "{HOME}": home
    }
    
    # Legacy absolute paths to be replaced
    # Only replace if storage_root is explicitly set to avoid "Vanishing Data".
    if os.environ.get("BEJSON_STORAGE_ROOT"):
        mappings["/storage/emulated/0"] = storage_root
        mappings["/data/data/com.termux/files/home"] = home
    
    resolved = str(path_str)
    
    # Sort keys by length descending to avoid partial matches (e.g. {HOME}_STUFF)
    for placeholder in sorted(mappings.keys(), key=len, reverse=True):
        actual = mappings[placeholder]
        if actual:
            resolved = resolved.replace(placeholder, actual)
    
    # Handle home expansion
    resolved = os.path.expanduser(resolved)
    # Handle environment variables in path (e.g. $VAR)
    resolved = os.path.expandvars(resolved)
    
    return os.path.normpath(resolved)

def get_env_path(env_var: str, default: str) -> str:
    """Retrieves an environment variable and resolves it as a path."""
    val = os.getenv(env_var, default)
    return resolve_path(val)


# ==========================================================================
# SECTION 3 — PATH GUARD (C-01 FIXED)
# Sources: bejson_path_guard v1.1.0
# ==========================================================================

import os
from pathlib import Path

def bejson_safe_join(base_dir: str, *paths: str) -> str:
    """
    Safely join paths and ensure the result is within the base_dir.
    Mitigates path traversal attacks (Phase 2), including sibling-directory
    prefix bypasses (Phase 3, LIB-CH-H1 follow-up).
    """
    base_path = Path(base_dir).resolve()
    # Handle environment variables in paths if any
    resolved_paths = [os.path.expandvars(p) for p in paths]
    target_path = base_path.joinpath(*resolved_paths).resolve()

    is_inside = target_path == base_path
    if not is_inside:
        try:
            is_inside = target_path.is_relative_to(base_path)
        except AttributeError:
            is_inside = base_path in target_path.parents

    if not is_inside:
        raise ValueError(f"Path traversal detected: {target_path} is outside of {base_path}")

    return str(target_path)


def resolve_storage_path(path: str) -> str:
    """
    Standardized resolve_path utility for environment abstraction (Phase 1).
    Prioritizes $BEJSON_STORAGE_ROOT.
    """
    storage_root = os.environ.get("BEJSON_STORAGE_ROOT")
    if not storage_root:
        # Fallback to local home if storage root is unknown
        storage_root = os.path.expanduser("~")
        
    if not path:
        return storage_root

    # Standardize absolute paths from legacy hardcoding (if encountered)
    if path.startswith("/storage/emulated/0"):
        return path.replace("/storage/emulated/0", storage_root)
        
    return path

def _bejson_mfdb_escapes_root(relative_path: str) -> bool:
    """
    Relative-depth path traversal check.  Normalizes separators then counts
    directory depth segment by segment.  Returns True (path is unsafe) if any
    '..' segment attempts to drop the depth below 0, indicating an escape
    above the MFDB root.

    Mirrors _escapesRoot in lib_bejson_Core_mfdb_validators.ts exactly
    (Remediation NEW-08).

    Args:
        relative_path: A relative path string, e.g. '../104a.mfdb.bejson'.

    Returns:
        True  — path escapes root (unsafe, reject).
        False — path stays within root (safe).
    """
    normalized = relative_path.replace("\\", "/")
    parts = normalized.split("/")
    depth = 0
    for part in parts:
        if part == "..":
            depth -= 1
            if depth < 0:
                return True
        elif part != "." and part != "":
            depth += 1
    return False


PATH_GUARD_VERSION = "1.2.0"


# ==========================================================================
# SECTION 4 — BEJSON CORE
# Sources: bejson_core v2.0.5
# ==========================================================================

import json
import os
import sys
import time
import shutil
import tempfile
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

class BEJSONCoreError(Exception):
    """Raised when a BEJSON core operation fails."""
    def __init__(self, message: str, code: int = None):
        super().__init__(message)
        self.code = code

class ResilientPIDLock:
    def __init__(self, target_path: Union[str, Path], timeout_seconds: int = 10):
        self.target    = Path(target_path)
        self.lock_dir  = Path(f"{target_path}.lockdir")
        self.meta_file = self.lock_dir / "lock_meta.json"
        self.timeout   = timeout_seconds

    def acquire(self) -> bool:
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            try:
                self.lock_dir.mkdir(exist_ok=False)
                self.meta_file.write_text(json.dumps({
                    "pid":       os.getpid(),
                    "timestamp": int(time.time())
                }))
                return True
            except FileExistsError:
                if self.meta_file.exists():
                    try:
                        meta      = json.loads(self.meta_file.read_text())
                        owner_pid = meta.get("pid")
                        if owner_pid:
                            os.kill(owner_pid, 0)  # Signal 0: check if alive
                    except (ProcessLookupError, OSError):
                        # Owner is dead — safely reclaim
                        self.release()
                        continue
                    except Exception:
                        pass
                time.sleep(0.1)
        return False

    def release(self):
        if self.meta_file.exists():
            try:
                self.meta_file.unlink()
            except OSError:
                pass
        try:
            self.lock_dir.rmdir()
        except OSError:
            pass

    def __enter__(self):
        if not self.acquire():
            raise OSError(53, "Mutex lock timeout expired (E_MFDB_CORE_LOCK_FAILED)")
        return self

    def __exit__(self, *_):
        self.release()


def bejson_core_load_file(path: str) -> Optional[dict]:
    """Loads a BEJSON file and returns the dictionary."""
    path = resolve_path(path)
    if not path:
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"[BEJSON_CORE] Failed to load {path}: {e}")
        return None

def bejson_core_atomic_write(path: str, data: dict) -> bool:
    """Writes a BEJSON file atomically using a temp file and sync."""
    target_dir = os.path.dirname(os.path.abspath(path))
    os.makedirs(target_dir, exist_ok=True)

    # Strip internal metadata keys (starting with _) before write
    clean_data = {k: v for k, v in data.items() if not k.startswith("_")}

    fd, tmp_path = tempfile.mkstemp(dir=target_dir, suffix=".tmp")
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(clean_data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
        return True
    except Exception as e:
        logging.error(f"[BEJSON_CORE] Atomic write failed for {path}: {e}")
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        return False

def bejson_core_acquire_lock(file_path: str, timeout: int = 10) -> bool:
    """Acquire a simple directory-based lock."""
    lock_path = file_path + ".lock"
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            os.mkdir(lock_path)
            return True
        except FileExistsError:
            time.sleep(0.1)
    return False

def bejson_core_release_lock(file_path: str) -> None:
    """Release the simple directory-based lock."""
    lock_path = file_path + ".lock"
    try:
        os.rmdir(lock_path)
    except OSError:
        pass

# Global Field Map Cache
# Key: tuple of field names (sorted or as-is)
# Value: dict of {name: index}
_FIELD_MAP_CACHE: Dict[tuple, Dict[str, int]] = {}

def bejson_core_get_field_map(doc: dict) -> Dict[str, int]:
    """
    Returns a mapping of field name to index.
    Utilizes both in-document caching and a global cache for performance.
    """
    # High-performance in-document cache check
    if "_bejson_field_map" in doc:
        return doc["_bejson_field_map"]

    fields = doc.get("Fields", [])
    if not fields:
        return {}
    
    # Create a unique key for this field structure for the global cache
    field_names = tuple(f["name"] for f in fields)
    cache_key = (doc.get("Format_Version"), field_names)
    
    if cache_key in _FIELD_MAP_CACHE:
        field_map = _FIELD_MAP_CACHE[cache_key]
    else:
        # Build and update global cache
        field_map = {f["name"]: i for i, f in enumerate(fields)}
        _FIELD_MAP_CACHE[cache_key] = field_map
    
    # Inject into document for subsequent O(1) lookups
    try:
        doc["_bejson_field_map"] = field_map
    except Exception:
        pass # In case doc is immutable or not a dict
        
    return field_map

def bejson_core_get_field_index(doc: dict, field_name: str) -> int:
    """Returns the positional index of a field name using the cache."""
    field_map = bejson_core_get_field_map(doc)
    return field_map.get(field_name, -1)

def bejson_core_create_104(record_type: str, fields: list, values: list) -> dict:
    return {
        "Format": "BEJSON",
        "Format_Version": "104",
        "Format_Creator": "Elton Boehnen",
        "Records_Type": [record_type],
        "Fields": fields,
        "Values": values
    }

def bejson_core_create_104a(record_type: str, fields: list, values: list, **custom) -> dict:
    doc = {
        "Format": "BEJSON",
        "Format_Version": "104a",
        "Format_Creator": "Elton Boehnen",
        "Records_Type": [record_type],
        "Fields": fields,
        "Values": values
    }
    doc.update(custom)
    return doc

def bejson_core_create_104db(record_types: list, fields: list, values: list) -> dict:
    return {
        "Format": "BEJSON",
        "Format_Version": "104db",
        "Format_Creator": "Elton Boehnen",
        "Records_Type": record_types,
        "Fields": fields,
        "Values": values
    }

# --- Missing Functions for MFDB and Parser Compatibility ---

def bejson_core_load_string(content: str) -> Optional[dict]:
    try:
        return json.loads(content)
    except Exception as e:
        logging.error(f"[BEJSON_CORE] Failed to load JSON string: {e}")
        return None

def bejson_core_get_record_count(doc: dict) -> int:
    return len(doc.get("Values", []))

def bejson_core_add_record(doc: dict, record: list) -> bool:
    if len(record) != len(doc.get("Fields", [])):
        return False
    doc.setdefault("Values", []).append(record)
    return True

def bejson_core_remove_record(doc: dict, index: int) -> bool:
    values = doc.get("Values", [])
    if 0 <= index < len(values):
        values.pop(index)
        return True
    return False

def bejson_core_update_field(doc: dict, row_index: int, field_name: str, value: Any) -> bool:
    idx = bejson_core_get_field_index(doc, field_name)
    if idx == -1: return False
    values = doc.get("Values", [])
    if 0 <= row_index < len(values):
        values[row_index][idx] = value
        return True
    return False

def bejson_core_filter_rows(doc: dict, field_name: str, value: Any) -> list:
    idx = bejson_core_get_field_index(doc, field_name)
    if idx == -1: return []
    return [row for row in doc.get("Values", []) if row[idx] == value]

def bejson_core_sort_by_field(doc: dict, field_name: str, reverse: bool = False) -> None:
    idx = bejson_core_get_field_index(doc, field_name)
    if idx == -1: return
    doc["Values"].sort(key=lambda x: x[idx] if x[idx] is not None else "", reverse=reverse)

def bejson_core_is_valid(doc: dict) -> bool:
    # Simplified validity check
    required = ["Format", "Format_Version", "Format_Creator", "Records_Type", "Fields", "Values"]
    return all(k in doc for k in required)

def bejson_core_get_version(doc: dict) -> str:
    return doc.get("Format_Version", "unknown")

def bejson_core_get_stats(doc: dict) -> dict:
    return {
        "record_count": bejson_core_get_record_count(doc),
        "field_count": len(doc.get("Fields", [])),
        "version": bejson_core_get_version(doc)
    }


# ==========================================================================
# SECTION 5 — BEJSON VALIDATOR
# Sources: bejson_validator v2.0.3
# ==========================================================================

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional, Set, Union


VALID_VERSIONS = {"104", "104a", "104db"}
MANDATORY_KEYS = ("Format", "Format_Version", "Format_Creator", "Records_Type", "Fields", "Values")

@dataclass
class ValidationResult:
    valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    current_file: str = ""

    def add_error(self, message: str):
        self.valid = False
        self.errors.append(message)

    def add_warning(self, message: str):
        self.warnings.append(message)

    @property
    def is_valid(self) -> bool:
        """Alias for .valid. A caller reaching for result.is_valid instead
        of result.valid is a reasonable, common guess at this class's own
        API -- cheap to make both spellings work rather than requiring
        every consumer to know the exact attribute name. (Synced from the
        same fix applied in NewAgent's local copy of this file, 2026-08-13,
        after an AttributeError surfaced in a PROFILER-style caller.)"""
        return self.valid

class BEJSONValidationError(Exception):
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.code = code

def bejson_validator_check_json_syntax(input_, res: ValidationResult, is_file=False):
    if is_file:
        path = Path(input_)
        if not path.exists(): raise BEJSONValidationError(f"File not found: {input_}", E_FILE_NOT_FOUND)
        text = path.read_text(encoding="utf-8")
        res.current_file = str(path)
    else: text = input_
    if isinstance(text, dict): return text
    try: return json.loads(text)
    except Exception as e: raise BEJSONValidationError(f"Invalid JSON: {e}", E_INVALID_JSON)

def bejson_validator_check_mandatory_keys(doc):
    for key in MANDATORY_KEYS:
        if key not in doc: raise BEJSONValidationError(f"Missing key: {key}", E_MISSING_MANDATORY_KEY)
    if doc["Format"] != "BEJSON": raise BEJSONValidationError("Invalid Format", E_INVALID_FORMAT)
    if doc["Format_Creator"] != "Elton Boehnen":
        raise BEJSONValidationError("Invalid Format_Creator: Must be 'Elton Boehnen'", E_INVALID_FORMAT)
    version = doc.get("Format_Version", "")
    if version not in VALID_VERSIONS: raise BEJSONValidationError(f"Invalid version: {version}", E_INVALID_VERSION)
    return version

def bejson_validator_check_records_type(doc, version):
    rt = doc["Records_Type"]
    if not isinstance(rt, list):
        raise BEJSONValidationError("Records_Type must be a list", E_INVALID_RECORDS_TYPE)
    count = len(rt)
    if version in ("104", "104a"):
        if count != 1:
            raise BEJSONValidationError(f"BEJSON {version} must have exactly 1 record type. Found {count}.", E_INVALID_RECORDS_TYPE)
    elif version == "104db":
        if count < 2:
            raise BEJSONValidationError("104db requires 2+ types", E_INVALID_RECORDS_TYPE)

def bejson_validator_check_record_type_parent(doc, version):
    if version != "104db": return True
    fields = doc["Fields"]
    if not fields or fields[0].get("name") != "Record_Type_Parent":
        raise BEJSONValidationError("104db first field must be 'Record_Type_Parent'", E_INVALID_RECORD_TYPE_PARENT)
    valid_types = set(doc["Records_Type"])
    for i, record in enumerate(doc["Values"]):
        if not record: continue
        rtp = record[0]
        if rtp not in valid_types:
            raise BEJSONValidationError(f"Invalid Record_Type_Parent '{rtp}' at row {i}", E_INVALID_RECORD_TYPE_PARENT)
    return True

def bejson_validator_check_fields_structure(doc, version):
    fields = doc["Fields"]
    for i, f in enumerate(fields):
        fname = f.get("name")
        ftype = f.get("type")
        if not fname or not ftype:
            raise BEJSONValidationError(f"Field {i} missing name or type", E_INVALID_FIELDS)
        if version == "104a" and ftype in ("array", "object"):
            raise BEJSONValidationError(f"104a forbids complex type: {ftype}", E_INVALID_FIELDS)
        if version == "104db" and fname != "Record_Type_Parent" and "Record_Type_Parent" not in f:
            raise BEJSONValidationError(f"Field '{fname}' missing Record_Type_Parent in 104db", E_INVALID_RECORD_TYPE_PARENT)
    return len(fields)

def bejson_validator_check_values(doc, version, fields_count):
    fields = doc["Fields"]
    for i, record in enumerate(doc["Values"]):
        if len(record) != fields_count:
            raise BEJSONValidationError(f"Length mismatch at row {i}", E_RECORD_LENGTH_MISMATCH)
        for j, val in enumerate(record):
            ftype = fields[j].get("type")
            if val is None: continue
            
            # Full type validation including array/object
            if ftype == "string" and not isinstance(val, str):
                 raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({fields[j]['name']}): expected string", E_TYPE_MISMATCH)
            elif ftype == "integer" and (not isinstance(val, int) or isinstance(val, bool)):
                 raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({fields[j]['name']}): expected integer", E_TYPE_MISMATCH)
            elif ftype == "number" and (not isinstance(val, (int, float)) or isinstance(val, bool)):
                 # bool is a subclass of int in Python, so True/False pass isinstance(int,float).
                 # Explicitly exclude bool — BEJSON "number" means a numeric value, not a boolean.
                 raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({fields[j]['name']}): expected number, got bool", E_TYPE_MISMATCH)
            elif ftype == "boolean" and not isinstance(val, bool):
                 raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({fields[j]['name']}): expected boolean", E_TYPE_MISMATCH)
            elif ftype == "array" and not isinstance(val, list):
                 raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({fields[j]['name']}): expected array", E_TYPE_MISMATCH)
            elif ftype == "object" and not isinstance(val, dict):
                 raise BEJSONValidationError(f"Type mismatch at row {i}, col {j} ({fields[j]['name']}): expected object", E_TYPE_MISMATCH)

def bejson_validator_check_custom_headers(doc, version):
    mandatory_set = set(MANDATORY_KEYS)
    for key in doc:
        if key in mandatory_set or key == "Parent_Hierarchy": continue
        if version in ("104", "104db"):
            raise BEJSONValidationError(f"Custom key '{key}' forbidden in {version}", E_RESERVED_KEY_COLLISION)
        # 104a: Custom headers allowed, no strict PascalCase enforcement
        # Audit 2 Finding: Removed warning to avoid conflict with 104db rigidity.

def validate_bejson(input_data: Union[str, dict], is_file: bool = False) -> ValidationResult:
    """Thread-safe validation. Returns a ValidationResult object."""
    res = ValidationResult()
    try:
        doc = bejson_validator_check_json_syntax(input_data, res, is_file=is_file)
        version = bejson_validator_check_mandatory_keys(doc)
        bejson_validator_check_custom_headers(doc, version)
        bejson_validator_check_records_type(doc, version)
        bejson_validator_check_record_type_parent(doc, version)
        fields_count = bejson_validator_check_fields_structure(doc, version)
        bejson_validator_check_values(doc, version, fields_count)
    except BEJSONValidationError as e:
        res.add_error(str(e))
    except Exception as e:
        res.add_error(f"Unexpected validation error: {e}")
    return res

def bejson_validator_get_report(input_data, is_file: bool = False) -> str:
    """Return a human-readable validation report string."""
    res = validate_bejson(input_data, is_file=is_file)
    lines = ["BEJSON Validation Report"]
    lines.append("  File: " + (res.current_file or "<string>"))
    lines.append("  Valid: " + str(res.valid))
    if res.errors:
        lines.append("  Errors:")
        for e in res.errors:
            lines.append("    - " + e)
    if res.warnings:
        lines.append("  Warnings:")
        for w in res.warnings:
            lines.append("    - " + w)
    return "\n".join(lines)

# Compatibility wrappers (now internal state is gone)
def bejson_validator_validate_string(json_string):
    res = validate_bejson(json_string)
    if not res.valid:
        raise BEJSONValidationError(res.errors[0], E_INVALID_FORMAT)
    return True

def bejson_validator_validate_file(file_path):
    res = validate_bejson(file_path, is_file=True)
    if not res.valid:
        raise BEJSONValidationError(res.errors[0], E_INVALID_FORMAT)
    return True


# ==========================================================================
# SECTION 6 — LIST VALIDATOR
# Sources: bejson_list_validator v1.3.1
# ==========================================================================

from typing import Any, Dict

def validate_list(doc_data: dict) -> Dict[str, Any]:
    """
    doc_data: an already-loaded BEJSON document dict (e.g. from
    BEJSONCore.bejson_core_load_file() or MFDBCore.mfdb_core_get_entity_doc()).
    This function no longer performs any file I/O itself — the caller
    (typically MFDBCore) is responsible for loading the document.
    """
    # 1. Structural Validation (Sourced from Core) — validate_bejson() accepts
    # a dict natively (is_file=False, and bejson_validator_check_json_syntax
    # passes dicts straight through), so this no longer routes through the
    # file-path-only bejson_validator_validate_file().
    res = StandardValidator.validate_bejson(doc_data, is_file=False)
    if not res.valid:
        return {"is_valid": False, "errors": res.errors}

    doc = doc_data

    # 2. BEJSON Format Version Constraint
    # Accepts both "104a" (standalone list documents) and "104" (standard
    # MFDBCore entity docs, which carry Parent_Hierarchy instead of being
    # manifests themselves). Per Directive 2, Category/Nav are now regular
    # MFDBCore entities like Page/Post/Media, and MFDBCore.mfdb_core_get_entity_doc()
    # returns those as Format_Version "104" — the hierarchy check below only
    # cares about id/parent_id being present, not which of the two valid
    # BEJSON list-shaped formats the doc uses.
    if doc.get("Format_Version") not in ("104a", "104"):
        return {"is_valid": False, "errors": ["List Manager requires BEJSON 104 or 104a format."]}

    # 3. List Logic (Hierarchy & Integrity)
    values = doc.get("Values", [])
    # R7: use BEJSONCore field map cache instead of re-building per call
    f_map = BEJSONCore.bejson_core_get_field_map(doc)
    if "id" not in f_map or "parent_id" not in f_map:
        return {"is_valid": False, "errors": ["Missing core list fields: id, parent_id"]}
        
    id_idx = f_map["id"]
    pid_idx = f_map["parent_id"]
    
    ids = set()
    parent_refs = {}
    
    for i, row in enumerate(values):
        uid = row[id_idx]
        pid = row[pid_idx]
        if uid in ids:
            return {"is_valid": False, "errors": [f"Duplicate ID detected: {uid}"]}
        ids.add(uid)
        if pid: parent_refs[uid] = pid

    for uid, pid in parent_refs.items():
        if pid not in ids:
            return {"is_valid": False, "errors": [f"Orphan detected: {uid} -> {pid}"]}
        path = {uid}
        curr = pid
        while curr:
            if curr in path:
                return {"is_valid": False, "errors": [f"Circular dependency: {uid}"]}
            path.add(curr)
            curr = parent_refs.get(curr)

    return {"is_valid": True, "errors": [], "stats": {"item_count": len(ids)}}

if __name__ == "__main__":
    print("Python List Validator v1.3.0 Loaded (I/O decoupled, error branch fixed).")


# ==========================================================================
# SECTION 7 — MFDB VALIDATOR
# Sources: mfdb_validator v2.2.0
# ==========================================================================

import json
import os
import zipfile
from dataclasses import dataclass, field as dc_field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union




class MFDBValidationError(Exception):
    def __init__(self, message: str, code: int, context: dict = None):
        super().__init__(message)
        self.code = code
        self.context = context or {}

@dataclass
class MFDBValidationResult:
    valid: bool = True
    errors: List[str] = dc_field(default_factory=list)
    warnings: List[str] = dc_field(default_factory=list)
    findings: Dict[str, Any] = dc_field(default_factory=dict)
    
    def add_error(self, message: str, location: str = ""):
        self.valid = False
        entry = f"ERROR | Location: {location} | Message: {message}" if location else f"ERROR | Message: {message}"
        self.errors.append(entry)

    def add_warning(self, message: str, location: str = ""):
        entry = f"WARNING | Location: {location} | Message: {message}" if location else f"WARNING | Message: {message}"
        self.warnings.append(entry)

# Internal helpers
def _load_json(path: str) -> dict:
    p = Path(path)
    if p.is_file() and not path.lower().endswith(".zip"):
        return json.loads(p.read_text(encoding="utf-8"))
    if path.lower().endswith(".zip") and p.is_file():
        with zipfile.ZipFile(path, "r") as z:
            if "104a.mfdb.bejson" in z.namelist():
                return json.loads(z.read("104a.mfdb.bejson").decode("utf-8"))
            raise FileNotFoundError(f"104a.mfdb.bejson not found in archive: {path}")
    return json.loads(p.read_text(encoding="utf-8"))

def _rows_as_dicts(doc: dict) -> list[dict]:
    names = [f["name"] for f in doc["Fields"]]
    return [dict(zip(names, row)) for row in doc["Values"]]

def _resolve_entity_path(manifest_path: str, file_path_rel: str) -> str:
    if manifest_path.lower().endswith(".zip"):
        return os.path.join(manifest_path, file_path_rel)
    manifest_dir = os.path.dirname(os.path.abspath(manifest_path))
    return os.path.normpath(os.path.join(manifest_dir, file_path_rel))

# Validation functions
def validate_mfdb_archive(archive_path: str) -> MFDBValidationResult:
    res = MFDBValidationResult()
    p = Path(archive_path)
    if not p.exists():
        res.add_error(f"Archive not found: {archive_path}", "File System")
        return res
    try:
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            if "104a.mfdb.bejson" not in zip_ref.namelist():
                res.add_error("Archive missing 104a.mfdb.bejson at root", "Zip Structure")
    except Exception as e:
        res.add_error(f"Invalid zip: {e}", "Zip Parser")
    return res

def validate_mfdb_manifest(manifest_path: str) -> MFDBValidationResult:
    res = MFDBValidationResult()
    p = Path(manifest_path)
    if not p.exists():
        res.add_error(f"Manifest not found: {manifest_path}", "File System")
        return res
    
    bej_res = validate_bejson(manifest_path, is_file=True)
    if not bej_res.valid:
        for err in bej_res.errors: res.add_error(err, "BEJSON Validation")
        return res

    doc = _load_json(manifest_path)
    if doc.get("Format_Version") != "104a" or doc.get("Records_Type") != ["mfdb"]:
        res.add_error("Invalid manifest format or records type", "Manifest")
        return res

    field_names = [f["name"] for f in doc.get("Fields", [])]
    for req in ("entity_name", "file_path"):
        if req not in field_names: res.add_error(f"Missing required field: {req}", "Fields")

    seen_names, seen_paths = set(), set()
    for i, entry in enumerate(_rows_as_dicts(doc)):
        en, fp = entry.get("entity_name"), entry.get("file_path")
        if not en or not fp: res.add_error(f"Record {i}: null entity_name or file_path", "Values")
        if en in seen_names: res.add_error(f"Duplicate entity: {en}", "Values")
        if fp in seen_paths: res.add_error(f"Duplicate path: {fp}", "Values")
        seen_names.add(en); seen_paths.add(fp)

        # NEW-08: reject file_path values that attempt to escape the MFDB root
        if fp and _bejson_mfdb_escapes_root(fp):
            res.add_error(
                f"Path traversal detected in file_path for entity '{en}': '{fp}'",
                "Values"
            )
            continue

        resolved = _resolve_entity_path(manifest_path, fp)
        if not os.path.exists(resolved): res.add_error(f"Entity file not found: {fp}", "File System")
    
    return res

def validate_mfdb_entity_file(entity_path: str, check_bidirectional: bool = True) -> MFDBValidationResult:
    res = MFDBValidationResult()
    p = Path(entity_path)
    if not p.exists():
        res.add_error(f"Entity file not found: {entity_path}", "File System")
        return res

    bej_res = validate_bejson(entity_path, is_file=True)
    if not bej_res.valid:
        for err in bej_res.errors: res.add_error(err, "BEJSON Validation")
        return res

    doc = _load_json(entity_path)
    if doc.get("Format_Version") != "104":
        res.add_error("Entity file must be 104", "Format_Version")
        return res

    ph = doc.get("Parent_Hierarchy")
    if not ph:
        res.add_error("Missing Parent_Hierarchy", "Structure")
        return res

    manifest_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(entity_path)), ph))
    if not os.path.exists(manifest_path):
        res.add_error(f"Manifest not found at {manifest_path}", "Parent_Hierarchy")
        return res

    return res

def validate_mfdb_database(manifest_path: str, strict_fk: bool = False) -> MFDBValidationResult:
    res = validate_mfdb_manifest(manifest_path)
    if not res.valid: return res
    
    doc = _load_json(manifest_path)
    for entry in _rows_as_dicts(doc):
        resolved = _resolve_entity_path(manifest_path, entry["file_path"])
        ent_res = validate_mfdb_entity_file(resolved)
        if not ent_res.valid:
            for err in ent_res.errors: res.add_error(err, f"Entity:{entry['entity_name']}")
    return res

# Compatibility wrappers
def mfdb_validator_validate_manifest(p):
    res = validate_mfdb_manifest(p)
    if not res.valid: raise MFDBValidationError(res.errors[0], E_MFDB_NOT_MANIFEST)
    return True

def mfdb_validator_validate_database(p, strict_fk=False):
    res = validate_mfdb_database(p, strict_fk=strict_fk)
    if not res.valid: raise MFDBValidationError(res.errors[0], E_MFDB_NOT_MANIFEST)
    return True

# ── MFDB 1.32 chunked-package validation ───────────────────────────────────────
# Relocated from lib_bejson_Core_bejson_chunking.py (2026-07-13). The chunking
# library still owns create_mfdb132_package/unchunk_mfdb132_package (packaging
# and IO), but calls back into these functions for the actual validation —
# validation logic belongs in the validator family, not the chunker.

MFDB_MANIFEST_FILENAME = "104a.mfdb.bejson"

def mfdb_validator_is_mfdb132_package(doc: Dict[str, Any]) -> bool:
    """
    Discovery check: True if a document represents a packaged MFDB 1.32
    database (tagged via bejson_core_chunking_create_mfdb132_package) rather
    than a plain project chunk.
    """
    return (
        doc.get("Format_Version") == "104a"
        and doc.get("Schema_Name") == "MFDB-132"
        and doc.get("Package_Format") == "MFDB-Chunked-104a"
        and bool(doc.get("MFDB_Version"))
        and bool(doc.get("DB_Name"))
    )

def mfdb_validator_validate_mfdb132_package(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Level 1 validation for a chunked MFDB 1.32 package:
    - Must pass mfdb_validator_is_mfdb132_package()
    - Records_Type must be exactly ["MFDB-132"]
    - The manifest (104a.mfdb.bejson) must be present among the chunked files
      at Relative_Path == "104a.mfdb.bejson" (root of the package)

    This mirrors — but does not replace — validate_mfdb_database() above,
    which should still be run against the unchunked output.

    Returns {"valid": bool, "errors": [...], "warnings": [...]}.
    """
    errors: List[str] = []
    warnings: List[str] = []

    if not mfdb_validator_is_mfdb132_package(doc):
        errors.append("Document is not a recognized MFDB-132 package "
                       "(missing/incorrect Schema_Name/Package_Format/MFDB_Version/DB_Name).")
        return {"valid": False, "errors": errors, "warnings": warnings}

    if doc.get("Records_Type") != ["MFDB-132"]:
        errors.append("Records_Type must be exactly ['MFDB-132'] for an MFDB-132 package.")

    fields = doc.get("Fields", [])
    fm = {f["name"]: i for i, f in enumerate(fields)}
    manifest_found = False
    for row in doc.get("Values", []):
        if row[fm.get("Relative_Path", -1)] == MFDB_MANIFEST_FILENAME:
            manifest_found = True
            break

    if not manifest_found:
        errors.append(f"Chunked package does not contain the MFDB manifest "
                       f"({MFDB_MANIFEST_FILENAME}) — not a complete MFDB package.")

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}

def _mfdb_validator_find_row_by_relpath(doc: Dict[str, Any], rel_path: str) -> Optional[List[Any]]:
    fields = doc.get("Fields", [])
    fm = {f["name"]: i for i, f in enumerate(fields)}
    rel_idx = fm.get("Relative_Path")
    if rel_idx is None:
        return None
    for row in doc.get("Values", []):
        if row[rel_idx] == rel_path:
            return row
    return None

def mfdb_validator_detect_mfdb_in_chunk(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Scans any Chunked-104a document for an embedded, valid MFDB database
    (manifest at Relative_Path == '104a.mfdb.bejson' + its entity files).
    Does NOT require MFDB_Version/DB_Name/Package_Format headers on the
    chunk itself — only that a genuine manifest+entities are present inside
    the chunked file set. This is the Level-1/Level-2 MFDB validation logic,
    re-targeted to operate on chunk rows instead of files on disk.

    Returns:
    {
      "mfdb_detected": bool,   # a manifest row was found and parses as 104a
      "valid": bool,           # manifest + every listed entity check out
      "db_name": str | None,
      "mfdb_version": str | None,
      "entities": [
        {"entity_name": str, "file_path": str, "found_in_chunk": bool,
         "valid": bool, "errors": [str]}
      ],
      "errors": [str],         # manifest-level (Level 1) errors
      "warnings": [str],
    }
    """
    result: Dict[str, Any] = {
        "mfdb_detected": False,
        "valid": False,
        "db_name": None,
        "mfdb_version": None,
        "entities": [],
        "errors": [],
        "warnings": [],
    }

    fields = doc.get("Fields", [])
    fm = {f["name"]: i for i, f in enumerate(fields)}
    required = ("Relative_Path", "File_Content", "Is_Binary")
    if any(k not in fm for k in required):
        result["errors"].append("Chunk document is missing required Chunked-104 fields.")
        return result

    manifest_row = _mfdb_validator_find_row_by_relpath(doc, MFDB_MANIFEST_FILENAME)
    if manifest_row is None:
        result["errors"].append(f"No manifest ({MFDB_MANIFEST_FILENAME}) found in chunk — no MFDB present.")
        return result

    if manifest_row[fm["Is_Binary"]]:
        result["errors"].append("Manifest row is flagged Is_Binary — its content was never stored, cannot validate.")
        return result

    try:
        manifest_doc = json.loads(manifest_row[fm["File_Content"]])
    except Exception as e:
        result["errors"].append(f"Manifest content is not valid JSON: {e}")
        return result

    # ── Level 1: Manifest checks ──
    result["mfdb_detected"] = True
    result["db_name"] = manifest_doc.get("DB_Name")
    result["mfdb_version"] = manifest_doc.get("MFDB_Version")

    if manifest_doc.get("Format_Version") != "104a":
        result["errors"].append("Manifest Format_Version must be '104a'.")
    if manifest_doc.get("Records_Type") != ["mfdb"]:
        result["errors"].append("Manifest Records_Type must be exactly ['mfdb'].")

    manifest_fm = {f["name"]: i for i, f in enumerate(manifest_doc.get("Fields", []))}
    if "entity_name" not in manifest_fm or "file_path" not in manifest_fm:
        result["errors"].append("Manifest Fields must include 'entity_name' and 'file_path'.")
        return result

    seen_entity_names = set()
    seen_file_paths = set()

    # ── Level 2: Per-entity checks ──
    for entity_row in manifest_doc.get("Values", []):
        entity_name = entity_row[manifest_fm["entity_name"]]
        file_path = entity_row[manifest_fm["file_path"]]
        entity_result: Dict[str, Any] = {
            "entity_name": entity_name,
            "file_path": file_path,
            "found_in_chunk": False,
            "valid": False,
            "errors": [],
        }

        if not entity_name or not file_path:
            entity_result["errors"].append("entity_name/file_path must not be null.")
        if entity_name in seen_entity_names:
            entity_result["errors"].append(f"Duplicate entity_name '{entity_name}' in manifest.")
        if file_path in seen_file_paths:
            entity_result["errors"].append(f"Duplicate file_path '{file_path}' in manifest.")
        seen_entity_names.add(entity_name)
        seen_file_paths.add(file_path)

        entity_chunk_row = _mfdb_validator_find_row_by_relpath(doc, file_path)
        if entity_chunk_row is None:
            entity_result["errors"].append(f"Entity file '{file_path}' listed in manifest was not found in chunk.")
            result["entities"].append(entity_result)
            continue

        entity_result["found_in_chunk"] = True
        if entity_chunk_row[fm["Is_Binary"]]:
            entity_result["errors"].append("Entity row is flagged Is_Binary — content was never stored, cannot validate.")
            result["entities"].append(entity_result)
            continue

        try:
            entity_doc = json.loads(entity_chunk_row[fm["File_Content"]])
        except Exception as e:
            entity_result["errors"].append(f"Entity file content is not valid JSON: {e}")
            result["entities"].append(entity_result)
            continue

        if entity_doc.get("Format_Version") != "104":
            entity_result["errors"].append("Entity Format_Version must be '104'.")
        if entity_doc.get("Records_Type") != [entity_name]:
            entity_result["errors"].append(f"Entity Records_Type must be exactly ['{entity_name}'].")
        if "Parent_Hierarchy" not in entity_doc:
            entity_result["errors"].append("Entity is missing mandatory 'Parent_Hierarchy' key.")

        entity_result["valid"] = len(entity_result["errors"]) == 0
        result["entities"].append(entity_result)

    result["valid"] = (
        len(result["errors"]) == 0
        and all(e["valid"] for e in result["entities"])
    )
    return result


# ==========================================================================
# SECTION 8 — MFDB CORE
# Sources: mfdb_core v2.3.0
# ==========================================================================

# v1.21 adds Dynamic Recovery and Self-Healing.

import json
import os
import shutil
import tempfile
import time
import uuid
import zipfile
import hashlib
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional



class MFDBCoreError(Exception):
    """Raised when an MFDB core operation fails."""
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.code = code

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_manifest_entries(manifest_path: str) -> list[dict]:
    doc = _load_json(manifest_path)
    return _rows_as_dicts(doc)

def _get_manifest_entry(manifest_path: str, entity_name: str) -> dict:
    entries = _get_manifest_entries(manifest_path)
    entry   = next((e for e in entries if e.get("entity_name") == entity_name), None)
    if entry is None:
        raise MFDBCoreError(
            f"Entity '{entity_name}' not found in manifest: {manifest_path}",
            E_MFDB_CORE_ENTITY_NOT_FOUND,
        )
    return entry

def _read_file_content(path: str) -> Optional[str]:
    """Reads file content, supporting .mfdb.zip archives."""
    p = Path(path)
    try:
        if p.is_file() and not path.lower().endswith(".zip"):
            return p.read_text(encoding="utf-8")
        
        # Check for zip path parts
        parts = p.parts
        for i, part in enumerate(parts):
            if part.lower().endswith(".zip"):
                zip_path = str(Path(*parts[:i+1]))
                inner_path = "/".join(parts[i+1:])
                if os.path.exists(zip_path):
                    with zipfile.ZipFile(zip_path, "r") as z:
                        if inner_path in z.namelist():
                            return z.read(inner_path).decode("utf-8")
                        elif not inner_path and "104a.mfdb.bejson" in z.namelist():
                             return z.read("104a.mfdb.bejson").decode("utf-8")
        
        if not p.exists():
            return None
            
        return p.read_text(encoding="utf-8")
    except Exception:
        return None

def _get_entity_path(manifest_path: str, entity_name: str) -> str:
    entry = _get_manifest_entry(manifest_path, entity_name)
    return _resolve_entity_path(manifest_path, entry["file_path"])

def _load_entity_doc(manifest_path: str, entity_name: str) -> dict:
    """Load and validate the raw BEJSON 104 doc for an entity."""
    entity_path = _get_entity_path(manifest_path, entity_name)
    content = _read_file_content(entity_path)
    if content is None:
        raise MFDBCoreError(
            f"Failed to read entity file: {entity_name} ({entity_path})",
            E_MFDB_CORE_ENTITY_NOT_FOUND
        )
    doc = bejson_core_load_string(content)
    if doc is None:
        raise MFDBCoreError(
            f"Failed to load entity doc: {entity_name} ({entity_path})",
            E_MFDB_CORE_ENTITY_NOT_FOUND
        )
    return doc

def _write_entity_doc(doc: dict, entity_path: str) -> None:
    if not bejson_core_atomic_write(entity_path, doc):
        raise MFDBCoreError(f"Failed to write entity doc to {entity_path}", E_MFDB_CORE_WRITE_FAILED)

def _write_manifest_doc(doc: dict, manifest_path: str) -> None:
    if not bejson_core_atomic_write(manifest_path, doc):
        raise MFDBCoreError(f"Failed to write manifest doc to {manifest_path}", E_MFDB_CORE_WRITE_FAILED)

def _update_manifest_record_count(
    manifest_path: str, entity_name: str, count: int
) -> None:
    """Write a corrected record_count into the manifest for one entity."""
    doc        = _load_json(manifest_path)
    fn_list    = [f["name"] for f in doc["Fields"]]
    if "record_count" not in fn_list or "entity_name" not in fn_list:
        return
    rc_idx = fn_list.index("record_count")
    en_idx = fn_list.index("entity_name")
    for row in doc["Values"]:
        if row[en_idx] == entity_name:
            row[rc_idx] = count
            break
    _write_manifest_doc(doc, manifest_path)

def _calculate_file_hash(file_path: str) -> str:
    """Generate SHA-256 hash for archive integrity checks."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

# ---------------------------------------------------------------------------
# MFDBArchive (v1.2 Feature)
# ---------------------------------------------------------------------------

class MFDBArchive:
    """
    Handles .mfdb.zip packaging, virtual mounting, and atomic repacking.
    Standardized in MFDB v1.2 for portable transport.
    Enhanced for CoreEvolution with sticky mounting and validation safety.
    """

    @staticmethod
    def mount(archive_path: str, target_dir: str, force: bool = False, sticky: bool = True) -> str:
        """
        Extract an MFDB archive to a workspace and create a session lock.
        If sticky=True, it reuses existing valid extracted files.
        Returns the absolute path to the extracted manifest.
        """
        arc_p = Path(archive_path)
        if not arc_p.exists():
            raise MFDBCoreError(f"Archive not found: {archive_path}", E_MFDB_CORE_ARCHIVE_ERROR)

        target_p = Path(target_dir)
        lock_file = target_p / ".mfdb_lock"
        manifest_path = target_p / "104a.mfdb.bejson"

        # Sticky check: If valid files exist and hash matches, just return manifest
        if sticky and lock_file.exists() and manifest_path.exists():
            try:
                with open(lock_file, "r") as f:
                    lock_data = json.load(f)
                
                # Check if archive hash matches the one we mounted
                current_arc_hash = _calculate_file_hash(archive_path)
                if lock_data.get("original_hash") == current_arc_hash:
                    # Validate the database structure before trusting the sticky mount
                    if mfdb_validator_validate_database(str(manifest_path)):
                        return str(manifest_path.absolute())
            except Exception:
                pass # Fall through to full re-extract if sticky fails

        if lock_file.exists() and not force:
            with open(lock_file, "r") as f:
                lock_data = json.load(f)
            if lock_data.get("pid") != os.getpid():
                raise MFDBCoreError(
                    f"Workspace {target_dir} is already locked by PID {lock_data.get('pid')}",
                    E_MFDB_CORE_MOUNT_CONFLICT
                )

        # Clear existing workspace if it was invalid or if we are forcing re-extract
        if target_p.exists():
            shutil.rmtree(target_dir)
        target_p.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            # Secure extraction loop to mitigate Zip Slip.
            for member in zip_ref.namelist():
                # Skip directories as safe_join/open will handle them
                if member.endswith('/'): continue
                
                # Boundary check via safe_join
                try:
                    safe_path = bejson_safe_join(target_dir, member)
                    # Ensure parent directory exists
                    os.makedirs(os.path.dirname(safe_path), exist_ok=True)
                    with zip_ref.open(member) as source, open(safe_path, "wb") as target:
                        shutil.copyfileobj(source, target)
                except ValueError as e:
                    logging.error(f"[MFDB_CORE] Security Alert: {e}")
                    raise MFDBCoreError(f"Secure extraction failed: {e}", E_MFDB_CORE_ARCHIVE_ERROR)

        if not manifest_path.exists():
            shutil.rmtree(target_dir)
            raise MFDBCoreError("Invalid MFDB Archive: 104a.mfdb.bejson missing.", E_MFDB_CORE_ARCHIVE_ERROR)

        # Create session lock with metadata
        lock_data = {
            "pid": os.getpid(),
            "mounted_at": datetime.now(timezone.utc).isoformat(),
            "original_hash": _calculate_file_hash(archive_path),
            "archive_path": str(arc_p.absolute())
        }
        with open(lock_file, "w") as f:
            json.dump(lock_data, f)

        return str(manifest_path.absolute())

    @staticmethod
    def commit(mount_dir: str, archive_path: Optional[str] = None, validate: bool = True) -> str:
        """
        Repack the workspace into a .mfdb.zip file atomically.
        Refuses to write if validation fails (if validate=True).
        """
        mount_p = Path(mount_dir)
        lock_file = mount_p / ".mfdb_lock"
        manifest_path = mount_p / "104a.mfdb.bejson"
        
        if not lock_file.exists():
            raise MFDBCoreError(f"No active mount session found in {mount_dir}", E_MFDB_CORE_INVALID_OPERATION)

        if validate:
            if not manifest_path.exists():
                raise MFDBCoreError("Commit rejected: Manifest missing in workspace.", E_MFDB_CORE_WRITE_FAILED)
            
            # Run full database validation before repacking
            try:
                mfdb_validator_validate_database(str(manifest_path))
            except Exception as e:
                raise MFDBCoreError(f"Commit rejected: Validation failed. {str(e)}", E_MFDB_CORE_WRITE_FAILED)

        with open(lock_file, "r") as f:
            lock_data = json.load(f)

        dest_path = archive_path or lock_data.get("archive_path")
        if not dest_path:
            raise MFDBCoreError("Destination archive path unknown.", E_MFDB_CORE_ARCHIVE_ERROR)

        # Create new archive in temp location
        fd, temp_arc = tempfile.mkstemp(suffix=".mfdb.zip")
        os.close(fd)

        try:
            with zipfile.ZipFile(temp_arc, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(mount_dir):
                    for file in files:
                        if file == ".mfdb_lock": continue
                        file_path = Path(root) / file
                        arc_name = file_path.relative_to(mount_dir)
                        zipf.write(file_path, arc_name)
            
            # Atomic swap
            shutil.move(temp_arc, dest_path)
            
            # Update lock with new hash to maintain sticky state
            lock_data["original_hash"] = _calculate_file_hash(dest_path)
            with open(lock_file, "w") as f:
                json.dump(lock_data, f)
                
        except Exception as e:
            if os.path.exists(temp_arc): os.remove(temp_arc)
            raise MFDBCoreError(f"Commit failed: {str(e)}", E_MFDB_CORE_WRITE_FAILED)

        return dest_path

    @staticmethod
    def resurrect_file(mount_dir: str, relative_path: str) -> bool:
        """
        Surgically extract a single file from the .mfdb.zip archive into the workspace.
        Used for recovery when an entity file is missing or corrupted.
        """
        mount_p = Path(mount_dir)
        lock_file = mount_p / ".mfdb_lock"
        if not lock_file.exists():
            return False

        with open(lock_file, "r") as f:
            lock_data = json.load(f)
        
        archive_path = lock_data.get("archive_path")
        if not archive_path or not os.path.exists(archive_path):
            return False

        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                # Check if file exists in zip
                if relative_path in zip_ref.namelist():
                    zip_ref.extract(relative_path, mount_dir)
                    return True
        except Exception:
            pass
        return False

    @staticmethod
    def unmount(mount_dir: str, cleanup: bool = True):
        """Release the lock and optionally delete the workspace."""
        mount_p = Path(mount_dir)
        lock_file = mount_p / ".mfdb_lock"
        if lock_file.exists():
            os.remove(lock_file)
        if cleanup and mount_p.exists():
            shutil.rmtree(mount_dir)

# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def mfdb_core_discover(file_path: str) -> str:
    """
    Identify the MFDB role of any file.
    Returns one of: 'manifest', 'entity', 'archive', 'standalone'
    """
    p = Path(file_path)
    if not p.exists():
        raise MFDBCoreError(f"File not found: {file_path}", E_MFDB_CORE_MANIFEST_NOT_FOUND)

    if p.suffix == ".zip" and ".mfdb" in p.name:
        return "archive"

    try:
        doc = _load_json(file_path)
    except Exception:
        return "standalone"

    version  = doc.get("Format_Version", "")
    filename = p.name
    if version == "104a" and filename.endswith(".mfdb.bejson"):
        return "manifest"
    if version == "104" and doc.get("Parent_Hierarchy"):
        return "entity"
    return "standalone"

# ---------------------------------------------------------------------------
# Recovery & Repair (v1.21 Feature)
# ---------------------------------------------------------------------------

def mfdb_core_deep_verify(manifest_path: str) -> List[Dict[str, Any]]:
    """
    Performs a deep audit of the entire MFDB database.
    Checks for:
      - Positional integrity (field vs value length)
      - Type adherence (basic primitives)
      - Manifest-entity consistency (record counts)
      - Foreign key potential breakage (optional warnings)
    Returns a list of finding dicts.
    """
    findings = []
    manifest_doc = bejson_core_load_file(manifest_path)
    entries = _rows_as_dicts(manifest_doc)
    
    for entry in entries:
        entity_name = entry.get("entity_name")
        file_path_rel = entry.get("file_path")
        expected_count = entry.get("record_count")
        
        entity_path = _resolve_entity_path(manifest_path, file_path_rel)
        if not os.path.exists(entity_path):
            findings.append({"entity": entity_name, "error": "MISSING_FILE", "path": file_path_rel})
            continue
            
        try:
            entity_doc = bejson_core_load_file(entity_path)
            # 1. Check positional integrity
            fields = entity_doc.get("Fields", [])
            field_count = len(fields)
            values = entity_doc.get("Values", [])
            actual_count = len(values)
            
            if expected_count is not None and expected_count != actual_count:
                findings.append({
                    "entity": entity_name, 
                    "warning": "COUNT_MISMATCH", 
                    "expected": expected_count, 
                    "actual": actual_count
                })
            
            for i, row in enumerate(values):
                if len(row) != field_count:
                    findings.append({
                        "entity": entity_name, 
                        "error": "POSITIONAL_VIOLATION", 
                        "row": i, 
                        "expected": field_count, 
                        "actual": len(row)
                    })
                
                # 2. Basic Type verification
                for j, val in enumerate(row):
                    if val is None: continue
                    f_type = fields[j].get("type")
                    if f_type == "integer" and not isinstance(val, int):
                         findings.append({"entity": entity_name, "warning": "TYPE_MISMATCH", "row": i, "field": fields[j]["name"], "expected": "integer", "actual": type(val).__name__})
                    elif f_type == "number" and not isinstance(val, (int, float)):
                         findings.append({"entity": entity_name, "warning": "TYPE_MISMATCH", "row": i, "field": fields[j]["name"], "expected": "number", "actual": type(val).__name__})
                    elif f_type == "boolean" and not isinstance(val, bool):
                         findings.append({"entity": entity_name, "warning": "TYPE_MISMATCH", "row": i, "field": fields[j]["name"], "expected": "boolean", "actual": type(val).__name__})

        except Exception as e:
            findings.append({"entity": entity_name, "error": "CORRUPT_JSON", "message": str(e)})
            
    return findings

def mfdb_core_self_heal(manifest_path: str) -> Dict[str, Any]:
    """
    Attempts to fix common issues identified by deep_verify.
    Actions:
      - Resyncs record_count in manifest.
      - Padds short records with nulls (Positional Repair).
      - Removes invalid records if necessary (Extreme measure).
    Returns a report of actions taken.
    """
    report = {"actions": [], "remaining_errors": []}
    findings = mfdb_core_deep_verify(manifest_path)
    
    needs_manifest_sync = False
    
    for f in findings:
        entity = f.get("entity")
        try:
            if f.get("warning") == "COUNT_MISMATCH":
                # FIX (N1): was f["actual"] - direct bracket access while
                # every other field in this loop uses .get(). A malformed
                # deep_verify() finding missing "actual" (or a race between
                # verify and heal) raised an unhandled KeyError that aborted
                # the whole self-heal pass mid-loop, leaving already-healed
                # findings healed but everything after silently unprocessed.
                # Now: skip this one finding and keep going, same as any
                # other per-finding failure below.
                actual = f.get("actual")
                if actual is None:
                    report["remaining_errors"].append(
                        f"Skipped COUNT_MISMATCH heal for {entity}: finding has no 'actual' value"
                    )
                    continue
                _update_manifest_record_count(manifest_path, entity, actual)
                report["actions"].append(f"Resynced record_count for {entity} to {actual}")

            elif f.get("error") == "POSITIONAL_VIOLATION":
                # Attempt repair
                entity_path = _get_entity_path(manifest_path, entity)
                try:
                    doc = bejson_core_load_file(entity_path)
                    field_count = len(doc["Fields"])
                    repaired = 0
                    for i, row in enumerate(doc["Values"]):
                        if len(row) < field_count:
                            doc["Values"][i] = row + [None] * (field_count - len(row))
                            repaired += 1
                        elif len(row) > field_count:
                            doc["Values"][i] = row[:field_count]
                            repaired += 1
                    if repaired > 0:
                        bejson_core_atomic_write(entity_path, doc)
                        report["actions"].append(f"Repaired {repaired} positional violations in {entity}")
                except Exception as e:
                    report["remaining_errors"].append(f"Failed to repair {entity}: {str(e)}")

            elif f.get("error") == "MISSING_FILE":
                # Attempt resurrection
                mount_dir = os.path.dirname(os.path.abspath(manifest_path))
                fpath = f.get("path")
                if fpath is None:
                    report["remaining_errors"].append(f"Skipped resurrection for {entity}: finding has no 'path' value")
                    continue
                if MFDBArchive.resurrect_file(mount_dir, fpath):
                    report["actions"].append(f"Resurrected missing entity file: {fpath}")
                else:
                    report["remaining_errors"].append(f"Could not resurrect {entity}")

            elif f.get("error"):
                report["remaining_errors"].append(f"{entity}: {f.get('error')} - {f.get('message', '')}")
        except Exception as e:
            # FIX (N1, extended): any other unexpected shape of a single
            # finding can no longer abort the batch either - captured and
            # reported like any other heal failure, and the loop continues.
            report["remaining_errors"].append(f"Unexpected error healing finding for {entity}: {e}")

    return report

def _mfdb_core_repair_hierarchy(entity_path: str, new_hierarchy: str) -> bool:
    """Surgically update the Parent_Hierarchy header in a BEJSON 104 file."""
    try:
        doc = bejson_core_load_file(entity_path)
        doc["Parent_Hierarchy"] = new_hierarchy
        bejson_core_atomic_write(entity_path, doc)
        return True
    except Exception:
        return False

def mfdb_core_smart_repair(manifest_path: str, error: MFDBValidationError) -> bool:
    """
    Attempt to automatically repair the MFDB workspace based on a validation error.
    Supported:
      - E_MFDB_ENTITY_NOT_FOUND (33): Resurrects from archive.
      - E_MFDB_BIDIRECTIONAL_FAIL (38) / E_MFDB_MANIFEST_NOT_FOUND (37): Patches Parent_Hierarchy.
    """
    mount_dir = os.path.dirname(os.path.abspath(manifest_path))
    ctx = error.context

    if error.code == E_MFDB_ENTITY_NOT_FOUND or error.code == 33:
        rel_path = ctx.get("file_path_rel")
        if rel_path:
            return MFDBArchive.resurrect_file(mount_dir, rel_path)

    if error.code == E_MFDB_BIDIRECTIONAL_FAIL or error.code == E_MFDB_MANIFEST_NOT_FOUND:
        entity_path = ctx.get("actual_path")
        new_hierarchy = ctx.get("suggested_hierarchy")
        # If suggested_hierarchy is missing but we are in a mount_dir, 
        # assume standard v1.21 structure
        if not new_hierarchy and entity_path:
             new_hierarchy = "../104a.mfdb.bejson"

        if entity_path and new_hierarchy:
            return _mfdb_core_repair_hierarchy(entity_path, new_hierarchy)

    return False

# ---------------------------------------------------------------------------
# Read operations
# ---------------------------------------------------------------------------

def mfdb_core_load_manifest(manifest_path: str) -> list[dict]:
    """
    Validate and load the manifest.
    Returns all manifest records as a list of field-name-keyed dicts.
    """
    mfdb_validator_validate_manifest(manifest_path)
    doc = _load_json(manifest_path)
    if not isinstance(doc, dict):
        raise MFDBCoreError(f"Failed to load manifest: {manifest_path} (not a dict)", E_MFDB_CORE_MANIFEST_NOT_FOUND)
    return _rows_as_dicts(doc)

def mfdb_core_load_entity(manifest_path: str, entity_name: str) -> list[dict]:
    """
    Load all records for a named entity.
    Returns a list of field-name-keyed dicts (dense - no null-padding).
    When Debug_Reads is enabled, logs a READ entry to the meta entity.
    """
    _t0 = time.monotonic()
    doc = _load_entity_doc(manifest_path, entity_name)
    if not isinstance(doc, dict):
        raise MFDBCoreError(f"Failed to load entity: {entity_name} (not a dict)", E_MFDB_CORE_ENTITY_NOT_FOUND)
    result = _rows_as_dicts(doc)
    _mfdb_meta_log(
        manifest_path, "READ", entity_name,
        field_name=None, field_exists=None,
        row_index=None, success=True,
        duration_ms=int((time.monotonic() - _t0) * 1000),
        notes=f"rows_returned={len(result)}",
        reads_only=True,
    )
    return result

def mfdb_core_get_entity_doc(manifest_path: str, entity_name: str) -> dict:
    """Return the raw BEJSON 104 document dict for a named entity."""
    return _load_entity_doc(manifest_path, entity_name)

def mfdb_core_get_stats(manifest_path: str) -> dict:
    """Return a summary statistics dict for the entire MFDB."""
    doc     = _load_json(manifest_path)
    entries = _rows_as_dicts(doc)

    entity_stats = []
    for entry in entries:
        resolved = _resolve_entity_path(manifest_path, entry["file_path"])
        if os.path.exists(resolved):
            edoc        = _load_json(resolved)
            rec_count   = len(edoc.get("Values", []))
            field_count = len(edoc.get("Fields", []))
        else:
            rec_count   = -1
            field_count = -1

        entity_stats.append({
            "entity_name":  entry["entity_name"],
            "file_path":    entry["file_path"],
            "record_count": rec_count,
            "field_count":  field_count,
            "primary_key":  entry.get("primary_key"),
        })

    return {
        "db_name":        doc.get("DB_Name", ""),
        "schema_version": doc.get("Schema_Version", ""),
        "entity_count":   len(entries),
        "entities":       entity_stats,
    }

# ---------------------------------------------------------------------------
# Query operations
# ---------------------------------------------------------------------------

def mfdb_core_query_entity(
    manifest_path: str,
    entity_name: str,
    predicate: Callable[[dict], bool],
) -> list[dict]:
    """Return all records from an entity for which predicate(record) is True."""
    records = mfdb_core_load_entity(manifest_path, entity_name)
    return [r for r in records if predicate(r)]

def mfdb_core_build_index(
    manifest_path: str,
    entity_name: str,
    field_name: str,
) -> dict:
    """Build an in-memory hash index on a field for fast lookups."""
    records = mfdb_core_load_entity(manifest_path, entity_name)
    return {r[field_name]: r for r in records if r.get(field_name) is not None}

def mfdb_core_join(
    manifest_path: str,
    from_entity:   str,
    to_entity:     str,
    from_fk:       str,
    to_pk:         str,
) -> list[dict]:
    """Cross-entity equi-join."""
    from_records = mfdb_core_load_entity(manifest_path, from_entity)
    to_index     = mfdb_core_build_index(manifest_path, to_entity, to_pk)

    results = []
    for record in from_records:
        fk_val = record.get(from_fk)
        target = to_index.get(fk_val, {})
        merged = dict(record)
        for k, v in target.items():
            merged[f"{to_entity}__{k}"] = v
        results.append(merged)

    return results

# ---------------------------------------------------------------------------
# Write operations
# ---------------------------------------------------------------------------

def mfdb_core_add_entity_record(
    manifest_path: str,
    entity_name:   str,
    values:        list,
    sync_count:    bool = True,
) -> dict:
    """Append a record to an entity file. Lock held for the full read-modify-write cycle."""
    _t0 = time.monotonic()
    _success = False
    entity_path = _get_entity_path(manifest_path, entity_name)
    try:
        with ResilientPIDLock(entity_path, timeout_seconds=10):
            doc = _load_entity_doc(manifest_path, entity_name)
            if not bejson_core_add_record(doc, values):
                raise BEJSONCoreError(f"Failed to add record to {entity_name}")
            _write_entity_doc(doc, entity_path)
            if sync_count:
                _update_manifest_record_count(manifest_path, entity_name, len(doc["Values"]))
        _success = True
        return doc
    finally:
        _mfdb_meta_log(
            manifest_path, "ADD", entity_name,
            field_name=None, field_exists=None,
            row_index=None, success=_success,
            duration_ms=int((time.monotonic() - _t0) * 1000),
            notes="" if _success else "add_record returned False",
        )

def mfdb_core_remove_entity_record(
    manifest_path: str,
    entity_name:   str,
    record_index:  int,
    sync_count:    bool = True,
) -> dict:
    """Remove a record at record_index from an entity file. Lock held for the full read-modify-write cycle."""
    _t0 = time.monotonic()
    _success = False
    entity_path = _get_entity_path(manifest_path, entity_name)
    try:
        with ResilientPIDLock(entity_path, timeout_seconds=10):
            doc = _load_entity_doc(manifest_path, entity_name)
            if not bejson_core_remove_record(doc, record_index):
                raise BEJSONCoreError(f"Failed to remove record {record_index} from {entity_name}")
            _write_entity_doc(doc, entity_path)
            if sync_count:
                _update_manifest_record_count(manifest_path, entity_name, len(doc["Values"]))
        _success = True
        return doc
    finally:
        _mfdb_meta_log(
            manifest_path, "REMOVE", entity_name,
            field_name=None, field_exists=None,
            row_index=record_index, success=_success,
            duration_ms=int((time.monotonic() - _t0) * 1000),
            notes="",
        )

def mfdb_core_update_entity_record(
    manifest_path: str,
    entity_name:   str,
    record_index:  int,
    field_name:    str,
    new_value:     Any,
) -> dict:
    """Update a single named field in a specific record. Lock held for the full read-modify-write cycle."""
    _t0 = time.monotonic()
    _success = False
    _field_exists = None
    entity_path = _get_entity_path(manifest_path, entity_name)
    try:
        with ResilientPIDLock(entity_path, timeout_seconds=10):
            doc = _load_entity_doc(manifest_path, entity_name)
            if not isinstance(doc, dict):
                raise BEJSONCoreError(f"Malformed entity doc for {entity_name}")
            _field_exists = any(f["name"] == field_name for f in doc.get("Fields", []))
            if not bejson_core_update_field(doc, record_index, field_name, new_value):
                raise BEJSONCoreError(f"Failed to update field '{field_name}' in {entity_name}")
            _write_entity_doc(doc, entity_path)
        _success = True
        return doc
    finally:
        _mfdb_meta_log(
            manifest_path, "UPDATE", entity_name,
            field_name=field_name, field_exists=_field_exists,
            row_index=record_index, success=_success,
            duration_ms=int((time.monotonic() - _t0) * 1000),
            notes="" if _field_exists else f"SCHEMA DRIFT: field '{field_name}' not in Fields[]",
        )

def mfdb_core_update_entity_record_bulk(
    manifest_path: str,
    entity_name:   str,
    record_index:  int,
    updates:       Dict[str, Any],
) -> dict:
    """Update multiple named fields in a specific record. Lock held for the full read-modify-write cycle."""
    _t0 = time.monotonic()
    _success = False
    _missing_fields: list = []
    entity_path = _get_entity_path(manifest_path, entity_name)
    try:
        with ResilientPIDLock(entity_path, timeout_seconds=10):
            doc = _load_entity_doc(manifest_path, entity_name)
            if not isinstance(doc, dict):
                raise BEJSONCoreError(f"Malformed entity doc for {entity_name}")
            _known = {f["name"] for f in doc.get("Fields", [])}
            _missing_fields = [k for k in updates if k not in _known]
            for field_name, new_value in updates.items():
                if not bejson_core_update_field(doc, record_index, field_name, new_value):
                    raise BEJSONCoreError(f"Failed to update field '{field_name}' in {entity_name}")
            _write_entity_doc(doc, entity_path)
        _success = True
        return doc
    finally:
        _notes = (f"SCHEMA DRIFT: unknown fields {_missing_fields}" if _missing_fields else "")
        _mfdb_meta_log(
            manifest_path, "UPDATE_BULK", entity_name,
            field_name=",".join(updates.keys()),
            field_exists=(len(_missing_fields) == 0),
            row_index=record_index, success=_success,
            duration_ms=int((time.monotonic() - _t0) * 1000),
            notes=_notes,
        )

# ---------------------------------------------------------------------------
# Manifest sync
# ---------------------------------------------------------------------------

def mfdb_core_sync_manifest_count(manifest_path: str, entity_name: str) -> int:
    """Re-count actual rows in an entity file and update the manifest."""
    entity_path = _get_entity_path(manifest_path, entity_name)
    edoc        = _load_json(entity_path)
    count       = len(edoc.get("Values", []))
    _update_manifest_record_count(manifest_path, entity_name, count)
    return count

def mfdb_core_sync_all_counts(manifest_path: str) -> dict:
    """Sync record_count for every entity listed in the manifest."""
    entries = _get_manifest_entries(manifest_path)
    results = {}
    for entry in entries:
        name = entry["entity_name"]
        results[name] = mfdb_core_sync_manifest_count(manifest_path, name)
    return results

# ---------------------------------------------------------------------------
# Database creation
# ---------------------------------------------------------------------------

def mfdb_core_create_entity_file(
    manifest_path:  str,
    entity_name:    str,
    fields:         list[dict],
    description:    str = "",
    primary_key:    str = "",
    schema_version: str = "1.0",
    file_path_rel:  str = "",
) -> str:
    """Create a new entity file and register it in an existing manifest."""
    manifest_dir = os.path.dirname(os.path.abspath(manifest_path))

    if not file_path_rel:
        file_path_rel = f"data/{entity_name.lower()}.bejson"

    resolved = os.path.normpath(os.path.join(manifest_dir, file_path_rel))
    os.makedirs(os.path.dirname(resolved), exist_ok=True)

    entity_dir         = os.path.dirname(resolved)
    rel_to_manifest    = os.path.relpath(manifest_path, entity_dir)

    entity_doc = {
        "Format":           "BEJSON",
        "Format_Version":   "104",
        "Format_Creator":   "Elton Boehnen",
        "Parent_Hierarchy": rel_to_manifest,
        "Records_Type":     [entity_name],
        "Fields":           fields,
        "Values":           [],
    }
    bejson_core_atomic_write(resolved, entity_doc)

    manifest_doc = _load_json(manifest_path)
    fn_list      = [f["name"] for f in manifest_doc["Fields"]]

    new_row = []
    for fn in fn_list:
        if   fn == "entity_name":    new_row.append(entity_name)
        elif fn == "file_path":      new_row.append(file_path_rel)
        elif fn == "description":    new_row.append(description or None)
        elif fn == "record_count":   new_row.append(0)
        elif fn == "schema_version": new_row.append(schema_version)
        elif fn == "primary_key":    new_row.append(primary_key or None)
        else:                        new_row.append(None)

    manifest_doc["Values"].append(new_row)
    _write_manifest_doc(manifest_doc, manifest_path)

    return resolved

def mfdb_core_create_database(
    root_dir:       str,
    db_name:        str,
    entities:       list[dict],
    db_description: str = "",
    schema_version: str = "1.0.0",
    author:         str = "Elton Boehnen",
    mfdb_version:   str = "1.31",
    network_role:   str = "Master",
    debug_mode:     bool = False,
    debug_row_cap:  int  = 500,
    debug_reads:    bool = False,
) -> str:
    """
    Create a new MFDB from scratch.
    debug_mode=True auto-creates a meta-{uuid} entity and activates write/read
    audit logging. Zero overhead when False.
    """
    root = Path(root_dir)
    root.mkdir(parents=True, exist_ok=True)
    manifest_path = str(root / "104a.mfdb.bejson")

    manifest_fields = [
        {"name": "entity_name",    "type": "string"},
        {"name": "file_path",      "type": "string"},
        {"name": "description",    "type": "string"},
        {"name": "record_count",   "type": "integer"},
        {"name": "schema_version", "type": "string"},
        {"name": "primary_key",    "type": "string"},
    ]

    manifest_values     = []
    entity_defs_to_file = []

    for entity in entities:
        name   = entity["name"]
        fp_rel = entity.get("file_path", f"data/{name.lower()}.bejson")
        desc   = entity.get("description", "")
        pk     = entity.get("primary_key", "")
        sv     = entity.get("schema_version", "1.0")
        fields = entity["fields"]

        manifest_values.append([name, fp_rel, desc or None, 0, sv, pk or None])
        entity_defs_to_file.append((name, fp_rel, fields))

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    manifest_doc = {
        "Format":          "BEJSON",
        "Format_Version":  "104a",
        "Format_Creator":  "Elton Boehnen",
        "MFDB_Version":    mfdb_version,
        "Network_Role": network_role,
        "DB_Name":         db_name,
        "DB_Description":  db_description,
        "Schema_Version":  schema_version,
        "Author":          author,
        "Created_At":      created_at,
        "Records_Type":    ["mfdb"],
        "Fields":          manifest_fields,
        "Values":          manifest_values,
    }

    bejson_core_atomic_write(manifest_path, manifest_doc)

    for entity_name, fp_rel, fields in entity_defs_to_file:
        resolved   = os.path.normpath(os.path.join(root_dir, fp_rel))
        entity_dir = os.path.dirname(resolved)
        os.makedirs(entity_dir, exist_ok=True)

        rel_to_manifest = os.path.relpath(manifest_path, entity_dir)

        entity_doc = {
            "Format":           "BEJSON",
            "Format_Version":   "104",
            "Format_Creator":   "Elton Boehnen",
            "Parent_Hierarchy": rel_to_manifest,
            "Records_Type":     [entity_name],
            "Fields":           fields,
            "Values":           [],
        }
        bejson_core_atomic_write(resolved, entity_doc)

    if debug_mode:
        mfdb_core_enable_debug(manifest_path, row_cap=debug_row_cap, debug_reads=debug_reads)

    return manifest_path

def mfdb_core_resolve_path(path_str: str) -> str:
    """
    Hardening: Resolve system placeholders in paths using lib_bejson_Core_bejson_env.
    Supports: {INTERNAL_STORAGE}, {ADMIN_ROOT}, {PROJECTS_ROOT}, 
             internal_storage, ~, and environment variables in ${VAR} format.
    """
    if not path_str:
        return path_str
    
    return resolve_path(path_str)


# ── Federated Master / Slave node system ───────────────────────────────────────
# Network_Role ("Master" | "Slave") is already emitted on manifest creation
# (mfdb_core_create_database). This block wires the full runtime protocol:
#   - ConnectedSlave entity schema + creator (Master side)
#   - mfdb_federation_push_config   — Master atomically drops a 104a doc into
#                                      a Slave's local dropzone directory
#   - mfdb_federation_poll_dropzone — Slave polls its own dropzone for incoming
#                                      Master configs
#   - mfdb_federation_distill_logs  — Slave truncates overflow entity rows and
#                                      pushes a distilled summary to Master

CONNECTED_SLAVE_SCHEMA: List[Dict[str, str]] = [
    {"name": "slave_id",           "type": "string"},
    {"name": "label",              "type": "string"},
    {"name": "url",                "type": "string"},
    {"name": "role",               "type": "string"},
    {"name": "status",             "type": "string"},
    {"name": "supported_entities", "type": "array"},
]


def mfdb_core_create_connected_slave_entity(manifest_path: str) -> str:
    """
    Register a ConnectedSlave entity in the Master manifest and create its
    entity file. Raises if the node is not a Master (Network_Role check).
    Returns the created entity file path.
    """
    manifest_doc = _load_json(manifest_path)
    role = manifest_doc.get("Network_Role", "")
    if role != "Master":
        raise ValueError(
            "ConnectedSlave entity may only be created on a Master node "
            f"(Network_Role='Master'). Got: '{role}'"
        )
    return mfdb_core_create_entity_file(
        manifest_path=manifest_path,
        entity_name="ConnectedSlave",
        fields=CONNECTED_SLAVE_SCHEMA,
        description="Registry of Slave nodes connected to this Master.",
        primary_key="slave_id",
    )


def mfdb_federation_push_config(config_doc: dict, slave_target_path: str) -> bool:
    """
    Master → Slave atomic drop-zone push.
    Writes config_doc as a BEJSON 104a document to slave_target_path using a
    same-directory temp file + OS rename — guards against partial reads on the
    Slave side if it polls mid-write.
    """
    dest = os.path.abspath(slave_target_path)
    dest_dir = os.path.dirname(dest)
    os.makedirs(dest_dir, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(dir=dest_dir, suffix=".tmp")
    os.close(fd)
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(config_doc, f, indent=2)
        os.rename(temp_path, dest)
        return True
    except Exception as e:
        logging.error(f"[MFDB_FEDERATION] push_config failed: {e}")
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
        return False


def mfdb_federation_poll_dropzone(
    dropzone_dir: str,
    callback: Callable[[str, dict], None],
    poll_interval: float = 2.0,
    timeout: float = 60.0,
) -> int:
    """
    Slave: poll a local dropzone directory for incoming BEJSON 104a config docs
    pushed by the Master. Each .bejson file found is parsed, passed to callback,
    then removed. Runs until timeout seconds elapse.
    Returns the count of configs processed.
    """
    dropzone_p = Path(dropzone_dir)
    dropzone_p.mkdir(parents=True, exist_ok=True)

    processed = 0
    deadline  = time.time() + timeout

    while time.time() < deadline:
        for fpath in sorted(dropzone_p.glob("*.bejson")):
            try:
                doc = json.loads(fpath.read_text(encoding="utf-8"))
                callback(str(fpath), doc)
                fpath.unlink()
                processed += 1
            except Exception as e:
                logging.warning(f"[MFDB_FEDERATION] poll_dropzone skipped {fpath}: {e}")
        time.sleep(poll_interval)

    return processed


def mfdb_federation_distill_logs(
    slave_manifest_path: str,
    entity_name: str,
    master_poll_dir: str,
    max_rows: int = 100,
) -> bool:
    """
    Slave → Master one-way push (log distillation).
    Reads the entity file, extracts rows above max_rows (oldest overflow),
    pushes a distilled summary doc to master_poll_dir via an atomic rename,
    then truncates the local entity file back to max_rows.
    Returns True on success (including when there was nothing to distill),
    False only on error.
    """
    try:
        entity_path = _resolve_entity_path(slave_manifest_path, entity_name)
        doc  = _load_json(entity_path)
        rows = doc.get("Values", [])

        if len(rows) <= max_rows:
            return True  # Nothing to distill — not an error, matches SH (0) / TS (true)

        overflow = rows[:-max_rows]
        kept     = rows[-max_rows:]

        # Push distilled summary to Master's poll dir
        master_poll_p = Path(master_poll_dir)
        master_poll_p.mkdir(parents=True, exist_ok=True)

        ts      = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        dest    = str(master_poll_p / f"distilled_{entity_name}_{ts}.bejson")

        summary_doc = {
            "Format":             "BEJSON",
            "Format_Version":     "104a",
            "Format_Creator":     "Elton Boehnen",
            "Distill_Source":     entity_name,
            "Distill_Timestamp":  datetime.now(timezone.utc).isoformat(),
            "Records_Type":       ["DistilledLog"],
            "Fields":             doc.get("Fields", []),
            "Values":             overflow,
        }

        if not mfdb_federation_push_config(summary_doc, dest):
            return False

        # Truncate local entity to max_rows
        doc["Values"] = kept
        bejson_core_atomic_write(entity_path, doc)

        # Update record count in manifest
        manifest_doc = _load_json(slave_manifest_path)
        fields = manifest_doc.get("Fields", [])
        fm     = {f["name"]: i for i, f in enumerate(fields)}
        for row in manifest_doc.get("Values", []):
            if row[fm.get("entity_name", 0)] == entity_name and "record_count" in fm:
                row[fm["record_count"]] = len(kept)
                break
        bejson_core_atomic_write(slave_manifest_path, manifest_doc)

        return True

    except Exception as e:
        logging.error(f"[MFDB_FEDERATION] distill_logs failed: {e}")
        return False


# ── Meta-GUID Debug Entity System ──────────────────────────────────────────────
# Auto-created per MFDB when debug_mode=True. Named meta-{uuid4} to guarantee
# no collision with any user-defined entity. Gated entirely by Debug_Mode header
# on the manifest — zero overhead when off. _mfdb_meta_log() is a direct writer
# that bypasses the normal write functions to prevent infinite recursion.

META_DEBUG_FIELDS: List[Dict[str, str]] = [
    {"name": "timestamp",     "type": "string"},   # ISO 8601 UTC
    {"name": "operation",     "type": "string"},   # ADD|REMOVE|UPDATE|UPDATE_BULK|READ|SCHEMA_SNAPSHOT|ERROR
    {"name": "target_entity", "type": "string"},   # which entity was targeted
    {"name": "field_name",    "type": "string"},   # field targeted (UPDATE only, else null)
    {"name": "field_exists",  "type": "boolean"},  # was the field in Fields[]? (UPDATE only)
    {"name": "row_index",     "type": "integer"},  # record index (REMOVE/UPDATE only, else null)
    {"name": "success",       "type": "boolean"},  # did the operation succeed?
    {"name": "duration_ms",   "type": "integer"},  # wall-clock ms
    {"name": "pid",           "type": "integer"},  # process ID
    {"name": "notes",         "type": "string"},   # extra context, drift warnings, etc.
]


def _mfdb_debug_is_enabled(manifest_path: str) -> bool:
    """Return True if Debug_Mode is 'true' in the manifest headers."""
    try:
        doc = _load_json(manifest_path)
        return str(doc.get("Debug_Mode", "false")).lower() == "true"
    except Exception:
        return False


def _mfdb_debug_reads_enabled(manifest_path: str) -> bool:
    """Return True if Debug_Reads is also 'true' (separate flag for read audit)."""
    try:
        doc = _load_json(manifest_path)
        return str(doc.get("Debug_Reads", "false")).lower() == "true"
    except Exception:
        return False


def _mfdb_debug_get_meta_entity_name(manifest_path: str) -> Optional[str]:
    """Return the meta entity name from the manifest header, or None."""
    try:
        doc = _load_json(manifest_path)
        name = doc.get("Debug_Meta_Entity", "")
        return name if name else None
    except Exception:
        return None


def _mfdb_meta_log(
    manifest_path: str,
    operation:     str,
    target_entity: str,
    field_name:    Optional[str],
    field_exists:  Optional[bool],
    row_index:     Optional[int],
    success:       bool,
    duration_ms:   int,
    notes:         str,
    reads_only:    bool = False,
) -> None:
    """
    Direct writer for the meta debug entity. Bypasses all normal write
    functions to prevent recursion. Silently no-ops when debug is off,
    or when reads_only=True and Debug_Reads is off.
    Acquires its own ResilientPIDLock on the meta entity file.
    """
    try:
        if not _mfdb_debug_is_enabled(manifest_path):
            return
        if reads_only and not _mfdb_debug_reads_enabled(manifest_path):
            return

        meta_name = _mfdb_debug_get_meta_entity_name(manifest_path)
        if not meta_name:
            return

        meta_path = _get_entity_path(manifest_path, meta_name)
        row = [
            datetime.now(timezone.utc).isoformat(),
            operation,
            target_entity,
            field_name,
            field_exists,
            row_index,
            success,
            duration_ms,
            os.getpid(),
            notes or "",
        ]

        with ResilientPIDLock(meta_path, timeout_seconds=5):
            doc = _load_json(meta_path)
            doc.setdefault("Values", []).append(row)
            bejson_core_atomic_write(meta_path, doc)

        # Auto-trim if over cap
        _mfdb_meta_auto_trim(manifest_path, meta_name, meta_path)

    except Exception as e:
        logging.debug(f"[MFDB_DEBUG] meta log write failed (non-fatal): {e}")


def _mfdb_meta_auto_trim(manifest_path: str, meta_name: str, meta_path: str) -> None:
    """Trim meta entity to Debug_Row_Cap rows when exceeded. Oldest rows removed first."""
    try:
        cap_str = _load_json(manifest_path).get("Debug_Row_Cap", "500")
        cap = int(cap_str)
        doc = _load_json(meta_path)
        rows = doc.get("Values", [])
        if len(rows) > cap:
            doc["Values"] = rows[-cap:]
            bejson_core_atomic_write(meta_path, doc)
            _update_manifest_record_count(manifest_path, meta_name, len(doc["Values"]))
    except Exception:
        pass


def _mfdb_debug_schema_snapshot(manifest_path: str, meta_name: str) -> None:
    """
    Log a SCHEMA_SNAPSHOT entry for every registered entity.
    Called once on enable_debug(). Used by detect_schema_drift() as the
    baseline to diff against.
    """
    try:
        entries = _get_manifest_entries(manifest_path)
        for entry in entries:
            ename = entry.get("entity_name", "")
            if not ename or ename == meta_name:
                continue
            try:
                edoc   = _load_json(_get_entity_path(manifest_path, ename))
                fields = [f["name"] for f in edoc.get("Fields", [])]
                _mfdb_meta_log(
                    manifest_path, "SCHEMA_SNAPSHOT", ename,
                    field_name=",".join(fields),
                    field_exists=True,
                    row_index=None, success=True,
                    duration_ms=0,
                    notes=f"field_count={len(fields)}",
                )
            except Exception:
                pass
    except Exception as e:
        logging.debug(f"[MFDB_DEBUG] schema snapshot failed: {e}")


# ── Public Debug API ───────────────────────────────────────────────────────────

def mfdb_core_enable_debug(
    manifest_path:  str,
    row_cap:        int  = 500,
    debug_reads:    bool = False,
) -> str:
    """
    Activate the debug system on an existing MFDB.
    Creates a meta-{uuid4} entity, writes Debug_Mode/Debug_Meta_Entity/
    Debug_Row_Cap/Debug_Reads headers to the manifest, then logs an initial
    SCHEMA_SNAPSHOT of all registered entities as the drift baseline.
    Returns the meta entity name.
    """
    doc = _load_json(manifest_path)

    # Reuse existing meta entity if already present
    existing = doc.get("Debug_Meta_Entity", "")
    if existing:
        meta_name = existing
    else:
        meta_name = f"meta-{uuid.uuid4()}"

    doc["Debug_Mode"]        = "true"
    doc["Debug_Meta_Entity"] = meta_name
    doc["Debug_Row_Cap"]     = str(row_cap)
    doc["Debug_Reads"]       = "true" if debug_reads else "false"
    bejson_core_atomic_write(manifest_path, doc)

    # Create meta entity file if it doesn't exist
    meta_fp_rel  = f"data/{meta_name}.bejson"
    manifest_dir = os.path.dirname(os.path.abspath(manifest_path))
    meta_abs     = os.path.join(manifest_dir, meta_fp_rel)

    if not os.path.exists(meta_abs):
        os.makedirs(os.path.dirname(meta_abs), exist_ok=True)
        rel_to_manifest = os.path.relpath(manifest_path, os.path.dirname(meta_abs))
        meta_doc = {
            "Format":           "BEJSON",
            "Format_Version":   "104",
            "Format_Creator":   "Elton Boehnen",
            "Parent_Hierarchy": rel_to_manifest,
            "Records_Type":     [meta_name],
            "Fields":           META_DEBUG_FIELDS,
            "Values":           [],
        }
        bejson_core_atomic_write(meta_abs, meta_doc)

        # Register in manifest if not already there
        entries = _get_manifest_entries(manifest_path)
        if not any(e.get("entity_name") == meta_name for e in entries):
            doc2 = _load_json(manifest_path)
            doc2.setdefault("Values", []).append(
                [meta_name, meta_fp_rel, "Debug audit log (auto-generated)", 0, "1.0", None]
            )
            bejson_core_atomic_write(manifest_path, doc2)

    # Initial schema snapshot as drift baseline
    _mfdb_debug_schema_snapshot(manifest_path, meta_name)
    return meta_name


def mfdb_core_disable_debug(manifest_path: str) -> None:
    """Set Debug_Mode=false. Meta entity and its data are preserved."""
    doc = _load_json(manifest_path)
    doc["Debug_Mode"] = "false"
    bejson_core_atomic_write(manifest_path, doc)


def mfdb_core_get_debug_log(manifest_path: str) -> List[Dict[str, Any]]:
    """
    Return all meta entity rows as list-of-dicts keyed by META_DEBUG_FIELDS.
    Returns empty list when debug is off or meta entity missing.
    """
    meta_name = _mfdb_debug_get_meta_entity_name(manifest_path)
    if not meta_name:
        return []
    try:
        doc   = _load_json(_get_entity_path(manifest_path, meta_name))
        fm    = {f["name"]: i for i, f in enumerate(doc.get("Fields", META_DEBUG_FIELDS))}
        return [
            {field: row[idx] for field, idx in fm.items()}
            for row in doc.get("Values", [])
        ]
    except Exception:
        return []


def mfdb_core_get_failed_ops(manifest_path: str) -> List[Dict[str, Any]]:
    """
    Return only failed (success=False) operations from the debug log,
    sorted by timestamp ascending. Useful for post-mortem review.
    """
    all_rows = mfdb_core_get_debug_log(manifest_path)
    return sorted(
        [r for r in all_rows if r.get("success") is False],
        key=lambda r: r.get("timestamp", ""),
    )


def mfdb_core_clear_debug_log(manifest_path: str) -> int:
    """
    Wipe all rows from the meta entity. Schema is preserved.
    Returns the number of rows deleted.
    """
    meta_name = _mfdb_debug_get_meta_entity_name(manifest_path)
    if not meta_name:
        return 0
    try:
        meta_path = _get_entity_path(manifest_path, meta_name)
        with ResilientPIDLock(meta_path, timeout_seconds=10):
            doc  = _load_json(meta_path)
            deleted = len(doc.get("Values", []))
            doc["Values"] = []
            bejson_core_atomic_write(meta_path, doc)
        _update_manifest_record_count(manifest_path, meta_name, 0)
        return deleted
    except Exception:
        return 0


def mfdb_core_debug_summary(manifest_path: str) -> Dict[str, Any]:
    """
    Aggregate view of the debug log:
      - total_ops           int
      - unique_entities     list[str]
      - failed_ops          int
      - schema_drift_hits   int   (field_exists=False count)
      - top_3_slowest       list[dict]   (op, entity, duration_ms)
      - reads_logged        int
      - writes_logged       int
      - ops_by_type         dict[str, int]
    Returns empty dict when debug is off.
    """
    if not _mfdb_debug_is_enabled(manifest_path):
        return {}

    rows = mfdb_core_get_debug_log(manifest_path)
    if not rows:
        return {"total_ops": 0}

    write_ops = {"ADD", "REMOVE", "UPDATE", "UPDATE_BULK"}

    ops_by_type: Dict[str, int] = {}
    for r in rows:
        ops_by_type[r["operation"]] = ops_by_type.get(r["operation"], 0) + 1

    return {
        "total_ops":         len(rows),
        "unique_entities":   sorted({r["target_entity"] for r in rows}),
        "failed_ops":        sum(1 for r in rows if r.get("success") is False),
        "schema_drift_hits": sum(1 for r in rows if r.get("field_exists") is False),
        "top_3_slowest":     sorted(
            [{"op": r["operation"], "entity": r["target_entity"], "duration_ms": r["duration_ms"]}
             for r in rows],
            key=lambda x: x["duration_ms"], reverse=True
        )[:3],
        "reads_logged":      sum(1 for r in rows if r["operation"] == "READ"),
        "writes_logged":     sum(1 for r in rows if r["operation"] in write_ops),
        "ops_by_type":       ops_by_type,
    }


def mfdb_core_detect_schema_drift(manifest_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Compare each entity's live Fields[] against the SCHEMA_SNAPSHOT baseline
    stored in the debug log when enable_debug() was called.

    Returns a dict keyed by entity_name:
      {
        "entity_name": {
          "added_fields":   [str],   # in live schema, not in snapshot
          "removed_fields": [str],   # in snapshot, not in live schema
          "drifted":        bool,
        }
      }
    Returns empty dict when debug is off or no snapshot exists.
    """
    if not _mfdb_debug_is_enabled(manifest_path):
        return {}

    rows = mfdb_core_get_debug_log(manifest_path)
    # Find the most recent SCHEMA_SNAPSHOT entry per entity
    snapshots: Dict[str, set] = {}
    for r in rows:
        if r["operation"] == "SCHEMA_SNAPSHOT" and r.get("field_name"):
            snap_fields = set(r["field_name"].split(",")) if r["field_name"] else set()
            snapshots[r["target_entity"]] = snap_fields

    if not snapshots:
        return {}

    report: Dict[str, Dict[str, Any]] = {}
    for ename, snap_fields in snapshots.items():
        try:
            edoc        = _load_json(_get_entity_path(manifest_path, ename))
            live_fields = {f["name"] for f in edoc.get("Fields", [])}
            added       = sorted(live_fields - snap_fields)
            removed     = sorted(snap_fields - live_fields)
            report[ename] = {
                "added_fields":   added,
                "removed_fields": removed,
                "drifted":        bool(added or removed),
            }
        except Exception:
            pass

    return report
