/**
 * @file minab_types.ts
 * @description Unified TypeScript interfaces and domain types for the Minab Incident data architecture.
 * Mirror of minab_data_model.json.
 * 
 * People for Peace & Justice ry (PFPJ ry)
 * Campaign: Justice for Minab Children & Mothers
 * Incident Date: February 28, 2026
 */

/**
 * Civic or educational role of an individual at the time of the airstrike.
 */
export type VictimRole =
  | 'student'
  | 'teacher'
  | 'staff'
  | 'parent'
  | 'community'
  | 'unborn_fetus';

/**
 * Casualty classification status for victims.
 */
export type CasualtyStatus = 'killed' | 'injured' | 'missing';

/**
 * Survival/casualty status for mothers of victims.
 */
export type MotherStatus = 'killed' | 'injured' | 'survived';

/**
 * Forensic or administrative methodology used to verify victim identity.
 */
export type IdentificationMethod =
  | 'visual'
  | 'dna'
  | 'personal_belongings'
  | 'unrecovered'
  | 'official_records'
  | 'eyewitness';

/**
 * Gender categorization.
 */
export type Gender = 'female' | 'male' | 'unknown' | 'other';

/**
 * Facial recognition or OCR matching confidence level.
 */
export type MatchConfidence = 'HIGH' | 'MEDIUM' | 'LOW' | 'MANUAL_VERIFIED';

/**
 * Evidence verification hierarchy tiers.
 * - Tier 1: Primary / Forensic / Court-admissible evidence
 * - Tier 2: Official military / Government admissions / 15-6 investigations
 * - Tier 3: Verified OSINT / Independent investigative media (Bellingcat, BBC Verify)
 * - Tier 4: Eyewitness testimonies / Local reporting
 */
export type SourceTier =
  | 1
  | 2
  | 3
  | 4
  | '1'
  | '2'
  | '3'
  | '4'
  | 'tier_1'
  | 'tier_2'
  | 'tier_3'
  | 'tier_4'
  | 'Tier 1'
  | 'Tier 2'
  | 'Tier 3'
  | 'Tier 4'
  | 'primary_legal_evidence'
  | 'official_investigation'
  | 'verified_osint'
  | 'media_report'
  | 'witness_testimony';

/**
 * Multilingual text record supporting Persian, English, and Arabic.
 */
export interface MultilingualText {
  /** English text / translation */
  en: string;
  /** Persian (Farsi) original text */
  fa?: string;
  /** Arabic translation */
  ar?: string;
}

/**
 * Physical and digital coordinates on the 100-child memorial mosaic grid.
 */
export interface PhotoGridCoordinates {
  /** 0-based sequential index on the 100-child memorial mosaic (0-99) */
  grid_index?: number | null;
  /** Border index number matching the official visual roster */
  border_index?: number | string | null;
  /** Row index in the visual mosaic grid layout */
  row?: number | null;
  /** Column index in the visual mosaic grid layout */
  col?: number | null;
  /** Standardized filename of the portrait (e.g. Asma_Zakeri_41.jpg) */
  filename?: string | null;
  /** Confidence rating of name-to-photo extraction */
  match_confidence?: MatchConfidence | null;
}

/**
 * Geographic WGS84 coordinates.
 */
export interface IncidentCoordinates {
  /** Latitude in decimal degrees (-90.0 to 90.0) */
  latitude: number;
  /** Longitude in decimal degrees (-180.0 to 180.0) */
  longitude: number;
}

/**
 * Evidence citation or reference source documenting incident details and victim profiles.
 */
export interface SourceReference {
  /** Unique source identifier (e.g., 'SRC-001', 'EVD-MUN-002') */
  id: string;
  /** Headline or title of the cited document / report */
  title: string;
  /** Publishing agency, news outlet, or court archive (e.g. 'CENTCOM', 'BBC Verify') */
  outlet: string;
  /** URL or digital permalink to the source */
  url?: string | null;
  /** Publication date in ISO format (YYYY-MM-DD) */
  publication_date?: string | null;
  /** Verification tier of the source */
  tier: SourceTier;
  /** Normalized reliability score from 0.0 to 1.0 */
  reliability_score: number;
  /** Contextual notes or evidentiary notes */
  notes?: string | null;
  /** Cryptographic SHA-256 hash of the evidence archive file */
  archive_hash?: string | null;
}

/**
 * Recorded oral history quote or sworn testimony from a mother.
 */
export interface MotherQuote {
  /** English translation of the testimony */
  quote_en: string;
  /** Original Persian quote transcript */
  quote_fa?: string | null;
  /** Date testimony was recorded (YYYY-MM-DD) */
  date?: string | null;
  /** Setting/context (e.g., 'Vigil speech', 'Deposition') */
  context?: string | null;
  /** Foreign key referencing the recording SourceReference.id */
  source_id?: string | null;
}

/**
 * Individual record of a direct victim, casualty, or survivor of the Minab strike.
 */
export interface Victim {
  /** Unique identifier (e.g., 'VIC-001', 'asma-zakeri') */
  id: string;
  /** Full standardized name in Latin transliteration */
  full_name_en: string;
  /** Full official name in Persian (Farsi) */
  full_name_fa: string;
  /** Father's first name */
  father_name?: string | null;
  /** Foreign key reference to MotherProfile.id */
  mother_id?: string | null;
  /** Age in years at the time of the incident (null for unborn fetus or unknown) */
  age?: number | null;
  /** Age in months (used for infants or developmental tracking) */
  age_months?: number | null;
  /** Gender of the victim */
  gender?: Gender | null;
  /** Civic or educational role */
  role: VictimRole;
  /** Classroom or school grade designation (e.g., 'Grade 1', 'Grade 3B') */
  grade_or_class?: string | null;
  /** Casualty status */
  status: CasualtyStatus;
  /** Identification method used to confirm identity */
  identification_method: IdentificationMethod;
  /** Final resting place / cemetery */
  burial_location?: string | null;
  /** URL or relative path to portrait photo */
  photo_url?: string | null;
  /** Mosaic coordinates or layout position */
  photo_grid?: PhotoGridCoordinates | string | null;
  /** Multilingual biographical summary, dreams, personal stories */
  biography?: MultilingualText | string | null;
  /** Foreign key reference to FamilyCluster.cluster_id */
  family_cluster_id?: string | null;
  /** Array of SourceReference.id strings referencing supporting evidence */
  sources: string[];
  /** Detailed medical or physical injuries description */
  injuries_description?: string | null;
  /** Date of martyrdom/death (YYYY-MM-DD) */
  date_of_death?: string | null;
}

/**
 * Comprehensive profile of a mother affected by the Minab incident.
 */
export interface MotherProfile {
  /** Unique identifier (e.g., 'MOM-001', 'mother-zakeri') */
  id: string;
  /** Full standardized name in Latin transliteration */
  full_name_en: string;
  /** Full official name in Persian (Farsi) */
  full_name_fa: string;
  /** Spouse's full name */
  spouse_name?: string | null;
  /** True if the mother was herself killed or injured */
  is_casualty: boolean;
  /** Mother's personal casualty status */
  status: MotherStatus;
  /** Mother's profession or occupation */
  profession?: string | null;
  /** Narrative summary of her family, bereavement, and advocacy */
  narrative_summary?: MultilingualText | string | null;
  /** Recorded quotes and testimonies */
  quotes?: Array<MotherQuote | string>;
  /** Foreign keys of her children (each must exist in Victim registry) */
  children_ids: string[];
  /** Foreign keys of other family members */
  other_family_member_ids?: string[];
  /** Portrait photo path or URL */
  photo_url?: string | null;
  /** Foreign key reference to FamilyCluster.cluster_id */
  family_cluster_id?: string | null;
  /** Array of SourceReference.id strings referencing evidence */
  sources: string[];
}

/**
 * Aggregated family unit documenting intergenerational loss.
 */
export interface FamilyCluster {
  /** Unique family cluster identifier (e.g., 'FAM-001', 'cluster-zakeri') */
  cluster_id: string;
  /** Family surname in Latin script */
  family_surname_en: string;
  /** Family surname in Persian (Farsi) script */
  family_surname_fa: string;
  /** Foreign key reference to matriarch MotherProfile.id */
  mother_id?: string | null;
  /** Total count of family members killed */
  total_killed: number;
  /** Total count of family members injured */
  total_injured: number;
  /** List of all Victim.id and MotherProfile.id members belonging to this household */
  member_ids: string[];
  /** Description of household loss and background */
  description?: MultilingualText | string | null;
  /** Residential neighborhood or district in Minab */
  neighborhood_or_residence?: string | null;
  /** Array of SourceReference.id strings documenting the cluster */
  sources?: string[];
}

/**
 * Core factual metadata and chronology of the airstrike incident.
 */
export interface IncidentMetadata {
  /** Canonical incident identifier (e.g., 'MINAB-2026-0228') */
  incident_id: string;
  /** Official incident title in English */
  incident_name_en: string;
  /** Official incident title in Persian */
  incident_name_fa: string;
  /** Incident date in ISO format (YYYY-MM-DD) */
  incident_date: string;
  /** Approximate local strike time (e.g., '08:45 IRST') */
  incident_time_local?: string | null;
  /** Target school facility name in English */
  target_facility_en: string;
  /** Target school facility name in Persian */
  target_facility_fa: string;
  /** City name */
  city: string;
  /** Province name */
  province: string;
  /** Country name */
  country: string;
  /** Target coordinates */
  coordinates: IncidentCoordinates;
  /** Forensic weapon system identified */
  weapon_system: string;
  /** Responsible military command / unit */
  responsible_force?: string | null;
  /** Applicable legal evidentiary standard */
  legal_standard_of_proof: string;
  /** Multilingual overview summary */
  summary?: MultilingualText | null;
}

/**
 * Aggregate casualty statistics.
 */
export interface DatasetSummaryStats {
  total_estimated_killed?: number;
  total_documented_victims?: number;
  total_documented_mothers?: number;
  total_family_clusters?: number;
  total_sources_cited?: number;
}

/**
 * Top-level Unified Minab Incident Dataset.
 */
export interface MinabIncidentDataset {
  /** Factual incident metadata */
  incident_metadata: IncidentMetadata;
  /** Evidence citations and source registry */
  sources: SourceReference[];
  /** Direct victim registry */
  victims: Victim[];
  /** Mothers of victims registry */
  mothers: MotherProfile[];
  /** Aggregated family bereavement clusters */
  family_clusters: FamilyCluster[];
  /** Summary statistics */
  summary_stats?: DatasetSummaryStats;
  /** Semantic version of data release (e.g. '1.0.0') */
  version?: string;
  /** Timestamp of last export / validation */
  last_updated?: string;
}

/* ========================================================================= */
/* COMPOSITE & UI INTEGRATION TYPES                                          */
/* ========================================================================= */

/**
 * Enriched Victim record with resolved Mother and FamilyCluster relations.
 */
export interface VictimWithRelations extends Victim {
  mother?: MotherProfile | null;
  family_cluster?: FamilyCluster | null;
  resolved_sources?: SourceReference[];
}

/**
 * Enriched MotherProfile record with resolved Child and Family relations.
 */
export interface MotherWithRelations extends MotherProfile {
  children?: Victim[];
  family_cluster?: FamilyCluster | null;
  resolved_sources?: SourceReference[];
}

/**
 * Enriched FamilyCluster with resolved Member records.
 */
export interface FamilyClusterWithRelations extends FamilyCluster {
  mother?: MotherProfile | null;
  victims?: Victim[];
  resolved_sources?: SourceReference[];
}

/**
 * Filter parameters for querying victims in the PFP Web Platform.
 */
export interface VictimFilterOptions {
  searchQuery?: string;
  role?: VictimRole | 'all';
  status?: CasualtyStatus | 'all';
  gender?: Gender | 'all';
  identificationMethod?: IdentificationMethod | 'all';
  minAge?: number;
  maxAge?: number;
  grade?: string;
  hasPhoto?: boolean;
  clusterId?: string;
  motherId?: string;
}

/* ========================================================================= */
/* CSV EXPORT FLAT ROW SCHEMAS                                               */
/* ========================================================================= */

/**
 * Flat structure for Victim CSV export.
 */
export interface VictimCsvRow {
  id: string;
  full_name_en: string;
  full_name_fa: string;
  father_name: string;
  mother_id: string;
  age: string;
  gender: string;
  role: string;
  grade_or_class: string;
  status: string;
  identification_method: string;
  burial_location: string;
  photo_url: string;
  grid_index: string;
  border_index: string;
  biography_en: string;
  biography_fa: string;
  family_cluster_id: string;
  sources: string;
  injuries_description: string;
  date_of_death: string;
}

/**
 * Flat structure for MotherProfile CSV export.
 */
export interface MotherCsvRow {
  id: string;
  full_name_en: string;
  full_name_fa: string;
  spouse_name: string;
  is_casualty: string;
  status: string;
  profession: string;
  narrative_summary_en: string;
  narrative_summary_fa: string;
  children_ids: string;
  children_count: number;
  other_family_member_ids: string;
  family_cluster_id: string;
  sources: string;
}

/**
 * Flat structure for FamilyCluster CSV export.
 */
export interface FamilyClusterCsvRow {
  cluster_id: string;
  family_surname_en: string;
  family_surname_fa: string;
  mother_id: string;
  total_killed: number;
  total_injured: number;
  member_count: number;
  member_ids: string;
  description_en: string;
  description_fa: string;
  neighborhood_or_residence: string;
  sources: string;
}

/**
 * Flat structure for SourceReference CSV export.
 */
export interface SourceCsvRow {
  id: string;
  title: string;
  outlet: string;
  url: string;
  publication_date: string;
  tier: string;
  reliability_score: number;
  notes: string;
  archive_hash: string;
}

/* ========================================================================= */
/* VALIDATION RESULT TYPES                                                   */
/* ========================================================================= */

export type ValidationSeverity = 'ERROR' | 'WARNING' | 'INFO';

export interface ValidationIssue {
  severity: ValidationSeverity;
  code: string;
  entityType: 'victim' | 'mother' | 'family_cluster' | 'source' | 'metadata' | 'general';
  entityId?: string;
  field?: string;
  message: string;
  details?: Record<string, unknown>;
}

export interface ValidationSummaryReport {
  isValid: boolean;
  totalErrors: number;
  totalWarnings: number;
  totalVictims: number;
  totalMothers: number;
  totalFamilyClusters: number;
  totalSources: number;
  foreignKeyIntegrity: {
    orphanedVictimMothers: number;
    orphanedMotherChildren: number;
    orphanedClusterMothers: number;
    orphanedClusterMembers: number;
    unresolvedSources: number;
  };
  issues: ValidationIssue[];
}

/* ========================================================================= */
/* RUNTIME TYPE GUARDS & UTILITIES                                           */
/* ========================================================================= */

/**
 * Type guard for Victim entity.
 */
export function isVictim(obj: unknown): obj is Victim {
  if (!obj || typeof obj !== 'object') return false;
  const v = obj as Record<string, unknown>;
  return (
    typeof v.id === 'string' &&
    typeof v.full_name_en === 'string' &&
    typeof v.full_name_fa === 'string' &&
    typeof v.role === 'string' &&
    typeof v.status === 'string' &&
    typeof v.identification_method === 'string' &&
    Array.isArray(v.sources)
  );
}

/**
 * Type guard for MotherProfile entity.
 */
export function isMotherProfile(obj: unknown): obj is MotherProfile {
  if (!obj || typeof obj !== 'object') return false;
  const m = obj as Record<string, unknown>;
  return (
    typeof m.id === 'string' &&
    typeof m.full_name_en === 'string' &&
    typeof m.full_name_fa === 'string' &&
    typeof m.is_casualty === 'boolean' &&
    typeof m.status === 'string' &&
    Array.isArray(m.children_ids) &&
    Array.isArray(m.sources)
  );
}

/**
 * Type guard for FamilyCluster entity.
 */
export function isFamilyCluster(obj: unknown): obj is FamilyCluster {
  if (!obj || typeof obj !== 'object') return false;
  const f = obj as Record<string, unknown>;
  return (
    typeof f.cluster_id === 'string' &&
    typeof f.family_surname_en === 'string' &&
    typeof f.family_surname_fa === 'string' &&
    typeof f.total_killed === 'number' &&
    typeof f.total_injured === 'number' &&
    Array.isArray(f.member_ids)
  );
}

/**
 * Type guard for SourceReference entity.
 */
export function isSourceReference(obj: unknown): obj is SourceReference {
  if (!obj || typeof obj !== 'object') return false;
  const s = obj as Record<string, unknown>;
  return (
    typeof s.id === 'string' &&
    typeof s.title === 'string' &&
    typeof s.outlet === 'string' &&
    (typeof s.tier === 'string' || typeof s.tier === 'number') &&
    typeof s.reliability_score === 'number'
  );
}

/**
 * Type guard for full MinabIncidentDataset.
 */
export function isMinabIncidentDataset(obj: unknown): obj is MinabIncidentDataset {
  if (!obj || typeof obj !== 'object') return false;
  const d = obj as Record<string, unknown>;
  return (
    d.incident_metadata !== undefined &&
    Array.isArray(d.sources) &&
    Array.isArray(d.victims) &&
    Array.isArray(d.mothers) &&
    Array.isArray(d.family_clusters)
  );
}

/**
 * Extract localized text helper.
 */
export function getLocalizedText(
  field: MultilingualText | string | null | undefined,
  lang: 'en' | 'fa' | 'ar' = 'en'
): string {
  if (!field) return '';
  if (typeof field === 'string') return field;
  return field[lang] || field.en || '';
}

/**
 * Flatten Victim record for CSV export.
 */
export function victimToCsvRow(victim: Victim): VictimCsvRow {
  let gridIndex = '';
  let borderIndex = '';
  if (victim.photo_grid && typeof victim.photo_grid === 'object') {
    gridIndex = victim.photo_grid.grid_index !== undefined && victim.photo_grid.grid_index !== null ? String(victim.photo_grid.grid_index) : '';
    borderIndex = victim.photo_grid.border_index !== undefined && victim.photo_grid.border_index !== null ? String(victim.photo_grid.border_index) : '';
  } else if (typeof victim.photo_grid === 'string') {
    gridIndex = victim.photo_grid;
  }

  const bioEn = typeof victim.biography === 'object' && victim.biography ? victim.biography.en || '' : (typeof victim.biography === 'string' ? victim.biography : '');
  const bioFa = typeof victim.biography === 'object' && victim.biography ? victim.biography.fa || '' : '';

  return {
    id: victim.id,
    full_name_en: victim.full_name_en,
    full_name_fa: victim.full_name_fa,
    father_name: victim.father_name || '',
    mother_id: victim.mother_id || '',
    age: victim.age !== undefined && victim.age !== null ? String(victim.age) : '',
    gender: victim.gender || '',
    role: victim.role,
    grade_or_class: victim.grade_or_class || '',
    status: victim.status,
    identification_method: victim.identification_method,
    burial_location: victim.burial_location || '',
    photo_url: victim.photo_url || '',
    grid_index: gridIndex,
    border_index: borderIndex,
    biography_en: bioEn,
    biography_fa: bioFa,
    family_cluster_id: victim.family_cluster_id || '',
    sources: victim.sources.join('; '),
    injuries_description: victim.injuries_description || '',
    date_of_death: victim.date_of_death || '2026-02-28',
  };
}

/**
 * Flatten MotherProfile record for CSV export.
 */
export function motherToCsvRow(mother: MotherProfile): MotherCsvRow {
  const summaryEn = typeof mother.narrative_summary === 'object' && mother.narrative_summary ? mother.narrative_summary.en || '' : (typeof mother.narrative_summary === 'string' ? mother.narrative_summary : '');
  const summaryFa = typeof mother.narrative_summary === 'object' && mother.narrative_summary ? mother.narrative_summary.fa || '' : '';

  return {
    id: mother.id,
    full_name_en: mother.full_name_en,
    full_name_fa: mother.full_name_fa,
    spouse_name: mother.spouse_name || '',
    is_casualty: mother.is_casualty ? 'YES' : 'NO',
    status: mother.status,
    profession: mother.profession || '',
    narrative_summary_en: summaryEn,
    narrative_summary_fa: summaryFa,
    children_ids: mother.children_ids.join('; '),
    children_count: mother.children_ids.length,
    other_family_member_ids: (mother.other_family_member_ids || []).join('; '),
    family_cluster_id: mother.family_cluster_id || '',
    sources: mother.sources.join('; '),
  };
}

/**
 * Flatten FamilyCluster record for CSV export.
 */
export function familyClusterToCsvRow(cluster: FamilyCluster): FamilyClusterCsvRow {
  const descEn = typeof cluster.description === 'object' && cluster.description ? cluster.description.en || '' : (typeof cluster.description === 'string' ? cluster.description : '');
  const descFa = typeof cluster.description === 'object' && cluster.description ? cluster.description.fa || '' : '';

  return {
    cluster_id: cluster.cluster_id,
    family_surname_en: cluster.family_surname_en,
    family_surname_fa: cluster.family_surname_fa,
    mother_id: cluster.mother_id || '',
    total_killed: cluster.total_killed,
    total_injured: cluster.total_injured,
    member_count: cluster.member_ids.length,
    member_ids: cluster.member_ids.join('; '),
    description_en: descEn,
    description_fa: descFa,
    neighborhood_or_residence: cluster.neighborhood_or_residence || '',
    sources: (cluster.sources || []).join('; '),
  };
}

/**
 * Flatten SourceReference record for CSV export.
 */
export function sourceToCsvRow(source: SourceReference): SourceCsvRow {
  return {
    id: source.id,
    title: source.title,
    outlet: source.outlet,
    url: source.url || '',
    publication_date: source.publication_date || '',
    tier: String(source.tier),
    reliability_score: source.reliability_score,
    notes: source.notes || '',
    archive_hash: source.archive_hash || '',
  };
}
