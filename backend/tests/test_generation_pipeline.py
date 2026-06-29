from backend.generation.generation_service import (
    GenerationService
)

from backend.generation.generation_validator import (
    GenerationValidator
)


def test_generation_pipeline():

    molecules = (
        GenerationService()
        .run()
    )

    GenerationValidator.validate(
        molecules
    )

    assert len(
        molecules
    ) > 0
