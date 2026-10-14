import React, { useEffect, useState } from 'react';

export interface TargetProtein {
  id: string;
  name: string;
  gene_symbol: string;
  uniprot_id: string;
  chembl_id: string;
  pdb_id: string;
  disease_domain: string;
  indication: string;
  active_site_residues: string[];
  default_threshold_pic50: number;
  description: string;
  model_ready: boolean;
}

interface TargetSelectorProps {
  selectedTarget: string;
  onSelectTarget: (targetId: string) => void;
  className?: string;
}

const FALLBACK_TARGETS: TargetProtein[] = [
  {
    id: 'EGFR',
    name: 'Epidermal Growth Factor Receptor',
    gene_symbol: 'EGFR',
    uniprot_id: 'P00533',
    chembl_id: 'CHEMBL203',
    pdb_id: '1M17',
    disease_domain: 'Oncology',
    indication: 'Non-Small Cell Lung Cancer & Glioblastoma',
    active_site_residues: ['Met793', 'Thr790', 'Lys745'],
    default_threshold_pic50: 7.0,
    description: 'Receptor tyrosine kinase driving cell proliferation.',
    model_ready: true,
  },
  {
    id: 'KRAS',
    name: 'GTPase KRas (G12D/G12C)',
    gene_symbol: 'KRAS',
    uniprot_id: 'P01116',
    chembl_id: 'CHEMBL2189121',
    pdb_id: '6OIM',
    disease_domain: 'Oncology',
    indication: 'Pancreatic, Colorectal & NSCLC Cancers',
    active_site_residues: ['Cys12', 'Asp12', 'Lys16'],
    default_threshold_pic50: 6.5,
    description: 'Key driver oncogene target for RAS inhibitors.',
    model_ready: true,
  },
  {
    id: 'BACE1',
    name: 'Beta-Site APP Cleaving Enzyme 1',
    gene_symbol: 'BACE1',
    uniprot_id: 'P56817',
    chembl_id: 'CHEMBL4822',
    pdb_id: '1FKN',
    disease_domain: 'Neurodegeneration',
    indication: "Alzheimer's Disease & Amyloid Pathology",
    active_site_residues: ['Asp32', 'Asp228', 'Thr72'],
    default_threshold_pic50: 6.8,
    description: 'Primary target for amyloid-beta reduction.',
    model_ready: true,
  },
  {
    id: 'HER2',
    name: 'Human EGF Receptor 2',
    gene_symbol: 'ERBB2',
    uniprot_id: 'P04626',
    chembl_id: 'CHEMBL1824',
    pdb_id: '3RCD',
    disease_domain: 'Oncology',
    indication: 'HER2+ Breast Cancer & Gastric Cancers',
    active_site_residues: ['Thr798', 'Met801', 'Lys753'],
    default_threshold_pic50: 7.0,
    description: 'Kinase off-target counter-screening partner.',
    model_ready: true,
  },
  {
    id: 'BRAF',
    name: 'Serine/Threonine-Protein Kinase B-Raf',
    gene_symbol: 'BRAF',
    uniprot_id: 'P15056',
    chembl_id: 'CHEMBL5145',
    pdb_id: '4EHE',
    disease_domain: 'Oncology',
    indication: 'Melanoma, Thyroid & Colorectal Cancers',
    active_site_residues: ['Val600', 'Glu600', 'Lys483'],
    default_threshold_pic50: 7.2,
    description: 'MAPK signaling pathway oncogene target.',
    model_ready: true,
  },
];

export const TargetSelector: React.FC<TargetSelectorProps> = ({
  selectedTarget,
  onSelectTarget,
  className = '',
}) => {
  const [targets, setTargets] = useState<TargetProtein[]>(FALLBACK_TARGETS);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/proteins/targets')
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setTargets(data);
        }
      })
      .catch(() => {});
  }, []);

  const activeInfo = targets.find((t) => t.id === selectedTarget) || targets[0];

  return (
    <div style={{ position: 'relative', display: 'inline-block' }} className={className}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <span
          style={{
            fontFamily: 'var(--font-gtstandardmono)',
            fontSize: 11,
            fontWeight: 700,
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            color: 'var(--color-graphite)',
          }}
        >
          TARGET PROTEIN:
        </span>
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 12,
            background: 'var(--color-paper-white)',
            border: '1.5px solid var(--color-ink-black)',
            borderRadius: 'var(--radius-full)',
            padding: '6px 16px',
            cursor: 'pointer',
            boxShadow: '0 4px 12px rgba(0,0,0,0.04)',
            transition: 'all 0.15s ease',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <span
              style={{
                width: 8,
                height: 8,
                borderRadius: '50%',
                background: 'var(--color-signal-orange)',
                display: 'inline-block',
              }}
            />
            <span
              style={{
                fontSize: 13,
                fontWeight: 700,
                color: 'var(--color-ink-black)',
                fontFamily: 'var(--font-gtstandardmono)',
              }}
            >
              {activeInfo?.id}
            </span>
            <span
              style={{
                fontSize: 11,
                color: 'var(--color-graphite)',
                fontFamily: 'var(--font-gtstandardmono)',
              }}
            >
              PDB: {activeInfo?.pdb_id}
            </span>
            <span
              style={{
                fontSize: 10,
                fontWeight: 700,
                textTransform: 'uppercase',
                padding: '2px 8px',
                borderRadius: 4,
                background:
                  activeInfo?.disease_domain === 'Neurodegeneration'
                    ? 'var(--color-sky-tint)'
                    : 'var(--color-cream-wash)',
                color: 'var(--color-ink-black)',
                border: '1px solid var(--color-ink-black)',
                fontFamily: 'var(--font-gtstandardmono)',
              }}
            >
              {activeInfo?.disease_domain}
            </span>
          </div>
          <span style={{ fontSize: 10, color: 'var(--color-graphite)' }}>{isOpen ? '▲' : '▼'}</span>
        </button>
      </div>

      {isOpen && (
        <div
          style={{
            position: 'absolute',
            right: 0,
            marginTop: 8,
            width: 340,
            zIndex: 100,
            background: 'var(--color-paper-white)',
            border: '2px solid var(--color-ink-black)',
            borderRadius: 'var(--radius-cards)',
            padding: 12,
            boxShadow: '0 12px 36px rgba(0,0,0,0.12)',
            animation: 'fadeIn 0.2s ease',
          }}
        >
          <div
            style={{
              fontFamily: 'var(--font-gtstandardmono)',
              fontSize: 11,
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: '0.06em',
              color: 'var(--color-graphite)',
              paddingBottom: 8,
              marginBottom: 8,
              borderBottom: '1px solid var(--color-lavender-mist)',
            }}
          >
            SELECT ACTIVE DISCOVERY TARGET
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6, maxHeight: 300, overflowY: 'auto' }}>
            {targets.map((target) => {
              const isSelected = target.id === selectedTarget;
              return (
                <button
                  key={target.id}
                  onClick={() => {
                    onSelectTarget(target.id);
                    setIsOpen(false);
                  }}
                  style={{
                    width: '100%',
                    textAlign: 'left',
                    borderRadius: 'var(--radius-cards)',
                    padding: 12,
                    background: isSelected ? 'var(--color-cream-wash)' : 'var(--color-faint-slate)',
                    border: isSelected ? '1.5px solid var(--color-ink-black)' : '1px solid var(--color-lavender-mist)',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: 4,
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <span
                        style={{
                          fontWeight: 700,
                          fontSize: 14,
                          color: 'var(--color-ink-black)',
                          fontFamily: 'var(--font-gtstandardmono)',
                        }}
                      >
                        {target.id}
                      </span>
                      <span
                        style={{
                          fontSize: 11,
                          color: 'var(--color-graphite)',
                          fontFamily: 'var(--font-gtstandardmono)',
                        }}
                      >
                        PDB: {target.pdb_id}
                      </span>
                    </div>
                    <span
                      style={{
                        fontSize: 10,
                        fontWeight: 700,
                        textTransform: 'uppercase',
                        padding: '2px 8px',
                        borderRadius: 4,
                        background: target.model_ready ? 'var(--color-sky-tint)' : 'var(--color-faint-slate)',
                        color: 'var(--color-ink-black)',
                        border: '1px solid var(--color-ink-black)',
                        fontFamily: 'var(--font-gtstandardmono)',
                      }}
                    >
                      {target.model_ready ? 'GNN Trained' : 'Training'}
                    </span>
                  </div>
                  <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--color-ink-black)' }}>
                    {target.name}
                  </div>
                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      fontSize: 11,
                      color: 'var(--color-graphite)',
                      marginTop: 2,
                    }}
                  >
                    <span>{target.indication}</span>
                    <span style={{ fontFamily: 'var(--font-gtstandardmono)', fontWeight: 700, color: 'var(--color-ink-black)' }}>
                      pIC50 ≥ {target.default_threshold_pic50}
                    </span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
