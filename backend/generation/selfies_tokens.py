from __future__ import annotations

"""
Shared SELFIES token vocabularies used by the
mutation operators.

Keeping these centralized ensures every mutator
uses a consistent chemical vocabulary.
"""

# Atom/Bond substitutions
REPLACEMENT_TOKENS = (
    "[C]",
    "[O]",
    "[N]",
    "[F]",
    "[=C]",
)

# Insertions
INSERTION_TOKENS = (
    "[C]",
    "[O]",
    "[N]",
    "[F]",
    "[=C]",
)

# Topology modifications
BRANCH_TOKENS = (
    "[Branch1]",
)