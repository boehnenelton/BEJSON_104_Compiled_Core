#!/usr/bin/env bash
# Library:        bejson_core_compiled.sh
# Family:         Compiled
# Description:    Single-file compiled BEJSON+MFDB core for Bash (Termux-ready).
#                 No source directives. source /path/to/bejson_core_compiled.sh
# Version:        1.1.1
# Library_Version:226
# Date:           2026-08-19
# Schema_Name:    MFDB-132
# Author:         Elton Boehnen
# Contact:        boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton
# RELATIONAL_ID:  7de17d9e-5267-4021-bc2c-37109e4b913c
#
# Merged sources:
#   bejson_errors         v1.5.0  (+ MFDB_CORE 57-60 backfilled for compiled
#                          parity only — real Lib_SH source still lacks them, see H-02 note below)
#   bejson_core           v2.0.5
#   bejson_validator      v2.1.0
#   bejson_list_validator v1.1.0  (surface parity)
#   mfdb_validator        v2.1.1
#   mfdb_core             v2.2.0
#
# NOTE: mfdb_core is 2.2.0 here vs 2.3.0 in PY/JS — real per-language source
# split, not a compiled-artifact bug. Documented, not force-unified.

set -euo pipefail
BEJSON_CORE_COMPILED_VERSION="1.1.1"


# ==========================================================================
# SECTION 1 — ERROR REGISTRY
# Sources: bejson_errors v1.5.0
# ==========================================================================

# Library:        lib_bejson_Core_bejson_errors.sh
# Family:         Core
# Description:    Centralized error code registry for all Bash BEJSON libraries. Mirrors lib_bejson_Core_bejson_errors.js and lib_bejson_Core_bejson_errors.py.
# Version:        1.5.0
# Date:           2026-07-30
# Author:         Elton Boehnen
# Contact:        boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton
# Format_Creator: Elton Boehnen
# RELATIONAL_ID:  2d9c4b71-5a3e-4f8d-b1c6-7e0a2f8d3c95
#
# Changelog:
#   1.5.0 - LEGACY ALIASES section deleted (Step 2 — 1.32 finalization).
#           E_VAL_NOT_JSON, E_VAL_MISSING_KEY, E_VAL_BAD_FORMAT,
#           E_VAL_BAD_VERSION, E_VAL_BAD_CREATOR, E_VAL_SCHEMA_MISMATCH,
#           E_VAL_INVALID_TYPE removed. lib_bejson_Core_bejson_validator.sh
#           updated to use primary unified codes at all return sites.
#   1.4.0 - Removed Core_Nesting range (130-159) — that family now owns its
#           codes in lib_bejson_CoreNesting_bejson_errors.sh. MFDB codes
#           (30-49, 50-79) remain here: MFDB is implemented as part of the
#           Core family, not a separate family directory.

# ===========================================================================
# BEJSON VALIDATOR ERRORS (1–19)  — mirrors E_* in lib_bejson_Core_bejson_errors.js / .py
# ===========================================================================
[[ -v E_INVALID_JSON                ]] || readonly E_INVALID_JSON=1
[[ -v E_MISSING_MANDATORY_KEY       ]] || readonly E_MISSING_MANDATORY_KEY=2
[[ -v E_INVALID_FORMAT              ]] || readonly E_INVALID_FORMAT=3
[[ -v E_INVALID_VERSION             ]] || readonly E_INVALID_VERSION=4
[[ -v E_INVALID_RECORDS_TYPE        ]] || readonly E_INVALID_RECORDS_TYPE=5
[[ -v E_INVALID_FIELDS              ]] || readonly E_INVALID_FIELDS=6
[[ -v E_INVALID_VALUES              ]] || readonly E_INVALID_VALUES=7
[[ -v E_TYPE_MISMATCH               ]] || readonly E_TYPE_MISMATCH=8
[[ -v E_RECORD_LENGTH_MISMATCH      ]] || readonly E_RECORD_LENGTH_MISMATCH=9
[[ -v E_RESERVED_KEY_COLLISION      ]] || readonly E_RESERVED_KEY_COLLISION=10
[[ -v E_INVALID_RECORD_TYPE_PARENT  ]] || readonly E_INVALID_RECORD_TYPE_PARENT=11
[[ -v E_NULL_VIOLATION              ]] || readonly E_NULL_VIOLATION=12
[[ -v E_FILE_NOT_FOUND              ]] || readonly E_FILE_NOT_FOUND=13
[[ -v E_PERMISSION_DENIED           ]] || readonly E_PERMISSION_DENIED=14
[[ -v E_ATOMIC_WRITE_FAILED         ]] || readonly E_ATOMIC_WRITE_FAILED=15
[[ -v E_INVALID_FORMAT_CREATOR      ]] || readonly E_INVALID_FORMAT_CREATOR=16

# ===========================================================================
# BEJSON CORE ERRORS (20–29)
# ===========================================================================
[[ -v E_CORE_INVALID_VERSION        ]] || readonly E_CORE_INVALID_VERSION=20
[[ -v E_CORE_INVALID_OPERATION      ]] || readonly E_CORE_INVALID_OPERATION=21
[[ -v E_CORE_INDEX_OUT_OF_BOUNDS    ]] || readonly E_CORE_INDEX_OUT_OF_BOUNDS=22
[[ -v E_CORE_FIELD_NOT_FOUND        ]] || readonly E_CORE_FIELD_NOT_FOUND=23
[[ -v E_CORE_TYPE_CONVERSION_FAILED ]] || readonly E_CORE_TYPE_CONVERSION_FAILED=24
[[ -v E_CORE_BACKUP_FAILED          ]] || readonly E_CORE_BACKUP_FAILED=25
[[ -v E_CORE_WRITE_FAILED           ]] || readonly E_CORE_WRITE_FAILED=26
[[ -v E_CORE_QUERY_FAILED           ]] || readonly E_CORE_QUERY_FAILED=27
[[ -v E_CORE_ENCRYPTION_FAILED      ]] || readonly E_CORE_ENCRYPTION_FAILED=28
[[ -v E_CORE_DECRYPTION_FAILED      ]] || readonly E_CORE_DECRYPTION_FAILED=29

# ===========================================================================
# MFDB VALIDATOR ERRORS (30–49)
# ===========================================================================
[[ -v E_MFDB_NOT_MANIFEST           ]] || readonly E_MFDB_NOT_MANIFEST=30
[[ -v E_MFDB_NOT_ENTITY_FILE        ]] || readonly E_MFDB_NOT_ENTITY_FILE=31
[[ -v E_MFDB_MANIFEST_RECORDS_TYPE  ]] || readonly E_MFDB_MANIFEST_RECORDS_TYPE=32
[[ -v E_MFDB_ENTITY_NOT_FOUND       ]] || readonly E_MFDB_ENTITY_NOT_FOUND=33
[[ -v E_MFDB_ENTITY_NAME_MISMATCH   ]] || readonly E_MFDB_ENTITY_NAME_MISMATCH=34
[[ -v E_MFDB_DUPLICATE_ENTRY        ]] || readonly E_MFDB_DUPLICATE_ENTRY=35
[[ -v E_MFDB_NO_PARENT_HIERARCHY    ]] || readonly E_MFDB_NO_PARENT_HIERARCHY=36
[[ -v E_MFDB_MANIFEST_NOT_FOUND     ]] || readonly E_MFDB_MANIFEST_NOT_FOUND=37
[[ -v E_MFDB_BIDIRECTIONAL_FAIL     ]] || readonly E_MFDB_BIDIRECTIONAL_FAIL=38
[[ -v E_MFDB_FK_UNRESOLVED          ]] || readonly E_MFDB_FK_UNRESOLVED=39
[[ -v E_MFDB_MISSING_REQUIRED_FIELD ]] || readonly E_MFDB_MISSING_REQUIRED_FIELD=40
[[ -v E_MFDB_NULL_REQUIRED          ]] || readonly E_MFDB_NULL_REQUIRED=41
[[ -v E_MFDB_INVALID_ARCHIVE        ]] || readonly E_MFDB_INVALID_ARCHIVE=42

# ===========================================================================
# MFDB CORE ERRORS (50–79)
# ===========================================================================
# MFDB Core error codes — aligned with canonical PY/TS registry
# NOTE (H-02, 2026-08-19): codes 57-60 below are NOT present in the real
# Lib_SH/Core/lib_bejson_Core_bejson_errors.sh (v1.5.0) source. Backfilled
# here for compiled-artifact parity only. The upstream Lib_SH errors file
# still needs this same backfill — flagging, not silently fixing it there.
[[ -v E_MFDB_CORE_MANIFEST_NOT_FOUND ]] || readonly E_MFDB_CORE_MANIFEST_NOT_FOUND=50
[[ -v E_MFDB_CORE_ENTITY_NOT_FOUND  ]] || readonly E_MFDB_CORE_ENTITY_NOT_FOUND=51
[[ -v E_MFDB_CORE_WRITE_FAILED      ]] || readonly E_MFDB_CORE_WRITE_FAILED=52
[[ -v E_MFDB_CORE_LOCK_FAILED       ]] || readonly E_MFDB_CORE_LOCK_FAILED=53
[[ -v E_MFDB_CORE_INVALID_OPERATION ]] || readonly E_MFDB_CORE_INVALID_OPERATION=54
[[ -v E_MFDB_CORE_INDEX_OUT_OF_BOUNDS ]] || readonly E_MFDB_CORE_INDEX_OUT_OF_BOUNDS=55
[[ -v E_MFDB_CORE_JOIN_FAILED       ]] || readonly E_MFDB_CORE_JOIN_FAILED=56
[[ -v E_MFDB_CORE_DUPLICATE_ENTITY_NAME ]] || readonly E_MFDB_CORE_DUPLICATE_ENTITY_NAME=57
[[ -v E_MFDB_CORE_RECORD_COUNT_SYNC_FAILED ]] || readonly E_MFDB_CORE_RECORD_COUNT_SYNC_FAILED=58
[[ -v E_MFDB_CORE_NULL_MANIFEST     ]] || readonly E_MFDB_CORE_NULL_MANIFEST=59
[[ -v E_MFDB_CORE_ENTITY_NOT_IN_MANIFEST ]] || readonly E_MFDB_CORE_ENTITY_NOT_IN_MANIFEST=60
[[ -v E_MFDB_CORE_ARCHIVE_ERROR     ]] || readonly E_MFDB_CORE_ARCHIVE_ERROR=70
[[ -v E_MFDB_CORE_MOUNT_CONFLICT    ]] || readonly E_MFDB_CORE_MOUNT_CONFLICT=71
[[ -v E_MFDB_CORE_CREATE_FAILED     ]] || readonly E_MFDB_CORE_CREATE_FAILED=72


# Core_Nesting codes moved to lib_bejson_CoreNesting_bejson_errors.sh (v1.4.0)


# ==========================================================================
# SECTION 2 — BEJSON CORE
# Sources: bejson_core v2.0.5
# ==========================================================================

# Library:        lib_bejson_Core_bejson_core.sh
# Family:         Core
# Description:    Low-level primitive operations for BEJSON document manipulation.
# BEJSON:         BEJSON stands for BOEHNEN ELTON JSON. Authoritative definition;
#                 do not restate or reinterpret this acronym elsewhere.
# MFDB:           MFDB stands for Multi File Database. Authoritative definition;
#                 do not restate or reinterpret this acronym elsewhere.
# Version:        2.0.5
# Date:           2026-07-22
# Author:         Elton Boehnen
# Contact:        boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton
# Format_Creator: Elton Boehnen
# RELATIONAL_ID:  0803e16a-d44d-4fcc-9ba4-bf7909109fe0

#===============================================================================

#-------------------------------------------------------------------------------
# SAFETY & ERROR HANDLING
#-------------------------------------------------------------------------------

# NOTE: set -o nounset intentionally omitted — library files must not modify
# global shell options; doing so breaks host scripts that source this file. (SH3)
set -o pipefail

# Source the validator library and error registry (assumes same directory)
_CORE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"


#-------------------------------------------------------------------------------
# ATOMIC FILE OPERATIONS
#-------------------------------------------------------------------------------

__bejson_core_atomic_backup() {
    local file_path="$1"
    [[ ! -f "$file_path" ]] && return 0
    local backup_path="${file_path}.backup.$(date +%Y%m%d_%H%M%S).$$"
    cp -p "$file_path" "$backup_path" 2>/dev/null || return $E_CORE_BACKUP_FAILED
    echo "$backup_path"
    return 0
}

__bejson_core_restore_backup() {
    local file_path="$1"
    local backup_path="$2"
    [[ -f "$backup_path" ]] && mv "$backup_path" "$file_path" 2>/dev/null
}

bejson_core_atomic_write() {
    local file_path="$1"
    local content="$2"
    local create_backup="${3:-true}"
    local backup_path=""

    if [[ "$create_backup" == "true" ]]; then
        backup_path=$(__bejson_core_atomic_backup "$file_path") || return $?
    fi

    local target_dir=$(dirname "$file_path")
    mkdir -p "$target_dir"
    local temp_file="${target_dir}/.bejson_$$.tmp"

    printf '%s' "$content" > "$temp_file" 2>/dev/null || {
        [[ -n "$backup_path" ]] && __bejson_core_restore_backup "$file_path" "$backup_path"
        return $E_CORE_WRITE_FAILED
    }

    # NOTE SH6: On Android exFAT SD card paths (/storage/<UUID>/...), sync(1) may be a
    # no-op or unavailable. The || true swallow is intentional — writes to SD have
    # weaker durability guarantees than internal storage on Android.
    sync "$temp_file" 2>/dev/null || true
    mv "$temp_file" "$file_path" 2>/dev/null || {
        cp -p "$temp_file" "$file_path" 2>/dev/null && rm -f "$temp_file" || {
            [[ -n "$backup_path" ]] && __bejson_core_restore_backup "$file_path" "$backup_path"
            return $E_CORE_WRITE_FAILED
        }
    }
    sync "$(dirname "$file_path")" 2>/dev/null || true
    return 0
}

#-------------------------------------------------------------------------------
# MUTEX LOCKING (Policy Sec. 47)
#-------------------------------------------------------------------------------

resilient_lock_acquire() {
    local target="$1"
    local lock_dir="${target}.lockdir"
    local meta="${lock_dir}/lock_meta.json"
    local timeout="${2:-10}"
    local start
    start=$(date +%s)
    
    while true; do
        if mkdir "$lock_dir" 2>/dev/null; then
            # Lock acquired — write PID metadata
            printf '{"pid": %d, "timestamp": %d}\n' "$$" "$(date +%s)" > "$meta"
            return 0
        fi
        
        # Check for dead-process orphan
        if [[ -f "$meta" ]]; then
            local pid
            pid=$(jq -r '.pid // empty' "$meta" 2>/dev/null)
            if [[ -n "$pid" ]] && ! kill -0 "$pid" 2>/dev/null; then
                # Safe reclamation: owner process is dead
                rm -rf "$lock_dir" 2>/dev/null
                continue
            fi
        fi
        
        if [[ $(($(date +%s) - start)) -ge $timeout ]]; then
            return 53  # E_MFDB_CORE_LOCK_FAILED
        fi
        sleep 0.2
    done
}

resilient_lock_release() {
    local target="$1"
    local lock_dir="${target}.lockdir"
    [[ -d "$lock_dir" ]] && rm -rf "$lock_dir" 2>/dev/null
    return 0
}

bejson_core_load_file() {
    local file_path="$1"
    if [[ ! -f "$file_path" ]]; then
        return $E_CORE_FIELD_NOT_FOUND
    fi
    cat "$file_path"
}

#-------------------------------------------------------------------------------
# FIELD & RECORD OPERATIONS
#-------------------------------------------------------------------------------

bejson_core_get_field_index() {
    local doc="$1"
    local field_name="$2"
    echo "$doc" | jq --arg fn "$field_name" '.Fields | map(.name) | index($fn) // -1'
}

bejson_core_get_record_count() {
    local doc="$1"
    echo "$doc" | jq '.Values | length'
}

bejson_core_add_record() {
    local doc="$1"
    local values_json="$2"
    echo "$doc" | jq --argjson row "$values_json" '.Values += [$row]'
}

bejson_core_remove_record() {
    local doc="$1"
    local index="$2"
    echo "$doc" | jq --argjson idx "$index" 'del(.Values[$idx])'
}

bejson_core_update_field() {
    # --arg always writes a JSON string. Inspect declared field type and use
    # --argjson when the field is not a string so integers/booleans/numbers round-trip
    # correctly. Falls back to --arg only for string-typed fields.
    local doc="$1"
    local rec_idx="$2"
    local field_name="$3"
    local new_val="$4"
    local f_idx
    f_idx=$(bejson_core_get_field_index "$doc" "$field_name")
    if [[ "$f_idx" == "-1" ]]; then return $E_CORE_FIELD_NOT_FOUND; fi

    local field_type
    field_type=$(echo "$doc" | jq -r --argjson fi "$f_idx" '.Fields[$fi].type // "string"')

    if [[ "$field_type" == "string" ]]; then
        echo "$doc" | jq --argjson ri "$rec_idx" --argjson fi "$f_idx" --arg nv "$new_val" '(.Values[$ri][$fi]) = $nv'
    else
        # Use --argjson so the value is written as the correct JSON type (number, boolean, etc.)
        echo "$doc" | jq --argjson ri "$rec_idx" --argjson fi "$f_idx" --argjson nv "$new_val" '(.Values[$ri][$fi]) = $nv'
    fi
}

#-------------------------------------------------------------------------------
# QUERY & SORT
#-------------------------------------------------------------------------------

bejson_core_filter_rows() {
    local doc="$1"
    local field_name="$2"
    local value="$3"
    local f_idx=$(bejson_core_get_field_index "$doc" "$field_name")
    if [[ "$f_idx" == "-1" ]]; then return $E_CORE_FIELD_NOT_FOUND; fi
    echo "$doc" | jq --argjson fi "$f_idx" --arg val "$value" '.Values | map(select(.[$fi] == $val))'
}

bejson_core_sort_by_field() {
    local doc="$1"
    local field_name="$2"
    local ascending="${3:-true}"
    local f_idx=$(bejson_core_get_field_index "$doc" "$field_name")
    if [[ "$f_idx" == "-1" ]]; then return $E_CORE_FIELD_NOT_FOUND; fi
    if [[ "$ascending" == "true" ]]; then
        echo "$doc" | jq --argjson fi "$f_idx" '.Values |= sort_by(.[$fi])'
    else
        echo "$doc" | jq --argjson fi "$f_idx" '.Values |= (sort_by(.[$fi]) | reverse)'
    fi
}

# Export functions
export -f bejson_core_atomic_write
export -f bejson_core_load_file
export -f bejson_core_get_field_index
export -f bejson_core_get_record_count
export -f bejson_core_add_record
export -f bejson_core_remove_record
export -f bejson_core_update_field
export -f bejson_core_filter_rows
export -f bejson_core_sort_by_field
export -f resilient_lock_acquire
export -f resilient_lock_release


# ==========================================================================
# SECTION 3 — BEJSON VALIDATOR
# Sources: bejson_validator v2.1.0
# ==========================================================================

# Library:        lib_bejson_Core_bejson_validator.sh
# Family:         Core
# Description:    Structural integrity checker for positional values and mandatory keys.
# Version:        2.1.0
# Date:           2026-07-30
# Author:         Elton Boehnen
# Contact:        boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton
# Format_Creator: Elton Boehnen
# RELATIONAL_ID:  5f8a3c71-9d2e-4b6f-a0c4-1e7b5d9f2a83
#
# Changelog:
#   2.1.0 - Step 2 (1.32 finalization): removed local re-declarations of legacy
#           E_VAL_* aliases and migrated all 5 return sites to primary unified
#           codes (E_INVALID_JSON, E_MISSING_MANDATORY_KEY, E_INVALID_FORMAT,
#           E_INVALID_FORMAT_CREATOR, E_RECORD_LENGTH_MISMATCH). Aliases no
#           longer exist in lib_bejson_Core_bejson_errors.sh.

set -o pipefail

# Source the error registry (assumes same directory)
_VAL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#-------------------------------------------------------------------------------
# CORE VALIDATION
#-------------------------------------------------------------------------------

bejson_validator_check_dependencies() {
    if ! command -v jq >/dev/null 2>&1; then
        echo "ERROR: jq is required for BEJSON validation" >&2
        return 1
    fi
    local jq_ver
    jq_ver=$(jq --version | sed 's/jq-//')
    local jq_major jq_minor
    jq_major="${jq_ver%%.*}"
    jq_minor="${jq_ver#*.}"; jq_minor="${jq_minor%%.*}"
    if [[ "$jq_major" -lt 1 ]] || { [[ "$jq_major" -eq 1 ]] && [[ "$jq_minor" -lt 6 ]]; }; then
        echo "ERROR: jq >= 1.6 is required. Found: $jq_ver" >&2
        return 1
    fi
    return 0
}

bejson_validator_validate_file() {
    local file_path="$1"
    if [[ ! -f "$file_path" ]]; then
        echo "ERROR: File not found: $file_path" >&2
        return 1
    fi

    # 1. Basic JSON check
    if ! jq . "$file_path" >/dev/null 2>&1; then
        return $E_INVALID_JSON
    fi

    # 2. Mandatory Keys — exact presence check via jq (FIX SH1)
    #    Using =~ on a joined key string caused substring collisions:
    #    "Format" matched inside "Format_Creator", making missing bare "Format" go undetected.
    for k in Format Format_Version Format_Creator Records_Type Fields Values; do
        if ! jq -e --arg key "$k" 'has($key)' "$file_path" >/dev/null 2>&1; then
            return $E_MISSING_MANDATORY_KEY
        fi
    done

    # 3. Format & Creator check
    local fmt creator
    fmt=$(jq -r '.Format' "$file_path")
    creator=$(jq -r '.Format_Creator' "$file_path")
    [[ "$fmt"     != "BEJSON"        ]] && return $E_INVALID_FORMAT
    [[ "$creator" != "Elton Boehnen" ]] && return $E_INVALID_FORMAT_CREATOR

    # 4. Records Length check
    local field_count bad_records
    field_count=$(jq '.Fields | length' "$file_path")
    bad_records=$(jq --argjson fc "$field_count" '.Values | map(select(length != $fc)) | length' "$file_path")
    if [[ "$bad_records" -gt 0 ]]; then
        return $E_RECORD_LENGTH_MISMATCH
    fi

    return 0
}

# Export functions for subshell use
export -f bejson_validator_check_dependencies
export -f bejson_validator_validate_file


# ==========================================================================
# SECTION 4 — LIST VALIDATOR
# Sources: bejson_list_validator v1.1.0
# ==========================================================================

# Library:        lib_bejson_Core_bejson_list_validator.sh
# Family:         Core
# Description:    Hierarchical list validator for BEJSON 104a documents. Validates
#                 id/parent_id integrity and orphan/cycle detection.
# Version:        1.1.0
# Date:           2026-06-28
# Author:         Elton Boehnen
# Contact:        boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton
# Format_Creator: Elton Boehnen
# RELATIONAL_ID:  1bcc48c9-36c0-4a25-8aac-1e163a231384


bejson_list_validator_validate() {
    local file="$1"
    bejson_validator_validate_file "$file" || return $?
    local ver=$(jq -r ".Format_Version" "$file")
    [[ "$ver" != "104a" ]] && return 4
    return 0
}


# ==========================================================================
# SECTION 5 — MFDB VALIDATOR
# Sources: mfdb_validator v2.1.1
# ==========================================================================

# Library:        lib_bejson_Core_mfdb_validator.sh
# Family:         Core
# Description:    Bidirectional path and manifest-entity relationship validator.
#                 Also owns MFDB-132-package validation
#                 (mfdb_validator_is_mfdb132_package,
#                 mfdb_validator_validate_mfdb132_package,
#                 mfdb_validator_detect_mfdb_in_chunk) — relocated here from
#                 lib_bejson_Core_bejson_chunking.sh, which should only own
#                 packaging/IO, not validation logic. See changelog note
#                 dated 2026-07-13.
# Version:        2.1.1
# Date:           2026-07-14
# Author:         Elton Boehnen
# Contact:        boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton
# Format_Creator: Elton Boehnen
# RELATIONAL_ID:  e5b2cda2-bcc8-4a39-b710-eef526056d4d
#
# BUGFIX (2026-07-14): mfdb_validator_detect_mfdb_in_chunk's manifest_content
# extraction piped `jq -r ... | head -n1`. jq -r prints a string's real
# embedded newlines as literal line breaks, so any pretty-printed (multi-line)
# manifest — the normal case — was truncated to its first line ("{"),
# making it fail JSON parsing. Fixed by selecting the first match inside jq
# itself ([.Values[] | select(...)] | .[0]) and removing the shell-side
# `head -n1` truncation entirely. See /docs/BUGFIX_sh_detect_mfdb_truncation.md.

# NOTE: set -o nounset intentionally omitted — library files must not modify
# global shell options; doing so breaks host scripts that source this file. (SH3)
set -o pipefail

# Source base validator if not already loaded
_MFDB_VAL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#-------------------------------------------------------------------------------
# Error codes (30–49)
#-------------------------------------------------------------------------------

[[ -v E_MFDB_NOT_MANIFEST ]] || readonly E_MFDB_NOT_MANIFEST=30
[[ -v E_MFDB_NOT_ENTITY_FILE ]] || readonly E_MFDB_NOT_ENTITY_FILE=31
[[ -v E_MFDB_MANIFEST_RECORDS_TYPE ]] || readonly E_MFDB_MANIFEST_RECORDS_TYPE=32
[[ -v E_MFDB_ENTITY_NOT_FOUND ]] || readonly E_MFDB_ENTITY_NOT_FOUND=33
[[ -v E_MFDB_ENTITY_NAME_MISMATCH ]] || readonly E_MFDB_ENTITY_NAME_MISMATCH=34
[[ -v E_MFDB_DUPLICATE_ENTRY ]] || readonly E_MFDB_DUPLICATE_ENTRY=35
[[ -v E_MFDB_NO_PARENT_HIERARCHY ]] || readonly E_MFDB_NO_PARENT_HIERARCHY=36
[[ -v E_MFDB_MANIFEST_NOT_FOUND ]] || readonly E_MFDB_MANIFEST_NOT_FOUND=37
[[ -v E_MFDB_BIDIRECTIONAL_FAIL ]] || readonly E_MFDB_BIDIRECTIONAL_FAIL=38
[[ -v E_MFDB_FK_UNRESOLVED ]] || readonly E_MFDB_FK_UNRESOLVED=39
[[ -v E_MFDB_MISSING_REQUIRED_FIELD ]] || readonly E_MFDB_MISSING_REQUIRED_FIELD=40
[[ -v E_MFDB_NULL_REQUIRED ]] || readonly E_MFDB_NULL_REQUIRED=41
[[ -v E_MFDB_INVALID_ARCHIVE ]] || readonly E_MFDB_INVALID_ARCHIVE=42

#-------------------------------------------------------------------------------
# Validation state
#-------------------------------------------------------------------------------

__MFDB_VALIDATION_ERRORS=()
__MFDB_VALIDATION_WARNINGS=()

mfdb_validator_reset_state() {
    __MFDB_VALIDATION_ERRORS=()
    __MFDB_VALIDATION_WARNINGS=()
}

__mfdb_add_error() {
    local message="$1"
    local location="${2:-}"
    __MFDB_VALIDATION_ERRORS+=("ERROR | Location: $location | Message: $message")
}

mfdb_validator_has_errors()   { [[ ${#__MFDB_VALIDATION_ERRORS[@]}   -gt 0 ]]; }
mfdb_validator_get_errors()    { printf '%s\n' "${__MFDB_VALIDATION_ERRORS[@]+"${__MFDB_VALIDATION_ERRORS[@]}"}"; }

#-------------------------------------------------------------------------------
# Archive Validation
#-------------------------------------------------------------------------------

# mfdb_validator_validate_archive <archive_path>
mfdb_validator_validate_archive() {
    local archive_path="$1"
    mfdb_validator_reset_state
    if [[ ! -f "$archive_path" ]]; then
        __mfdb_add_error "Archive not found: $archive_path" "File System"
        return $E_MFDB_MANIFEST_NOT_FOUND
    fi

    if ! unzip -l "$archive_path" | grep -q "104a.mfdb.bejson"; then
        __mfdb_add_error "Missing 104a.mfdb.bejson manifest inside archive" "Zip Structure"
        return $E_MFDB_INVALID_ARCHIVE
    fi
    return 0
}

#-------------------------------------------------------------------------------
# Main validation
#-------------------------------------------------------------------------------

mfdb_validator_validate_manifest() {
    local manifest_path="$1"
    mfdb_validator_reset_state
    [[ ! -f "$manifest_path" ]] && return $E_MFDB_MANIFEST_NOT_FOUND
    bejson_validator_validate_file "$manifest_path" || return $E_MFDB_NOT_MANIFEST
    
    local rt=$(jq -r '.Records_Type | @json' "$manifest_path" 2>/dev/null)
    [[ "$rt" != '["mfdb"]' ]] && return $E_MFDB_MANIFEST_RECORDS_TYPE
    return 0
}

#-------------------------------------------------------------------------------
# Dependency check
#-------------------------------------------------------------------------------

mfdb_validator_check_dependencies() {
    if ! command -v unzip >/dev/null 2>&1; then
        echo "ERROR: Required command 'unzip' not found" >&2
        return 1
    fi
    # Strictly enforce jq >= 1.6 via base validator
    if ! bejson_validator_check_dependencies; then
        return 1
    fi
    return 0
}

#-------------------------------------------------------------------------------
# MFDB 1.32 chunked-package validation
#-------------------------------------------------------------------------------
# Relocated from lib_bejson_Core_bejson_chunking.sh (2026-07-13). The chunking
# library still owns bejson_core_chunking_create_mfdb132_package /
# bejson_core_chunking_unchunk_mfdb132_package (packaging and IO), but calls
# back into these functions for the actual validation — validation logic
# belongs in the validator family, not the chunker.

MFDB_VALIDATOR_MANIFEST_FILENAME="104a.mfdb.bejson"

# mfdb_validator_is_mfdb132_package <doc_json>
# Echoes "true" or "false".
mfdb_validator_is_mfdb132_package() {
    local doc_json="$1"
    printf '%s' "$doc_json" | jq -r '
        if (.Format_Version == "104a")
           and (.Schema_Name == "MFDB-132")
           and (.Package_Format == "MFDB-Chunked-104a")
           and (.MFDB_Version != null and .MFDB_Version != "")
           and (.DB_Name != null and .DB_Name != "")
        then "true" else "false" end'
}

# mfdb_validator_validate_mfdb132_package <doc_json>
# Prints {"valid":bool,"errors":[...],"warnings":[...]} as JSON.
mfdb_validator_validate_mfdb132_package() {
    local doc_json="$1"
    local is_pkg
    is_pkg=$(mfdb_validator_is_mfdb132_package "$doc_json")

    if [[ "$is_pkg" != "true" ]]; then
        jq -n '{"valid": false, "errors": ["Document is not a recognized MFDB-132 package (missing/incorrect Schema_Name/Package_Format/MFDB_Version/DB_Name)."], "warnings": []}'
        return
    fi

    printf '%s' "$doc_json" | jq \
        --arg manifest "$MFDB_VALIDATOR_MANIFEST_FILENAME" '
        def records_type_ok: (.Records_Type == ["MFDB-132"]);
        def manifest_found: ([.Values[] | select(.[5] == $manifest)] | length) > 0;
        {
          "valid": (records_type_ok and manifest_found),
          "errors": (
            (if records_type_ok then [] else ["Records_Type must be exactly [\"MFDB-132\"] for an MFDB-132 package."] end)
            +
            (if manifest_found then [] else ["Chunked package does not contain the MFDB manifest (\($manifest)) — not a complete MFDB package."] end)
          ),
          "warnings": []
        }'
}

# mfdb_validator_detect_mfdb_in_chunk <doc_json>
# Prints a JSON object: {mfdb_detected, valid, db_name, mfdb_version,
# entities: [...], errors: [...], warnings: [...]}
mfdb_validator_detect_mfdb_in_chunk() {
    local doc_json="$1"
    local manifest_name="$MFDB_VALIDATOR_MANIFEST_FILENAME"

    local manifest_content
    manifest_content=$(printf '%s' "$doc_json" | jq -r --arg m "$manifest_name" '
        ([.Values[] | select(.[5] == $m)] | .[0]) as $row
        | if $row == null then "__NOT_FOUND__"
          elif $row[6] == true then "__IS_BINARY__"
          else $row[2] end' 2>/dev/null)

    if [[ "$manifest_content" == "__NOT_FOUND__" || -z "$manifest_content" ]]; then
        jq -n --arg m "$manifest_name" '{
            "mfdb_detected": false, "valid": false, "db_name": null, "mfdb_version": null,
            "entities": [], "errors": ["No manifest (\($m)) found in chunk — no MFDB present."], "warnings": []
        }'
        return
    fi
    if [[ "$manifest_content" == "__IS_BINARY__" ]]; then
        jq -n '{
            "mfdb_detected": false, "valid": false, "db_name": null, "mfdb_version": null,
            "entities": [], "errors": ["Manifest row is flagged Is_Binary — its content was never stored, cannot validate."], "warnings": []
        }'
        return
    fi

    if ! printf '%s' "$manifest_content" | jq -e . >/dev/null 2>&1; then
        jq -n '{
            "mfdb_detected": true, "valid": false, "db_name": null, "mfdb_version": null,
            "entities": [], "errors": ["Manifest content is not valid JSON."], "warnings": []
        }'
        return
    fi

    # Level 1 manifest checks + build the entity list with per-entity Level 2
    # checks, by looking each entity's file_path up in the chunk itself.
    jq -n \
        --argjson doc "$doc_json" \
        --argjson manifest "$manifest_content" \
        --arg m "$manifest_name" '
        def find_row($rel): ([$doc.Values[] | select(.[5] == $rel)] | if length > 0 then .[0] else null end);

        ($manifest.Format_Version == "104a") as $fmt_ok |
        ($manifest.Records_Type == ["mfdb"]) as $rt_ok |
        ($manifest.Fields // [] | map(.name)) as $mfields |
        ($mfields | index("entity_name")) as $en_idx |
        ($mfields | index("file_path")) as $fp_idx |

        if ($en_idx == null or $fp_idx == null) then
          {
            "mfdb_detected": true, "valid": false,
            "db_name": ($manifest.DB_Name // null),
            "mfdb_version": ($manifest.MFDB_Version // null),
            "entities": [],
            "errors": (
              (if $fmt_ok then [] else ["Manifest Format_Version must be \"104a\"."] end)
              + (if $rt_ok then [] else ["Manifest Records_Type must be exactly [\"mfdb\"]."] end)
              + ["Manifest Fields must include \"entity_name\" and \"file_path\"."]
            ),
            "warnings": []
          }
        else
        {
          "mfdb_detected": true,
          "db_name": ($manifest.DB_Name // null),
          "mfdb_version": ($manifest.MFDB_Version // null),
          "entities": [
            $manifest.Values[] as $erow |
            ($erow[$en_idx]) as $entity_name |
            ($erow[$fp_idx]) as $file_path |
            (find_row($file_path)) as $chunk_row |
            {
              "entity_name": $entity_name,
              "file_path": $file_path,
              "found_in_chunk": ($chunk_row != null),
              "errors": (
                (if ($entity_name != null and $file_path != null) then [] else ["entity_name/file_path must not be null."] end)
                + (if $chunk_row == null then
                     ["Entity file \($file_path) listed in manifest was not found in chunk."]
                   elif $chunk_row[6] == true then
                     ["Entity row is flagged Is_Binary — content was never stored, cannot validate."]
                   else
                     ($chunk_row[2] | try (fromjson) as $edoc | (
                        (if $edoc.Format_Version == "104" then [] else ["Entity Format_Version must be \"104\"."] end)
                        + (if $edoc.Records_Type == [$entity_name] then [] else ["Entity Records_Type must be exactly [\"\($entity_name)\"]."] end)
                        + (if ($edoc | has("Parent_Hierarchy")) then [] else ["Entity is missing mandatory \"Parent_Hierarchy\" key."] end)
                     ) catch ["Entity file content is not valid JSON."])
                   end)
              )
            }
            | . + {"valid": (.errors | length == 0)}
          ],
          "errors": (
            (if $fmt_ok then [] else ["Manifest Format_Version must be \"104a\"."] end)
            + (if $rt_ok then [] else ["Manifest Records_Type must be exactly [\"mfdb\"]."] end)
          ),
          "warnings": []
        }
        | . + {"valid": ((.errors | length == 0) and (.entities | all(.valid)))}
        end'
}

# Export functions
export -f mfdb_validator_validate_archive
export -f mfdb_validator_validate_manifest
export -f mfdb_validator_reset_state
export -f mfdb_validator_has_errors
export -f mfdb_validator_get_errors
export -f mfdb_validator_check_dependencies
export -f mfdb_validator_is_mfdb132_package
export -f mfdb_validator_validate_mfdb132_package
export -f mfdb_validator_detect_mfdb_in_chunk


# ==========================================================================
# SECTION 6 — MFDB CORE
# Sources: mfdb_core v2.2.0
# ==========================================================================

# Library:        lib_bejson_Core_mfdb_core.sh
# Family:         Core
# Description:    Multi-file database orchestrator managing manifests and entity synchronization.
# Version:        2.2.0
# Date:           2026-07-31
# Author:         Elton Boehnen
# Contact:        boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton
# Format_Creator: Elton Boehnen
# RELATIONAL_ID:  4b9f1c73-8d2e-4a6b-b5f0-3c7e2a1d9b48
#
# FEATURE (2026-07-31): Meta-GUID debug entity system — full Bash port.
# mfdb_core_enable_debug, mfdb_core_disable_debug, mfdb_core_get_debug_log,
# mfdb_core_get_failed_ops, mfdb_core_clear_debug_log, mfdb_core_debug_summary,
# mfdb_core_detect_schema_drift. Internal _mfdb_meta_log direct writer gated
# by Debug_Mode manifest header — zero overhead when off.
#
# FEATURE (2026-07-29): Network_Role parameter added to mfdb_core_create_database
# (arg $7, default "Standalone"). Federation functions added:
# mfdb_federation_push_config, mfdb_federation_poll_dropzone,
# mfdb_federation_distill_logs, mfdb_core_create_connected_slave_entity.

# NOTE: set -o nounset intentionally omitted — library files must not modify
# global shell options; doing so breaks host scripts that source this file. (SH3)
set -o pipefail

# Source dependencies if not already loaded.
_MFDB_CORE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"



#-------------------------------------------------------------------------------
# Error codes (50–79)
#-------------------------------------------------------------------------------

# Error codes sourced from lib_bejson_Core_bejson_errors.sh (via bejson_core.sh chain).
# Local guards remain as fallback for scripts that source mfdb_core.sh directly.
[[ -v E_MFDB_CORE_MANIFEST_NOT_FOUND ]] || readonly E_MFDB_CORE_MANIFEST_NOT_FOUND=50
[[ -v E_MFDB_CORE_ENTITY_NOT_FOUND   ]] || readonly E_MFDB_CORE_ENTITY_NOT_FOUND=51
[[ -v E_MFDB_CORE_WRITE_FAILED       ]] || readonly E_MFDB_CORE_WRITE_FAILED=52
[[ -v E_MFDB_CORE_LOCK_FAILED        ]] || readonly E_MFDB_CORE_LOCK_FAILED=53
[[ -v E_MFDB_CORE_INVALID_OPERATION  ]] || readonly E_MFDB_CORE_INVALID_OPERATION=54
[[ -v E_MFDB_CORE_INDEX_OUT_OF_BOUNDS ]] || readonly E_MFDB_CORE_INDEX_OUT_OF_BOUNDS=55
[[ -v E_MFDB_CORE_JOIN_FAILED         ]] || readonly E_MFDB_CORE_JOIN_FAILED=56
[[ -v E_MFDB_CORE_DUPLICATE_ENTITY_NAME ]] || readonly E_MFDB_CORE_DUPLICATE_ENTITY_NAME=57
[[ -v E_MFDB_CORE_RECORD_COUNT_SYNC_FAILED ]] || readonly E_MFDB_CORE_RECORD_COUNT_SYNC_FAILED=58
[[ -v E_MFDB_CORE_NULL_MANIFEST       ]] || readonly E_MFDB_CORE_NULL_MANIFEST=59
[[ -v E_MFDB_CORE_ENTITY_NOT_IN_MANIFEST ]] || readonly E_MFDB_CORE_ENTITY_NOT_IN_MANIFEST=60
[[ -v E_MFDB_CORE_ARCHIVE_ERROR      ]] || readonly E_MFDB_CORE_ARCHIVE_ERROR=70
[[ -v E_MFDB_CORE_MOUNT_CONFLICT     ]] || readonly E_MFDB_CORE_MOUNT_CONFLICT=71
[[ -v E_MFDB_CORE_CREATE_FAILED      ]] || readonly E_MFDB_CORE_CREATE_FAILED=72

#-------------------------------------------------------------------------------
# MFDBArchive (v1.2 Feature)
#-------------------------------------------------------------------------------

# mfdb_archive_mount <archive_path> <target_dir> [force]
# Extracts archive to workspace and creates session lock.
mfdb_archive_mount() {
    local archive_path="$1"
    local target_dir="$2"
    local force="${3:-false}"

    if [[ ! -f "$archive_path" ]]; then
        echo "ERROR: Archive not found: $archive_path" >&2
        return $E_MFDB_CORE_ARCHIVE_ERROR
    fi

    local lock_file="$target_dir/.mfdb_lock"
    if [[ -f "$lock_file" && "$force" != "true" ]]; then
        local old_pid
        old_pid=$(jq -r '.pid' "$lock_file")
        if kill -0 "$old_pid" 2>/dev/null; then
            echo "ERROR: Workspace $target_dir is locked by active PID $old_pid" >&2
            return $E_MFDB_CORE_MOUNT_CONFLICT
        fi
    fi

    mkdir -p "$target_dir"
    unzip -q -o "$archive_path" -d "$target_dir" || {
        echo "ERROR: Extraction failed for $archive_path" >&2
        return $E_MFDB_CORE_ARCHIVE_ERROR
    }

    if [[ ! -f "$target_dir/104a.mfdb.bejson" ]]; then
        echo "ERROR: Invalid MFDB Archive: manifest missing" >&2
        rm -rf "$target_dir"
        return $E_MFDB_CORE_ARCHIVE_ERROR
    fi

    local hash
    hash=$(sha256sum "$archive_path" | awk '{print $1}')
    
    jq -n \
        --arg pid "$$" \
        --arg path "$(realpath "$archive_path")" \
        --arg hash "$hash" \
        --arg time "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
        '{pid: $pid|tonumber, archive_path: $path, original_hash: $hash, mounted_at: $time}' \
        > "$lock_file"

    echo "$(realpath "$target_dir/104a.mfdb.bejson")"
}

# mfdb_archive_commit <mount_dir> [archive_path]
# Repacks workspace into .mfdb.zip atomically.
mfdb_archive_commit() {
    local mount_dir="$1"
    local archive_path="${2:-}"
    local lock_file="$mount_dir/.mfdb_lock"

    if [[ ! -f "$lock_file" ]]; then
        echo "ERROR: No active mount session in $mount_dir" >&2
        return $E_MFDB_CORE_INVALID_OPERATION
    fi

    local dest
    if [[ -n "$archive_path" ]]; then
        dest="$archive_path"
    else
        dest=$(jq -r '.archive_path' "$lock_file")
    fi

    local tmp_zip
    tmp_zip="${TMPDIR:-/tmp}/mfdb_commit_$$.zip"
    rm -f "$tmp_zip"

    (cd "$mount_dir" && zip -r -q "$tmp_zip" . -x ".mfdb_lock") || {
        rm -f "$tmp_zip"
        echo "ERROR: Repack failed for $mount_dir" >&2
        return $E_MFDB_CORE_WRITE_FAILED
    }

    mv "$tmp_zip" "$dest" || {
        rm -f "$tmp_zip"
        echo "ERROR: Atomic swap failed for $dest" >&2
        return $E_MFDB_CORE_WRITE_FAILED
    }

    local new_hash
    new_hash=$(sha256sum "$dest" | awk '{print $1}')
    local tmp_lock
    tmp_lock=$(mktemp)
    jq --arg h "$new_hash" '.original_hash = $h' "$lock_file" > "$tmp_lock" && mv "$tmp_lock" "$lock_file"

    echo "$(realpath "$dest")"
}

# mfdb_archive_unmount <mount_dir> [cleanup]
mfdb_archive_unmount() {
    local mount_dir="$1"
    local cleanup="${2:-true}"
    local lock_file="$mount_dir/.mfdb_lock"

    [[ -f "$lock_file" ]] && rm -f "$lock_file"
    [[ "$cleanup" == "true" && -d "$mount_dir" ]] && rm -rf "$mount_dir"
}

#-------------------------------------------------------------------------------
# Discovery
#-------------------------------------------------------------------------------

# mfdb_core_discover <file_path>
# Prints: 'manifest', 'entity', 'archive', or 'standalone'
mfdb_core_discover() {
    local file_path="$1"

    if [[ ! -f "$file_path" ]]; then
        echo "ERROR: File not found: $file_path" >&2
        return $E_MFDB_CORE_MANIFEST_NOT_FOUND
    fi

    if [[ "$file_path" == *".mfdb.zip" ]]; then
        echo "archive"
        return 0
    fi

    local version filename
    version="$(jq -r '.Format_Version // empty' "$file_path" 2>/dev/null)"
    filename="$(basename "$file_path")"

    if [[ "$version" == "104a" && "$filename" == *".mfdb.bejson" ]]; then
        echo "manifest"
    elif [[ "$version" == "104" ]]; then
        local ph
        ph="$(jq -r '.Parent_Hierarchy // empty' "$file_path" 2>/dev/null)"
        if [[ -n "$ph" ]]; then
            echo "entity"
        else
            echo "standalone"
        fi
    else
        echo "standalone"
    fi
}

#-------------------------------------------------------------------------------
# Internal helpers
#-------------------------------------------------------------------------------

__mfdb_core_resolve() {
    local manifest_path="$1"
    local file_path_rel="$2"
    local manifest_dir
    manifest_dir="$(cd "$(dirname "$manifest_path")" && pwd)"
    realpath -m "$manifest_dir/$file_path_rel" 2>/dev/null || echo "$manifest_dir/$file_path_rel"
}

__mfdb_field_index() {
    local file_path="$1"
    local field_name="$2"
    local doc
    doc=$(cat "$file_path")
    bejson_core_get_field_index "$doc" "$field_name"
}

__mfdb_core_en_idx() {
    __mfdb_field_index "$1" "entity_name"
}

__mfdb_core_fp_idx() {
    __mfdb_field_index "$1" "file_path"
}

__mfdb_core_get_file_path() {
    local manifest_path="$1"
    local entity_name="$2"
    local en_idx fp_idx
    en_idx="$(__mfdb_core_en_idx "$manifest_path")"
    fp_idx="$(__mfdb_core_fp_idx "$manifest_path")"
    jq -r --argjson ei "$en_idx" --argjson fi "$fp_idx" --arg en "$entity_name" \
        '.Values[] | select(.[$ei] == $en) | .[$fi] // empty' \
        "$manifest_path" 2>/dev/null | head -n1
}

#-------------------------------------------------------------------------------
# Dependency check
#-------------------------------------------------------------------------------

mfdb_core_check_dependencies() {
    mfdb_validator_check_dependencies || return $?
    if ! declare -f bejson_core_atomic_write > /dev/null 2>&1; then
        echo "ERROR: lib_bejson_Core_bejson_core.sh must be sourced before lib_bejson_Core_mfdb_core.sh" >&2
        return 1
    fi
    for cmd in unzip zip sha256sum; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            echo "ERROR: Required command '$cmd' not found" >&2
            return 1
        fi
    done
    return 0
}

#-------------------------------------------------------------------------------
# Read operations
#-------------------------------------------------------------------------------

mfdb_core_load_manifest() {
    local manifest_path="$1"
    if ! mfdb_validator_validate_manifest "$manifest_path"; then
        echo "ERROR: Manifest validation failed: $manifest_path" >&2
        return $E_MFDB_CORE_MANIFEST_NOT_FOUND
    fi
    jq -r '.Values[] | @tsv' "$manifest_path" 2>/dev/null
}

mfdb_core_list_entities() {
    local manifest_path="$1"
    local en_idx
    en_idx="$(__mfdb_core_en_idx "$manifest_path")"
    jq -r --argjson ei "$en_idx" '.Values[] | .[$ei] // empty' "$manifest_path" 2>/dev/null
}

mfdb_core_load_entity() {
    local manifest_path="$1"
    local entity_name="$2"
    local file_path_rel
    file_path_rel="$(__mfdb_core_get_file_path "$manifest_path" "$entity_name")"
    if [[ -z "$file_path_rel" ]]; then
        echo "ERROR: Entity '$entity_name' not found in manifest" >&2
        return $E_MFDB_CORE_ENTITY_NOT_FOUND
    fi
    local resolved
    resolved="$(__mfdb_core_resolve "$manifest_path" "$file_path_rel")"
    if [[ ! -f "$resolved" ]]; then
        echo "ERROR: Entity file not found: $resolved" >&2
        return $E_MFDB_CORE_ENTITY_NOT_FOUND
    fi
    jq -r '[.Fields[].name] | @tsv' "$resolved" 2>/dev/null
    jq -r '.Values[] | @tsv' "$resolved" 2>/dev/null
}

mfdb_core_get_entity_path() {
    local manifest_path="$1"
    local entity_name="$2"
    local file_path_rel
    file_path_rel="$(__mfdb_core_get_file_path "$manifest_path" "$entity_name")"
    if [[ -z "$file_path_rel" ]]; then
        echo "ERROR: Entity '$entity_name' not found in manifest" >&2
        return $E_MFDB_CORE_ENTITY_NOT_FOUND
    fi
    __mfdb_core_resolve "$manifest_path" "$file_path_rel"
}

mfdb_core_get_stats() {
    local manifest_path="$1"
    local db_name schema_version
    db_name="$(jq -r '.DB_Name // "N/A"' "$manifest_path" 2>/dev/null)"
    schema_version="$(jq -r '.Schema_Version // "N/A"' "$manifest_path" 2>/dev/null)"
    echo "=== MFDB Stats ==="
    echo "DB Name        : $db_name"
    echo "Schema Version : $schema_version"
    echo "Manifest       : $manifest_path"
    echo ""
    local en_idx fp_idx
    en_idx="$(__mfdb_core_en_idx "$manifest_path")"
    fp_idx="$(__mfdb_core_fp_idx "$manifest_path")"
    local entity_count=0
    while IFS=$'\t' read -r entity_name file_path_rel; do
        entity_count=$((entity_count + 1))
        local resolved
        resolved="$(__mfdb_core_resolve "$manifest_path" "$file_path_rel")"
        local rec_count="?"
        if [[ -f "$resolved" ]]; then
            rec_count="$(jq -r '.Values | length' "$resolved" 2>/dev/null)"
        fi
        printf "  %-24s  %-36s  records: %s\n" "$entity_name" "$file_path_rel" "$rec_count"
    done < <(jq -r --argjson ei "$en_idx" --argjson fi "$fp_idx" \
        '.Values[] | [.[$ei] // "null", .[$fi] // "null"] | @tsv' \
        "$manifest_path" 2>/dev/null)
    echo ""
    echo "Total entities : $entity_count"
}

#-------------------------------------------------------------------------------
# Write operations
#-------------------------------------------------------------------------------

mfdb_core_add_entity_record() {
    local manifest_path="$1"
    local entity_name="$2"
    local json_values_array="$3"
    local file_path_rel
    file_path_rel="$(__mfdb_core_get_file_path "$manifest_path" "$entity_name")"
    if [[ -z "$file_path_rel" ]]; then
        echo "ERROR: Entity '$entity_name' not found in manifest" >&2
        return $E_MFDB_CORE_ENTITY_NOT_FOUND
    fi
    local resolved
    resolved="$(__mfdb_core_resolve "$manifest_path" "$file_path_rel")"
    if [[ ! -f "$resolved" ]]; then
        echo "ERROR: Entity file not found: $resolved" >&2
        return $E_MFDB_CORE_ENTITY_NOT_FOUND
    fi
    if ! echo "$json_values_array" | jq -e 'if type == "array" then true else error end' > /dev/null 2>&1; then
        echo "ERROR: json_values_array must be a JSON array string" >&2
        return $E_MFDB_CORE_INVALID_OPERATION
    fi
    local tmp_file
    tmp_file="$(mktemp "${resolved}.tmp.XXXXXX")"
    if ! jq --argjson row "$json_values_array" '.Values += [$row]' "$resolved" > "$tmp_file" 2>/dev/null; then
        rm -f "$tmp_file"
        echo "ERROR: Failed to append record to $resolved" >&2
        return $E_MFDB_CORE_WRITE_FAILED
    fi
    mv "$tmp_file" "$resolved"
    mfdb_core_sync_manifest_count "$manifest_path" "$entity_name"
}

mfdb_core_remove_entity_record() {
    local manifest_path="$1"
    local entity_name="$2"
    local record_index="$3"
    local file_path_rel
    file_path_rel="$(__mfdb_core_get_file_path "$manifest_path" "$entity_name")"
    if [[ -z "$file_path_rel" ]]; then
        echo "ERROR: Entity '$entity_name' not found in manifest" >&2
        return $E_MFDB_CORE_ENTITY_NOT_FOUND
    fi
    local resolved
    resolved="$(__mfdb_core_resolve "$manifest_path" "$file_path_rel")"
    if [[ ! -f "$resolved" ]]; then
        echo "ERROR: Entity file not found: $resolved" >&2
        return $E_MFDB_CORE_ENTITY_NOT_FOUND
    fi
    local rec_count
    rec_count="$(jq -r '.Values | length' "$resolved" 2>/dev/null)"
    if [[ "$record_index" -lt 0 || "$record_index" -ge "$rec_count" ]]; then
        echo "ERROR: Record index $record_index is out of bounds (count: $rec_count)" >&2
        return $E_MFDB_CORE_INDEX_OUT_OF_BOUNDS
    fi
    local tmp_file
    tmp_file="$(mktemp "${resolved}.tmp.XXXXXX")"
    if ! jq --argjson ri "$record_index" 'del(.Values[$ri])' "$resolved" > "$tmp_file" 2>/dev/null; then
        rm -f "$tmp_file"
        echo "ERROR: Failed to remove record $record_index from $resolved" >&2
        return $E_MFDB_CORE_WRITE_FAILED
    fi
    mv "$tmp_file" "$resolved"
    mfdb_core_sync_manifest_count "$manifest_path" "$entity_name"
}

#-------------------------------------------------------------------------------
# Manifest sync
#-------------------------------------------------------------------------------

mfdb_core_sync_manifest_count() {
    local manifest_path="$1"
    local entity_name="$2"
    local file_path_rel
    file_path_rel="$(__mfdb_core_get_file_path "$manifest_path" "$entity_name")"
    [[ -z "$file_path_rel" ]] && return $E_MFDB_CORE_ENTITY_NOT_FOUND
    local resolved
    resolved="$(__mfdb_core_resolve "$manifest_path" "$file_path_rel")"
    [[ ! -f "$resolved" ]] && return $E_MFDB_CORE_ENTITY_NOT_FOUND
    local actual_count
    actual_count="$(jq -r '.Values | length' "$resolved" 2>/dev/null)"
    local en_idx rc_idx
    en_idx="$(__mfdb_core_en_idx "$manifest_path")"
    rc_idx="$(__mfdb_field_index "$manifest_path" "record_count")"
    [[ "$rc_idx" == "-1" ]] && return 0
    local tmp_file
    tmp_file="$(mktemp "${manifest_path}.tmp.XXXXXX")"
    if ! jq --argjson ei "$en_idx" --argjson ri "$rc_idx" \
            --arg en "$entity_name" --argjson count "$actual_count" \
            '(.Values[] | select(.[$ei] == $en) | .[$ri]) = $count' \
            "$manifest_path" > "$tmp_file" 2>/dev/null; then
        rm -f "$tmp_file"
        return $E_MFDB_CORE_WRITE_FAILED
    fi
    mv "$tmp_file" "$manifest_path"
    echo "$actual_count"
}

mfdb_core_sync_all_counts() {
    local manifest_path="$1"
    while IFS= read -r entity_name; do
        local count
        count="$(mfdb_core_sync_manifest_count "$manifest_path" "$entity_name")"
        printf "%-24s  %s records\n" "$entity_name" "$count"
    done < <(mfdb_core_list_entities "$manifest_path")
}

#-------------------------------------------------------------------------------
# Database creation
#-------------------------------------------------------------------------------

mfdb_core_create_entity_file() {
    local manifest_path="$1"
    local entity_name="$2"
    local fields_json="$3"
    local description="${4:-}"
    local primary_key="${5:-}"
    local schema_version="${6:-1.0}"
    local file_path_rel="${7:-}"
    if [[ -z "$file_path_rel" ]]; then
        file_path_rel="data/$(echo "$entity_name" | tr '[:upper:]' '[:lower:]').bejson"
    fi
    local manifest_dir resolved entity_dir rel_to_manifest
    manifest_dir="$(cd "$(dirname "$manifest_path")" && pwd)"
    resolved="$(realpath -m "$manifest_dir/$file_path_rel" 2>/dev/null || echo "$manifest_dir/$file_path_rel")"
    entity_dir="$(dirname "$resolved")"
    mkdir -p "$entity_dir"
    rel_to_manifest="$(realpath --relative-to="$entity_dir" "$manifest_path" 2>/dev/null || echo "../$(basename "$manifest_path")")"
    local tmp_entity
    tmp_entity="$(mktemp "${resolved}.tmp.XXXXXX")"
    jq -n \
        --arg en "$entity_name" \
        --arg ph "$rel_to_manifest" \
        --argjson fields "$fields_json" \
        '{
            "Format":           "BEJSON",
            "Format_Version":   "104",
            "Format_Creator":   "Elton Boehnen",
            "Parent_Hierarchy": $ph,
            "Records_Type":     [$en],
            "Fields":           $fields,
            "Values":           []
        }' > "$tmp_entity" 2>/dev/null && mv "$tmp_entity" "$resolved"
    local en_idx fp_idx
    en_idx="$(__mfdb_core_en_idx "$manifest_path")"
    fp_idx="$(__mfdb_core_fp_idx "$manifest_path")"
    # Duplicate-entity guard (parity with PY/TS/JS registerEntity — H-02)
    if jq -e --argjson idx "$en_idx" --arg en "$entity_name" \
        '.Values | any(.[$idx] == $en)' "$manifest_path" >/dev/null 2>&1; then
        echo "ERROR: Entity '$entity_name' is already registered (E_MFDB_CORE_DUPLICATE_ENTITY_NAME)" >&2
        return $E_MFDB_CORE_DUPLICATE_ENTITY_NAME
    fi
    local new_row_json
    new_row_json="$(jq -r \
        --arg en "$entity_name" \
        --arg fp "$file_path_rel" \
        --arg desc "${description:-null}" \
        --arg pk "${primary_key:-null}" \
        --arg sv "$schema_version" \
        '[.Fields[].name] | map(
            if . == "entity_name"    then $en
            elif . == "file_path"    then $fp
            elif . == "description"  then (if $desc == "null" then null else $desc end)
            elif . == "record_count" then 0
            elif . == "schema_version" then $sv
            elif . == "primary_key"  then (if $pk == "null" then null else $pk end)
            else null
            end
        )' "$manifest_path" 2>/dev/null)"
    local tmp_manifest
    tmp_manifest="$(mktemp "${manifest_path}.tmp.XXXXXX")"
    jq --argjson row "$new_row_json" '.Values += [$row]' "$manifest_path" > "$tmp_manifest" && mv "$tmp_manifest" "$manifest_path"
    echo "$resolved"
}

mfdb_core_create_database() {
    local root_dir="$1"
    local db_name="$2"
    local db_description="${3:-}"
    local entities_json="$4"
    local schema_version="${5:-1.0.0}"
    local author="${6:-Elton Boehnen}"
    local network_role="${7:-Standalone}"   # "Master" | "Slave" | "Standalone"
    mkdir -p "$root_dir"
    local manifest_path="$root_dir/104a.mfdb.bejson"
    local created_at
    created_at="$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ")"
    # Build manifest Values from entities_json.
    local manifest_values_json
    manifest_values_json="$(echo "$entities_json" | jq -c \
        '[.[] | [
            .name,
            (.file_path // ("data/" + (.name | ascii_downcase) + ".bejson")),
            (.description // null),
            0,
            (.schema_version // "1.0"),
            (.primary_key // null)
        ]]')"

    local tmp_manifest
    tmp_manifest="$(mktemp "${manifest_path}.tmp.XXXXXX")"

    if ! jq -n \
        --arg db_name "$db_name" \
        --arg db_desc "$db_description" \
        --arg sv "$schema_version" \
        --arg author "$author" \
        --arg created_at "$created_at" \
        --arg network_role "$network_role" \
        --argjson values "$manifest_values_json" \
        '{
            "Format":          "BEJSON",
            "Format_Version":  "104a",
            "Format_Creator":  "Elton Boehnen",
            "MFDB_Version":    "1.31",
            "Network_Role":    $network_role,
            "DB_Name":         $db_name,
            "DB_Description":  $db_desc,
            "Schema_Version":  $sv,
            "Author":          $author,
            "Created_At":      $created_at,
            "Records_Type":    ["mfdb"],
            "Fields": [
                {"name":"entity_name",    "type":"string"},
                {"name":"file_path",      "type":"string"},
                {"name":"description",    "type":"string"},
                {"name":"record_count",   "type":"integer"},
                {"name":"schema_version", "type":"string"},
                {"name":"primary_key",    "type":"string"}
            ],
            "Values": $values
        }' > "$tmp_manifest"; then
        rm -f "$tmp_manifest"
        echo "ERROR: Failed to generate manifest JSON" >&2
        return $E_MFDB_CORE_CREATE_FAILED
    fi

    mv "$tmp_manifest" "$manifest_path"

    local entity_count
    entity_count="$(echo "$entities_json" | jq -r 'length')"
    for (( i=0; i<entity_count; i++ )); do
        local ename fp_rel efields
        ename="$(echo "$entities_json" | jq -r ".[$i].name" 2>/dev/null)"
        fp_rel="$(echo "$entities_json" | jq -r ".[$i].file_path // (\"data/\" + (.[$i].name | ascii_downcase) + \".bejson\")" 2>/dev/null)"
        efields="$(echo "$entities_json" | jq -c ".[$i].fields" 2>/dev/null)"
        local resolved entity_dir rel_to_manifest
        resolved="$(realpath -m "$root_dir/$fp_rel" 2>/dev/null || echo "$root_dir/$fp_rel")"
        entity_dir="$(dirname "$resolved")"
        mkdir -p "$entity_dir"
        rel_to_manifest="$(realpath --relative-to="$entity_dir" "$manifest_path" 2>/dev/null || echo "../$(basename "$manifest_path")")"
        local tmp_entity
        tmp_entity="$(mktemp "${resolved}.tmp.XXXXXX")"
        jq -n \
            --arg en "$ename" \
            --arg ph "$rel_to_manifest" \
            --argjson fields "$efields" \
            '{
                "Format":           "BEJSON",
                "Format_Version":   "104",
                "Format_Creator":   "Elton Boehnen",
                "Parent_Hierarchy": $ph,
                "Records_Type":     [$en],
                "Fields":           $fields,
                "Values":           []
            }' > "$tmp_entity" 2>/dev/null && mv "$tmp_entity" "$resolved"
    done
    echo "$manifest_path"
}

# Export functions
export -f mfdb_archive_mount
export -f mfdb_archive_commit
export -f mfdb_archive_unmount
export -f mfdb_core_check_dependencies
export -f mfdb_core_discover
export -f mfdb_core_load_manifest
export -f mfdb_core_list_entities
export -f mfdb_core_load_entity
export -f mfdb_core_get_entity_path
export -f mfdb_core_get_stats
export -f mfdb_core_add_entity_record
export -f mfdb_core_remove_entity_record
export -f mfdb_core_sync_manifest_count
export -f mfdb_core_sync_all_counts
export -f mfdb_core_create_entity_file
export -f mfdb_core_create_database

# ── Federated Master / Slave node system ───────────────────────────────────────
# Network_Role ("Master"|"Slave"|"Standalone") is now emitted on
# mfdb_core_create_database. This block wires the full runtime federation
# protocol: ConnectedSlave entity creator, Master→Slave atomic push,
# Slave dropzone poller, and Slave→Master log distillation.

# mfdb_core_create_connected_slave_entity <manifest_path>
# Creates the ConnectedSlave entity file and registers it in the manifest.
# Fails if Network_Role != "Master".
mfdb_core_create_connected_slave_entity() {
    local manifest_path="$1"
    local role
    role=$(jq -r '.Network_Role // ""' "$manifest_path" 2>/dev/null)
    if [[ "$role" != "Master" ]]; then
        echo "[MFDB_FEDERATION] ERROR: ConnectedSlave may only be created on a Master node. Got: '$role'" >&2
        return 1
    fi

    local fields_json='[
        {"name":"slave_id",           "type":"string"},
        {"name":"label",              "type":"string"},
        {"name":"url",                "type":"string"},
        {"name":"role",               "type":"string"},
        {"name":"status",             "type":"string"},
        {"name":"supported_entities", "type":"array"}
    ]'
    mfdb_core_create_entity_file \
        "$manifest_path" "ConnectedSlave" "$fields_json" \
        "Registry of Slave nodes connected to this Master." "slave_id"
}
export -f mfdb_core_create_connected_slave_entity

# mfdb_federation_push_config <config_json_string> <slave_target_path>
# Master → Slave atomic drop-zone push. Writes config via same-dir temp + mv.
# Returns 0 on success, 1 on error.
mfdb_federation_push_config() {
    local config_json="$1"
    local slave_target_path="$2"
    local dest_dir
    dest_dir="$(dirname "$slave_target_path")"
    mkdir -p "$dest_dir"
    local temp_path="$slave_target_path.tmp.$$"
    if echo "$config_json" > "$temp_path" && mv "$temp_path" "$slave_target_path"; then
        return 0
    else
        rm -f "$temp_path"
        echo "[MFDB_FEDERATION] ERROR: push_config failed for $slave_target_path" >&2
        return 1
    fi
}
export -f mfdb_federation_push_config

# mfdb_federation_poll_dropzone <dropzone_dir> <handler_function> [poll_interval_sec=2] [timeout_sec=60]
# Slave: polls dropzone_dir for incoming .bejson files from Master.
# Each file is passed to handler_function <file_path> then removed.
# handler_function must be exported with export -f.
# Returns count of configs processed on stdout.
mfdb_federation_poll_dropzone() {
    local dropzone_dir="$1"
    local handler_fn="$2"
    local poll_interval="${3:-2}"
    local timeout="${4:-60}"
    mkdir -p "$dropzone_dir"

    local processed=0
    local deadline=$(( $(date +%s) + timeout ))

    while [[ "$(date +%s)" -lt "$deadline" ]]; do
        for fpath in "$dropzone_dir"/*.bejson; do
            [[ -f "$fpath" ]] || continue
            if "$handler_fn" "$fpath"; then
                rm -f "$fpath"
                (( processed++ )) || true
            else
                echo "[MFDB_FEDERATION] poll_dropzone: handler failed for $fpath" >&2
            fi
        done
        sleep "$poll_interval"
    done

    echo "$processed"
}
export -f mfdb_federation_poll_dropzone

# mfdb_federation_distill_logs <slave_manifest_path> <entity_name> <master_poll_dir> [max_rows=100]
# Slave → Master one-way log push. Overflow rows pushed as distilled summary,
# local entity truncated to max_rows. Returns 0 on success, 1 on error.
mfdb_federation_distill_logs() {
    local slave_manifest="$1"
    local entity_name="$2"
    local master_poll_dir="$3"
    local max_rows="${4:-100}"

    # Resolve entity file path
    local entity_path
    entity_path=$(mfdb_core_get_entity_path "$slave_manifest" "$entity_name" 2>/dev/null)
    [[ -z "$entity_path" || ! -f "$entity_path" ]] && {
        echo "[MFDB_FEDERATION] ERROR: entity '$entity_name' not found." >&2; return 1
    }

    local total_rows
    total_rows=$(jq '.Values | length' "$entity_path" 2>/dev/null)
    [[ "$total_rows" -le "$max_rows" ]] && return 0  # Nothing to distill

    # Build overflow and kept arrays
    local overflow_json kept_json
    overflow_json=$(jq --argjson mr "$max_rows" '.Values[0:(.Values|length)-$mr]' "$entity_path")
    kept_json=$(jq --argjson mr "$max_rows" '.Values[(.Values|length)-$mr:]' "$entity_path")

    # Push distilled summary to Master poll dir
    mkdir -p "$master_poll_dir"
    local ts dest summary_json fields_json
    ts=$(date -u +"%Y%m%dT%H%M%SZ")
    dest="$master_poll_dir/distilled_${entity_name}_${ts}.bejson"
    fields_json=$(jq -c '.Fields' "$entity_path")

    summary_json=$(jq -n \
        --arg src "$entity_name" \
        --arg ts "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
        --argjson fields "$fields_json" \
        --argjson values "$overflow_json" \
        '{
            "Format":"BEJSON","Format_Version":"104a","Format_Creator":"Elton Boehnen",
            "Distill_Source":$src,"Distill_Timestamp":$ts,
            "Records_Type":["DistilledLog"],"Fields":$fields,"Values":$values
        }')

    mfdb_federation_push_config "$summary_json" "$dest" || return 1

    # Truncate local entity
    local tmp_entity
    tmp_entity="$(mktemp "${entity_path}.tmp.XXXXXX")"
    jq --argjson kept "$kept_json" '.Values = $kept' "$entity_path" > "$tmp_entity" \
        && mv "$tmp_entity" "$entity_path" \
        || { rm -f "$tmp_entity"; return 1; }

    # Update manifest record count
    mfdb_core_sync_manifest_count "$slave_manifest" "$entity_name"
    return 0
}
export -f mfdb_federation_distill_logs

# ── Meta-GUID Debug Entity System (Bash) ───────────────────────────────────────
# All functions gate on Debug_Mode manifest header. _mfdb_meta_log is a direct
# jq-based writer — bypasses mfdb_core_add_entity_record to prevent recursion.
# Requires jq >= 1.6.

_mfdb_debug_is_enabled() {
    local manifest_path="$1"
    local mode
    mode=$(jq -r '.Debug_Mode // "false"' "$manifest_path" 2>/dev/null)
    [[ "${mode,,}" == "true" ]]
}

_mfdb_debug_reads_enabled() {
    local manifest_path="$1"
    local flag
    flag=$(jq -r '.Debug_Reads // "false"' "$manifest_path" 2>/dev/null)
    [[ "${flag,,}" == "true" ]]
}

_mfdb_debug_get_meta_name() {
    jq -r '.Debug_Meta_Entity // ""' "$1" 2>/dev/null
}

_mfdb_debug_get_entity_path() {
    local manifest_path="$1"
    local entity_name="$2"
    local rel_path
    rel_path=$(jq -r --arg e "$entity_name" \
        '[.Fields | to_entries | .[] | select(.value.name=="entity_name") | .key][0] as $ei |
         [.Fields | to_entries | .[] | select(.value.name=="file_path") | .key][0] as $fi |
         .Values[] | select(.[$ei]==$e) | .[$fi]' \
        "$manifest_path" 2>/dev/null | head -1)
    [[ -z "$rel_path" ]] && return 1
    echo "$(dirname "$(realpath "$manifest_path")")/$rel_path"
}

# _mfdb_meta_log <manifest> <operation> <target_entity> <field_name|-> <field_exists|-> <row_index|-> <success:0|1> <duration_ms> <notes> [reads_only:0|1]
_mfdb_meta_log() {
    local manifest_path="$1"
    local operation="$2"
    local target_entity="$3"
    local field_name="${4:--}"
    local field_exists="${5:--}"    # "true", "false", or "-" (null)
    local row_index="${6:--}"       # integer or "-" (null)
    local success="${7:-1}"         # 1=true 0=false
    local duration_ms="${8:-0}"
    local notes="${9:-}"
    local reads_only="${10:-0}"

    _mfdb_debug_is_enabled "$manifest_path" || return 0
    if [[ "$reads_only" -eq 1 ]]; then
        _mfdb_debug_reads_enabled "$manifest_path" || return 0
    fi

    local meta_name
    meta_name=$(_mfdb_debug_get_meta_name "$manifest_path")
    [[ -z "$meta_name" ]] && return 0

    local meta_path
    meta_path=$(_mfdb_debug_get_entity_path "$manifest_path" "$meta_name") || return 0

    local ts
    ts=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")

    # Build null-safe values for optional fields
    local jq_field_name jq_field_exists jq_row_index
    [[ "$field_name"   == "-" ]] && jq_field_name="null"   || jq_field_name="\"$field_name\""
    [[ "$field_exists" == "-" ]] && jq_field_exists="null" || jq_field_exists="$field_exists"
    [[ "$row_index"    == "-" ]] && jq_row_index="null"    || jq_row_index="$row_index"
    local jq_success
    [[ "$success" -eq 1 ]] && jq_success="true" || jq_success="false"

    local tmp
    tmp=$(mktemp "${meta_path}.tmp.XXXXXX")
    jq --argjson ts "\"$ts\"" \
       --argjson op "\"$operation\"" \
       --argjson te "\"$target_entity\"" \
       --argjson fn "$jq_field_name" \
       --argjson fe "$jq_field_exists" \
       --argjson ri "$jq_row_index" \
       --argjson sc "$jq_success" \
       --argjson dm "$duration_ms" \
       --argjson pid "$$" \
       --argjson nt "\"$notes\"" \
       '.Values += [[$ts,$op,$te,$fn,$fe,$ri,$sc,$dm,$pid,$nt]]' \
       "$meta_path" > "$tmp" && mv "$tmp" "$meta_path" || rm -f "$tmp"

    # Auto-trim
    local cap
    cap=$(jq -r '.Debug_Row_Cap // "500"' "$manifest_path" 2>/dev/null)
    local count
    count=$(jq '.Values | length' "$meta_path" 2>/dev/null)
    if [[ "$count" -gt "$cap" ]]; then
        local keep_from=$(( count - cap ))
        local tmp2
        tmp2=$(mktemp "${meta_path}.tmp.XXXXXX")
        jq --argjson kf "$keep_from" '.Values = .Values[$kf:]' "$meta_path" > "$tmp2" \
            && mv "$tmp2" "$meta_path" || rm -f "$tmp2"
    fi
}
export -f _mfdb_meta_log

_mfdb_debug_schema_snapshot() {
    local manifest_path="$1"
    local meta_name="$2"

    local entities_json
    entities_json=$(mfdb_core_list_entities "$manifest_path" 2>/dev/null)

    echo "$entities_json" | jq -r '.[]' 2>/dev/null | while IFS= read -r ename; do
        [[ -z "$ename" || "$ename" == "$meta_name" ]] && continue
        local entity_path
        entity_path=$(_mfdb_debug_get_entity_path "$manifest_path" "$ename") || continue
        [[ -f "$entity_path" ]] || continue
        local fields
        fields=$(jq -r '[.Fields[].name] | join(",")' "$entity_path" 2>/dev/null)
        local fc
        fc=$(jq '.Fields | length' "$entity_path" 2>/dev/null)
        _mfdb_meta_log "$manifest_path" "SCHEMA_SNAPSHOT" "$ename" \
            "$fields" "true" "-" 1 0 "field_count=$fc"
    done
}
export -f _mfdb_debug_schema_snapshot

# mfdb_core_enable_debug <manifest_path> [row_cap=500] [debug_reads=0]
# Creates meta-{uuid} entity, sets debug headers, logs initial SCHEMA_SNAPSHOT.
# Prints meta entity name. Returns 0 on success.
mfdb_core_enable_debug() {
    local manifest_path="$1"
    local row_cap="${2:-500}"
    local debug_reads="${3:-0}"
    local debug_reads_str="false"
    [[ "$debug_reads" -eq 1 ]] && debug_reads_str="true"

    local existing_meta
    existing_meta=$(_mfdb_debug_get_meta_name "$manifest_path")

    local meta_name
    if [[ -n "$existing_meta" ]]; then
        meta_name="$existing_meta"
    else
        meta_name="meta-$(cat /proc/sys/kernel/random/uuid 2>/dev/null || uuidgen 2>/dev/null || date +%s%N)"
    fi

    # Update manifest headers
    local tmp
    tmp=$(mktemp "${manifest_path}.tmp.XXXXXX")
    jq --arg mn "$meta_name" --arg rc "$row_cap" --arg dr "$debug_reads_str" \
        '.Debug_Mode="true" | .Debug_Meta_Entity=$mn | .Debug_Row_Cap=$rc | .Debug_Reads=$dr' \
        "$manifest_path" > "$tmp" && mv "$tmp" "$manifest_path" || { rm -f "$tmp"; return 1; }

    # Create meta entity file if it doesn't exist
    local manifest_dir
    manifest_dir="$(dirname "$(realpath "$manifest_path")")"
    local meta_fp_rel="data/${meta_name}.bejson"
    local meta_abs="$manifest_dir/$meta_fp_rel"

    if [[ ! -f "$meta_abs" ]]; then
        mkdir -p "$(dirname "$meta_abs")"
        local rel_to_manifest
        rel_to_manifest=$(realpath --relative-to="$(dirname "$meta_abs")" "$manifest_path")
        jq -n \
            --arg ph "$rel_to_manifest" \
            --arg rt "$meta_name" \
            '{
                "Format":"BEJSON","Format_Version":"104","Format_Creator":"Elton Boehnen",
                "Parent_Hierarchy":$ph,"Records_Type":[$rt],
                "Fields":[
                    {"name":"timestamp","type":"string"},
                    {"name":"operation","type":"string"},
                    {"name":"target_entity","type":"string"},
                    {"name":"field_name","type":"string"},
                    {"name":"field_exists","type":"boolean"},
                    {"name":"row_index","type":"integer"},
                    {"name":"success","type":"boolean"},
                    {"name":"duration_ms","type":"integer"},
                    {"name":"pid","type":"integer"},
                    {"name":"notes","type":"string"}
                ],
                "Values":[]
            }' > "$meta_abs"

        # Register entity in manifest
        local already
        already=$(jq -r --arg e "$meta_name" \
            '[.Fields | to_entries | .[] | select(.value.name=="entity_name") | .key][0] as $ei |
             .Values[] | select(.[$ei]==$e) | .[$ei]' \
            "$manifest_path" 2>/dev/null | head -1)
        if [[ -z "$already" ]]; then
            local tmp2
            tmp2=$(mktemp "${manifest_path}.tmp.XXXXXX")
            jq --arg mn "$meta_name" --arg fp "$meta_fp_rel" \
                '.Values += [[$mn,$fp,"Debug audit log (auto-generated)",0,"1.0",null]]' \
                "$manifest_path" > "$tmp2" && mv "$tmp2" "$manifest_path" || rm -f "$tmp2"
        fi
    fi

    _mfdb_debug_schema_snapshot "$manifest_path" "$meta_name"
    echo "$meta_name"
    return 0
}
export -f mfdb_core_enable_debug

# mfdb_core_disable_debug <manifest_path>
mfdb_core_disable_debug() {
    local tmp
    tmp=$(mktemp "${1}.tmp.XXXXXX")
    jq '.Debug_Mode="false"' "$1" > "$tmp" && mv "$tmp" "$1" || rm -f "$tmp"
}
export -f mfdb_core_disable_debug

# mfdb_core_get_debug_log <manifest_path>
# Outputs the meta entity Values array as a JSON array of objects.
mfdb_core_get_debug_log() {
    local manifest_path="$1"
    local meta_name
    meta_name=$(_mfdb_debug_get_meta_name "$manifest_path")
    [[ -z "$meta_name" ]] && echo "[]" && return 0
    local meta_path
    meta_path=$(_mfdb_debug_get_entity_path "$manifest_path" "$meta_name") || { echo "[]"; return 0; }
    [[ -f "$meta_path" ]] || { echo "[]"; return 0; }
    jq '[.Fields as $f | .Values[] |
         . as $row |
         reduce range($f | length) as $i ({};
           . + {($f[$i].name): $row[$i]})]' "$meta_path" 2>/dev/null || echo "[]"
}
export -f mfdb_core_get_debug_log

# mfdb_core_get_failed_ops <manifest_path>
# Outputs failed (success=false) rows sorted by timestamp.
mfdb_core_get_failed_ops() {
    mfdb_core_get_debug_log "$1" | \
        jq '[.[] | select(.success==false)] | sort_by(.timestamp)' 2>/dev/null || echo "[]"
}
export -f mfdb_core_get_failed_ops

# mfdb_core_clear_debug_log <manifest_path>
# Wipes all Values from meta entity. Prints rows deleted.
mfdb_core_clear_debug_log() {
    local manifest_path="$1"
    local meta_name
    meta_name=$(_mfdb_debug_get_meta_name "$manifest_path")
    [[ -z "$meta_name" ]] && echo "0" && return 0
    local meta_path
    meta_path=$(_mfdb_debug_get_entity_path "$manifest_path" "$meta_name") || { echo "0"; return 0; }
    local deleted
    deleted=$(jq '.Values | length' "$meta_path" 2>/dev/null || echo 0)
    local tmp
    tmp=$(mktemp "${meta_path}.tmp.XXXXXX")
    jq '.Values=[]' "$meta_path" > "$tmp" && mv "$tmp" "$meta_path" || rm -f "$tmp"
    mfdb_core_sync_manifest_count "$manifest_path" "$meta_name" 2>/dev/null
    echo "$deleted"
}
export -f mfdb_core_clear_debug_log

# mfdb_core_debug_summary <manifest_path>
# Outputs a JSON summary object with aggregated debug stats.
mfdb_core_debug_summary() {
    local manifest_path="$1"
    _mfdb_debug_is_enabled "$manifest_path" || { echo "{}"; return 0; }
    local log
    log=$(mfdb_core_get_debug_log "$manifest_path")
    echo "$log" | jq '
        if length == 0 then {total_ops:0}
        else
          . as $rows |
          ($rows | length) as $total |
          ($rows | map(select(.success==false)) | length) as $failed |
          ($rows | map(select(.field_exists==false)) | length) as $drift |
          ($rows | map(select(.operation=="READ")) | length) as $reads |
          ($rows | map(select(.operation|IN("ADD","REMOVE","UPDATE","UPDATE_BULK"))) | length) as $writes |
          ($rows | group_by(.operation) | map({key:.[0].operation,value:length}) | from_entries) as $by_type |
          ($rows | unique_by(.target_entity) | map(.target_entity) | sort) as $entities |
          ($rows | sort_by(-.duration_ms) | .[0:3] |
           map({op:.operation,entity:.target_entity,duration_ms:.duration_ms})) as $slowest |
          {
            total_ops:$total, unique_entities:$entities,
            failed_ops:$failed, schema_drift_hits:$drift,
            top_3_slowest:$slowest, reads_logged:$reads,
            writes_logged:$writes, ops_by_type:$by_type
          }
        end
    ' 2>/dev/null || echo "{}"
}
export -f mfdb_core_debug_summary

# mfdb_core_detect_schema_drift <manifest_path>
# Diffs live Fields[] against SCHEMA_SNAPSHOT baseline in the debug log.
# Outputs a JSON object keyed by entity_name.
mfdb_core_detect_schema_drift() {
    local manifest_path="$1"
    _mfdb_debug_is_enabled "$manifest_path" || { echo "{}"; return 0; }
    local log
    log=$(mfdb_core_get_debug_log "$manifest_path")

    # Extract most-recent SCHEMA_SNAPSHOT per entity
    local snapshots
    snapshots=$(echo "$log" | jq '
        [ .[] | select(.operation=="SCHEMA_SNAPSHOT" and .field_name!=null) ] |
        group_by(.target_entity) | map(last) |
        map({key:.target_entity, value:(.field_name|split(","))}) |
        from_entries
    ' 2>/dev/null)

    [[ -z "$snapshots" || "$snapshots" == "null" || "$snapshots" == "{}" ]] && { echo "{}"; return 0; }

    local manifest_dir
    manifest_dir="$(dirname "$(realpath "$manifest_path")")"

    # For each entity in snapshots, load live fields and diff
    echo "$snapshots" | jq -r 'keys[]' | while IFS= read -r ename; do
        local entity_path
        entity_path=$(_mfdb_debug_get_entity_path "$manifest_path" "$ename") 2>/dev/null || continue
        [[ -f "$entity_path" ]] || continue
        local live_fields snap_fields added removed drifted
        live_fields=$(jq '[.Fields[].name]' "$entity_path" 2>/dev/null)
        snap_fields=$(echo "$snapshots" | jq --arg e "$ename" '.[$e]')
        added=$(jq -n --argjson l "$live_fields" --argjson s "$snap_fields" \
            '[$l[] | select(. as $f | $s | index($f) | not)] | sort')
        removed=$(jq -n --argjson l "$live_fields" --argjson s "$snap_fields" \
            '[$s[] | select(. as $f | $l | index($f) | not)] | sort')
        drifted=$(jq -n --argjson a "$added" --argjson r "$removed" \
            '($a | length > 0) or ($r | length > 0)')
        printf '"%s":{"added_fields":%s,"removed_fields":%s,"drifted":%s}\n' \
            "$ename" "$added" "$removed" "$drifted"
    done | jq -s 'map(split(":") | {key:.[0][1:-1], value:(.[1:] | join(":") | fromjson)}) | from_entries' \
        2>/dev/null || echo "{}"
}
export -f mfdb_core_detect_schema_drift
