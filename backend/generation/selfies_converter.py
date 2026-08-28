import selfies as sf


def smiles_to_selfies(
    smiles: str
) -> str:

    return sf.encoder(
        smiles
    )


def selfies_to_smiles(
    selfies_string: str
) -> str:

    return sf.decoder(
        selfies_string
    )
