import pytest
import os
from backend.generation.variational_jtvae import VariationalJTVAE
from backend.generation.encoder_service import EncoderService

def test_vjtv_encoder_direct():
    encoder = VariationalJTVAE(latent_dim=128)
    test_selfies = "[C][C][O]"
    latent = encoder.encode(test_selfies)
    assert isinstance(latent, list)
    assert len(latent) == 128
    assert all(isinstance(x, float) for x in latent)

def test_vjtv_encoder_invalid_smiles():
    encoder = VariationalJTVAE(latent_dim=128)
    with pytest.raises(ValueError):
        encoder.encode("[InvalidSelfiesTokenXYZ]")

def test_encoder_service_integration():
    service = EncoderService()
    assert "vjtv" in service.available_encoders()
    latent = service.encode("[C][C][O]")
    assert len(latent) == 128
