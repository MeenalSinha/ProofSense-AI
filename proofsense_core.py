"""
ProofSense AI - Core Engine (Standalone)
Can be imported and used without Streamlit
"""

import json
import re
from typing import List, Dict, Tuple
import numpy as np
from dataclasses import dataclass, asdict
from datetime import datetime

# Knowledge base simulation
KNOWLEDGE_BASE = {
    "general": [
        "The Earth orbits around the Sun in approximately 365.25 days.",
        "Photosynthesis is the process by which plants convert sunlight into energy.",
        "The speed of light in vacuum is approximately 299,792,458 meters per second.",
        "DNA contains the genetic instructions for the development of living organisms.",
        "The capital of France is Paris, which is located in the northern part of the country.",
        "Water boils at 100 degrees Celsius at sea level under standard atmospheric pressure.",
        "The human body has 206 bones in adults.",
        "The Internet was initially developed as ARPANET in the 1960s by the US Department of Defense.",
        "Shakespeare wrote approximately 37 plays during his lifetime.",
        "The Pacific Ocean is the largest ocean on Earth, covering about 165 million square kilometers."
    ],
    "finance": [
        "Compound interest is calculated on the initial principal and accumulated interest from previous periods.",
        "The stock market operates through exchanges where buyers and sellers trade shares of publicly held companies.",
        "Diversification is a risk management strategy that mixes different investments within a portfolio.",
        "The Federal Reserve is the central banking system of the United States, established in 1913.",
        "A credit score typically ranges from 300 to 850, with higher scores indicating better creditworthiness.",
        "Market capitalization is calculated by multiplying a company's share price by its total number of outstanding shares.",
        "Treasury bonds are debt securities issued by the US Department of Treasury.",
        "The S&P 500 is a stock market index tracking the performance of 500 large companies listed on US exchanges.",
        "Inflation represents the rate at which the general level of prices for goods and services rises.",
        "A recession is typically defined as two consecutive quarters of negative GDP growth."
    ],
    "health": [
        "The human heart pumps approximately 5 liters of blood per minute at rest.",
        "Regular exercise can reduce the risk of chronic diseases including heart disease and diabetes.",
        "The recommended daily water intake varies by individual but is often cited as about 8 glasses per day.",
        "Vitamin D is produced by the body when skin is exposed to sunlight.",
        "The immune system protects the body against infectious diseases and foreign invaders.",
        "Sleep is essential for cognitive function, with most adults requiring 7-9 hours per night.",
        "Vaccines work by training the immune system to recognize and combat specific pathogens.",
        "The human brain contains approximately 86 billion neurons.",
        "Regular hand washing is one of the most effective ways to prevent the spread of infectious diseases.",
        "Mental health is as important as physical health and requires proper attention and care."
    ]
}

@dataclass
class Claim:
    text: str
    confidence_score: float
    risk_level: str
    evidence: List[str]
    warnings: List[str]
    explanation: str
    
    def to_dict(self):
        return asdict(self)

@dataclass
class VerificationResult:
    original_answer: str
    claims: List[Claim]
    overall_score: float
    total_claims: int
    verified_claims: int
    flagged_claims: int
    evidence_coverage: float
    risk_distribution: Dict[str, int]
    
    def to_dict(self):
        return {
            "original_answer": self.original_answer,
            "claims": [claim.to_dict() for claim in self.claims],
            "overall_score": self.overall_score,
            "total_claims": self.total_claims,
            "verified_claims": self.verified_claims,
            "flagged_claims": self.flagged_claims,
            "evidence_coverage": self.evidence_coverage,
            "risk_distribution": self.risk_distribution,
        }

class ProofSenseEngine:
    """Core verification engine for ProofSense AI"""
    
    def __init__(self, domain: str = "general"):
        self.domain = domain
        self.knowledge_base = KNOWLEDGE_BASE.get(domain, KNOWLEDGE_BASE["general"])
        
        # Overconfident language patterns
        self.overconfident_patterns = [
            r'\balways\b', r'\bnever\b', r'\bguaranteed\b', r'\bcertainly\b',
            r'\bdefinitely\b', r'\bimpossible\b', r'\bno doubt\b', r'\bwithout question\b',
            r'\b100%\b', r'\babsolutely\b', r'\bundoubtedly\b', r'\binevitably\b'
        ]
        
    def extract_claims(self, text: str) -> List[str]:
        """Break text into atomic factual claims"""
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        
        claims = []
        for sentence in sentences:
            if len(sentence.strip()) > 10:
                sub_claims = re.split(r',\s*(?:and|but|however|moreover)\s+', sentence)
                claims.extend([c.strip() for c in sub_claims if len(c.strip()) > 10])
        
        return claims
    
    def calculate_similarity(self, claim: str, evidence: str) -> float:
        """Simple similarity calculation"""
        claim_words = set(claim.lower().split())
        evidence_words = set(evidence.lower().split())
        
        stop_words = {'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'is', 'are', 'was', 'were'}
        claim_words -= stop_words
        evidence_words -= stop_words
        
        if not claim_words or not evidence_words:
            return 0.0
        
        intersection = claim_words & evidence_words
        union = claim_words | evidence_words
        
        return len(intersection) / len(union) if union else 0.0
    
    def retrieve_evidence(self, claim: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Retrieve relevant evidence from knowledge base"""
        evidence_scores = []
        
        for evidence in self.knowledge_base:
            similarity = self.calculate_similarity(claim, evidence)
            if similarity > 0.1:
                evidence_scores.append((evidence, similarity))
        
        evidence_scores.sort(key=lambda x: x[1], reverse=True)
        return evidence_scores[:top_k]
    
    def detect_overconfident_language(self, claim: str) -> List[str]:
        """Detect overconfident or absolute language"""
        warnings = []
        claim_lower = claim.lower()
        
        for pattern in self.overconfident_patterns:
            matches = re.findall(pattern, claim_lower)
            if matches:
                warnings.append(f"Overconfident language detected: '{matches[0]}'")
        
        return warnings
    
    def calculate_claim_score(self, claim: str, evidence_list: List[Tuple[str, float]]) -> Tuple[float, str]:
        """Calculate confidence score for a single claim"""
        if not evidence_list:
            return 0.0, "high"
        
        best_match_score = evidence_list[0][1] if evidence_list else 0.0
        source_count_factor = min(len(evidence_list) / 3, 1.0)
        avg_evidence_score = np.mean([score for _, score in evidence_list]) if evidence_list else 0.0
        
        confidence_score = (
            best_match_score * 0.5 +
            source_count_factor * 0.3 +
            avg_evidence_score * 0.2
        ) * 100
        
        if confidence_score >= 70:
            risk_level = "verified"
        elif confidence_score >= 50:
            risk_level = "low"
        elif confidence_score >= 30:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        return confidence_score, risk_level
    
    def generate_explanation(self, claim: str, score: float, evidence_list: List[Tuple[str, float]], 
                           warnings: List[str]) -> str:
        """Generate human-readable explanation"""
        if score >= 70:
            explanation = f"✅ This claim is well-supported with strong evidence (verifiability confidence: {score:.1f}/100)."
        elif score >= 50:
            explanation = f"⚠️ This claim has moderate support but could benefit from additional verification (verifiability confidence: {score:.1f}/100)."
        elif score >= 30:
            explanation = f"⚠️ This claim has weak support in available sources (verifiability confidence: {score:.1f}/100). Exercise caution."
        else:
            explanation = f"❌ This claim lacks supporting evidence in retrieved sources (verifiability confidence: {score:.1f}/100). High risk of hallucination."
        
        if not evidence_list:
            explanation += " No matching evidence found in prototype evidence store."
        elif len(evidence_list) < 2:
            explanation += " Limited supporting sources found."
        
        if warnings:
            explanation += f" Additionally, {len(warnings)} language warning(s) detected."
        
        return explanation
    
    def verify_answer(self, answer: str) -> VerificationResult:
        """Main verification pipeline"""
        claim_texts = self.extract_claims(answer)
        
        verified_claims = []
        risk_counts = {"verified": 0, "low": 0, "medium": 0, "high": 0}
        
        for claim_text in claim_texts:
            evidence_list = self.retrieve_evidence(claim_text)
            score, risk_level = self.calculate_claim_score(claim_text, evidence_list)
            warnings = self.detect_overconfident_language(claim_text)
            explanation = self.generate_explanation(claim_text, score, evidence_list, warnings)
            
            claim = Claim(
                text=claim_text,
                confidence_score=score,
                risk_level=risk_level,
                evidence=[ev for ev, _ in evidence_list],
                warnings=warnings,
                explanation=explanation
            )
            
            verified_claims.append(claim)
            risk_counts[risk_level] += 1
        
        overall_score = np.mean([c.confidence_score for c in verified_claims]) if verified_claims else 0.0
        verified_count = risk_counts["verified"] + risk_counts["low"]
        flagged_count = risk_counts["medium"] + risk_counts["high"]
        evidence_coverage = (verified_count / len(verified_claims) * 100) if verified_claims else 0.0
        
        return VerificationResult(
            original_answer=answer,
            claims=verified_claims,
            overall_score=overall_score,
            total_claims=len(verified_claims),
            verified_claims=verified_count,
            flagged_claims=flagged_count,
            evidence_coverage=evidence_coverage,
            risk_distribution=risk_counts
        )

# CLI interface for quick testing
if __name__ == "__main__":
    print("🔍 ProofSense AI - Core Engine Test\n")
    
    engine = ProofSenseEngine("general")
    
    test_text = "The Earth orbits the Sun in 365 days. The Internet was definitely invented in 1995 by Bill Gates."
    
    print(f"Testing: {test_text}\n")
    
    result = engine.verify_answer(test_text)
    
    print(f"Overall Score: {result.overall_score:.1f}/100")
    print(f"Total Claims: {result.total_claims}")
    print(f"Verified: {result.verified_claims} | Flagged: {result.flagged_claims}\n")
    
    for i, claim in enumerate(result.claims, 1):
        print(f"\nClaim {i}: {claim.text}")
        print(f"  Score: {claim.confidence_score:.1f}/100")
        print(f"  Risk: {claim.risk_level}")
        print(f"  Warnings: {len(claim.warnings)}")
        print(f"  Evidence: {len(claim.evidence)} sources")
