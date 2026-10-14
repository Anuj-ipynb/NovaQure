/**
 * Sanitize SMILES strings before rendering in UI labels or 3Dmol/RDKit parsers.
 * Replaces explicit valence non-canonical markers like [NH1] with standard aromatic [nH].
 */
export function sanitizeSmiles(smiles: string): string {
  if (!smiles || typeof smiles !== 'string') return '';
  return smiles
    .replace(/\[NH1\]/g, '[nH]')
    .replace(/\[NH\]/g, '[nH]')
    .replace(/\[NH2\]/g, 'NH2')
    .replace(/\[CH1\]/g, 'CH')
    .replace(/\[CH2\]/g, 'CH2');
}
