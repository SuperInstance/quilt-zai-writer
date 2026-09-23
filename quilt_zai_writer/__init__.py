"""quilt-zai-writer — creative canon writing via ZAI GLM-4.5.

Long-form canon essays through ZAI's reasoning + generation pipeline.
"""
from .writer import write_essay, write_pack

__version__ = "0.1.0"
__all__ = ["write_essay", "write_pack"]
