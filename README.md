# BEJSON 104 Compiled Core Ecosystem

**Author:** Elton Boehnen  
**Contact:** boehnenelton2024@gmail.com | [boehnenelton2024.pages.dev](https://boehnenelton2024.pages.dev) | [github.com/boehnenelton](https://github.com/boehnenelton)  
**Version:** `1.1.1` (Library Version `226`)  
**Schema Name:** `MFDB-132`  
**Relational GUID:** `d8011c25-dc40-4835-a938-ff727e6eb7a4`  

---

## Table of Contents
1. [Overview & Core Architecture](#1-overview--core-architecture)
2. [Ecosystem Specifications & Formats](#2-ecosystem-specifications--formats)
   - [BEJSON 104 (Standard Entity Document)](#bejson-104-standard-entity-document)
   - [BEJSON 104a (Standalone / Flat Meta Document)](#bejson-104a-standalone--flat-meta-document)
   - [BEJSON 104db (Multi-Entity Relational Document)](#bejson-104db-multi-entity-relational-document)
   - [MFDB-132 (Modular File Database Architecture)](#mfdb-132-modular-file-database-architecture)
3. [Single-File Zero-Dependency Paradigm](#3-single-file-zero-dependency-paradigm)
4. [Cross-Language Polyglot Parity Matrix](#4-cross-language-polyglot-parity-matrix)
5. [Unified Error Registry & Numeric Catalogue](#5-unified-error-registry--numeric-catalogue)
   - [BEJSON Validation Codes (1-16)](#bejson-validation-codes-1-16)
   - [BEJSON Core Operation Codes (17-29)](#bejson-core-operation-codes-17-29)
   - [MFDB Validation Codes (30-42)](#mfdb-validation-codes-30-42)
   - [MFDB Core Engine Codes (50-72)](#mfdb-core-engine-codes-50-72)
6. [Core Engine Operations & High-Performance Field Caching](#6-core-engine-operations--high-performance-field-caching)
7. [Validation Subsystem & Strict Type Checking](#7-validation-subsystem--strict-type-checking)
8. [MFDB Relational Engine & Database Management](#8-mfdb-relational-engine--database-management)
9. [Hierarchical List Engine & Tree Integrity](#9-hierarchical-list-engine--tree-integrity)
10. [Path Guard Security & Traversal Mitigation](#10-path-guard-security--traversal-mitigation)
11. [Federated Master/Slave Node Topology](#11-federated-masterslave-node-topology)
12. [Meta-GUID Debug Audit & Telemetry Engine](#12-meta-guid-debug-audit--telemetry-engine)
13. [AES-256-GCM Record-Level Encryption](#13-aes-256-gcm-record-level-encryption)
14. [Comprehensive Code Examples & Polyglot Usage](#14-comprehensive-code-examples--polyglot-usage)
    - [Python Quickstart & Advanced Usage](#python-quickstart--advanced-usage)
    - [TypeScript / JavaScript Engine Integration](#typescript--javascript-engine-integration)
    - [POSIX Shell / Bash System Utilities](#posix-shell--bash-system-utilities)
15. [Testing, Benchmarking & Hardening Matrix](#15-testing-benchmarking--hardening-matrix)
16. [Project History & Changelog](#16-project-history--changelog)
17. [License & Author Credits](#17-license--author-credits)

---

## 1. Overview & Core Architecture

The **BEJSON 104 Compiled Core Ecosystem** is an enterprise-grade, single-file, zero-dependency data management framework engineered by **Elton Boehnen**. It provides deterministic execution across resource-constrained environments (such as Android Termux runtimes), cloud microservices, and client-side web applications.

Traditional data stores rely on binary database engines (e.g., SQLite) or key-repetitive JSON/YAML files that incur massive storage and parsing overhead. BEJSON (Boehnen Elton JSON) solves this problem by decoupling schema definitions from records, storing data in column-oriented fields and positional record arrays.

By utilizing positional arrays, BEJSON:
- Reduces file size by 40% to 70% compared to standard JSON array-of-objects structures.
- Remains 100% compliant with standard JSON parsers in all programming languages.
- Enables $O(1)$ constant-time field access via high-performance field map caching.
- Eliminates object key repetition while maintaining human readability.

The **Compiled Core** consolidates the complete BEJSON validation, core manipulation, path guard, hierarchical listing, and MFDB (Modular File Database) engine into single, standalone files per target language:
- `bejson_core_compiled.py` (Python 3 stdlib)
- `bejson_core_compiled.ts` (TypeScript / Node.js / Deno)
- `bejson_core_compiled.js` (JavaScript / CommonJS Node.js)
- `bejson_core_compiled.sh` (POSIX Shell / Bash stdlib)

---

## 2. Ecosystem Specifications & Formats

The BEJSON ecosystem defines three core document specifications, each tailored to specific data storage requirements:

### BEJSON 104 (Standard Entity Document)
Designated for primary entity data storage within an MFDB database. Contains an explicit reference to its parent database manifest via `Parent_Hierarchy`.

**Rules:**
- `Records_Type`: Exactly 1 string entry declaring the entity name.
- `Header Rules`: Forbids custom headers except `Parent_Hierarchy`.
- `Fields`: Supports primitive types (`string`, `integer`, `number`, `boolean`) and complex types (`array`, `object`).

```json
{
  "Format": "BEJSON",
  "Format_Version": "104",
  "Format_Creator": "Elton Boehnen",
  "Parent_Hierarchy": "../104a.mfdb.bejson",
  "Records_Type": ["User"],
  "Fields": [
    {"name": "user_id", "type": "string"},
    {"name": "username", "type": "string"},
    {"name": "age", "type": "integer"}
  ],
  "Values": [
    ["usr_101", "alice", 30],
    ["usr_102", "bob", 25]
  ]
}
```

### BEJSON 104a (Standalone / Flat Meta Document)
Used for database manifests (`104a.mfdb.bejson`), standalone configuration files, and flat metadata stores.

**Rules:**
- `Records_Type`: Exactly 1 string entry.
- `Header Rules`: Permits arbitrary `PascalCase` custom top-level headers (e.g., `DB_Name`, `MFDB_Version`, `Author`).
- `Fields`: Strictly primitive types (`string`, `integer`, `number`, `boolean`). Complex `array` or `object` types are strictly forbidden in 104a fields.

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "DB_Name": "SystemCoreDB",
  "MFDB_Version": "1.32",
  "Records_Type": ["mfdb"],
  "Fields": [
    {"name": "entity_name", "type": "string"},
    {"name": "file_path", "type": "string"},
    {"name": "record_count", "type": "integer"}
  ],
  "Values": [
    ["User", "data/user.bejson", 2]
  ]
}
```

### BEJSON 104db (Multi-Entity Relational Document)
Used when multiple distinct entities must co-exist within a single plain-text file.

**Rules:**
- `Records_Type`: 2 or more entity strings.
- `Header Rules`: First field MUST be named `Record_Type_Parent` with type `string`.
- `Fields`: Every subsequent field must specify a `Record_Type_Parent` property mapping it to a declared entity.

```json
{
  "Format": "BEJSON",
  "Format_Version": "104db",
  "Format_Creator": "Elton Boehnen",
  "Records_Type": ["User", "Post"],
  "Fields": [
    {"name": "Record_Type_Parent", "type": "string"},
    {"name": "id", "type": "string", "Record_Type_Parent": "User"},
    {"name": "name", "type": "string", "Record_Type_Parent": "User"},
    {"name": "title", "type": "string", "Record_Type_Parent": "Post"}
  ],
  "Values": [
    ["User", "u1", "Elton", null],
    ["Post", "p1", null, "BEJSON Core Released"]
  ]
}
```

### MFDB-132 (Modular File Database Architecture)
MFDB (Modular File Database) links multiple BEJSON 104 entity files using a central BEJSON 104a manifest (`104a.mfdb.bejson`). It enforces relational integrity, foreign key resolution, atomic file writes, PID locking, and multi-node federation.

---

## 3. Single-File Zero-Dependency Paradigm

The compiled core eliminates dependency rot, build-step fragility, and multi-file package overhead.

- **Zero Third-Party Dependencies**: Relies exclusively on core platform features (`json`, `os`, `pathlib`, `hashlib`, `zipfile` in Python; standard ES2022 / Web APIs / Node stdlib in TS/JS; `jq` / POSIX builtins in Shell).
- **Single-File Portability**: Simply drop `bejson_core_compiled.py`, `bejson_core_compiled.js`, or `bejson_core_compiled.sh` into any application directory.
- **No Intra-Package Imports**: Internal modules (`bejson_errors`, `bejson_env`, `bejson_path_guard`, `bejson_core`, `bejson_validator`, `bejson_list_validator`, `mfdb_validator`, `mfdb_core`) are completely merged into a single coherent namespace.

---

## 4. Cross-Language Polyglot Parity Matrix

The compiled core delivers bit-for-bit behavioral parity across all supported runtimes. A database created in Python can be validated in TypeScript, queried in JavaScript, and processed in Bash with identical behavior and error codes.

| Subsystem Module | Python (`.py`) | TypeScript (`.ts`) | JavaScript (`.js`) | POSIX Shell (`.sh`) |
| :--- | :---: | :---: | :---: | :---: |
| **Error Registry** | v2.4.0 | v2.4.0 | v2.4.0 | v2.4.0 |
| **Environment / Path Guard** | v1.1.0 (C-01) | v1.1.0 (C-01) | v1.1.0 (C-01) | v1.1.0 (C-01) |
| **BEJSON Core Engine** | v2.0.5 | v2.1.4 | v2.1.4 | v2.0.0 |
| **BEJSON Validator** | v2.0.3 | v2.0.2 | v2.0.2 | v2.0.0 |
| **List Validator** | v1.3.1 | v1.2.0 | v1.2.0 | v1.1.0 |
| **MFDB Validator** | v2.2.0 | v2.1.0 | v2.1.0 | v2.0.0 |
| **MFDB Core Engine** | v2.3.0 | v2.2.0 | v2.2.0 | v2.0.0 |
| **Federation Nodes** | Master/Slave | Master/Slave | Master/Slave | Master/Slave |
| **Meta-GUID Debug Engine** | Full Support | Full Support | Full Support | Full Support |

---

## 5. Unified Error Registry & Numeric Catalogue

The core maintains a unified, non-overlapping numeric error catalogue spanning all subsystems:

### BEJSON Validation Codes (1-16)
- `1`: `E_INVALID_JSON` / `INVALID_JSON`
- `2`: `E_MISSING_MANDATORY_KEY` / `MISSING_MANDATORY_KEY`
- `3`: `E_INVALID_FORMAT` / `INVALID_FORMAT_VALUE`
- `4`: `E_INVALID_VERSION` / `INVALID_FORMAT_VERSION`
- `5`: `E_INVALID_RECORDS_TYPE` / `INVALID_RECORDS_TYPE`
- `6`: `E_INVALID_FIELDS` / `INVALID_FIELDS`
- `7`: `E_INVALID_VALUES` / `INVALID_VALUES`
- `8`: `E_TYPE_MISMATCH` / `VALUE_TYPE_MISMATCH`
- `9`: `E_RECORD_LENGTH_MISMATCH` / `RECORD_LENGTH_MISMATCH`
- `10`: `E_RESERVED_KEY_COLLISION` / `RESERVED_KEY_COLLISION`
- `11`: `E_INVALID_RECORD_TYPE_PARENT` / `INVALID_RECORD_TYPE_PARENT`
- `12`: `E_NULL_VIOLATION` / `NULL_VIOLATION`
- `13`: `E_FILE_NOT_FOUND` / `FILE_NOT_FOUND`
- `14`: `E_PERMISSION_DENIED` / `PERMISSION_DENIED`
- `15`: `E_ATOMIC_WRITE_FAILED` / `ATOMIC_WRITE_FAILED`
- `16`: `E_INVALID_FORMAT_CREATOR` / `INVALID_FORMAT_CREATOR`

### BEJSON Core Operation Codes (17-29)
- `17`: `E_CORE_PARSE_ERROR` / `PARSE_ERROR`
- `18`: `E_CORE_SERIALIZATION_ERROR` / `SERIALIZATION_ERROR`
- `19`: `E_CORE_NULL_DOCUMENT` / `NULL_DOCUMENT`
- `20`: `E_CORE_INVALID_VERSION` / `INVALID_VERSION`
- `21`: `E_CORE_INVALID_OPERATION` / `INVALID_OPERATION`
- `22`: `E_CORE_INDEX_OUT_OF_BOUNDS` / `INDEX_OUT_OF_BOUNDS`
- `23`: `E_CORE_FIELD_NOT_FOUND` / `FIELD_NOT_FOUND`
- `24`: `E_CORE_TYPE_CONVERSION_FAILED` / `TYPE_CONVERSION_FAILED`
- `25`: `E_CORE_BACKUP_FAILED` / `BACKUP_FAILED`
- `26`: `E_CORE_WRITE_FAILED` / `WRITE_FAILED`
- `27`: `E_CORE_QUERY_FAILED` / `QUERY_FAILED`
- `28`: `E_CORE_ENCRYPTION_FAILED` / `ENCRYPTION_FAILED`
- `29`: `E_CORE_DECRYPTION_FAILED` / `DECRYPTION_FAILED`

### MFDB Validation Codes (30-42)
- `30`: `E_MFDB_NOT_MANIFEST` / `NOT_A_MANIFEST`
- `31`: `E_MFDB_NOT_ENTITY_FILE` / `NOT_AN_ENTITY`
- `32`: `E_MFDB_MANIFEST_RECORDS_TYPE` / `MANIFEST_RECORDS_TYPE_INVALID`
- `33`: `E_MFDB_ENTITY_NOT_FOUND` / `ENTITY_FILE_NOT_FOUND`
- `34`: `E_MFDB_ENTITY_NAME_MISMATCH` / `ENTITY_NAME_MISMATCH`
- `35`: `E_MFDB_DUPLICATE_ENTRY` / `DUPLICATE_ENTRY`
- `36`: `E_MFDB_NO_PARENT_HIERARCHY` / `MISSING_PARENT_HIERARCHY`
- `37`: `E_MFDB_MANIFEST_NOT_FOUND` / `MANIFEST_FILE_NOT_FOUND`
- `38`: `E_MFDB_BIDIRECTIONAL_FAIL` / `BIDIRECTIONAL_PATH_FAILED`
- `39`: `E_MFDB_FK_UNRESOLVED` / `FK_UNRESOLVED`
- `40`: `E_MFDB_MISSING_REQUIRED_FIELD` / `MISSING_REQUIRED_MANIFEST_FIELD`
- `41`: `E_MFDB_NULL_REQUIRED` / `NULL_IN_REQUIRED_MANIFEST_FIELD`
- `42`: `E_MFDB_INVALID_ARCHIVE` / `INVALID_ARCHIVE`

### MFDB Core Engine Codes (50-72)
- `50`: `E_MFDB_CORE_MANIFEST_NOT_FOUND` / `MANIFEST_NOT_FOUND`
- `51`: `E_MFDB_CORE_ENTITY_NOT_FOUND` / `ENTITY_NOT_FOUND`
- `52`: `E_MFDB_CORE_WRITE_FAILED` / `WRITE_FAILED`
- `53`: `E_MFDB_CORE_LOCK_FAILED` / `LOCK_FAILED`
- `54`: `E_MFDB_CORE_INVALID_OPERATION` / `INVALID_OPERATION`
- `55`: `E_MFDB_CORE_INDEX_OUT_OF_BOUNDS` / `INDEX_OUT_OF_BOUNDS`
- `56`: `E_MFDB_CORE_JOIN_FAILED` / `JOIN_FAILED`
- `57`: `E_MFDB_CORE_DUPLICATE_ENTITY_NAME` / `DUPLICATE_ENTITY_NAME`
- `58`: `E_MFDB_CORE_RECORD_COUNT_SYNC_FAILED` / `RECORD_COUNT_SYNC_FAILED`
- `59`: `E_MFDB_CORE_NULL_MANIFEST` / `NULL_MANIFEST`
- `60`: `E_MFDB_CORE_ENTITY_NOT_IN_MANIFEST` / `ENTITY_NOT_IN_MANIFEST`
- `70`: `E_MFDB_CORE_ARCHIVE_ERROR` / `ARCHIVE_ERROR`
- `71`: `E_MFDB_CORE_MOUNT_CONFLICT` / `MOUNT_CONFLICT`
- `72`: `E_MFDB_CORE_CREATE_FAILED` / `CREATE_FAILED`

---

## 6. Core Engine Operations & High-Performance Field Caching

To process tabular plain-text data without performance degradation, the core implements a global **Field Map Cache** (`_FIELD_MAP_CACHE`).

When accessing a BEJSON document, field positions are cached in memory as a tuple mapping (`field_name -> position_index`). Subsequent cell lookups, updates, or filter operations complete in $O(1)$ constant time.

Key Core Functions:
- `bejson_core_load_file(path)` / `bejson_core_load_string(content)`
- `bejson_core_atomic_write(path, data)`: Writes to a temporary `.tmp` file, calls `os.fsync()`, and performs an atomic POSIX `replace` to prevent corrupted writes on power loss.
- `bejson_core_get_field_map(doc)`: Returns or builds the cached index map.
- `bejson_core_add_record(doc, record)`
- `bejson_core_update_field(doc, row_index, field_name, value)`
- `bejson_core_remove_record(doc, index)`
- `bejson_core_filter_rows(doc, field_name, value)`

---

## 7. Validation Subsystem & Strict Type Checking

BEJSON validation enforces strict positional structure, format compliance, and data type safety.

The validation pipeline performs 6 sequential checks:
1. **Syntax Integrity**: Verifies document is a valid JSON object tree.
2. **Mandatory Header Verification**: Ensures all 6 required top-level keys exist (`Format`, `Format_Version`, `Format_Creator`, `Records_Type`, `Fields`, `Values`).
3. **Creator & Version Constraint**: Validates `Format_Creator == "Elton Boehnen"` and `Format_Version in ["104", "104a", "104db"]`.
4. **Fields Structure**: Checks for non-empty names, valid type declarations, and prevents duplicate field names.
5. **Values Matrix Alignment**: Enforces that every row in `Values` exactly matches the length of `Fields` and that cell values strictly adhere to the declared type (`string`, `integer`, `number`, `boolean`, `array`, `object`). Note: `boolean` values in `number`/`integer` columns are strictly rejected.
6. **Version-Specific Spec Enforcement**:
   - `104`: Forbids custom headers (except `Parent_Hierarchy`), enforces 1 `Records_Type`.
   - `104a`: Requires primitive-only fields, enforces `PascalCase` custom headers.
   - `104db`: Enforces `Record_Type_Parent` as the first column and checks discriminator validity for every record.

---

## 8. MFDB Relational Engine & Database Management

MFDB manages relational database operations across multiple BEJSON files with transaction safety:

- **Atomic Workspace Management**: Supports mounting and committing compressed database archives (`.mfdb.zip`) via `MFDBArchive.mount()` and `MFDBArchive.commit()`.
- **Resilient PID Locking**: Implements `ResilientPIDLock`, a directory-based mutex mechanism (`.lockdir/lock_meta.json`) with stale PID detection and automatic reclamation if a process crashes mid-transaction.
- **Relational Joins**: `mfdb_core_join()` executes cross-entity equi-joins by constructing in-memory hash indexes on target primary keys.
- **Self-Healing & Auto-Repair**: `mfdb_core_deep_verify()` audits positional integrity and count accuracy. `mfdb_core_self_heal()` resynchronizes record counts, pads short rows with nulls, and resurrects missing entity files from backup archives.

---

## 9. Hierarchical List Engine & Tree Integrity

`validate_list()` provides tree and menu integrity checks for BEJSON documents containing `id` and `parent_id` columns:
- **Duplicate ID Detection**: Rejects documents with duplicate unique identifiers.
- **Orphan Detection**: Identifies child records referencing a `parent_id` that does not exist in the document.
- **Cycle & Loop Detection**: Detects circular parent-child dependency loops (e.g., $A \rightarrow B \rightarrow C \rightarrow A$) using path traversal tracking.

---

## 10. Path Guard Security & Traversal Mitigation

Security is built directly into file resolution:

### Path Traversal Mitigation (`bejson_safe_join`)
Mitigates path traversal attacks by resolving base directories and target paths, validating that targets strictly reside within `base_dir`. Prevents sibling directory prefix bypasses (e.g., `/storage/emulated/0/Admin-secret` matching `/storage/emulated/0/Admin`).

### Relative Depth Check (`_bejson_mfdb_escapes_root`)
Evaluates relative paths segment-by-segment to prevent `..` sequences from escaping above the database root directory.

### Secure Zip Extraction
`MFDBArchive.mount()` evaluates every archive member path through `bejson_safe_join()` before extracting, eliminating Zip Slip vulnerabilities.

---

## 11. Federated Master/Slave Node Topology

MFDB includes built-in edge federation for multi-device sync across distributed Android hardware:

- **Node Roles**: Nodes declare `Network_Role` as `"Master"` or `"Slave"`.
- **ConnectedSlave Entity**: Master nodes maintain a registered `ConnectedSlave` entity tracking connected edge devices (`slave_id`, `url`, `role`, `status`, `supported_entities`).
- **Atomic Config Push**: `mfdb_federation_push_config()` drops configuration documents into a target dropzone directory using temporary file writing and atomic renaming.
- **Dropzone Polling**: `mfdb_federation_poll_dropzone()` continuously monitors local dropzone directories for incoming config payloads.
- **Log Distillation**: `mfdb_federation_distill_logs()` extracts historical overflow records exceeding `max_rows` from a Slave node, transmits a distilled summary to the Master node, and truncates the local log.

---

## 12. Meta-GUID Debug Audit & Telemetry Engine

When `debug_mode=True` is enabled, MFDB automatically provisions an isolated meta-entity named `meta-{UUID4}` (e.g., `meta-d8011c25-dc40-4835-a938-ff727e6eb7a4`).

### Features:
- **Zero Overhead when Off**: Completely dormant unless `Debug_Mode="true"` is declared in the manifest.
- **Non-Recursive Direct Writer**: `_mfdb_meta_log()` writes audit records directly, bypassing public core mutation functions to eliminate infinite recursion.
- **Telemetry Attributes**: Logs UTC timestamps, operation type (`ADD`, `REMOVE`, `UPDATE`, `READ`, `SCHEMA_SNAPSHOT`), target entity, field name, schema drift flags, row index, execution duration in milliseconds, process PID, and error notes.
- **Automatic Log Trimming**: Automatically trims the debug log to maintain a user-configurable row cap (default: 500 rows).
- **Schema Drift Detection**: `detectSchemaDrift()` compares live entity structures against baseline `SCHEMA_SNAPSHOT` records to highlight added or removed fields over time.

---

## 13. AES-256-GCM Record-Level Encryption

BEJSON supports record-level field encryption using AES-256-GCM and PBKDF2 key derivation:

- **Key Derivation**: `deriveKey(password, salt)` uses PBKDF2 with SHA-256 and 100,000 iterations.
- **Session Key Caching**: Derived keys are cached in a 4-slot LRU cache to eliminate key derivation bottlenecks during bulk record processing.
- **Encrypted Value Format**: Values are encrypted cell-by-cell and stored with their metadata:
  ```
  ENC:AES-GCM:<salt_base64>:<iv_base64>:<ciphertext_base64>
  ```
- **Selective Column Protection**: Unencrypted discriminator fields (e.g., `Record_Type_Parent`) and structural flags remain readable to permit filtering and index management without decrypting the entire file.

---

## 14. Comprehensive Code Examples & Polyglot Usage

### Python Quickstart & Advanced Usage

```python
from bejson_core_compiled import (
    bejson_core_create_104a,
    validate_bejson,
    mfdb_core_create_database,
    mfdb_core_add_entity_record,
    mfdb_core_load_entity,
    mfdb_core_enable_debug,
    mfdb_core_get_debug_log
)

# 1. Create a standalone BEJSON 104a document
fields = [
    {"name": "id", "type": "string"},
    {"name": "count", "type": "integer"}
]
values = [["item_1", 42]]
doc = bejson_core_create_104a("Inventory", fields, values)

# 2. Validate document
result = validate_bejson(doc)
print(f"Is Valid: {result.valid}")

# 3. Create an MFDB Database with Debug Audit
entities = [
    {
        "name": "Product",
        "file_path": "data/product.bejson",
        "primary_key": "sku",
        "fields": [
            {"name": "sku", "type": "string"},
            {"name": "price", "type": "number"}
        ]
    }
]
manifest_path = mfdb_core_create_database(
    root_dir="./my_db",
    db_name="StoreDB",
    entities=entities,
    debug_mode=True
)

# 4. Insert record & query telemetry
mfdb_core_add_entity_record(manifest_path, "Product", ["SKU-001", 19.99])
products = mfdb_core_load_entity(manifest_path, "Product")
print("Products:", products)

# 5. Review Debug Telemetry
log = mfdb_core_get_debug_log(manifest_path)
print(f"Audit Records Logged: {len(log)}")
```

### TypeScript / JavaScript Engine Integration

```typescript
import {
  createEmpty104a,
  validateDocument,
  createManifest,
  registerEntity,
  appendRecord
} from './bejson_core_compiled';

// 1. Create 104a doc
const fields = [
  { name: "id", type: "string" },
  { name: "active", type: "boolean" }
];
const doc = createEmpty104a("Device", fields);

// 2. Append record
const updatedDoc = appendRecord(doc, ["dev_01", true]);

// 3. Validate
const res = validateDocument(updatedDoc);
console.log("Valid:", res.valid);
```

### POSIX Shell / Bash System Utilities

```bash
source ./bejson_core_compiled.sh

# Validate a BEJSON file
bejson_validator_validate_file "data/product.bejson"
echo "Validation Exit Code: $?"

# Get field index position
bejson_core_get_field_index "data/product.bejson" "price"
```

---

## 15. Testing, Benchmarking & Hardening Matrix

The Compiled Core passes a rigorous automated test suite covering:
- **Type Safety Tests**: Verifies strict type rejection (e.g., boolean values in integer/number columns).
- **Concurrency & Locking Tests**: Validates PID lock acquisition, timeout handling, and stale PID reclamation.
- **Security Traversal Audits**: Confirms rejection of path traversal attempts and Zip Slip vectors.
- **Self-Healing Benchmarks**: Tests auto-repair functions across corrupted file sets.

---

## 16. Project History & Changelog

### Version 1.1.1 (2026-08-19)
- **C-01 Security Fix Integration**: Updated `bejson_safe_join()` to resolve sibling-directory prefix traversal vulnerabilities.
- **Header Synchronization**: Aligned JS/TS/PY compiled core headers with Schema `MFDB-132`.
- **LRU Key Cache Expansion**: Expanded AES-GCM decryption key cache to a 4-slot LRU queue for multi-entity sessions.
- **Self-Healing Hardening**: Fixed edge-case `KeyError` exceptions during `mfdb_core_self_heal()` batch passes.

---

## 17. License & Author Credits

### Author & Copyright
**Elton Boehnen**  
Email: boehnenelton2024@gmail.com  
Website: [boehnenelton2024.pages.dev](https://boehnenelton2024.pages.dev)  
GitHub: [github.com/boehnenelton](https://github.com/boehnenelton)  

### Credit Requirement
In accordance with core project policy, all modified, derived, or bundled versions of this library **must credit Elton Boehnen** (`boehnenelton2024@gmail.com`) in the file header and documentation.