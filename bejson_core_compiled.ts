// Node.js declarations — no @types/node required
declare const require: (module: string) => any;
declare const process: any;
const fs:   any = typeof require !== 'undefined' ? require('fs')   : null;
const path: any = typeof require !== 'undefined' ? require('path') : null;
/**
 * Library:        bejson_core_compiled.ts
 * Family:         Compiled
 * Description:    Single-file compiled BEJSON+MFDB core for TypeScript.
 *                 No intra-package imports. E.PROP aliases expanded per-section.
 *                 Compile: tsc --noImplicitAny false --lib ES2020,dom
 * Version:         1.1.1
 * Library_Version: 226
 * Date:            2026-08-19
 * Schema_Name:     MFDB-132
 * Author:          Elton Boehnen
 * Contact:         boehnenelton2024@gmail.com | boehnenelton2024.pages.dev | github.com/boehnenelton
 * RELATIONAL_ID:   0ea81ced-e3cf-4371-ba62-ff9e16f91c70
 *
 * Merged sources:
 *   bejson_types          v2.4.0  (MFDB_CORE_CODES 57-60 sourced here, not mfdb_core.ts)
 *   bejson_field_map      v2.1.1
 *   bejson_core           v2.1.4
 *   bejson_validators     v2.0.2
 *   bejson_list_validator v1.2.0
 *   mfdb_validators       v2.1.0
 *   mfdb_core             v2.2.0
 *
 * NOTE: bejson_core is 2.1.4 here vs 2.0.5 in SH/PY, and mfdb_core is 2.2.0
 * here vs 2.3.0 in PY/JS — real per-language source split, not a
 * compiled-artifact bug. Documented, not force-unified.
 */
export const VERSION = '1.1.1';


// ==========================================================================
// SECTION 1 — TYPES
// Sources: bejson_types v2.4.0
// ==========================================================================

// ---------------------------------------------------------------------------
// Primitive and union types
// ---------------------------------------------------------------------------

export type BEJSONVersion = "104" | "104a" | "104db";

export type BEJSONFieldType =
  | "string"
  | "integer"
  | "number"
  | "boolean"
  | "array"
  | "object";

export type BEJSONPrimitiveType = "string" | "integer" | "number" | "boolean";

export type BEJSONValue =
  | string
  | number
  | boolean
  | null
  | unknown[]
  | Record<string, unknown>;

// ---------------------------------------------------------------------------
// Field and Document interfaces
// ---------------------------------------------------------------------------

export interface BEJSONField {
  name: string;
  type: BEJSONFieldType;
  
  Record_Type_Parent?: string;
}

export interface BEJSONDocument {
  Format: "BEJSON";
  Format_Version: "104" | "104a" | "104db";
  Format_Creator: "Elton Boehnen";
  Records_Type: string[];
  Fields: BEJSONField[];
  Values: BEJSONValue[][];
  
  Parent_Hierarchy?: string;
  [key: string]: unknown; // custom 104a headers + index access
}

// ---------------------------------------------------------------------------
// Validation result types
// ---------------------------------------------------------------------------

export interface ValidationError {
  code: number;
  message: string;
  field?: string;
  recordIndex?: number;
}

export interface ValidationWarning {
  code: number;
  message: string;
  field?: string;
  recordIndex?: number;
}

export interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
}

// ---------------------------------------------------------------------------
// MFDB-specific interfaces
// ---------------------------------------------------------------------------

export interface MFDBManifestRecord {
  entity_name: string;
  file_path: string;
  description?: string | null;
  record_count?: number | null;
  schema_version?: string | null;
  primary_key?: string | null;
}

export interface MFDBDatabaseMeta {
  mfdb_version: string;
  db_name: string;
  db_description?: string;
  schema_version?: string;
  author?: string;
  created_at?: string;
}

export type MFDBFileRole = "manifest" | "entity" | "standalone";

// ---------------------------------------------------------------------------
// Error classes
// ---------------------------------------------------------------------------

export class BEJSONValidationError extends Error {
  public readonly code: number;
  constructor(code: number, message: string) {
    super(message);
    this.name = "BEJSONValidationError";
    this.code = code;
  }
}

export class BEJSONCoreError extends Error {
  public readonly code: number;
  constructor(code: number, message: string) {
    super(message);
    this.name = "BEJSONCoreError";
    this.code = code;
  }
}

export class MFDBValidationError extends Error {
  public readonly code: number;
  constructor(code: number, message: string) {
    super(message);
    this.name = "MFDBValidationError";
    this.code = code;
  }
}

export class MFDBCoreError extends Error {
  public readonly code: number;
  constructor(code: number, message: string) {
    super(message);
    this.name = "MFDBCoreError";
    this.code = code;
  }
}

// ---------------------------------------------------------------------------
// Validation error code catalogue
// ---------------------------------------------------------------------------

export const BEJSON_VALIDATION_CODES = {
  
  INVALID_JSON: 1,
  
  MISSING_MANDATORY_KEY: 2,
  
  INVALID_FORMAT_VALUE: 3,
  
  INVALID_FORMAT_VERSION: 4,
  
  INVALID_RECORDS_TYPE: 5,
  
  INVALID_FIELDS: 6,
  
  INVALID_VALUES: 7,
  
  VALUE_TYPE_MISMATCH: 8,
  
  RECORD_LENGTH_MISMATCH: 9,
  
  RESERVED_KEY_COLLISION: 10,
  
  INVALID_RECORD_TYPE_PARENT: 11,
  
  NULL_VIOLATION: 12,
  
  FILE_NOT_FOUND: 13,
  
  PERMISSION_DENIED: 14,
  
  ATOMIC_WRITE_FAILED: 15,
  
  INVALID_FORMAT_CREATOR: 16,
  
  DUPLICATE_FIELD_NAME: 6,        // alias: same block as INVALID_FIELDS (E_INVALID_FIELDS=6)
  VERSION_CONSTRAINT: 4,          // alias: maps to INVALID_FORMAT_VERSION
  FORBIDDEN_CUSTOM_KEY: 10,       // alias: maps to RESERVED_KEY_COLLISION
  INVALID_CUSTOM_KEY: 10,         // alias: maps to RESERVED_KEY_COLLISION
  MISSING_DISCRIMINATOR: 11,      // alias: maps to INVALID_RECORD_TYPE_PARENT
  INVALID_VALUES_STRUCTURE: 7,    // alias: maps to INVALID_VALUES
  MFDB_FK_UNRESOLVED: 39,          // alias: maps to MFDB_VALIDATION_CODES.FK_UNRESOLVED
} as const;

export const BEJSON_CORE_CODES = {
  
  INVALID_VERSION: 20,
  
  INVALID_OPERATION: 21,
  
  INDEX_OUT_OF_BOUNDS: 22,
  
  FIELD_NOT_FOUND: 23,
  
  TYPE_CONVERSION_FAILED: 24,
  
  BACKUP_FAILED: 25,
  
  WRITE_FAILED: 26,
  
  QUERY_FAILED: 27,
  
  ENCRYPTION_FAILED: 28,
  
  DECRYPTION_FAILED: 29,
  
  // Extended core codes (JS-only in errors.js; now unified in TS)
  PARSE_ERROR: 17,
  SERIALIZATION_ERROR: 18,
  NULL_DOCUMENT: 19,
  
  // Aliases for codes referenced in bejson_core.ts
  UNSUPPORTED_OPERATION: 21,      // alias: maps to INVALID_OPERATION
  WRITE_TYPE_MISMATCH: 8,         // alias: maps to TYPE_MISMATCH  
  WRITE_LENGTH_MISMATCH: 9,       // alias: maps to INDEX_OUT_OF_BOUNDS
} as const;

export const MFDB_VALIDATION_CODES = {
  
  NOT_A_MANIFEST: 30,
  
  NOT_AN_ENTITY: 31,
  
  MANIFEST_RECORDS_TYPE_INVALID: 32,
  
  ENTITY_FILE_NOT_FOUND: 33,
  
  ENTITY_NAME_MISMATCH: 34,
  
  DUPLICATE_ENTRY: 35,
  
  MISSING_PARENT_HIERARCHY: 36,
  
  MANIFEST_FILE_NOT_FOUND: 37,
  
  BIDIRECTIONAL_PATH_FAILED: 38,
  
  FK_UNRESOLVED: 39,
  
  MISSING_REQUIRED_MANIFEST_FIELD: 40,
  
  NULL_IN_REQUIRED_MANIFEST_FIELD: 41,
  
  INVALID_ARCHIVE: 42,
} as const;

export const MFDB_CORE_CODES = {
  
  MANIFEST_NOT_FOUND: 50,
  
  ENTITY_NOT_FOUND: 51,
  
  WRITE_FAILED: 52,
  
  LOCK_FAILED: 53,
  
  INVALID_OPERATION: 54,
  
  INDEX_OUT_OF_BOUNDS: 55,
  
  JOIN_FAILED: 56,
  
  DUPLICATE_ENTITY_NAME: 57,
  
  RECORD_COUNT_SYNC_FAILED: 58,
  
  NULL_MANIFEST: 59,
  
  ENTITY_NOT_IN_MANIFEST: 60,
  
  ARCHIVE_ERROR: 70,
  
  MOUNT_CONFLICT: 71,
  
  CREATE_FAILED: 72,
  
  // Referenced in mfdb_validators.ts via MFDB_CORE_CODES — these belong to validation layer
  // but are emitted through MFDB_CORE_CODES in the current validators
  INVALID_MFDB_VERSION: 4,        // alias: maps to INVALID_FORMAT_VERSION
  MISSING_DB_NAME: 2,             // alias: maps to MISSING_MANDATORY_KEY
} as const;

// CORE_NESTING_CODES moved to lib_bejson_CoreNesting_bejson_errors.ts (v2.4.0)


// ==========================================================================
// SECTION 2 — FIELD MAP
// Sources: bejson_field_map v2.1.1
// ==========================================================================


/**
 * Field Map type: mapping of field name to its positional index.
 */
export type FieldMap = { [key: string]: number };

/**
 * Internal global cache for FieldMaps.
 */
const _FIELD_MAP_CACHE: Map<string, FieldMap> = new Map();

/**
 * Generates a mapping of field names to their indices for a BEJSON document.
 * Utilizes a global cache to speed up repeated access to similar structures.
 */
export function bejson_core_get_field_map(doc: BEJSONDocument): FieldMap {
    if (!doc || !doc.Fields) return {};
    
    const fieldNames = doc.Fields.map(f => f.name);
    const cacheKey = (doc.Format_Version || '104') + ':' + fieldNames.join(',');
    
    const cached = _FIELD_MAP_CACHE.get(cacheKey);
    if (cached) return cached;
    
    const fieldMap: FieldMap = {};
    doc.Fields.forEach((f, i) => {
        fieldMap[f.name] = i;
    });
    
    _FIELD_MAP_CACHE.set(cacheKey, fieldMap);
    return fieldMap;
}

/**
 * Returns the index of a specific field by name, using the cache.
 */
export function bejson_core_get_field_index(doc: BEJSONDocument, fieldName: string): number {
    const fieldMap = bejson_core_get_field_map(doc);
    const idx = fieldMap[fieldName];
    return (idx !== undefined) ? idx : -1;
}

/**
 * Clears the internal field map cache.
 */
export function bejson_core_clear_field_map_cache(): void {
    _FIELD_MAP_CACHE.clear();
}


// ==========================================================================
// SECTION 3 — BEJSON CORE
// Sources: bejson_core v2.1.4
// ==========================================================================


// ---------------------------------------------------------------------------
// Parse & Serialize
// ---------------------------------------------------------------------------

/**
 * Optimal BEJSON Parsing Standard (TS)
 * Enforces native JSON.parse() immediately wrapped in structural validation.
 * Removed regex pre-processor to eliminate fragility.
 */
export function parse(text: string): BEJSONDocument {
  if (typeof text !== 'string') {
    throw new BEJSONCoreError(BEJSON_CORE_CODES.PARSE_ERROR, 'Input must be a string.');
  }

  let raw: unknown;
  try {
    // 1. Parse Object Tree using native engine directly
    raw = JSON.parse(text);
  } catch (e) {
    throw new BEJSONCoreError(
      BEJSON_CORE_CODES.PARSE_ERROR,
      "Invalid JSON: " + String(e)
    );
  }

  if (raw === null || typeof raw !== "object" || Array.isArray(raw)) {
    throw new BEJSONCoreError(
      BEJSON_CORE_CODES.PARSE_ERROR,
      "Parsed JSON root must be an object."
    );
  }

  return raw as BEJSONDocument;
}

export function serialize(doc: BEJSONDocument, indent: number = 2): string {
  if (doc === null || doc === undefined) {
    throw new BEJSONCoreError(
      BEJSON_CORE_CODES.NULL_DOCUMENT,
      "Cannot serialize null or undefined document."
    );
  }
  try {
    // Strip internal metadata keys (starting with _) before serialization
    const cleanDoc: Record<string, any> = {};
    for (const key in doc) {
      if (Object.prototype.hasOwnProperty.call(doc, key) && !key.startsWith("_")) {
        cleanDoc[key] = doc[key];
      }
    }
    return JSON.stringify(cleanDoc, null, indent || undefined);
  } catch (e) {
    throw new BEJSONCoreError(
      BEJSON_CORE_CODES.SERIALIZATION_ERROR,
      "Serialization failed: " + String(e)
    );
  }
}

// ---------------------------------------------------------------------------
// Field index helpers
// ---------------------------------------------------------------------------

export function getFieldIndex(doc: BEJSONDocument, name: string): number {
  _assertDoc(doc);
  const idx = doc.Fields.findIndex((f) => f.name === name);
  if (idx === -1) {
    throw new BEJSONCoreError(
      BEJSON_CORE_CODES.FIELD_NOT_FOUND,
      "Field not found: " + name
    );
  }
  return idx;
}

export function getFieldNames(doc: BEJSONDocument): string[] {
  _assertDoc(doc);
  return doc.Fields.map((f) => f.name);
}

export function getFields(doc: BEJSONDocument): BEJSONField[] {
  _assertDoc(doc);
  return doc.Fields.map((f) => Object.assign({}, f));
}

// ---------------------------------------------------------------------------
// Record accessors
// ---------------------------------------------------------------------------

export function getRecord(
  doc: BEJSONDocument,
  index: number
): Record<string, BEJSONValue> {
  _assertDoc(doc);
  _assertIndex(doc, index);
  return _rowToObject(doc.Fields, doc.Values[index]);
}

export function getAllRecords(
  doc: BEJSONDocument
): Record<string, BEJSONValue>[] {
  _assertDoc(doc);
  return doc.Values.map((row) => _rowToObject(doc.Fields, row));
}

export function getFieldValue(
  doc: BEJSONDocument,
  index: number,
  fieldName: string
): BEJSONValue {
  _assertDoc(doc);
  _assertIndex(doc, index);
  const fi = getFieldIndex(doc, fieldName);
  return doc.Values[index][fi];
}

export function getRecordCount(doc: BEJSONDocument): number {
  _assertDoc(doc);
  return doc.Values.length;
}


// ---------------------------------------------------------------------------
// Factory functions — createEmpty104 / createEmpty104a / createEmpty104db
// (R1: NEW — previously undefined, causing ReferenceError in all TS Gaming
// and Core event/grid/physics/asset classes that import createEmpty104)
// ---------------------------------------------------------------------------

/**
 * Create a valid, empty BEJSON 104 document.
 * @param recordType  Single string entry for Records_Type.
 * @param fields      Field definitions array.
 * @param values      Optional initial values (default: empty array).
 * @param parentHierarchy Optional Parent_Hierarchy path string.
 */
export function createEmpty104(
  recordType: string,
  fields: BEJSONField[],
  values: BEJSONValue[][] = [],
  parentHierarchy?: string
): BEJSONDocument {
  const doc: BEJSONDocument = {
    Format: "BEJSON",
    Format_Version: "104",
    Format_Creator: "Elton Boehnen",
    Records_Type: [recordType],
    Fields: fields,
    Values: values,
  };
  if (parentHierarchy !== undefined) {
    (doc as Record<string, unknown>)["Parent_Hierarchy"] = parentHierarchy;
  }
  return doc;
}

/**
 * Create a valid, empty BEJSON 104a document.
 * @param recordType    Single string entry for Records_Type.
 * @param fields        Field definitions (primitive types only: string/integer/number/boolean).
 * @param customHeaders Optional PascalCase file-level metadata keys (104a only).
 */
export function createEmpty104a(
  recordType: string,
  fields: BEJSONField[],
  customHeaders: Record<string, string | number | boolean> = {}
): BEJSONDocument {
  return {
    Format: "BEJSON",
    Format_Version: "104a",
    Format_Creator: "Elton Boehnen",
    Records_Type: [recordType],
    Fields: fields,
    Values: [],
    ...customHeaders,
  };
}

/**
 * Create a valid, empty BEJSON 104db document.
 * @param recordTypes  Two or more entity name strings.
 * @param fields       Fields array — first entry must be Record_Type_Parent.
 */
export function createEmpty104db(
  recordTypes: [string, string, ...string[]],
  fields: BEJSONField[]
): BEJSONDocument {
  return {
    Format: "BEJSON",
    Format_Version: "104db",
    Format_Creator: "Elton Boehnen",
    Records_Type: recordTypes,
    Fields: fields,
    Values: [],
  };
}

// ---------------------------------------------------------------------------
// 104db — entity-scoped record access
// ---------------------------------------------------------------------------

export function getRecordsByType(
  doc: BEJSONDocument,
  type: string
): Record<string, BEJSONValue>[] {
  _assertDoc(doc);
  if (doc.Format_Version !== "104db") {
    throw new BEJSONCoreError(
      BEJSON_CORE_CODES.UNSUPPORTED_OPERATION,
      "getRecordsByType is only valid on BEJSON 104db documents."
    );
  }
  return doc.Values.filter((row) => row[0] === type).map((row) =>
    _rowToObject(doc.Fields, row)
  );
}

// ---------------------------------------------------------------------------
// Mutations
// ---------------------------------------------------------------------------

export function appendRecord(
  doc: BEJSONDocument,
  values: BEJSONValue[]
): BEJSONDocument {
  _assertDoc(doc);
  _assertRowLength(doc, values);
  const coerced = values.map((v, i) => _coerceValue(v, doc.Fields[i].type));
  return _cloneWith(doc, { Values: [...doc.Values, coerced] });
}

export function updateRecord(
  doc: BEJSONDocument,
  index: number,
  values: BEJSONValue[]
): BEJSONDocument {
  _assertDoc(doc);
  _assertIndex(doc, index);
  _assertRowLength(doc, values);
  const coerced = values.map((v, i) => _coerceValue(v, doc.Fields[i].type));
  const newValues = doc.Values.map((row, i) =>
    i === index ? coerced : row
  );
  return _cloneWith(doc, { Values: newValues });
}

export function deleteRecord(doc: BEJSONDocument, index: number): BEJSONDocument {
  _assertDoc(doc);
  _assertIndex(doc, index);
  const newValues = doc.Values.filter((_, i) => i !== index);
  return _cloneWith(doc, { Values: newValues });
}

export function setFieldValue(
  doc: BEJSONDocument,
  index: number,
  fieldName: string,
  value: BEJSONValue
): BEJSONDocument {
  _assertDoc(doc);
  _assertIndex(doc, index);
  const fi = getFieldIndex(doc, fieldName);
  const coerced = _coerceValue(value, doc.Fields[fi].type);
  const newRow = [...doc.Values[index]];
  newRow[fi] = coerced;
  const newValues = doc.Values.map((row, i) => (i === index ? newRow : row));
  return _cloneWith(doc, { Values: newValues });
}

// ---------------------------------------------------------------------------
// Encryption Utilities Optimized
// ---------------------------------------------------------------------------

/**
 * Derives a CryptoKey from a password and salt.
 * Caller should cache this key to avoid PBKDF2 bottlenecks.
 */
export async function deriveKey(password: string, salt: Uint8Array): Promise<CryptoKey> {
  const enc = new TextEncoder();
  const keyMaterial = await crypto.subtle.importKey(
    "raw",
    enc.encode(password),
    { name: "PBKDF2" },
    false,
    ["deriveKey"]
  );
  return await crypto.subtle.deriveKey(
    { name: "PBKDF2", salt: salt as BufferSource, iterations: 100000, hash: "SHA-256" },
    keyMaterial,
    { name: "AES-GCM", length: 256 },
    false,
    ["encrypt", "decrypt"]
  );
}

// Internal Key Cache for current session/document operation.
// LIB-C5 fix (2026-08-08): was a single slot -- not a security defect
// (worst case was just a repeated PBKDF2 derivation when switching
// passwords/salts, never wrong encryption), but any workflow touching
// more than one password+salt pair (e.g. multiple entities decrypted
// in the same session) thrashed the cache on every call. Small
// fixed-size LRU (4 slots) removes the thrashing for realistic
// multi-entity sessions while keeping memory bounded.
const _KEY_CACHE_MAX_SLOTS = 4;
const _keyCache: Array<{ password: string; salt: string; key: CryptoKey }> = [];

async function _getOrDeriveKey(password: string, salt: Uint8Array): Promise<CryptoKey> {
  const saltHex = _ab2hex(salt as BufferSource);
  const hitIdx = _keyCache.findIndex((e) => e.password === password && e.salt === saltHex);
  if (hitIdx !== -1) {
    const [hit] = _keyCache.splice(hitIdx, 1);
    _keyCache.push(hit); // move to most-recently-used end
    return hit.key;
  }
  const key = await deriveKey(password, salt);
  if (_keyCache.length >= _KEY_CACHE_MAX_SLOTS) {
    _keyCache.shift(); // evict least-recently-used
  }
  _keyCache.push({ password, salt: saltHex, key });
  return key;
}

// Accepts either a raw ArrayBuffer (e.g. crypto.subtle.encrypt's return value) or a
// typed-array view over one (e.g. crypto.getRandomValues output) — both are valid
// BufferSource shapes, but TS 5.7+'s generic ArrayBufferLike typing on bare 'Uint8Array'
// no longer lets them flow interchangeably without an explicit, byte-accurate view.
function _toUint8(buf: BufferSource): Uint8Array {
  return ArrayBuffer.isView(buf)
    ? new Uint8Array(buf.buffer, buf.byteOffset, buf.byteLength)
    : new Uint8Array(buf);
}

function _ab2hex(buf: BufferSource): string {
  return Array.from(_toUint8(buf))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

function _ab2base64(buf: BufferSource): string {
  return btoa(String.fromCharCode(...Array.from(_toUint8(buf))));
}

function _base642ab(base64: string): Uint8Array {
  const b = atob(base64);
  return new Uint8Array(b.length).map((_, i) => b.charCodeAt(i));
}

export async function encryptRecord(
  doc: BEJSONDocument,
  recordIndex: number,
  password: string,
  providedSalt?: Uint8Array
): Promise<BEJSONDocument> {
  _assertDoc(doc);
  _assertIndex(doc, recordIndex);

  // Reuse salt if provided, otherwise generate. Reusing salt allows key caching.
  const salt = providedSalt || crypto.getRandomValues(new Uint8Array(16));
  const key = await _getOrDeriveKey(password, salt);
  const saltB64 = _ab2base64(salt as BufferSource);

  const row = doc.Values[recordIndex];
  const newRow = [...row];

  for (let j = 0; j < newRow.length; j++) {
    const field = doc.Fields[j];
    if (field.name === "Record_Type_Parent" || field.name === "is_encrypted") continue;
    if (newRow[j] === null || (typeof newRow[j] === "string" && (newRow[j] as string).startsWith("ENC:AES-GCM:"))) continue;

    const dataEnc = new TextEncoder().encode(JSON.stringify(newRow[j]));
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const ciphertext = await crypto.subtle.encrypt({ name: "AES-GCM", iv: iv as BufferSource }, key, dataEnc);

    newRow[j] = "ENC:AES-GCM:" + saltB64 + ":" + _ab2base64(iv) + ":" + _ab2base64(ciphertext);
  }

  const ieIdx = doc.Fields.findIndex((f) => f.name === "is_encrypted");
  if (ieIdx !== -1) newRow[ieIdx] = true;

  const newValues = doc.Values.map((r, i) => (i === recordIndex ? newRow : r));
  return _cloneWith(doc, { Values: newValues });
}

export async function decryptRecord(
  doc: BEJSONDocument,
  recordIndex: number,
  password: string
): Promise<BEJSONDocument> {
  _assertDoc(doc);
  _assertIndex(doc, recordIndex);

  const row = doc.Values[recordIndex];
  const newRow = [...row];

  for (let j = 0; j < newRow.length; j++) {
    const val = newRow[j];
    if (typeof val !== "string" || !val.startsWith("ENC:AES-GCM:")) continue;

    const parts = val.split(":");
    if (parts.length !== 5) continue;

    const salt = _base642ab(parts[2]);
    const iv = _base642ab(parts[3]);
    const ct = _base642ab(parts[4]);

    const key = await _getOrDeriveKey(password, salt);
    const decrypted = await crypto.subtle.decrypt({ name: "AES-GCM", iv: iv as BufferSource }, key, ct as BufferSource);
    newRow[j] = JSON.parse(new TextDecoder().decode(decrypted));
  }

  const ieIdx = doc.Fields.findIndex((f) => f.name === "is_encrypted");
  if (ieIdx !== -1) {
    newRow[ieIdx] = newRow.some((v, idx) => doc.Fields[idx].name !== "is_encrypted" && typeof v === "string" && v.startsWith("ENC:AES-GCM:"));
  }

  const newValues = doc.Values.map((r, i) => (i === recordIndex ? newRow : r));
  return _cloneWith(doc, { Values: newValues });
}

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

function _assertDoc(doc: BEJSONDocument): void {
  if (doc === null || doc === undefined) throw new BEJSONCoreError(BEJSON_CORE_CODES.NULL_DOCUMENT, "Document is null.");
}

function _assertIndex(doc: BEJSONDocument, index: number): void {
  if (index < 0 || index >= doc.Values.length) throw new BEJSONCoreError(BEJSON_CORE_CODES.INDEX_OUT_OF_BOUNDS, "Index out of bounds.");
}

function _assertRowLength(doc: BEJSONDocument, values: BEJSONValue[]): void {
  if (values.length !== doc.Fields.length) throw new BEJSONCoreError(BEJSON_CORE_CODES.WRITE_LENGTH_MISMATCH, "Length mismatch.");
}

function _rowToObject(fields: BEJSONField[], row: BEJSONValue[]): Record<string, BEJSONValue> {
  const obj: Record<string, BEJSONValue> = {};
  for (let i = 0; i < fields.length; i++) obj[fields[i].name] = row[i];
  return obj;
}

function _cloneWith(doc: BEJSONDocument, overrides: Partial<BEJSONDocument>): BEJSONDocument {
  return Object.assign({}, doc, overrides);
}

function _coerceValue(value: any, fieldType: string): BEJSONValue {
  if (fieldType === "string") return String(value);
  if (fieldType === "integer" || fieldType === "number") {
    const num = fieldType === "integer" ? parseInt(value, 10) : parseFloat(value);
    if (isNaN(num)) throw new BEJSONCoreError(BEJSON_CORE_CODES.WRITE_TYPE_MISMATCH, "Coercion failed.");
    return num;
  }
  if (fieldType === "boolean") {
    if (typeof value === "boolean") return value;
    if (String(value).toLowerCase() === "true") return true;
    if (String(value).toLowerCase() === "false") return false;
    throw new BEJSONCoreError(BEJSON_CORE_CODES.WRITE_TYPE_MISMATCH, "Coercion failed.");
  }
  return value as BEJSONValue;
}


// ==========================================================================
// SECTION 4 — VALIDATORS
// Sources: bejson_validators v2.0.2
// ==========================================================================


// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

export function validateDocument(doc: unknown): ValidationResult {
  const result = _makeResult();

  // Step 1: structural sanity before touching any BEJSON fields
  if (doc === null || doc === undefined || typeof doc !== "object" || Array.isArray(doc)) {
    _err(result, BEJSON_VALIDATION_CODES.INVALID_FORMAT_VALUE, "Document root must be a non-null object.");
    return result;
  }

  const d = doc as Record<string, unknown>;

  // Step 2: mandatory keys
  _checkMandatoryKeys(d, result);
  if (!result.valid) return result; // can't proceed without the six keys

  const bej = doc as BEJSONDocument;

  // Step 3: top-level value checks (Format, Format_Creator, Format_Version)
  _checkTopLevel(bej, result);
  if (!result.valid) return result;

  // Step 4: Fields array
  _checkFields(bej, result);
  if (!result.valid) return result;

  // Step 5: Values array
  _checkValues(bej, result);

  // Step 6: version-specific rules
  switch (bej.Format_Version) {
    case "104":
      _check104Specific(bej, result);
      break;
    case "104a":
      _check104aSpecific(bej, result);
      break;
    case "104db":
      _check104dbSpecific(bej, result);
      break;
  }

  return result;
}

export function validate104(doc: unknown): ValidationResult {
  const result = validateDocument(doc);
  if (result.valid) {
    const bej = doc as BEJSONDocument;
    if (bej.Format_Version !== "104") {
      _err(result, BEJSON_VALIDATION_CODES.INVALID_FORMAT_VERSION, "Expected Format_Version \"104\", got \"" + bej.Format_Version + "\".");
    }
  }
  return result;
}

export function validate104a(doc: unknown): ValidationResult {
  const result = validateDocument(doc);
  if (result.valid) {
    const bej = doc as BEJSONDocument;
    if (bej.Format_Version !== "104a") {
      _err(result, BEJSON_VALIDATION_CODES.INVALID_FORMAT_VERSION, "Expected Format_Version \"104a\", got \"" + bej.Format_Version + "\".");
    }
  }
  return result;
}

export function validate104db(doc: unknown): ValidationResult {
  const result = validateDocument(doc);
  if (result.valid) {
    const bej = doc as BEJSONDocument;
    if (bej.Format_Version !== "104db") {
      _err(result, BEJSON_VALIDATION_CODES.INVALID_FORMAT_VERSION, "Expected Format_Version \"104db\", got \"" + bej.Format_Version + "\".");
    }
  }
  return result;
}

export function assertValid(doc: unknown): void {
  const result = validateDocument(doc);
  if (!result.valid && result.errors.length > 0) {
    const e = result.errors[0];
    throw new BEJSONValidationError(e.code, e.message);
  }
}

export function isValid(doc: unknown): boolean {
  return validateDocument(doc).valid;
}

// ---------------------------------------------------------------------------
// Step 2 — mandatory keys
// ---------------------------------------------------------------------------

const MANDATORY_KEYS = ["Format", "Format_Version", "Format_Creator", "Records_Type", "Fields", "Values"] as const;

function _checkMandatoryKeys(d: Record<string, unknown>, r: ValidationResult): void {
  for (const key of MANDATORY_KEYS) {
    if (!(key in d) || d[key] === undefined) {
      _err(r, BEJSON_VALIDATION_CODES.MISSING_MANDATORY_KEY, "Missing mandatory key: " + key, key);
    }
  }
}

// ---------------------------------------------------------------------------
// Step 3 — top-level value constraints
// ---------------------------------------------------------------------------

function _checkTopLevel(doc: BEJSONDocument, r: ValidationResult): void {
  if (doc.Format !== "BEJSON") {
    _err(r, BEJSON_VALIDATION_CODES.INVALID_FORMAT_VALUE, "Format must be \"BEJSON\", got \"" + doc.Format + "\".", "Format");
  }

  const validVersions = ["104", "104a", "104db"];
  if (!validVersions.includes(doc.Format_Version as string)) {
    _err(r, BEJSON_VALIDATION_CODES.INVALID_FORMAT_VERSION, "Format_Version must be one of " + JSON.stringify(validVersions) + ", got \"" + doc.Format_Version + "\".", "Format_Version");
  }

  if (doc.Format_Creator !== "Elton Boehnen") {
    _err(r, BEJSON_VALIDATION_CODES.INVALID_FORMAT_CREATOR, "Format_Creator must be \"Elton Boehnen\", got \"" + doc.Format_Creator + "\".", "Format_Creator");
  }

  if (!Array.isArray(doc.Records_Type) || doc.Records_Type.length === 0) {
    _err(r, BEJSON_VALIDATION_CODES.INVALID_RECORDS_TYPE, "Records_Type must be a non-empty array.", "Records_Type");
  } else {
    for (const rt of doc.Records_Type) {
      if (typeof rt !== "string" || rt.trim() === "") {
        _err(r, BEJSON_VALIDATION_CODES.INVALID_RECORDS_TYPE, "All Records_Type entries must be non-empty strings.", "Records_Type");
        break;
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Step 4 — Fields array
// ---------------------------------------------------------------------------

const VALID_TYPES: BEJSONFieldType[] = ["string", "integer", "number", "boolean", "array", "object"];

function _checkFields(doc: BEJSONDocument, r: ValidationResult): void {
  if (!Array.isArray(doc.Fields) || doc.Fields.length === 0) {
    _err(r, BEJSON_VALIDATION_CODES.INVALID_FIELDS, "Fields must be a non-empty array.", "Fields");
    return;
  }

  const seen = new Set<string>();
  for (let i = 0; i < doc.Fields.length; i++) {
    const field = doc.Fields[i] as BEJSONField;

    if (!field || typeof field !== "object") {
      _err(r, BEJSON_VALIDATION_CODES.INVALID_FIELDS, "Fields[" + i + "] must be an object.", "Fields");
      continue;
    }
    if (typeof field.name !== "string" || field.name.trim() === "") {
      _err(r, BEJSON_VALIDATION_CODES.INVALID_FIELDS, "Fields[" + i + "].name must be a non-empty string.", "Fields");
    }
    if (!VALID_TYPES.includes(field.type as BEJSONFieldType)) {
      _err(r, BEJSON_VALIDATION_CODES.INVALID_FIELDS, "Fields[" + i + "].type is invalid: \"" + field.type + "\".", "Fields");
    }
    if (seen.has(field.name)) {
      _err(r, BEJSON_VALIDATION_CODES.DUPLICATE_FIELD_NAME, "Duplicate field name: \"" + field.name + "\".", field.name);
    } else {
      seen.add(field.name);
    }
  }
}

// ---------------------------------------------------------------------------
// Step 5 — Values array
// ---------------------------------------------------------------------------

function _checkValues(doc: BEJSONDocument, r: ValidationResult): void {
  if (!Array.isArray(doc.Values)) {
    _err(r, BEJSON_VALIDATION_CODES.INVALID_VALUES_STRUCTURE, "Values must be an array.", "Values");
    return;
  }

  const fieldCount = doc.Fields.length;

  for (let i = 0; i < doc.Values.length; i++) {
    const row = doc.Values[i];
    if (!Array.isArray(row)) {
      _err(r, BEJSON_VALIDATION_CODES.INVALID_VALUES_STRUCTURE, "Values[" + i + "] must be an array.", undefined, i);
      continue;
    }
    if (row.length !== fieldCount) {
      _err(r, BEJSON_VALIDATION_CODES.RECORD_LENGTH_MISMATCH,
        "Values[" + i + "] has " + row.length + " elements but Fields has " + fieldCount + ".",
        undefined, i);
      continue;
    }

    // Type-check each cell
    for (let fi = 0; fi < fieldCount; fi++) {
      const field = doc.Fields[fi];
      const val = row[fi];
      if (val === null) continue; // null always valid
      if (!_typeMatches(val, field.type)) {
        _err(r, BEJSON_VALIDATION_CODES.VALUE_TYPE_MISMATCH,
          "Values[" + i + "][" + fi + "] (" + field.name + "): expected " + field.type + ", got " + typeof val + ".",
          field.name, i);
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Step 6a — 104-specific rules
// ---------------------------------------------------------------------------

const FORBIDDEN_CUSTOM_KEYS_104 = new Set(MANDATORY_KEYS);

function _check104Specific(doc: BEJSONDocument, r: ValidationResult): void {
  // Single record type
  if (doc.Records_Type.length !== 1) {
    _err(r, BEJSON_VALIDATION_CODES.VERSION_CONSTRAINT, "BEJSON 104 requires exactly one Records_Type entry.", "Records_Type");
  }

  // No custom top-level keys (Parent_Hierarchy is the only exception)
  for (const key of Object.keys(doc)) {
    if (!FORBIDDEN_CUSTOM_KEYS_104.has(key as typeof MANDATORY_KEYS[number]) && key !== "Parent_Hierarchy") {
      _err(r, BEJSON_VALIDATION_CODES.FORBIDDEN_CUSTOM_KEY, "BEJSON 104 forbids custom top-level key: \"" + key + "\".", key);
    }
  }

  // Parent_Hierarchy, if present, must be a string
  if ("Parent_Hierarchy" in doc && typeof doc.Parent_Hierarchy !== "string") {
    _err(r, BEJSON_VALIDATION_CODES.VERSION_CONSTRAINT, "Parent_Hierarchy must be a string when present.", "Parent_Hierarchy");
  }
}

// ---------------------------------------------------------------------------
// Step 6b — 104a-specific rules
// ---------------------------------------------------------------------------

const PRIMITIVE_TYPES: BEJSONPrimitiveType[] = ["string", "integer", "number", "boolean"];
const PASCAL_CASE_RE = /^[A-Z][A-Za-z0-9]*(_[A-Za-z0-9]+)*$/;

function _check104aSpecific(doc: BEJSONDocument, r: ValidationResult): void {
  // Single record type
  if (doc.Records_Type.length !== 1) {
    _err(r, BEJSON_VALIDATION_CODES.VERSION_CONSTRAINT, "BEJSON 104a requires exactly one Records_Type entry.", "Records_Type");
  }

  // Fields must be primitive-only
  for (let i = 0; i < doc.Fields.length; i++) {
    const field = doc.Fields[i];
    if (!PRIMITIVE_TYPES.includes(field.type as BEJSONPrimitiveType)) {
      _err(r, BEJSON_VALIDATION_CODES.VERSION_CONSTRAINT,
        "BEJSON 104a: Fields[" + i + "].type \"" + field.type + "\" is not a primitive type.", field.name);
    }
  }

  // Custom keys: must be PascalCase, must not collide with mandatory keys
  for (const key of Object.keys(doc)) {
    if (FORBIDDEN_CUSTOM_KEYS_104.has(key as typeof MANDATORY_KEYS[number])) continue;
    if (key === "Parent_Hierarchy") {
      // Parent_Hierarchy is not defined for 104a but not strictly forbidden;
      // emit a warning rather than an error since the spec is silent here.
      continue;
    }
    if (!PASCAL_CASE_RE.test(key)) {
      _err(r, BEJSON_VALIDATION_CODES.INVALID_CUSTOM_KEY,
        "BEJSON 104a: custom header \"" + key + "\" must be PascalCase.", key);
    }
  }
}

// ---------------------------------------------------------------------------
// Step 6c — 104db-specific rules
// ---------------------------------------------------------------------------

function _check104dbSpecific(doc: BEJSONDocument, r: ValidationResult): void {
  // Two or more record types
  if (doc.Records_Type.length < 2) {
    _err(r, BEJSON_VALIDATION_CODES.VERSION_CONSTRAINT, "BEJSON 104db requires at least two Records_Type entries.", "Records_Type");
  }

  // No custom top-level keys (not even Parent_Hierarchy)
  for (const key of Object.keys(doc)) {
    if (!FORBIDDEN_CUSTOM_KEYS_104.has(key as typeof MANDATORY_KEYS[number])) {
      _err(r, BEJSON_VALIDATION_CODES.FORBIDDEN_CUSTOM_KEY, "BEJSON 104db forbids custom top-level key: \"" + key + "\".", key);
    }
  }

  // First field must be Record_Type_Parent: string
  if (doc.Fields.length === 0 || doc.Fields[0].name !== "Record_Type_Parent") {
    _err(r, BEJSON_VALIDATION_CODES.MISSING_DISCRIMINATOR, "BEJSON 104db: first field must be named \"Record_Type_Parent\".", "Fields");
    return; // can't continue safely
  }
  if (doc.Fields[0].type !== "string") {
    _err(r, BEJSON_VALIDATION_CODES.MISSING_DISCRIMINATOR, "BEJSON 104db: Record_Type_Parent field type must be \"string\".", "Record_Type_Parent");
  }

  // Every field except Record_Type_Parent must have Record_Type_Parent property
  const validEntities = new Set(doc.Records_Type);
  for (let i = 1; i < doc.Fields.length; i++) {
    const field = doc.Fields[i];
    if (!field.Record_Type_Parent) {
      _err(r, BEJSON_VALIDATION_CODES.MISSING_DISCRIMINATOR,
        "BEJSON 104db: Fields[" + i + "] (\"" + field.name + "\") is missing Record_Type_Parent assignment.", field.name);
    } else if (!validEntities.has(field.Record_Type_Parent)) {
      _err(r, BEJSON_VALIDATION_CODES.VERSION_CONSTRAINT,
        "BEJSON 104db: Fields[" + i + "].Record_Type_Parent \"" + field.Record_Type_Parent + "\" is not in Records_Type.", field.name);
    }
  }

  // Every record's discriminator must match a declared entity
  if (Array.isArray(doc.Values)) {
    for (let i = 0; i < doc.Values.length; i++) {
      const row = doc.Values[i];
      if (!Array.isArray(row) || row.length === 0) continue;
      const discriminator = row[0];
      if (typeof discriminator !== "string" || !validEntities.has(discriminator)) {
        _err(r, BEJSON_VALIDATION_CODES.VERSION_CONSTRAINT,
          "Values[" + i + "][0] discriminator \"" + discriminator + "\" not in Records_Type.", "Record_Type_Parent", i);
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Type matching helper
// ---------------------------------------------------------------------------

function _typeMatches(val: unknown, type: BEJSONFieldType): boolean {
  if (val === null) return true;
  switch (type) {
    case "string":
      return typeof val === "string";
    case "integer":
      return typeof val === "number" && Number.isInteger(val);
    case "number":
      return typeof val === "number";
    case "boolean":
      return typeof val === "boolean";
    case "array":
      return Array.isArray(val);
    case "object":
      return typeof val === "object" && !Array.isArray(val) && val !== null;
    default:
      return false;
  }
}

// ---------------------------------------------------------------------------
// Result helpers
// ---------------------------------------------------------------------------

function _makeResult(): ValidationResult {
  return { valid: true, errors: [], warnings: [] };
}

function _err(
  r: ValidationResult,
  code: number,
  message: string,
  field?: string,
  recordIndex?: number
): void {
  r.valid = false;
  const e: ValidationError = { code, message };
  if (field !== undefined) e.field = field;
  if (recordIndex !== undefined) e.recordIndex = recordIndex;
  r.errors.push(e);
}

function _warn(
  r: ValidationResult,
  code: number,
  message: string,
  field?: string,
  recordIndex?: number
): void {
  const w: ValidationWarning = { code, message };
  if (field !== undefined) w.field = field;
  if (recordIndex !== undefined) w.recordIndex = recordIndex;
  r.warnings.push(w);
}

// Export _warn so mfdb_validators can reuse the pattern
export { _warn as _emitWarning, _err as _emitError, _makeResult };


// ==========================================================================
// SECTION 5 — LIST VALIDATOR
// Sources: bejson_list_validator v1.2.0
// ==========================================================================


/**
 * Validates a Hierarchical List (BEJSON 104a with id and parent_id fields).
 * Ensures no orphans exist and structure follows positional integrity.
 */
export function validateList(jsonString: string): ValidationResult {
  // LIB-C4 fix (2026-08-08): was parsing jsonString twice (once to
  // validate, once into `doc`). Wasteful, not incorrect (same string,
  // deterministic parse) -- but a malformed jsonString would also throw
  // JSON.parse's raw SyntaxError instead of a clean ValidationResult.
  // Parse once and wrap in try/catch for a proper validation error.
  let doc: BEJSONDocument;
  try {
    doc = JSON.parse(jsonString);
  } catch (e) {
    return {
      valid: false,
      errors: [{ code: BEJSON_VALIDATION_CODES.INVALID_JSON, message: `Malformed JSON: ${(e as Error).message}` }],
      warnings: []
    };
  }

  const result = validateDocument(doc);
  if (!result.valid) return result;

  if (doc.Format_Version !== "104a") {
    result.valid = false;
    result.errors.push({
      code: BEJSON_VALIDATION_CODES.VERSION_CONSTRAINT,
      message: "Hierarchical List must be BEJSON 104a."
    });
    return result;
  }

  const idIdx = doc.Fields.findIndex(f => f.name === "id");
  const pidIdx = doc.Fields.findIndex(f => f.name === "parent_id");

  if (idIdx === -1 || pidIdx === -1) {
    result.valid = false;
    result.errors.push({
      code: BEJSON_VALIDATION_CODES.MISSING_MANDATORY_KEY,
      message: "Hierarchical List requires 'id' and 'parent_id' fields."
    });
    return result;
  }

  const ids = new Set<any>();
  const parentRefs = new Map<any, any>();

  for (let i = 0; i < doc.Values.length; i++) {
    const row = doc.Values[i];
    const id = row[idIdx];
    const pid = row[pidIdx];

    if (id === null || id === undefined) {
      result.valid = false;
      result.errors.push({
        code: BEJSON_VALIDATION_CODES.VALUE_TYPE_MISMATCH,
        message: `Row ${i} has null or undefined id.`,
        recordIndex: i
      });
      continue;
    }

    if (ids.has(id)) {
      result.valid = false;
      result.errors.push({
        code: BEJSON_VALIDATION_CODES.DUPLICATE_FIELD_NAME, // Using duplicate field name code for duplicate IDs
        message: `Duplicate ID detected: ${id}`,
        recordIndex: i
      });
    }
    ids.add(id);

    if (pid !== null && pid !== undefined && pid !== "") {
      parentRefs.set(id, pid);
    }
  }

  // Orphan Detection
  for (const [uid, pid] of parentRefs.entries()) {
    if (!ids.has(pid)) {
      result.valid = false;
      result.errors.push({
        code: BEJSON_VALIDATION_CODES.MFDB_FK_UNRESOLVED,
        message: `Orphan detected: Record ${uid} references non-existent parent ${pid}.`
      });
    }
  }

  // Cycle Detection (Bonus for TS implementation)
  for (const startId of parentRefs.keys()) {
    let currentId = startId;
    const visited = new Set([currentId]);
    while (parentRefs.has(currentId)) {
      currentId = parentRefs.get(currentId);
      if (visited.has(currentId)) {
        result.valid = false;
        result.errors.push({
          code: BEJSON_VALIDATION_CODES.VERSION_CONSTRAINT,
          message: `Cycle detected in hierarchy involving ID: ${currentId}`
        });
        break;
      }
      visited.add(currentId);
    }
  }

  return result;
}


// ==========================================================================
// SECTION 6 — MFDB VALIDATORS
// Sources: mfdb_validators v2.1.0
// ==========================================================================


// ---------------------------------------------------------------------------
// Discovery algorithm
// ---------------------------------------------------------------------------

export function discoverRole(doc: unknown, filename: string): MFDBFileRole {
  if (doc === null || doc === undefined || typeof doc !== "object" || Array.isArray(doc)) {
    return "standalone";
  }
  const d = doc as BEJSONDocument;
  if (d.Format_Version === "104a" && filename.endsWith(".mfdb.bejson")) {
    return "manifest";
  }
  if (d.Format_Version === "104" && "Parent_Hierarchy" in d) {
    return "entity";
  }
  return "standalone";
}

// ---------------------------------------------------------------------------
// Level 1 — Manifest validation
// ---------------------------------------------------------------------------

export function validateManifest(
  doc: unknown,
  options: {
    
    resolvedPaths?: Set<string>;
  } = {}
): ValidationResult {
  const r = _makeResult();

  // Must be valid BEJSON 104a
  const bejsonResult = validateDocument(doc);
  if (!bejsonResult.valid) {
    for (const e of bejsonResult.errors) {
      _err(r, e.code, "[BEJSON] " + e.message, e.field, e.recordIndex);
    }
    return r;
  }

  const manifest = doc as BEJSONDocument;

  if (manifest.Format_Version !== "104a") {
    _err(r, MFDB_VALIDATION_CODES.NOT_A_MANIFEST, "Manifest must be Format_Version \"104a\", got \"" + manifest.Format_Version + "\".");
    return r;
  }

  // Records_Type must be exactly ["mfdb"]
  if (
    !Array.isArray(manifest.Records_Type) ||
    manifest.Records_Type.length !== 1 ||
    manifest.Records_Type[0] !== "mfdb"
  ) {
    _err(r, MFDB_VALIDATION_CODES.MANIFEST_RECORDS_TYPE_INVALID, "Manifest Records_Type must be exactly [\"mfdb\"].", "Records_Type");
  }

  // Required custom headers
  if (typeof manifest["MFDB_Version"] !== "string" || (manifest["MFDB_Version"] as string).trim() === "") {
    _err(r, MFDB_CORE_CODES.INVALID_MFDB_VERSION,
      "Manifest is missing required header MFDB_Version.", "MFDB_Version");
  }
  if (typeof manifest["DB_Name"] !== "string" || (manifest["DB_Name"] as string).trim() === "") {
    _err(r, MFDB_CORE_CODES.MISSING_DB_NAME,
      "Manifest is missing required header DB_Name.", "DB_Name");
  }

  // entity_name and file_path field presence
  const fieldNames = manifest.Fields.map((f) => f.name);
  if (!fieldNames.includes("entity_name")) {
    _err(r, MFDB_VALIDATION_CODES.MISSING_REQUIRED_MANIFEST_FIELD, "Manifest Fields must include \"entity_name\".", "entity_name");
  }
  if (!fieldNames.includes("file_path")) {
    _err(r, MFDB_VALIDATION_CODES.MISSING_REQUIRED_MANIFEST_FIELD, "Manifest Fields must include \"file_path\".", "file_path");
  }

  if (!r.valid) return r; // can't proceed without required fields

  const enIdx = fieldNames.indexOf("entity_name");
  const fpIdx = fieldNames.indexOf("file_path");

  const seenNames = new Set<string>();
  const seenPaths = new Set<string>();

  for (let i = 0; i < manifest.Values.length; i++) {
    const row = manifest.Values[i];

    const entityName = row[enIdx];
    const filePath = row[fpIdx];

    // Null checks
    if (entityName === null) {
      _err(r, MFDB_VALIDATION_CODES.NULL_IN_REQUIRED_MANIFEST_FIELD,
        "Values[" + i + "].entity_name must not be null.", "entity_name", i);
    }
    if (filePath === null) {
      _err(r, MFDB_VALIDATION_CODES.NULL_IN_REQUIRED_MANIFEST_FIELD,
        "Values[" + i + "].file_path must not be null.", "file_path", i);
    }

    // Uniqueness
    if (typeof entityName === "string") {
      if (seenNames.has(entityName)) {
        _err(r, MFDB_VALIDATION_CODES.DUPLICATE_ENTRY,
          "Duplicate entity_name: \"" + entityName + "\".", "entity_name", i);
      } else {
        seenNames.add(entityName);
      }
    }
    if (typeof filePath === "string") {
      if (seenPaths.has(filePath)) {
        _err(r, MFDB_VALIDATION_CODES.DUPLICATE_ENTRY,
          "Duplicate file_path: \"" + filePath + "\".", "file_path", i);
      } else {
        seenPaths.add(filePath);
      }

      // File existence (optional — caller must provide resolvedPaths)
      if (options.resolvedPaths && !options.resolvedPaths.has(filePath)) {
        _err(r, MFDB_VALIDATION_CODES.ENTITY_FILE_NOT_FOUND,
          "file_path \"" + filePath + "\" does not exist on disk.", "file_path", i);
      }
    }
  }

  return r;
}

// ---------------------------------------------------------------------------
// Level 2 — Entity file validation
// ---------------------------------------------------------------------------

export interface EntityValidationOptions {
  
  expectedEntityName: string;
  
  expectedParentHierarchy?: string;
  
  manifestRelativePath?: string;
  
  entityRelativePath?: string;
}

export function validateEntityFile(
  doc: unknown,
  options: EntityValidationOptions
): ValidationResult {
  const r = _makeResult();

  // Must be valid BEJSON 104
  const bejsonResult = validateDocument(doc);
  if (!bejsonResult.valid) {
    for (const e of bejsonResult.errors) {
      _err(r, e.code, "[BEJSON] " + e.message, e.field, e.recordIndex);
    }
    return r;
  }

  const entity = doc as BEJSONDocument;

  if (entity.Format_Version !== "104") {
    _err(r, MFDB_VALIDATION_CODES.NOT_AN_ENTITY, "Entity file must be Format_Version \"104\", got \"" + entity.Format_Version + "\".");
    return r;
  }

  // Parent_Hierarchy required
  if (!("Parent_Hierarchy" in entity) || entity.Parent_Hierarchy === undefined || entity.Parent_Hierarchy === null) {
    _err(r, MFDB_VALIDATION_CODES.MISSING_PARENT_HIERARCHY, "Entity file must contain Parent_Hierarchy key.", "Parent_Hierarchy");
  } else if (typeof entity.Parent_Hierarchy !== "string" || entity.Parent_Hierarchy.trim() === "") {
    _err(r, MFDB_VALIDATION_CODES.MISSING_PARENT_HIERARCHY, "Parent_Hierarchy must be a non-empty string.", "Parent_Hierarchy");
  }

  // Records_Type must be exactly one string
  if (!Array.isArray(entity.Records_Type) || entity.Records_Type.length !== 1) {
    _err(r, MFDB_VALIDATION_CODES.NOT_AN_ENTITY, "Entity file Records_Type must contain exactly one entry.", "Records_Type");
    return r;
  }

  // Records_Type[0] must match the registered entity_name (case-sensitive)
  const actualName = entity.Records_Type[0];
  if (actualName !== options.expectedEntityName) {
    _err(r, MFDB_VALIDATION_CODES.ENTITY_NAME_MISMATCH,
      "Entity file Records_Type[0] is \"" + actualName + "\" but manifest expects \"" + options.expectedEntityName + "\".",
      "Records_Type");
  }

  // Parent_Hierarchy path check (if caller provided expected value)
  if (
    options.expectedParentHierarchy !== undefined &&
    typeof entity.Parent_Hierarchy === "string" &&
    entity.Parent_Hierarchy !== options.expectedParentHierarchy
  ) {
    _err(r, MFDB_VALIDATION_CODES.MANIFEST_FILE_NOT_FOUND,
      "Parent_Hierarchy \"" + entity.Parent_Hierarchy + "\" does not match expected \"" + options.expectedParentHierarchy + "\".",
      "Parent_Hierarchy");
  }

  // Bidirectional check: entity's declared path must equal what the manifest recorded
  if (options.entityRelativePath !== undefined && options.manifestRelativePath !== undefined) {
    // The manifest says this entity lives at entityRelativePath.
    // The entity's Parent_Hierarchy + its own path should resolve back to manifestRelativePath.
    // We do a lightweight string-based check here — full path resolution is the caller's job.
    // We emit a warning rather than an error because resolution is environment-dependent.
    if (typeof entity.Parent_Hierarchy === "string") {
      _warn(r, MFDB_VALIDATION_CODES.BIDIRECTIONAL_PATH_FAILED,
        "Bidirectional path check: verify that \"" + options.entityRelativePath +
        "\" + Parent_Hierarchy \"" + entity.Parent_Hierarchy +
        "\" resolves to manifest at \"" + options.manifestRelativePath + "\".",
        "Parent_Hierarchy");
    }
  }

  // No path escaping
  if (typeof entity.Parent_Hierarchy === "string") {
    if (entity.Parent_Hierarchy.includes("..") && _escapesRoot(entity.Parent_Hierarchy)) {
      _err(r, MFDB_VALIDATION_CODES.MISSING_PARENT_HIERARCHY,
        "Parent_Hierarchy must not escape the database root directory.", "Parent_Hierarchy");
    }
  }

  return r;
}

// ---------------------------------------------------------------------------
// Level 3 — Database-wide validation
// ---------------------------------------------------------------------------

export interface DatabaseValidationOptions {
  
  strict?: boolean;
  
  resolvedPaths?: Set<string>;
}

export function validateDatabase(
  manifest: unknown,
  entityDocs: Map<string, unknown>,
  options: DatabaseValidationOptions = {}
): ValidationResult {
  const r = _makeResult();

  // Level 1
  const l1 = validateManifest(manifest, { resolvedPaths: options.resolvedPaths });
  for (const e of l1.errors) _err(r, e.code, "[L1] " + e.message, e.field, e.recordIndex);
  for (const w of l1.warnings) _warn(r, w.code, "[L1] " + w.message, w.field, w.recordIndex);
  if (!r.valid) return r;

  const manifestDoc = manifest as BEJSONDocument;
  const records = decodeManifestRecords(manifestDoc);

  // Level 2 — per entity
  for (const record of records) {
    const entityDoc = entityDocs.get(record.file_path);
    if (!entityDoc) {
      _err(r, MFDB_VALIDATION_CODES.ENTITY_FILE_NOT_FOUND,
        "[L2] Entity document not provided for file_path \"" + record.file_path + "\".", "file_path");
      continue;
    }

    const l2 = validateEntityFile(entityDoc, {
      expectedEntityName: record.entity_name,
      entityRelativePath: record.file_path,
    });
    for (const e of l2.errors) _err(r, e.code, "[L2:" + record.entity_name + "] " + e.message, e.field, e.recordIndex);
    for (const w of l2.warnings) _warn(r, w.code, "[L2:" + record.entity_name + "] " + w.message, w.field, w.recordIndex);
  }

  // Level 3 — record_count advisory check + FK resolution (warnings only unless strict)
  // FIX (N3): was gated behind `if (r.valid)`, so a single L2 structural
  // error suppressed all L3 record-count/FK findings for that manifest -
  // fixing the L2 error made previously-hidden L3 issues surface on the
  // next validate, giving a false "everything else is fine" impression
  // while L2 errors existed. Now runs unconditionally. This is safe
  // without any extra suppression logic: `valid` starts true (_makeResult)
  // and _err()/_warn() only ever push it false, never back to true, so
  // running L3 after an L1/L2 failure can only add more findings - it can
  // never mask or reverse an already-invalid result.
  _checkRecordCounts(manifestDoc, records, entityDocs, r);
  _checkFKResolution(records, entityDocs, options.strict === true, r);

  return r;
}

// ---------------------------------------------------------------------------
// Helper — decode manifest Values into MFDBManifestRecord objects
// ---------------------------------------------------------------------------

export function decodeManifestRecords(manifest: BEJSONDocument): MFDBManifestRecord[] {
  const fieldNames = manifest.Fields.map((f) => f.name);
  return manifest.Values.map((row) => {
    const obj: Record<string, BEJSONValue> = {};
    for (let i = 0; i < fieldNames.length; i++) {
      obj[fieldNames[i]] = row[i];
    }
    return {
      entity_name: obj["entity_name"] as string,
      file_path: obj["file_path"] as string,
      description: (obj["description"] as string | null) ?? null,
      record_count: (obj["record_count"] as number | null) ?? null,
      schema_version: (obj["schema_version"] as string | null) ?? null,
      primary_key: (obj["primary_key"] as string | null) ?? null,
    } as MFDBManifestRecord;
  });
}

export function decodeDatabaseMeta(manifest: BEJSONDocument): MFDBDatabaseMeta {
  return {
    mfdb_version: (manifest["MFDB_Version"] as string) ?? "",
    db_name: (manifest["DB_Name"] as string) ?? "",
    db_description: (manifest["DB_Description"] as string) ?? undefined,
    schema_version: (manifest["Schema_Version"] as string) ?? undefined,
    author: (manifest["Author"] as string) ?? undefined,
    created_at: (manifest["Created_At"] as string) ?? undefined,
  };
}

// ---------------------------------------------------------------------------
// Level 3 sub-checks
// ---------------------------------------------------------------------------

function _checkRecordCounts(
  manifestDoc: BEJSONDocument,
  records: MFDBManifestRecord[],
  entityDocs: Map<string, unknown>,
  r: ValidationResult
): void {
  const rcIdx = manifestDoc.Fields.findIndex((f) => f.name === "record_count");
  if (rcIdx === -1) return; // field not declared — skip

  for (let i = 0; i < records.length; i++) {
    const record = records[i];
    if (record.record_count === null) continue;

    const entityDoc = entityDocs.get(record.file_path) as BEJSONDocument | undefined;
    if (!entityDoc) continue;

    const actualCount = entityDoc.Values.length;
    if (actualCount !== record.record_count) {
      _warn(r, 0,
        "[L3] record_count mismatch for \"" + record.entity_name + "\": manifest says " +
        record.record_count + ", file has " + actualCount + " rows.",
        "record_count", i);
    }
  }
}

function _checkFKResolution(
  records: MFDBManifestRecord[],
  entityDocs: Map<string, unknown>,
  strict: boolean,
  r: ValidationResult
): void {
  // Build a map of primary_key field names to entity names
  const pkMap = new Map<string, string>(); // pk_field → entity_name
  for (const rec of records) {
    if (rec.primary_key) {
      pkMap.set(rec.primary_key, rec.entity_name);
    }
  }

  // For each entity, find FK fields (ending in _fk) and try to resolve them
  for (const rec of records) {
    const entityDoc = entityDocs.get(rec.file_path) as BEJSONDocument | undefined;
    if (!entityDoc) continue;

    for (const field of entityDoc.Fields) {
      if (!field.name.endsWith("_fk")) continue;

      // Derive expected PK field name: strip _fk suffix
      const expectedPK = field.name.slice(0, -3); // e.g. user_id_fk → user_id
      if (!pkMap.has(expectedPK)) {
        const msg = "[L3] FK field \"" + field.name + "\" in entity \"" + rec.entity_name +
          "\" cannot resolve to any manifest primary_key \"" + expectedPK + "\".";
        if (strict) {
          _err(r, MFDB_VALIDATION_CODES.FK_UNRESOLVED, msg, field.name);
        } else {
          _warn(r, MFDB_VALIDATION_CODES.FK_UNRESOLVED, msg, field.name);
        }
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Utility
// ---------------------------------------------------------------------------

function _escapesRoot(relPath: string): boolean {
  const parts = relPath.replace(/\\/g, "/").split("/");
  let depth = 0;
  for (const part of parts) {
    if (part === "..") {
      depth--;
      if (depth < 0) return true;
    } else if (part !== "." && part !== "") {
      depth++;
    }
  }
  return false;
}

// ---------------------------------------------------------------------------
// MFDB 1.32 chunked-package validation
// ---------------------------------------------------------------------------
// Relocated from lib_bejson_Core_bejson_chunking.ts (2026-07-13). The
// chunking library still owns createMfdb132Package/unchunkMfdb132Package
// (packaging and IO), but calls back into these functions for the actual
// validation — validation logic belongs in the validator family, not the
// chunker. Local, loosely-typed field-map shapes are used here instead of
// importing ChunkedDocument from the chunking library, to avoid a circular
// import (chunking → validator → chunking).

const MFDB_MANIFEST_FILENAME = "104a.mfdb.bejson";

interface MfdbFieldDef {
  name: string;
  type: string;
}

interface MfdbChunkedDoc {
  Format_Version?: string;
  Schema_Name?: string;
  Package_Format?: string;
  MFDB_Version?: string;
  DB_Name?: string;
  Records_Type?: string[];
  Fields?: MfdbFieldDef[];
  Values?: any[][];
  [key: string]: any;
}

export interface MfdbPackageValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

export interface MfdbEntityCheck {
  entity_name: string;
  file_path: string;
  found_in_chunk: boolean;
  valid: boolean;
  errors: string[];
}

export interface MfdbInChunkDetection {
  mfdb_detected: boolean;
  valid: boolean;
  db_name: string | null;
  mfdb_version: string | null;
  entities: MfdbEntityCheck[];
  errors: string[];
  warnings: string[];
}

export function isMfdb132Package(doc: MfdbChunkedDoc): boolean {
  return (
    doc.Format_Version === "104a" &&
    doc.Schema_Name === "MFDB-132" &&
    doc.Package_Format === "MFDB-Chunked-104a" &&
    !!doc.MFDB_Version &&
    !!doc.DB_Name
  );
}

export function validateMfdb132Package(doc: MfdbChunkedDoc): MfdbPackageValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];

  if (!isMfdb132Package(doc)) {
    errors.push(
      "Document is not a recognized MFDB-132 package (missing/incorrect " +
        "Schema_Name/Package_Format/MFDB_Version/DB_Name)."
    );
    return { valid: false, errors, warnings };
  }

  if (JSON.stringify(doc.Records_Type) !== JSON.stringify(["MFDB-132"])) {
    errors.push("Records_Type must be exactly ['MFDB-132'] for an MFDB-132 package.");
  }

  const fields = doc.Fields || [];
  const fm: Record<string, number> = {};
  fields.forEach((f, i) => (fm[f.name] = i));

  let manifestFound = false;
  for (const row of doc.Values || []) {
    if (row[fm["Relative_Path"]] === MFDB_MANIFEST_FILENAME) {
      manifestFound = true;
      break;
    }
  }

  if (!manifestFound) {
    errors.push(
      `Chunked package does not contain the MFDB manifest (${MFDB_MANIFEST_FILENAME}) — ` +
        "not a complete MFDB package."
    );
  }

  return { valid: errors.length === 0, errors, warnings };
}

function _findRowByRelPath(doc: MfdbChunkedDoc, relPath: string): any[] | null {
  const fields = doc.Fields || [];
  const fm: Record<string, number> = {};
  fields.forEach((f, i) => (fm[f.name] = i));
  const relIdx = fm["Relative_Path"];
  if (relIdx === undefined) return null;
  for (const row of doc.Values || []) {
    if (row[relIdx] === relPath) return row;
  }
  return null;
}

export function detectMfdbInChunk(doc: MfdbChunkedDoc): MfdbInChunkDetection {
  const result: MfdbInChunkDetection = {
    mfdb_detected: false,
    valid: false,
    db_name: null,
    mfdb_version: null,
    entities: [],
    errors: [],
    warnings: [],
  };

  const fields = doc.Fields || [];
  const fm: Record<string, number> = {};
  fields.forEach((f, i) => (fm[f.name] = i));
  const required = ["Relative_Path", "File_Content", "Is_Binary"];
  if (required.some((k) => fm[k] === undefined)) {
    result.errors.push("Chunk document is missing required Chunked-104 fields.");
    return result;
  }

  const manifestRow = _findRowByRelPath(doc, MFDB_MANIFEST_FILENAME);
  if (manifestRow === null) {
    result.errors.push(`No manifest (${MFDB_MANIFEST_FILENAME}) found in chunk — no MFDB present.`);
    return result;
  }

  if (manifestRow[fm["Is_Binary"]]) {
    result.errors.push("Manifest row is flagged Is_Binary — its content was never stored, cannot validate.");
    return result;
  }

  let manifestDoc: any;
  try {
    manifestDoc = JSON.parse(manifestRow[fm["File_Content"]]);
  } catch (e: any) {
    result.errors.push(`Manifest content is not valid JSON: ${e.message}`);
    return result;
  }

  result.mfdb_detected = true;
  result.db_name = manifestDoc.DB_Name ?? null;
  result.mfdb_version = manifestDoc.MFDB_Version ?? null;

  if (manifestDoc.Format_Version !== "104a") {
    result.errors.push("Manifest Format_Version must be '104a'.");
  }
  if (JSON.stringify(manifestDoc.Records_Type) !== JSON.stringify(["mfdb"])) {
    result.errors.push("Manifest Records_Type must be exactly ['mfdb'].");
  }

  const manifestFields: MfdbFieldDef[] = manifestDoc.Fields || [];
  const manifestFm: Record<string, number> = {};
  manifestFields.forEach((f, i) => (manifestFm[f.name] = i));
  if (manifestFm["entity_name"] === undefined || manifestFm["file_path"] === undefined) {
    result.errors.push("Manifest Fields must include 'entity_name' and 'file_path'.");
    return result;
  }

  const seenEntityNames = new Set<string>();
  const seenFilePaths = new Set<string>();

  for (const entityRow of manifestDoc.Values || []) {
    const entityName = entityRow[manifestFm["entity_name"]];
    const filePath = entityRow[manifestFm["file_path"]];
    const entityResult: MfdbEntityCheck = {
      entity_name: entityName,
      file_path: filePath,
      found_in_chunk: false,
      valid: false,
      errors: [],
    };

    if (!entityName || !filePath) {
      entityResult.errors.push("entity_name/file_path must not be null.");
    }
    if (seenEntityNames.has(entityName)) {
      entityResult.errors.push(`Duplicate entity_name '${entityName}' in manifest.`);
    }
    if (seenFilePaths.has(filePath)) {
      entityResult.errors.push(`Duplicate file_path '${filePath}' in manifest.`);
    }
    seenEntityNames.add(entityName);
    seenFilePaths.add(filePath);

    const entityChunkRow = _findRowByRelPath(doc, filePath);
    if (entityChunkRow === null) {
      entityResult.errors.push(`Entity file '${filePath}' listed in manifest was not found in chunk.`);
      result.entities.push(entityResult);
      continue;
    }

    entityResult.found_in_chunk = true;
    if (entityChunkRow[fm["Is_Binary"]]) {
      entityResult.errors.push("Entity row is flagged Is_Binary — content was never stored, cannot validate.");
      result.entities.push(entityResult);
      continue;
    }

    let entityDoc: any;
    try {
      entityDoc = JSON.parse(entityChunkRow[fm["File_Content"]]);
    } catch (e: any) {
      entityResult.errors.push(`Entity file content is not valid JSON: ${e.message}`);
      result.entities.push(entityResult);
      continue;
    }

    if (entityDoc.Format_Version !== "104") {
      entityResult.errors.push("Entity Format_Version must be '104'.");
    }
    if (JSON.stringify(entityDoc.Records_Type) !== JSON.stringify([entityName])) {
      entityResult.errors.push(`Entity Records_Type must be exactly ['${entityName}'].`);
    }
    if (!("Parent_Hierarchy" in entityDoc)) {
      entityResult.errors.push("Entity is missing mandatory 'Parent_Hierarchy' key.");
    }

    entityResult.valid = entityResult.errors.length === 0;
    result.entities.push(entityResult);
  }

  result.valid = result.errors.length === 0 && result.entities.every((e) => e.valid);
  return result;
}


// ==========================================================================
// SECTION 7 — MFDB CORE
// Sources: mfdb_core v2.2.0 (structural logic) + MFDB_CORE_CODES from
// bejson_types v2.4.0 (57-60 defined there, not in mfdb_core.ts itself — M-01)
// ==========================================================================


// ---------------------------------------------------------------------------
// MFDBArchive Interface (v1.3
// ---------------------------------------------------------------------------

/**
 * Handles .mfdb.zip packaging and virtual mounting using File System Access API.
 */
export interface MFDBArchiveInterface {
  /**
   * Mounts a .mfdb.zip file into a FileSystemDirectoryHandle.
   */
  mount(zipFile: File | Blob, dirHandle: any): Promise<string>;

  /**
   * Repacks a FileSystemDirectoryHandle back into a .mfdb.zip Blob.
   */
  commit(dirHandle: any): Promise<Blob>;
}

// ---------------------------------------------------------------------------
// Manifest factory
// ---------------------------------------------------------------------------

export type NetworkRole = "Master" | "Slave" | "Standalone";

export interface CreateManifestOptions extends MFDBDatabaseMeta {
  includeOptionalFields?: boolean;
  network_role?: NetworkRole;   // "Master" | "Slave" | "Standalone" (default)
}

export function createManifest(opts: CreateManifestOptions): BEJSONDocument {
  if (!opts.db_name || opts.db_name.trim() === "") {
    throw new MFDBCoreError(MFDB_CORE_CODES.MISSING_DB_NAME, "DB_Name is required when creating a manifest.");
  }

  const includeOptional = opts.includeOptionalFields !== false;
  const networkRole: NetworkRole = opts.network_role ?? "Standalone";

  const fields: BEJSONField[] = [
    { name: "entity_name", type: "string" },
    { name: "file_path", type: "string" },
  ];
  if (includeOptional) {
    fields.push(
      { name: "description", type: "string" },
      { name: "record_count", type: "integer" },
      { name: "schema_version", type: "string" },
      { name: "primary_key", type: "string" }
    );
  }

  const customHeaders: Record<string, string> = {
    MFDB_Version:  opts.mfdb_version ?? "1.31",
    Network_Role:  networkRole,
    DB_Name:       opts.db_name,
  };
  if (opts.db_description) customHeaders["DB_Description"] = opts.db_description;
  if (opts.schema_version) customHeaders["Schema_Version"] = opts.schema_version;
  if (opts.author)         customHeaders["Author"]         = opts.author;
  if (opts.created_at)     customHeaders["Created_At"]     = opts.created_at;

  return createEmpty104a("mfdb", fields, customHeaders);
}

// ---------------------------------------------------------------------------
// Entity registration
// ---------------------------------------------------------------------------

export function registerEntity(
  manifest: BEJSONDocument,
  record: MFDBManifestRecord
): BEJSONDocument {
  _assertManifest(manifest);

  const existing = decodeManifestRecords(manifest);
  if (existing.some((r) => r.entity_name === record.entity_name)) {
    throw new MFDBCoreError(
      MFDB_CORE_CODES.DUPLICATE_ENTITY_NAME,
      "Entity \"" + record.entity_name + "\" is already registered."
    );
  }

  const fieldNames = manifest.Fields.map((f) => f.name);
  const row: BEJSONValue[] = fieldNames.map((name) => {
    switch (name) {
      case "entity_name": return record.entity_name;
      case "file_path": return record.file_path;
      case "description": return record.description ?? null;
      case "record_count": return record.record_count ?? null;
      case "schema_version": return record.schema_version ?? null;
      case "primary_key": return record.primary_key ?? null;
      default: return null;
    }
  });

  return appendRecord(manifest, row);
}

export function unregisterEntity(
  manifest: BEJSONDocument,
  entityName: string
): BEJSONDocument {
  _assertManifest(manifest);
  const idx = _findEntityIndex(manifest, entityName);
  return deleteRecord(manifest, idx);
}

export function syncRecordCount(
  manifest: BEJSONDocument,
  entityName: string,
  count: number
): BEJSONDocument {
  _assertManifest(manifest);
  const idx = _findEntityIndex(manifest, entityName);

  try {
    getFieldIndex(manifest, "record_count");
  } catch {
    throw new MFDBCoreError(
      MFDB_CORE_CODES.RECORD_COUNT_SYNC_FAILED,
      "Manifest lacks \"record_count\" field."
    );
  }

  return setFieldValue(manifest, idx, "record_count", count);
}

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

function _assertManifest(doc: BEJSONDocument): void {
  if (!doc) {
    throw new MFDBCoreError(MFDB_CORE_CODES.NULL_MANIFEST, "Manifest is null or undefined.");
  }
}

function _findEntityIndex(manifest: BEJSONDocument, entityName: string): number {
  const enIdx = getFieldIndex(manifest, "entity_name");
  for (let i = 0; i < manifest.Values.length; i++) {
    if (manifest.Values[i][enIdx] === entityName) return i;
  }
  throw new MFDBCoreError(
    MFDB_CORE_CODES.ENTITY_NOT_IN_MANIFEST,
    "Entity \"" + entityName + "\" not found."
  );
}

// ---------------------------------------------------------------------------
// Federated Master / Slave node system
// ---------------------------------------------------------------------------
// Network_Role is now emitted on createManifest. This block wires the full
// runtime federation protocol. Node.js I/O functions (push/poll/distill)
// require the fs module — they throw at call-time if run in a browser.

export interface ConnectedSlaveSchema {
  slave_id:           string;
  label:              string;
  url:                string;
  role:               string;
  status:             string;
  supported_entities: string[];
}

export const CONNECTED_SLAVE_SCHEMA: BEJSONField[] = [
  { name: "slave_id",           type: "string" },
  { name: "label",              type: "string" },
  { name: "url",                type: "string" },
  { name: "role",               type: "string" },
  { name: "status",             type: "string" },
  { name: "supported_entities", type: "array"  },
];

/**
 * Register a ConnectedSlave entity in a Master manifest.
 * Throws if the manifest's Network_Role !== "Master".
 */
export function createConnectedSlaveEntity(manifest: BEJSONDocument): BEJSONDocument {
  const role = (manifest as any)["Network_Role"] ?? "";
  if (role !== "Master") {
    throw new MFDBCoreError(
      MFDB_CORE_CODES.INVALID_OPERATION ?? "INVALID_OPERATION",
      `ConnectedSlave may only be created on a Master node. Got: '${role}'`
    );
  }
  return registerEntity(manifest, {
    entity_name:    "ConnectedSlave",
    file_path:      "data/connectedslave.bejson",
    description:    "Registry of Slave nodes connected to this Master.",
    primary_key:    "slave_id",
    record_count:   0,
    schema_version: "1.0",
  });
}

export interface FederationPushResult { success: boolean; error?: string; }
export interface FederationPollOptions { pollInterval?: number; timeout?: number; }
export interface FederationDistillOptions { maxRows?: number; }

/**
 * Master → Slave atomic drop-zone push (Node.js only).
 * Writes configDoc to slaveTargetPath via same-dir temp + rename.
 */
export function federationPushConfig(
  configDoc: Record<string, unknown>,
  slaveTargetPath: string
): FederationPushResult {
  const fs   = require("fs");
  const path = require("path");
  const dest    = path.resolve(slaveTargetPath);
  const destDir = path.dirname(dest);
  fs.mkdirSync(destDir, { recursive: true });
  const tempPath = `${dest}.tmp.${Date.now()}`;
  try {
    fs.writeFileSync(tempPath, JSON.stringify(configDoc, null, 2), "utf8");
    fs.renameSync(tempPath, dest);
    return { success: true };
  } catch (err: any) {
    if (fs.existsSync(tempPath)) try { fs.unlinkSync(tempPath); } catch (_) {}
    return { success: false, error: err.message };
  }
}

/**
 * Slave: poll a local dropzone for incoming Master config docs (Node.js only).
 * Each .bejson file found is parsed, passed to callback, then removed.
 * Returns a getter that returns the count of configs processed so far.
 */
export function federationPollDropzone(
  dropzoneDir: string,
  callback: (filePath: string, doc: Record<string, unknown>) => void,
  { pollInterval = 2000, timeout = 60000 }: FederationPollOptions = {}
): () => number {
  const fs   = require("fs");
  const path = require("path");
  fs.mkdirSync(dropzoneDir, { recursive: true });

  let processed = 0;
  const deadline = Date.now() + timeout;

  const tick = () => {
    if (Date.now() >= deadline) return;
    const files: string[] = fs.readdirSync(dropzoneDir)
      .filter((f: string) => f.endsWith(".bejson"))
      .sort()
      .map((f: string) => path.join(dropzoneDir, f));

    for (const fpath of files) {
      try {
        const doc = JSON.parse(fs.readFileSync(fpath, "utf8"));
        callback(fpath, doc);
        fs.unlinkSync(fpath);
        processed++;
      } catch (e: any) {
        console.warn(`[MFDB_FEDERATION] poll_dropzone skipped ${fpath}: ${e.message}`);
      }
    }
    setTimeout(tick, pollInterval);
  };

  tick();
  return () => processed;
}

/**
 * Slave → Master one-way push (log distillation, Node.js only).
 * Overflow rows are pushed as a distilled summary to masterPollDir;
 * the local entity is truncated to maxRows.
 */
export function federationDistillLogs(
  slaveManifestPath: string,
  entityName: string,
  masterPollDir: string,
  { maxRows = 100 }: FederationDistillOptions = {}
): boolean {
  const fs   = require("fs");
  const path = require("path");

  const manifestDoc = JSON.parse(fs.readFileSync(slaveManifestPath, "utf8")) as BEJSONDocument;
  const records     = decodeManifestRecords(manifestDoc);
  const entry       = records.find(r => r.entity_name === entityName);
  if (!entry) {
    throw new MFDBCoreError(MFDB_CORE_CODES.ENTITY_NOT_IN_MANIFEST, `Entity '${entityName}' not found.`);
  }

  const entityPath = path.resolve(path.dirname(slaveManifestPath), entry.file_path);
  const entityDoc  = JSON.parse(fs.readFileSync(entityPath, "utf8")) as BEJSONDocument;
  const rows       = entityDoc.Values ?? [];

  if (rows.length <= maxRows) return true;

  const overflow = rows.slice(0, rows.length - maxRows);
  const kept     = rows.slice(rows.length - maxRows);

  fs.mkdirSync(masterPollDir, { recursive: true });
  // L-02: aligned to PY/SH format %Y%m%dT%H%M%SZ (was truncated ISO, e.g. "2026-08-16T1234Z")
  const ts   = new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d+Z$/, "Z");
  const dest = path.join(masterPollDir, `distilled_${entityName}_${ts}.bejson`);

  const summaryDoc = {
    Format: "BEJSON", Format_Version: "104a", Format_Creator: "Elton Boehnen",
    Distill_Source: entityName,
    Distill_Timestamp: new Date().toISOString(),
    Records_Type: ["DistilledLog"],
    Fields: entityDoc.Fields,
    Values: overflow,
  };

  const pushResult = federationPushConfig(summaryDoc, dest);
  if (!pushResult.success) return false;

  entityDoc.Values = kept;
  const tempEntity = entityPath + ".tmp." + Date.now();
  fs.writeFileSync(tempEntity, JSON.stringify(entityDoc, null, 2), "utf8");
  fs.renameSync(tempEntity, entityPath);

  const updatedManifest = syncRecordCount(manifestDoc, entityName, kept.length);
  const tempManifest    = slaveManifestPath + ".tmp." + Date.now();
  fs.writeFileSync(tempManifest, JSON.stringify(updatedManifest, null, 2), "utf8");
  fs.renameSync(tempManifest, slaveManifestPath);

  return true;
}

// ── Meta-GUID Debug Entity System (TypeScript) ─────────────────────────────────
// Full typed port of the Python/JS debug block. Node.js only — all functions
// that touch the filesystem silently no-op outside Node.

export const META_DEBUG_FIELDS: BEJSONField[] = [
  { name: "timestamp",     type: "string"  },
  { name: "operation",     type: "string"  },
  { name: "target_entity", type: "string"  },
  { name: "field_name",    type: "string"  },
  { name: "field_exists",  type: "boolean" },
  { name: "row_index",     type: "integer" },
  { name: "success",       type: "boolean" },
  { name: "duration_ms",   type: "integer" },
  { name: "pid",           type: "integer" },
  { name: "notes",         type: "string"  },
];

export interface MetaDebugRow {
  timestamp:     string;
  operation:     string;
  target_entity: string;
  field_name:    string | null;
  field_exists:  boolean | null;
  row_index:     number | null;
  success:       boolean;
  duration_ms:   number;
  pid:           number;
  notes:         string;
}

export interface MetaLogOptions {
  fieldName?:  string | null;
  fieldExists?: boolean | null;
  rowIndex?:   number | null;
  success?:    boolean;
  durationMs?: number;
  notes?:      string;
  readsOnly?:  boolean;
}

export interface DebugSummary {
  total_ops:         number;
  unique_entities:   string[];
  failed_ops:        number;
  schema_drift_hits: number;
  top_3_slowest:     { op: string; entity: string; duration_ms: number }[];
  reads_logged:      number;
  writes_logged:     number;
  ops_by_type:       Record<string, number>;
}

export interface SchemaDriftEntry {
  added_fields:   string[];
  removed_fields: string[];
  drifted:        boolean;
}

export interface EnableDebugOptions {
  rowCap?:     number;
  debugReads?: boolean;
}

function _debugIsEnabled(manifestPath: string): boolean {
  try {
    const doc = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
    return String(doc.Debug_Mode ?? "false").toLowerCase() === "true";
  } catch { return false; }
}

function _debugReadsEnabled(manifestPath: string): boolean {
  try {
    const doc = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
    return String(doc.Debug_Reads ?? "false").toLowerCase() === "true";
  } catch { return false; }
}

function _debugGetMetaName(manifestPath: string): string | null {
  try {
    const doc = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
    return doc.Debug_Meta_Entity || null;
  } catch { return null; }
}

function _debugGetEntityPath(manifestPath: string, entityName: string): string {
  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8")) as BEJSONDocument;
  const records  = decodeManifestRecords(manifest);
  const entry    = records.find(r => r.entity_name === entityName);
  if (!entry) throw new MFDBCoreError(MFDB_CORE_CODES.ENTITY_NOT_IN_MANIFEST, `Entity '${entityName}' not found`);
  return path.resolve(path.dirname(manifestPath), entry.file_path);
}

function _debugAtomicWrite(filePath: string, doc: unknown): void {
  const temp = `${filePath}.tmp.${Date.now()}`;
  fs.writeFileSync(temp, JSON.stringify(doc, null, 2), "utf8");
  fs.renameSync(temp, filePath);
}

function _metaAutoTrim(manifestPath: string, metaName: string, metaPath: string): void {
  try {
    const cap  = parseInt(JSON.parse(fs.readFileSync(manifestPath, "utf8")).Debug_Row_Cap ?? "500", 10);
    const doc  = JSON.parse(fs.readFileSync(metaPath, "utf8")) as BEJSONDocument;
    if ((doc.Values ?? []).length > cap) {
      doc.Values = doc.Values!.slice(-cap);
      _debugAtomicWrite(metaPath, doc);
    }
  } catch { /* non-fatal */ }
}

function _metaSchemaSnapshot(manifestPath: string, metaName: string): void {
  try {
    const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8")) as BEJSONDocument;
    const records  = decodeManifestRecords(manifest);
    for (const rec of records) {
      const ename = rec.entity_name;
      if (!ename || ename === metaName) continue;
      try {
        const edoc   = JSON.parse(fs.readFileSync(_debugGetEntityPath(manifestPath, ename), "utf8")) as BEJSONDocument;
        const fields = (edoc.Fields ?? []).map((f: BEJSONField) => f.name).join(",");
        _metaLog(manifestPath, "SCHEMA_SNAPSHOT", ename, {
          fieldName: fields, fieldExists: true, durationMs: 0,
          notes: `field_count=${(edoc.Fields ?? []).length}`,
        });
      } catch { /* skip unreadable entities */ }
    }
  } catch { /* non-fatal */ }
}

export function _metaLog(
  manifestPath: string,
  operation:    string,
  targetEntity: string,
  opts: MetaLogOptions = {}
): void {
  const {
    fieldName = null, fieldExists = null, rowIndex = null,
    success = true, durationMs = 0, notes = "", readsOnly = false,
  } = opts;

  try {
    if (!_debugIsEnabled(manifestPath)) return;
    if (readsOnly && !_debugReadsEnabled(manifestPath)) return;

    const metaName = _debugGetMetaName(manifestPath);
    if (!metaName) return;

    const metaPath = _debugGetEntityPath(manifestPath, metaName);
    const doc      = JSON.parse(fs.readFileSync(metaPath, "utf8")) as BEJSONDocument;
    doc.Values     = doc.Values ?? [];
    doc.Values.push([
      new Date().toISOString(), operation, targetEntity,
      fieldName, fieldExists, rowIndex, success, durationMs,
      process.pid, notes ?? "",
    ]);
    _debugAtomicWrite(metaPath, doc);
    _metaAutoTrim(manifestPath, metaName, metaPath);
  } catch { /* debug must never break the caller */ }
}

// ── Public Debug API (TS) ──────────────────────────────────────────────────────

export function enableDebug(
  manifestPath: string,
  { rowCap = 500, debugReads = false }: EnableDebugOptions = {}
): string {
  const crypto = require("crypto");
  const doc    = JSON.parse(fs.readFileSync(manifestPath, "utf8")) as BEJSONDocument;

  const metaName: string = (doc as any).Debug_Meta_Entity || `meta-${crypto.randomUUID()}`;
  (doc as any).Debug_Mode        = "true";
  (doc as any).Debug_Meta_Entity = metaName;
  (doc as any).Debug_Row_Cap     = String(rowCap);
  (doc as any).Debug_Reads       = debugReads ? "true" : "false";
  _debugAtomicWrite(manifestPath, doc);

  const metaFpRel = `data/${metaName}.bejson`;
  const metaAbs   = path.resolve(path.dirname(manifestPath), metaFpRel);

  if (!fs.existsSync(metaAbs)) {
    fs.mkdirSync(path.dirname(metaAbs), { recursive: true });
    const metaDoc = {
      Format: "BEJSON", Format_Version: "104", Format_Creator: "Elton Boehnen",
      Parent_Hierarchy: path.relative(path.dirname(metaAbs), manifestPath),
      Records_Type: [metaName],
      Fields: META_DEBUG_FIELDS, Values: [],
    };
    _debugAtomicWrite(metaAbs, metaDoc);

    const doc2    = JSON.parse(fs.readFileSync(manifestPath, "utf8")) as BEJSONDocument;
    const records = decodeManifestRecords(doc2);
    if (!records.find(r => r.entity_name === metaName)) {
      doc2.Values = doc2.Values ?? [];
      doc2.Values.push([metaName, metaFpRel, "Debug audit log (auto-generated)", 0, "1.0", null]);
      _debugAtomicWrite(manifestPath, doc2);
    }
  }

  _metaSchemaSnapshot(manifestPath, metaName);
  return metaName;
}

export function disableDebug(manifestPath: string): void {
  const doc = JSON.parse(fs.readFileSync(manifestPath, "utf8")) as BEJSONDocument;
  (doc as any).Debug_Mode = "false";
  _debugAtomicWrite(manifestPath, doc);
}

export function getDebugLog(manifestPath: string): MetaDebugRow[] {
  const metaName = _debugGetMetaName(manifestPath);
  if (!metaName) return [];
  try {
    const doc = JSON.parse(fs.readFileSync(_debugGetEntityPath(manifestPath, metaName), "utf8")) as BEJSONDocument;
    const fm: Record<string, number> = {};
    (doc.Fields ?? META_DEBUG_FIELDS).forEach((f: BEJSONField, i: number) => { fm[f.name] = i; });
    return (doc.Values ?? []).map((row: unknown[]) => {
      const out: Record<string, unknown> = {};
      for (const [k, i] of Object.entries(fm)) out[k] = row[i];
      return out as unknown as MetaDebugRow;
    });
  } catch { return []; }
}

export function getFailedOps(manifestPath: string): MetaDebugRow[] {
  return getDebugLog(manifestPath)
    .filter(r => r.success === false)
    .sort((a, b) => (a.timestamp > b.timestamp ? 1 : -1));
}

export function clearDebugLog(manifestPath: string): number {
  const metaName = _debugGetMetaName(manifestPath);
  if (!metaName) return 0;
  try {
    const metaPath = _debugGetEntityPath(manifestPath, metaName);
    const doc      = JSON.parse(fs.readFileSync(metaPath, "utf8")) as BEJSONDocument;
    const deleted  = (doc.Values ?? []).length;
    doc.Values     = [];
    _debugAtomicWrite(metaPath, doc);
    return deleted;
  } catch { return 0; }
}

export function debugSummary(manifestPath: string): DebugSummary | Record<string, never> {
  if (!_debugIsEnabled(manifestPath)) return {};
  const rows = getDebugLog(manifestPath);
  if (!rows.length) return { total_ops: 0 } as unknown as DebugSummary;

  const writeOps  = new Set(["ADD", "REMOVE", "UPDATE", "UPDATE_BULK"]);
  const opsByType: Record<string, number> = {};
  for (const r of rows) opsByType[r.operation] = (opsByType[r.operation] ?? 0) + 1;

  return {
    total_ops:         rows.length,
    unique_entities:   [...new Set(rows.map(r => r.target_entity))].sort(),
    failed_ops:        rows.filter(r => r.success === false).length,
    schema_drift_hits: rows.filter(r => r.field_exists === false).length,
    top_3_slowest:     [...rows]
      .sort((a, b) => b.duration_ms - a.duration_ms).slice(0, 3)
      .map(r => ({ op: r.operation, entity: r.target_entity, duration_ms: r.duration_ms })),
    reads_logged:  rows.filter(r => r.operation === "READ").length,
    writes_logged: rows.filter(r => writeOps.has(r.operation)).length,
    ops_by_type:   opsByType,
  };
}

export function detectSchemaDrift(manifestPath: string): Record<string, SchemaDriftEntry> {
  if (!_debugIsEnabled(manifestPath)) return {};
  const rows = getDebugLog(manifestPath);
  const snapshots: Record<string, Set<string>> = {};
  for (const r of rows) {
    if (r.operation === "SCHEMA_SNAPSHOT" && r.field_name) {
      snapshots[r.target_entity] = new Set(r.field_name.split(",").filter(Boolean));
    }
  }
  if (!Object.keys(snapshots).length) return {};

  const report: Record<string, SchemaDriftEntry> = {};
  for (const [ename, snapFields] of Object.entries(snapshots)) {
    try {
      const edoc       = JSON.parse(fs.readFileSync(_debugGetEntityPath(manifestPath, ename), "utf8")) as BEJSONDocument;
      const liveFields = new Set((edoc.Fields ?? []).map((f: BEJSONField) => f.name));
      const added      = [...liveFields].filter(f => !snapFields.has(f)).sort();
      const removed    = [...snapFields].filter(f => !liveFields.has(f)).sort();
      report[ename]    = { added_fields: added, removed_fields: removed, drifted: !!(added.length || removed.length) };
    } catch { /* skip */ }
  }
  return report;
}
