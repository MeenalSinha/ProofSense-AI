import streamlit as st
import json
import time
import re
from typing import List, Dict, Tuple
import numpy as np
from dataclasses import dataclass
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="ProofSense AI - Hallucination Detection",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Pastel gradient background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Glassmorphism sidebar */
    [data-testid="stSidebar"] {
        background: rgba(249, 229, 216, 0.7);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Headers with gradient */
    h1, h2, h3, h4, h5, h6 {
        color: #6A5D7B !important;
        font-weight: 700;
    }
    
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 900;
        margin: 1rem 0;
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.4);
        transition: all 0.3s ease;
        animation: fadeIn 0.6s ease-out;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Hero section with glassmorphism */
    .hero-section {
        background: linear-gradient(135deg, rgba(200, 184, 219, 0.6), rgba(163, 201, 168, 0.6));
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 3rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 2rem;
        animation: heroFadeIn 1s ease-out;
    }
    
    @keyframes heroFadeIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .hero-logo {
        font-size: 4rem;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .hero-title {
        color: white !important;
        font-size: 3.5rem;
        font-weight: 900;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .hero-subtitle {
        color: white;
        font-size: 1.5rem;
        font-weight: 400;
        opacity: 0.95;
    }
    
    /* Pastel buttons */
    .stButton>button {
        background: linear-gradient(135deg, #A3C9A8 0%, #B8D4BE 100%);
        color: white;
        border-radius: 15px;
        height: 3.5em;
        width: 100%;
        font-size: 1.1em;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 15px rgba(163, 201, 168, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #9EB5A5 0%, #B0C8B7 100%);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(163, 201, 168, 0.5);
    }
    
    .stButton>button:active {
        transform: translateY(0px);
    }
    
    /* Metric cards with glassmorphism */
    .metric-glass-card {
        background: linear-gradient(135deg, rgba(200, 184, 219, 0.7), rgba(212, 196, 232, 0.7));
        backdrop-filter: blur(15px);
        padding: 1.8rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .metric-glass-card:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 12px 40px rgba(200, 184, 219, 0.4);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 900;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.95rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Claim boxes with glassmorphism */
    .claim-box {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(15px);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    .claim-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .claim-high-risk {
        background: linear-gradient(135deg, rgba(255, 182, 193, 0.6), rgba(255, 160, 180, 0.6));
        border-left: 4px solid #ff4444;
    }
    
    .claim-medium-risk {
        background: linear-gradient(135deg, rgba(255, 237, 160, 0.6), rgba(255, 228, 140, 0.6));
        border-left: 4px solid #ff9800;
    }
    
    .claim-low-risk {
        background: linear-gradient(135deg, rgba(173, 216, 230, 0.6), rgba(153, 206, 220, 0.6));
        border-left: 4px solid #2196f3;
    }
    
    .claim-verified {
        background: linear-gradient(135deg, rgba(163, 201, 168, 0.6), rgba(143, 191, 148, 0.6));
        border-left: 4px solid #4caf50;
    }
    
    /* Score display with glassmorphism */
    .score-display {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        border: 2px solid rgba(255, 255, 255, 0.5);
        margin: 30px 0;
        animation: scaleIn 0.6s ease-out;
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Evidence boxes */
    .evidence-box {
        background: linear-gradient(135deg, rgba(230, 230, 250, 0.6), rgba(220, 220, 240, 0.6));
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 3px solid #667eea;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    /* Warning badges with glassmorphism */
    .warning-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 4px;
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    
    .warning-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    }
    
    .badge-red { 
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.8), rgba(255, 68, 68, 0.8));
        color: white; 
    }
    .badge-orange { 
        background: linear-gradient(135deg, rgba(255, 184, 77, 0.8), rgba(255, 152, 0, 0.8));
        color: white; 
    }
    .badge-blue { 
        background: linear-gradient(135deg, rgba(100, 181, 246, 0.8), rgba(33, 150, 243, 0.8));
        color: white; 
    }
    .badge-green { 
        background: linear-gradient(135deg, rgba(129, 199, 132, 0.8), rgba(76, 175, 80, 0.8));
        color: white; 
    }
    
    /* Info boxes with glassmorphism */
    .stAlert {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        color: #6A5D7B;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, rgba(163, 201, 168, 0.6), rgba(184, 212, 190, 0.6));
        color: white;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #A3C9A8, #B8D4BE) !important;
        color: white !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, rgba(200, 184, 219, 0.5), rgba(163, 201, 168, 0.5));
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 3rem;
        text-align: center;
        margin-top: 4rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Tech badge */
    .tech-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(163, 201, 168, 0.8), rgba(184, 212, 190, 0.8));
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        margin: 5px;
        font-size: 0.9rem;
        font-weight: 600;
        box-shadow: 0 2px 10px rgba(163, 201, 168, 0.3);
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Selectbox */
    .stSelectbox>div>div {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

def detect_claim_type(claim_text: str) -> Tuple[str, str]:
    """Detect claim type for visual badge"""
    text_lower = claim_text.lower()
    
    # Check for quantitative claims (numbers, percentages, measurements)
    if re.search(r'\d+\.?\d*\s*(?:%|percent|degrees|meters|dollars|years|days|hours|kg|km|miles|pounds)', text_lower):
        return "📊 Quantitative", "Contains numerical/measured data"
    
    # Check for causal claims (because, leads to, causes, results in)
    if re.search(r'\b(?:because|since|leads?\s+to|causes?|results?\s+in|due\s+to|therefore|thus|consequently)\b', text_lower):
        return "🧠 Causal", "Describes cause-effect relationships"
    
    # Default to factual
    return "📚 Factual", "States factual information"

def calculate_unsupported_ratio(result) -> float:
    """Calculate ratio of unsupported claims"""
    high_risk_claims = result.risk_distribution.get('high', 0)
    if result.total_claims == 0:
        return 0.0
    return (high_risk_claims / result.total_claims) * 100

# Knowledge base simulation (would be replaced with actual RAG/vector DB)
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
    claim_type: str = "📚 Factual"
    claim_type_desc: str = ""

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
        # Split by sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        
        claims = []
        for sentence in sentences:
            if len(sentence.strip()) > 10:  # Filter out very short fragments
                # Further split compound sentences with conjunctions
                sub_claims = re.split(r',\s*(?:and|but|however|moreover)\s+', sentence)
                claims.extend([c.strip() for c in sub_claims if len(c.strip()) > 10])
        
        return claims
    
    def calculate_similarity(self, claim: str, evidence: str) -> float:
        """Simple similarity calculation (in production, use embeddings)"""
        claim_words = set(claim.lower().split())
        evidence_words = set(evidence.lower().split())
        
        # Remove common stop words
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
            if similarity > 0.1:  # Threshold for relevance
                evidence_scores.append((evidence, similarity))
        
        # Sort by score and return top k
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
        
        # Factor 1: Best evidence match strength
        best_match_score = evidence_list[0][1] if evidence_list else 0.0
        
        # Factor 2: Number of supporting sources
        source_count_factor = min(len(evidence_list) / 3, 1.0)
        
        # Factor 3: Average evidence strength
        avg_evidence_score = np.mean([score for _, score in evidence_list]) if evidence_list else 0.0
        
        # Weighted combination
        confidence_score = (
            best_match_score * 0.5 +
            source_count_factor * 0.3 +
            avg_evidence_score * 0.2
        ) * 100
        
        # Determine risk level
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
        # Extract claims
        claim_texts = self.extract_claims(answer)
        
        verified_claims = []
        risk_counts = {"verified": 0, "low": 0, "medium": 0, "high": 0}
        
        for claim_text in claim_texts:
            # Retrieve evidence
            evidence_list = self.retrieve_evidence(claim_text)
            
            # Calculate score
            score, risk_level = self.calculate_claim_score(claim_text, evidence_list)
            
            # Detect warnings
            warnings = self.detect_overconfident_language(claim_text)
            
            # Detect claim type
            claim_type, claim_type_desc = detect_claim_type(claim_text)
            
            # Generate explanation
            explanation = self.generate_explanation(claim_text, score, evidence_list, warnings)
            
            # Create claim object
            claim = Claim(
                text=claim_text,
                confidence_score=score,
                risk_level=risk_level,
                evidence=[ev for ev, _ in evidence_list],
                warnings=warnings,
                explanation=explanation,
                claim_type=claim_type,
                claim_type_desc=claim_type_desc
            )
            
            verified_claims.append(claim)
            risk_counts[risk_level] += 1
        
        # Calculate overall metrics
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

def get_score_color(score: float) -> str:
    """Get color based on score"""
    if score >= 70:
        return "#4caf50"
    elif score >= 50:
        return "#2196f3"
    elif score >= 30:
        return "#ff9800"
    else:
        return "#ff4444"

def display_claim(claim: Claim, claim_num: int):
    """Display a single claim with all details"""
    risk_class = f"claim-{claim.risk_level}-risk" if claim.risk_level != "verified" else "claim-verified"
    
    st.markdown(f"""
    <div class="{risk_class} claim-box">
        <strong>Claim {claim_num}:</strong> {claim.text}
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        st.metric("Verifiability Confidence", f"{claim.confidence_score:.1f}/100")
    
    with col2:
        risk_badge_class = {
            "verified": "badge-green",
            "low": "badge-blue",
            "medium": "badge-orange",
            "high": "badge-red"
        }
        st.markdown(f"""
        <span class="warning-badge {risk_badge_class[claim.risk_level]}">
            {claim.risk_level.upper()} RISK
        </span>
        """, unsafe_allow_html=True)
        
        # Add claim type badge
        st.markdown(f"""
        <span class="warning-badge badge-blue" title="{claim.claim_type_desc}">
            {claim.claim_type}
        </span>
        """, unsafe_allow_html=True)
    
    with col3:
        if claim.warnings:
            for warning in claim.warnings:
                st.markdown(f"""
                <span class="warning-badge badge-orange">⚠️ {warning}</span>
                """, unsafe_allow_html=True)
    
    # Add "Why This Matters" tooltip for high-risk claims
    if claim.risk_level == "high":
        st.warning("⚠️ **Why This Matters:** High-risk claims can mislead users if acted upon. Always verify with authoritative sources before making decisions.")
    
    # Explanation
    st.info(claim.explanation)
    
    # Evidence
    if claim.evidence:
        with st.expander(f"📚 View Supporting Evidence ({len(claim.evidence)} sources from prototype evidence store)"):
            for i, evidence in enumerate(claim.evidence, 1):
                st.markdown(f"""
                <div class="evidence-box">
                    <strong>Evidence {i}:</strong> {evidence}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ No supporting evidence found in prototype evidence store (simulated RAG for demo)")
    
    st.markdown("---")

def generate_pdf_report(result: VerificationResult, domain: str) -> str:
    """Generate a mock PDF report (returns text content)"""
    report = f"""
ProofSense AI - Trust Verification Report
==========================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Domain: {domain.capitalize()}

OVERALL ASSESSMENT
------------------
Verifiability Confidence: {result.overall_score:.1f}/100
Total Claims Analyzed: {result.total_claims}
Verified Claims: {result.verified_claims}
Flagged Claims: {result.flagged_claims}
Evidence Coverage: {result.evidence_coverage:.1f}%

RISK DISTRIBUTION
-----------------
✅ Verified: {result.risk_distribution['verified']}
🔵 Low Risk: {result.risk_distribution['low']}
🟠 Medium Risk: {result.risk_distribution['medium']}
🔴 High Risk: {result.risk_distribution['high']}

ORIGINAL ANSWER
---------------
{result.original_answer}

DETAILED CLAIM ANALYSIS
-----------------------
"""
    
    for i, claim in enumerate(result.claims, 1):
        report += f"""
Claim {i}: {claim.text}
Confidence: {claim.confidence_score:.1f}/100
Risk Level: {claim.risk_level.upper()}
Explanation: {claim.explanation}
Evidence Sources: {len(claim.evidence)}
Warnings: {len(claim.warnings)}
"""
        if claim.warnings:
            for warning in claim.warnings:
                report += f"  - {warning}\n"
        report += "\n"
    
    report += """
---
This report was generated by ProofSense AI - Hallucination Detection System
For questions or concerns, please review the detailed analysis above.
"""
    
    return report

def main():
    # Hero Header Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-logo">🔍</div>
        <h1 class="hero-title">ProofSense AI</h1>
        <p class="hero-subtitle">Hallucination-Aware LLM Guardrail</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("ℹ️ **Important:** Scores represent verifiability confidence (evidence support), not factual correctness. Always verify critical information.")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Domain selection
        domain = st.selectbox(
            "Select Domain",
            ["general", "finance", "health"],
            help="Choose the knowledge domain for verification"
        )
        
        if domain == "health":
            st.warning("⚠️ Health information should be verified with qualified medical professionals.")
        
        st.markdown("---")
        
        # Sample queries
        st.subheader("📝 Sample Queries")
        
        sample_queries = {
            "general": [
                "The Earth orbits the Sun every 365 days and is the third planet from the Sun.",
                "Photosynthesis always occurs at night and plants use moonlight for energy.",
                "The Internet was definitely invented in 1995 by Bill Gates."
            ],
            "finance": [
                "Compound interest is calculated on principal and accumulated interest.",
                "The stock market is guaranteed to provide 20% annual returns without any risk.",
                "Credit scores range from 300 to 850, with higher scores indicating better creditworthiness."
            ],
            "health": [
                "The human heart pumps approximately 5 liters of blood per minute at rest.",
                "Drinking coffee always prevents all types of cancer without exception.",
                "Regular exercise can reduce the risk of chronic diseases including heart disease."
            ]
        }
        
        selected_sample = st.selectbox(
            "Load Sample Query",
            [""] + sample_queries[domain],
            help="Select a sample query to test"
        )
        
        st.markdown("---")
        
        # API mode info
        st.subheader("🔌 API Mode")
        st.caption("Mock API interface demonstrating integration capability")
        st.code("""
POST /api/verify
{
  "text": "Your text here",
  "domain": "general"
}
        """, language="json")
        st.caption("API integration available for wrapping other applications")
        
        st.markdown("---")
        st.info("💡 **Tip:** ProofSense works best with factual claims that can be verified against a prototype evidence store (simulated RAG).")
        st.caption("📚 Using prototype evidence store (simulated RAG for demo) - production would use real vector database with embeddings")
        st.caption("⚖️ **Important:** ProofSense evaluates evidence support, not factual correctness.")
    
    # Main interface tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Verification", "📊 Trust Dashboard", "📥 Export Report"])
    
    with tab1:
        st.subheader("Enter LLM Output for Verification")
        
        # Use sample if selected
        default_text = selected_sample if selected_sample else ""
        
        user_input = st.text_area(
            "Paste the AI-generated answer you want to verify:",
            value=default_text,
            height=150,
            placeholder="Enter or paste text here..."
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            verify_button = st.button("🔍 Verify Answer", type="primary", use_container_width=True)
        
        with col2:
            show_comparison = st.checkbox("Show Before/After", value=True)
        
        if verify_button and user_input:
            with st.spinner("🔄 Analyzing claims and retrieving evidence..."):
                # Simulate processing time
                time.sleep(1.5)
                
                # Initialize engine and verify
                engine = ProofSenseEngine(domain=domain)
                result = engine.verify_answer(user_input)
                
                # Store in session state
                st.session_state.verification_result = result
                st.session_state.domain = domain
            
            st.success("✅ Verification complete!")
        
        # Display results if available
        if 'verification_result' in st.session_state:
            result = st.session_state.verification_result
            
            st.markdown("---")
            
            # Overall Score Display
            score_color = get_score_color(result.overall_score)
            st.markdown(f"""
            <div class="score-display" style="background: linear-gradient(135deg, {score_color}22 0%, {score_color}44 100%); border: 3px solid {score_color};">
                <div style="color: {score_color};">Verifiability Confidence</div>
                <div style="color: {score_color}; font-size: 4rem;">{result.overall_score:.0f}/100</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Key metrics with glassmorphism
            st.markdown("### 📊 Key Metrics")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            unsupported_ratio = calculate_unsupported_ratio(result)
            
            metrics = [
                ("Total Claims", result.total_claims, "📝"),
                ("Verified", result.verified_claims, "✅"),
                ("Flagged", result.flagged_claims, "⚠️"),
                ("Evidence Coverage", f"{result.evidence_coverage:.0f}%", "📚"),
                ("Unsupported Claims", f"{unsupported_ratio:.0f}%", "🚨")
            ]
            
            for col, (label, value, emoji) in zip([col1, col2, col3, col4, col5], metrics):
                with col:
                    st.markdown(f"""
                    <div class="metric-glass-card">
                        <div style="font-size: 2rem;">{emoji}</div>
                        <div class="metric-value">{value}</div>
                        <div class="metric-label">{label}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Before/After Comparison
            if show_comparison:
                st.subheader("📊 Before vs After Comparison")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### ❌ Raw LLM Output")
                    st.text_area("", value=result.original_answer, height=200, disabled=True, label_visibility="collapsed")
                    st.caption("Original unverified response")
                
                with col2:
                    st.markdown("### ✅ ProofSense Verified")
                    
                    # Create annotated version
                    annotated = result.original_answer
                    risk_emoji = {
                        "verified": "✅",
                        "low": "🔵",
                        "medium": "🟠",
                        "high": "🔴"
                    }
                    
                    summary = f"Verifiability Confidence: {result.overall_score:.0f}/100\n"
                    summary += f"Analysis: {result.total_claims} claims | "
                    summary += f"{result.verified_claims} verified | "
                    summary += f"{result.flagged_claims} flagged\n\n"
                    summary += annotated
                    
                    st.text_area("", value=summary, height=200, disabled=True, label_visibility="collapsed")
                    st.caption("Verified with trust scoring")
                
                st.markdown("---")
            
            # Detailed Claim Analysis
            st.subheader("🔬 Detailed Claim Analysis")
            
            for i, claim in enumerate(result.claims, 1):
                display_claim(claim, i)
    
    with tab2:
        if 'verification_result' in st.session_state:
            result = st.session_state.verification_result
            
            st.subheader("📊 Trust Breakdown Visualization")
            
            # Calculate unsupported ratio
            unsupported_ratio = calculate_unsupported_ratio(result)
            
            # Show warning if high unsupported ratio
            if unsupported_ratio > 30:
                st.warning(f"⚠️ **{unsupported_ratio:.0f}% of claims lack sufficient evidence** - Exercise caution with this content")
            elif unsupported_ratio > 0:
                st.info(f"ℹ️ {unsupported_ratio:.0f}% of claims lack sufficient evidence")
            else:
                st.success("✅ All claims have supporting evidence")
            
            # Trust breakdown metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-glass-card">
                    <h4 style="color: white !important;">Evidence Strength</h4>
                    <div class="metric-value">{result.overall_score:.0f}%</div>
                    <div class="metric-label">Verifiability Confidence</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-glass-card">
                    <h4 style="color: white !important;">Claim Coverage</h4>
                    <div class="metric-value">{result.evidence_coverage:.0f}%</div>
                    <div class="metric-label">Verified Claims</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                risk_factor = (result.flagged_claims / result.total_claims * 100) if result.total_claims > 0 else 0
                st.markdown(f"""
                <div class="metric-glass-card">
                    <h4 style="color: white !important;">Risk Factor</h4>
                    <div class="metric-value">{risk_factor:.0f}%</div>
                    <div class="metric-label">Flagged Claims</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Risk distribution chart
            st.subheader("Risk Distribution")
            
            import plotly.graph_objects as go
            
            # Pie chart for risk distribution
            labels = ['Verified', 'Low Risk', 'Medium Risk', 'High Risk']
            values = [
                result.risk_distribution['verified'],
                result.risk_distribution['low'],
                result.risk_distribution['medium'],
                result.risk_distribution['high']
            ]
            colors = ['#4caf50', '#2196f3', '#ff9800', '#ff4444']
            
            # Filter out zero values for cleaner display
            filtered_data = [(label, value, color) for label, value, color in zip(labels, values, colors) if value > 0]
            if filtered_data:
                labels_filtered, values_filtered, colors_filtered = zip(*filtered_data)
            else:
                labels_filtered, values_filtered, colors_filtered = labels, values, colors
            
            fig = go.Figure(data=[go.Pie(
                labels=labels_filtered,
                values=values_filtered,
                marker=dict(
                    colors=colors_filtered,
                    line=dict(color='white', width=3)
                ),
                hole=0.45,
                textinfo='label+percent',
                textfont=dict(size=14, color='white', family='Inter'),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
                pull=[0.05 if v == max(values_filtered) else 0 for v in values_filtered],  # Pull out the largest slice
            )])
            
            fig.update_layout(
                title=dict(
                    text="Claim Risk Distribution",
                    font=dict(size=18, color='#6A5D7B', family='Inter')
                ),
                height=450,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    font=dict(size=13, color='#6A5D7B', family='Inter'),
                    bgcolor='rgba(255, 255, 255, 0.8)',
                    bordercolor='rgba(106, 93, 123, 0.2)',
                    borderwidth=1,
                ),
                paper_bgcolor='rgba(255, 255, 255, 0)',
                plot_bgcolor='rgba(255, 255, 255, 0)',
                margin=dict(t=60, b=40, l=40, r=120),
                font=dict(family='Inter'),
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=13,
                    font_family="Inter",
                    font_color="#6A5D7B"
                ),
            )
            
            # Add center annotation with total claims
            fig.add_annotation(
                text=f"<b>{result.total_claims}</b><br><span style='font-size:12px'>Total<br>Claims</span>",
                x=0.5, y=0.5,
                font=dict(size=24, color='#6A5D7B', family='Inter'),
                showarrow=False,
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Bar chart for confidence scores
            st.subheader("Verifiability Confidence Scores by Claim")
            
            claim_numbers = [f"Claim {i+1}" for i in range(len(result.claims))]
            confidence_scores = [claim.confidence_score for claim in result.claims]
            colors_bar = [get_score_color(score) for score in confidence_scores]
            
            fig2 = go.Figure(data=[go.Bar(
                x=claim_numbers,
                y=confidence_scores,
                marker=dict(
                    color=colors_bar,
                    line=dict(color='rgba(255, 255, 255, 0.8)', width=2),
                    pattern_shape="",
                ),
                text=[f"<b>{score:.1f}</b>" for score in confidence_scores],
                textposition='outside',
                textfont=dict(size=14, color='#6A5D7B', family='Inter'),
                hovertemplate='<b>%{x}</b><br>Score: %{y:.1f}/100<extra></extra>',
            )])
            
            fig2.update_layout(
                title=dict(
                    text="Individual Claim Verifiability Confidence Scores",
                    font=dict(size=18, color='#6A5D7B', family='Inter')
                ),
                xaxis=dict(
                    title="Claims",
                    titlefont=dict(size=14, color='#6A5D7B', family='Inter'),
                    tickfont=dict(size=12, color='#666', family='Inter'),
                    showgrid=False,
                    showline=True,
                    linewidth=2,
                    linecolor='rgba(106, 93, 123, 0.2)',
                ),
                yaxis=dict(
                    title="Verifiability Confidence Score",
                    titlefont=dict(size=14, color='#6A5D7B', family='Inter'),
                    tickfont=dict(size=12, color='#666', family='Inter'),
                    range=[0, 105],
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(200, 200, 200, 0.2)',
                    showline=True,
                    linewidth=2,
                    linecolor='rgba(106, 93, 123, 0.2)',
                ),
                plot_bgcolor='rgba(255, 255, 255, 0.9)',
                paper_bgcolor='rgba(255, 255, 255, 0)',
                height=450,
                margin=dict(t=60, b=60, l=60, r=40),
                font=dict(family='Inter'),
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=13,
                    font_family="Inter"
                ),
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
            # Warning summary
            st.subheader("⚠️ Language Warnings Summary")
            
            total_warnings = sum(len(claim.warnings) for claim in result.claims)
            
            if total_warnings > 0:
                # Create a styled warning card
                st.markdown(f"""
                <div class="glass-card" style="background: linear-gradient(135deg, rgba(255, 152, 0, 0.15), rgba(255, 193, 7, 0.15)); border-left: 4px solid #ff9800;">
                    <h4 style="color: #ff9800 !important; margin-top: 0;">
                        <span style="font-size: 1.5rem;">⚠️</span> Overconfident Language Detected
                    </h4>
                    <p style="font-size: 1.1rem; color: #666; margin: 0.5rem 0;">
                        Detected <strong style="color: #ff9800;">{total_warnings}</strong> overconfident language pattern(s) 
                        across <strong>{result.total_claims}</strong> claims
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show detailed warnings in expandable sections
                st.markdown("<br>", unsafe_allow_html=True)
                
                warning_details = []
                for i, claim in enumerate(result.claims, 1):
                    if claim.warnings:
                        warning_text = ', '.join([f"**{w.split(': ')[1].strip(chr(39))}**" if ': ' in w else f"**{w}**" for w in claim.warnings])
                        warning_details.append({
                            'Claim #': f"Claim {i}",
                            'Pattern Detected': warning_text,
                            'Risk Impact': '🔴 Increases hallucination risk'
                        })
                
                if warning_details:
                    import pandas as pd
                    warnings_df = pd.DataFrame(warning_details)
                    
                    # Style the dataframe
                    st.markdown("""
                    <style>
                    .dataframe {
                        font-family: 'Inter', sans-serif !important;
                        background: rgba(255, 255, 255, 0.8);
                        border-radius: 10px;
                    }
                    .dataframe th {
                        background: linear-gradient(135deg, #ff9800, #ffb300) !important;
                        color: white !important;
                        font-weight: 600 !important;
                        padding: 12px !important;
                    }
                    .dataframe td {
                        padding: 10px !important;
                        color: #666 !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    st.dataframe(warnings_df, use_container_width=True, hide_index=True)
            else:
                st.markdown("""
                <div class="glass-card" style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.15), rgba(129, 199, 132, 0.15)); border-left: 4px solid #4caf50;">
                    <h4 style="color: #4caf50 !important; margin-top: 0;">
                        <span style="font-size: 1.5rem;">✅</span> Clean Language Patterns
                    </h4>
                    <p style="font-size: 1.1rem; color: #666; margin: 0.5rem 0;">
                        No overconfident language patterns detected in any claims
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.info("👆 Please verify an answer in the Verification tab first")
    
    with tab3:
        if 'verification_result' in st.session_state:
            result = st.session_state.verification_result
            domain = st.session_state.get('domain', 'general')
            
            st.subheader("📥 Export Trust Report")
            
            st.info("Generate a comprehensive PDF-style report with all verification details")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                report_format = st.radio(
                    "Report Format",
                    ["Text Summary", "JSON Data", "Full Report"],
                    horizontal=True
                )
            
            with col2:
                if st.button("📄 Generate Report", type="primary", use_container_width=True):
                    if report_format == "Text Summary":
                        report_content = f"""
PROOFSENSE AI - TRUST REPORT
=============================

Verifiability Confidence: {result.overall_score:.1f}/100
Domain: {domain.capitalize()}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Summary:
- Total Claims: {result.total_claims}
- Verified: {result.verified_claims}
- Flagged: {result.flagged_claims}
- Evidence Coverage: {result.evidence_coverage:.1f}%

Risk Distribution:
- Verified: {result.risk_distribution['verified']}
- Low Risk: {result.risk_distribution['low']}
- Medium Risk: {result.risk_distribution['medium']}
- High Risk: {result.risk_distribution['high']}
                        """
                    elif report_format == "JSON Data":
                        report_data = {
                            "timestamp": datetime.now().isoformat(),
                            "domain": domain,
                            "overall_score": result.overall_score,
                            "total_claims": result.total_claims,
                            "verified_claims": result.verified_claims,
                            "flagged_claims": result.flagged_claims,
                            "evidence_coverage": result.evidence_coverage,
                            "risk_distribution": result.risk_distribution,
                            "claims": [
                                {
                                    "text": claim.text,
                                    "confidence_score": claim.confidence_score,
                                    "risk_level": claim.risk_level,
                                    "warnings_count": len(claim.warnings),
                                    "evidence_count": len(claim.evidence)
                                }
                                for claim in result.claims
                            ]
                        }
                        report_content = json.dumps(report_data, indent=2)
                    else:  # Full Report
                        report_content = generate_pdf_report(result, domain)
                    
                    st.download_button(
                        label="⬇️ Download Report",
                        data=report_content,
                        file_name=f"proofsense_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
            
            st.markdown("---")
            
            # Enhanced Preview Section
            st.markdown("""
            <div class="glass-card" style="border-left: 4px solid #667eea;">
                <h3 style="color: #6A5D7B !important; margin-top: 0;">
                    <span style="font-size: 1.8rem;">📋</span> Report Preview
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Create refined metric cards for preview
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-glass-card" style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.7), rgba(118, 75, 162, 0.7));">
                    <div style="font-size: 1.2rem; opacity: 0.9;">Verifiability Confidence</div>
                    <div class="metric-value" style="font-size: 2.5rem;">{result.overall_score:.1f}/100</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-glass-card" style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.7), rgba(129, 199, 132, 0.7));">
                    <div style="font-size: 1.2rem; opacity: 0.9;">Verified Claims</div>
                    <div class="metric-value" style="font-size: 2.5rem;">{result.verified_claims}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-glass-card" style="background: linear-gradient(135deg, rgba(255, 152, 0, 0.7), rgba(255, 193, 7, 0.7));">
                    <div style="font-size: 1.2rem; opacity: 0.9;">Flagged Claims</div>
                    <div class="metric-value" style="font-size: 2.5rem;">{result.flagged_claims}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Summary section with glassmorphism
            if report_format == "Text Summary":
                st.markdown("""
                <div class="glass-card" style="background: linear-gradient(135deg, rgba(230, 230, 250, 0.6), rgba(220, 220, 240, 0.6));">
                    <h4 style="color: #6A5D7B !important; margin-top: 0;">📊 Summary Highlights</h4>
                </div>
                """, unsafe_allow_html=True)
                
                summary_items = [
                    f"📝 **Total Claims Analyzed:** {result.total_claims}",
                    f"✅ **Verified Claims:** {result.verified_claims}",
                    f"⚠️ **Flagged Claims:** {result.flagged_claims}",
                    f"📚 **Evidence Coverage:** {result.evidence_coverage:.1f}%"
                ]
                
                for item in summary_items:
                    st.markdown(f"""
                    <div class="evidence-box" style="margin: 0.5rem 0;">
                        {item}
                    </div>
                    """, unsafe_allow_html=True)
            
            elif report_format == "JSON Data":
                st.markdown("""
                <div class="glass-card" style="background: linear-gradient(135deg, rgba(230, 230, 250, 0.6), rgba(220, 220, 240, 0.6));">
                    <h4 style="color: #6A5D7B !important; margin-top: 0;">💾 JSON Structure Preview</h4>
                </div>
                """, unsafe_allow_html=True)
                
                preview_data = {
                    "overall_score": result.overall_score,
                    "total_claims": result.total_claims,
                    "risk_distribution": result.risk_distribution
                }
                st.json(preview_data)
            
            else:  # Full Report
                st.markdown("""
                <div class="glass-card" style="background: linear-gradient(135deg, rgba(230, 230, 250, 0.6), rgba(220, 220, 240, 0.6));">
                    <h4 style="color: #6A5D7B !important; margin-top: 0;">📄 Full Report Contents</h4>
                    <ul style="color: #666; line-height: 2;">
                        <li>Overall assessment with verifiability confidence score</li>
                        <li>Complete risk distribution analysis</li>
                        <li>Original answer text</li>
                        <li>Detailed claim-by-claim breakdown</li>
                        <li>Evidence sources for each claim</li>
                        <li>Language warning analysis</li>
                        <li>Timestamp and domain information</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.markdown("""
            <div class="glass-card" style="text-align: center; padding: 3rem;">
                <h3 style="color: #6A5D7B !important;">
                    <span style="font-size: 3rem;">📊</span><br><br>
                    No Verification Results Yet
                </h3>
                <p style="color: #666; font-size: 1.1rem; margin-top: 1rem;">
                    Please verify an answer in the <strong>Verification</strong> tab first to generate a report.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer">
        <div class="hero-logo" style="font-size: 2.5rem;">🔍</div>
        <h3 style="color: #6A5D7B !important; margin: 1rem 0;">ProofSense AI</h3>
        <p style="font-size: 1.2rem; color: #8E8D8A; margin-bottom: 1.5rem;">
            Making AI Trustworthy Through Transparency and Evidence-Based Verification
        </p>
        <div style="margin: 1.5rem 0;">
            <span class="tech-badge">🔍 RAG-Based</span>
            <span class="tech-badge">⚡ Real-Time Analysis</span>
            <span class="tech-badge">🎯 Multi-Factor Scoring</span>
            <span class="tech-badge">🚀 Production-Ready Architecture</span>
        </div>
        <div style="margin: 2rem 0;">
            <a href="#" style="color: #A3C9A8; text-decoration: none; margin: 0 1rem;">GitHub</a>
            <a href="#" style="color: #A3C9A8; text-decoration: none; margin: 0 1rem;">Documentation</a>
            <a href="#" style="color: #A3C9A8; text-decoration: none; margin: 0 1rem;">API</a>
            <a href="#" style="color: #A3C9A8; text-decoration: none; margin: 0 1rem;">Contact</a>
        </div>
        <p style="opacity: 0.7; font-size: 0.95rem; margin-top: 2rem;">
            Built for AI Safety & Trust | Hackathon Project<br>
            Powered by Python + Streamlit + RAG | © 2025 ProofSense AI
        </p>
        <p style="opacity: 0.6; font-size: 0.85rem; margin-top: 1rem;">
            Version 1.0.0 | Open Source
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
