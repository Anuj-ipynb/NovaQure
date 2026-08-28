import torch
from pathlib import Path
import json

# Import the VJTVAE implementation
import sys, os
sys.path.append(os.path.abspath('.'))
from backend.generation.variational_jtvae import VariationalJTVAE
import selfies as sf

# Paths
MODEL_PATH = Path('models/vjtv.pt')
METADATA_PATH = Path('models/vjtv_metadata.json')

def load_model():
    """Load the pretrained VJTVAE checkpoint and instantiate the model."""
    # Load the checkpoint (state dict) – it was saved via torch.save(model.state_dict())
    checkpoint = torch.load(MODEL_PATH, map_location='cpu')
    # The checkpoint may contain a full state dict or a dict with a 'model_state_dict' key.
    state_dict = checkpoint.get('model_state_dict', checkpoint)
    # Retrieve hyper‑parameters from metadata (latent_dim, hidden_dim, mp_steps)
    metadata = json.loads(METADATA_PATH.read_text())
    model = VariationalJTVAE(
        latent_dim=metadata.get('latent_dim', 128),
        hidden_dim=metadata.get('hidden_dim', 256),
        mp_steps=metadata.get('mp_steps', 2),
    )
    model.load_state_dict(state_dict)
    model.eval()
    return model

def encode_selfies(model, selfies_str: str):
    """Encode a SELFIES string and return the latent vector as a Python list."""
    try:
        latent = model.encode(selfies_str)
        return latent
    except Exception as e:
        print(f"[ERROR] Encoding failed for {selfies_str}: {e}")
        return None

def sanity_check():
    model = load_model()
    test_smiles = ["CCO", "c1ccccc1", "CC(N)C(=O)O"]
    print("=== VJTVAE Model Check ===")
    for smi in test_smiles:
        try:
            selfies_str = sf.encoder(smi)
        except Exception as e:
            print(f"[WARN] SELFIES conversion failed for {smi}: {e}")
            continue
        latent = encode_selfies(model, selfies_str)
        if latent is None:
            continue
        print(f"SMILES: {smi}\n  SELFIES: {selfies_str}\n  Latent dim: {len(latent)} | Sample values: {latent[:5]}\n")

def test_encoder_service():
    from backend.generation.encoder_service import EncoderService
    service = EncoderService()
    print("=== EncoderService Integration Check ===")
    print("Available encoders:", service.available_encoders())
    
    test_selfies = "[C][C][O]"
    vec_vjtv = service.encode(test_selfies, encoder="vjtv")
    print(f"Encoded '{test_selfies}' via 'vjtv': len={len(vec_vjtv)} | values={vec_vjtv[:5]}")

if __name__ == "__main__":
    sanity_check()
    test_encoder_service()
