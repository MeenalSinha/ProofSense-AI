# ProofSense AI Configuration
# Customize these settings to adjust behavior

# Scoring weights (must sum to 1.0)
SCORING_WEIGHTS = {
    "best_match": 0.5,      # Weight for strongest evidence match
    "source_count": 0.3,    # Weight for number of sources
    "avg_quality": 0.2      # Weight for average evidence quality
}

# Risk level thresholds
RISK_THRESHOLDS = {
    "verified": 70,   # Score >= 70 = Verified
    "low": 50,        # Score >= 50 = Low Risk
    "medium": 30,     # Score >= 30 = Medium Risk
    # Score < 30 = High Risk
}

# Overconfident language patterns
OVERCONFIDENT_PATTERNS = [
    r'\balways\b',
    r'\bnever\b',
    r'\bguaranteed\b',
    r'\bcertainly\b',
    r'\bdefinitely\b',
    r'\bimpossible\b',
    r'\bno doubt\b',
    r'\bwithout question\b',
    r'\b100%\b',
    r'\b100 percent\b',
    r'\babsolutely\b',
    r'\bundoubtedly\b',
    r'\binevitably\b',
    r'\bwithout fail\b',
    r'\bfor sure\b',
    r'\bfor certain\b',
]

# Evidence retrieval settings
EVIDENCE_SETTINGS = {
    "top_k": 3,              # Number of evidence sources to retrieve
    "similarity_threshold": 0.1,  # Minimum similarity for relevance
    "min_claim_length": 10,   # Minimum characters for valid claim
}

# UI Settings
UI_CONFIG = {
    "show_before_after_default": True,
    "default_domain": "general",
    "max_claims_display": 50,
    "score_display_decimals": 1,
}

# Color scheme
COLORS = {
    "verified": "#4caf50",    # Green
    "low": "#2196f3",         # Blue
    "medium": "#ff9800",      # Orange
    "high": "#ff4444",        # Red
    "gradient_start": "#667eea",
    "gradient_end": "#764ba2",
}

# Export settings
EXPORT_CONFIG = {
    "include_timestamp": True,
    "include_domain": True,
    "include_evidence": True,
    "default_format": "Full Report",
}

# Domain-specific settings
DOMAIN_CONFIG = {
    "general": {
        "name": "General Knowledge",
        "icon": "📚",
        "disclaimer": None,
    },
    "finance": {
        "name": "Finance & Economics",
        "icon": "💰",
        "disclaimer": "Financial information should be verified with qualified advisors.",
    },
    "health": {
        "name": "Health & Medicine",
        "icon": "🏥",
        "disclaimer": "⚠️ Health information should be verified with qualified medical professionals.",
    },
}

# API mock settings
API_CONFIG = {
    "endpoint": "/api/verify",
    "method": "POST",
    "rate_limit": "100 requests/hour",
    "response_format": "JSON",
}

# Feature flags (for easy enable/disable)
FEATURES = {
    "before_after_comparison": True,
    "trust_dashboard": True,
    "export_reports": True,
    "overconfident_detection": True,
    "evidence_display": True,
    "sample_queries": True,
    "api_documentation": True,
}

# Advanced settings
ADVANCED = {
    "use_cache": True,
    "max_processing_time": 30,  # seconds
    "parallel_processing": False,  # For future multi-threading
    "logging_level": "INFO",
}
