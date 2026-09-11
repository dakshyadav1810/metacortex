# verification/moe.py

from src.verification.source_matcher import source_matcher
from src.verification.hallucination_hunter import hallucination_hunter
from src.verification.logic_checker import logic_checker


class MoEVerifier:
    def __init__(self, llm):
        self.llm = llm

    def verify(self, path):
        if not source_matcher(path, self.llm):
            return False, "SourceMismatch"

        if not hallucination_hunter(path, self.llm):
            return False, "HallucinationDetected"

        if not logic_checker(path, self.llm):
            return False, "LogicalInconsistency"

        return True, "Verified"
