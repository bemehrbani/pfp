/**
 * @file minab_web_hooks.ts
 * @description Production React integration hooks and state management utilities
 * for the PFP Web Platform (Memorial, Casualty Directory, and Mothers of Minab Campaign).
 * 
 * People for Peace & Justice ry (PFPJ ry)
 */

import { useState, useMemo, useCallback, useEffect } from 'react';
import type {
  Victim,
  MotherProfile,
  FamilyCluster,
  SourceReference,
  MinabIncidentDataset,
  VictimFilterOptions,
  VictimWithRelations,
  MotherWithRelations,
  FamilyClusterWithRelations
} from './minab_types';

/**
 * Hook to manage loading, caching, and state of the Minab incident dataset.
 */
export function useMinabDataset(datasetUrl = '/data/minab_incident_dataset.json') {
  const [data, setData] = useState<MinabIncidentDataset | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);

    fetch(datasetUrl)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then((json: MinabIncidentDataset) => {
        if (isMounted) {
          setData(json);
          setError(null);
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError(err instanceof Error ? err : new Error(String(err)));
        }
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [datasetUrl]);

  return { data, loading, error };
}

/**
 * Enriches victims with relational links to mothers and family clusters.
 */
export function useEnrichedVictims(dataset: MinabIncidentDataset | null): VictimWithRelations[] {
  return useMemo(() => {
    if (!dataset) return [];

    const mothersMap = new Map<string, MotherProfile>();
    dataset.mothers.forEach((m) => mothersMap.set(m.id, m));

    const clusterMap = new Map<string, FamilyCluster>();
    dataset.family_clusters.forEach((c) => clusterMap.set(c.cluster_id, c));

    const sourceMap = new Map<string, SourceReference>();
    dataset.sources.forEach((s) => sourceMap.set(s.id, s));

    return dataset.victims.map((v) => ({
      ...v,
      mother: v.mother_id ? mothersMap.get(v.mother_id) || null : null,
      family_cluster: v.family_cluster_id ? clusterMap.get(v.family_cluster_id) || null : null,
      resolved_sources: v.sources
        .map((sId) => sourceMap.get(sId))
        .filter((s): s is SourceReference => s !== undefined)
    }));
  }, [dataset]);
}

/**
 * Filter, search, and sort victims for memorial listings and casualty tables.
 */
export function useVictimFilter(
  victims: VictimWithRelations[],
  initialFilters: VictimFilterOptions = {}
) {
  const [filters, setFilters] = useState<VictimFilterOptions>(initialFilters);

  const filteredVictims = useMemo(() => {
    return victims.filter((v) => {
      // 1. Text search query (name EN, name FA, biography)
      if (filters.searchQuery && filters.searchQuery.trim() !== '') {
        const query = filters.searchQuery.toLowerCase().trim();
        const nameEn = v.full_name_en.toLowerCase();
        const nameFa = v.full_name_fa.toLowerCase();
        const bioText = typeof v.biography === 'object' && v.biography ? `${v.biography.en || ''} ${v.biography.fa || ''}`.toLowerCase() : '';

        const match = nameEn.includes(query) || nameFa.includes(query) || bioText.includes(query);
        if (!match) return false;
      }

      // 2. Role filter
      if (filters.role && filters.role !== 'all') {
        if (v.role !== filters.role) return false;
      }

      // 3. Status filter
      if (filters.status && filters.status !== 'all') {
        if (v.status !== filters.status) return false;
      }

      // 4. Gender filter
      if (filters.gender && filters.gender !== 'all') {
        if (v.gender !== filters.gender) return false;
      }

      // 5. Identification method filter
      if (filters.identificationMethod && filters.identificationMethod !== 'all') {
        if (v.identification_method !== filters.identificationMethod) return false;
      }

      // 6. Age bounds
      if (filters.minAge !== undefined && v.age !== null && v.age !== undefined) {
        if (v.age < filters.minAge) return false;
      }
      if (filters.maxAge !== undefined && v.age !== null && v.age !== undefined) {
        if (v.age > filters.maxAge) return false;
      }

      // 7. Cluster filter
      if (filters.clusterId && v.family_cluster_id !== filters.clusterId) {
        return false;
      }

      // 8. Mother filter
      if (filters.motherId && v.mother_id !== filters.motherId) {
        return false;
      }

      // 9. Photo availability
      if (filters.hasPhoto === true && !v.photo_url) {
        return false;
      }

      return true;
    });
  }, [victims, filters]);

  const updateFilter = useCallback((key: keyof VictimFilterOptions, value: unknown) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  }, []);

  const resetFilters = useCallback(() => {
    setFilters({});
  }, []);

  return {
    filters,
    filteredVictims,
    updateFilter,
    resetFilters,
    totalCount: victims.length,
    filteredCount: filteredVictims.length
  };
}

/**
 * Hook for mothers initiative showcase and testimonials.
 */
export function useMothersShowcase(dataset: MinabIncidentDataset | null): MotherWithRelations[] {
  return useMemo(() => {
    if (!dataset) return [];

    const victimMap = new Map<string, Victim>();
    dataset.victims.forEach((v) => victimMap.set(v.id, v));

    const clusterMap = new Map<string, FamilyCluster>();
    dataset.family_clusters.forEach((c) => clusterMap.set(c.cluster_id, c));

    const sourceMap = new Map<string, SourceReference>();
    dataset.sources.forEach((s) => sourceMap.set(s.id, s));

    return dataset.mothers.map((m) => ({
      ...m,
      children: m.children_ids
        .map((cId) => victimMap.get(cId))
        .filter((c): c is Victim => c !== undefined),
      family_cluster: m.family_cluster_id ? clusterMap.get(m.family_cluster_id) || null : null,
      resolved_sources: m.sources
        .map((sId) => sourceMap.get(sId))
        .filter((s): s is SourceReference => s !== undefined)
    }));
  }, [dataset]);
}

/**
 * Hook for family cluster visual breakdown and household impacts.
 */
export function useFamilyClusters(dataset: MinabIncidentDataset | null): FamilyClusterWithRelations[] {
  return useMemo(() => {
    if (!dataset) return [];

    const mothersMap = new Map<string, MotherProfile>();
    dataset.mothers.forEach((m) => mothersMap.set(m.id, m));

    const victimMap = new Map<string, Victim>();
    dataset.victims.forEach((v) => victimMap.set(v.id, v));

    const sourceMap = new Map<string, SourceReference>();
    dataset.sources.forEach((s) => sourceMap.set(s.id, s));

    return dataset.family_clusters.map((fc) => ({
      ...fc,
      mother: fc.mother_id ? mothersMap.get(fc.mother_id) || null : null,
      victims: fc.member_ids
        .map((id) => victimMap.get(id))
        .filter((v): v is Victim => v !== undefined),
      resolved_sources: (fc.sources || [])
        .map((sId) => sourceMap.get(sId))
        .filter((s): s is SourceReference => s !== undefined)
    }));
  }, [dataset]);
}
