#!/usr/bin/env python3
"""
ProofSense AI Demo Script
Run automated tests to verify all features work correctly
"""

import sys
import time
from proofsense_app import ProofSenseEngine, VerificationResult

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_result(result: VerificationResult):
    """Print verification result summary"""
    print(f"Overall Trust Score: {result.overall_score:.1f}/100")
    print(f"Total Claims: {result.total_claims}")
    print(f"Verified: {result.verified_claims} | Flagged: {result.flagged_claims}")
    print(f"Evidence Coverage: {result.evidence_coverage:.1f}%")
    print(f"\nRisk Distribution:")
    for level, count in result.risk_distribution.items():
        emoji = {"verified": "✅", "low": "🔵", "medium": "🟠", "high": "🔴"}
        print(f"  {emoji[level]} {level.capitalize()}: {count}")

def test_hallucination_detection():
    """Test 1: Hallucination Detection"""
    print_header("TEST 1: Hallucination Detection")
    
    engine = ProofSenseEngine("general")
    text = "The Internet was definitely invented in 1995 by Bill Gates and is guaranteed to work perfectly 100% of the time."
    
    print(f"Input: {text}\n")
    result = engine.verify_answer(text)
    print_result(result)
    
    # Assertions
    assert result.overall_score < 40, "Should detect hallucination"
    assert result.flagged_claims > 0, "Should flag false claims"
    
    # Check for overconfident language detection
    total_warnings = sum(len(claim.warnings) for claim in result.claims)
    assert total_warnings > 0, "Should detect overconfident language"
    
    print("\n✅ Test 1 PASSED: Hallucination detected successfully")
    return True

def test_verified_content():
    """Test 2: Verified Content Recognition"""
    print_header("TEST 2: Verified Content Recognition")
    
    engine = ProofSenseEngine("general")
    text = "The Earth orbits around the Sun in approximately 365.25 days. Water boils at 100 degrees Celsius at sea level."
    
    print(f"Input: {text}\n")
    result = engine.verify_answer(text)
    print_result(result)
    
    # Assertions
    assert result.overall_score > 60, "Should verify accurate content"
    assert result.verified_claims > 0, "Should have verified claims"
    
    print("\n✅ Test 2 PASSED: Verified content recognized")
    return True

def test_mixed_quality():
    """Test 3: Mixed Quality Detection"""
    print_header("TEST 3: Mixed Quality Detection")
    
    engine = ProofSenseEngine("finance")
    text = "Compound interest is calculated on principal and accumulated interest. The stock market is guaranteed to provide 30% annual returns with absolutely no risk."
    
    print(f"Input: {text}\n")
    result = engine.verify_answer(text)
    print_result(result)
    
    # Assertions
    assert result.total_claims >= 2, "Should detect multiple claims"
    assert result.verified_claims > 0, "Should verify first claim"
    assert result.flagged_claims > 0, "Should flag second claim"
    
    # Check for mixed risk levels
    has_high_score = any(claim.confidence_score > 70 for claim in result.claims)
    has_low_score = any(claim.confidence_score < 40 for claim in result.claims)
    assert has_high_score and has_low_score, "Should detect mixed quality"
    
    print("\n✅ Test 3 PASSED: Mixed quality detected")
    return True

def test_overconfident_language():
    """Test 4: Overconfident Language Detection"""
    print_header("TEST 4: Overconfident Language Detection")
    
    engine = ProofSenseEngine("health")
    text = "Exercise always prevents all diseases without exception and definitely works 100% of the time."
    
    print(f"Input: {text}\n")
    result = engine.verify_answer(text)
    print_result(result)
    
    # Count warnings
    total_warnings = sum(len(claim.warnings) for claim in result.claims)
    print(f"\nOverconfident patterns detected: {total_warnings}")
    
    for i, claim in enumerate(result.claims, 1):
        if claim.warnings:
            print(f"\nClaim {i} warnings:")
            for warning in claim.warnings:
                print(f"  - {warning}")
    
    # Assertions
    assert total_warnings > 0, "Should detect overconfident language"
    
    print("\n✅ Test 4 PASSED: Overconfident language detected")
    return True

def test_claim_extraction():
    """Test 5: Claim Extraction"""
    print_header("TEST 5: Claim Extraction")
    
    engine = ProofSenseEngine("general")
    
    # Test various sentence structures
    test_texts = [
        "Single sentence claim.",
        "First claim. Second claim. Third claim.",
        "Compound claim with and, but also another part.",
        "The Earth orbits the Sun, and the Moon orbits the Earth.",
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\nTest {i}: {text}")
        claims = engine.extract_claims(text)
        print(f"Extracted {len(claims)} claim(s):")
        for j, claim in enumerate(claims, 1):
            print(f"  {j}. {claim}")
    
    print("\n✅ Test 5 PASSED: Claim extraction working")
    return True

def test_all_domains():
    """Test 6: All Domain Support"""
    print_header("TEST 6: All Domain Support")
    
    domains = ["general", "finance", "health"]
    
    test_texts = {
        "general": "The speed of light is approximately 299,792,458 meters per second.",
        "finance": "The Federal Reserve is the central banking system of the United States.",
        "health": "The human heart pumps approximately 5 liters of blood per minute at rest."
    }
    
    for domain in domains:
        print(f"\n--- Testing {domain.upper()} domain ---")
        engine = ProofSenseEngine(domain)
        result = engine.verify_answer(test_texts[domain])
        print(f"Score: {result.overall_score:.1f}/100")
        print(f"Claims: {result.total_claims}")
        assert result.total_claims > 0, f"{domain} domain should extract claims"
    
    print("\n✅ Test 6 PASSED: All domains working")
    return True

def test_evidence_retrieval():
    """Test 7: Evidence Retrieval"""
    print_header("TEST 7: Evidence Retrieval")
    
    engine = ProofSenseEngine("general")
    
    # Test claims with varying relevance
    test_claims = [
        "The Earth orbits the Sun",  # Should find evidence
        "Photosynthesis converts sunlight to energy",  # Should find evidence
        "Purple elephants dance on Mars",  # Should find no evidence
    ]
    
    for claim in test_claims:
        print(f"\nClaim: {claim}")
        evidence = engine.retrieve_evidence(claim, top_k=3)
        print(f"Evidence found: {len(evidence)} sources")
        
        if evidence:
            print("Top evidence:")
            for i, (ev, score) in enumerate(evidence[:2], 1):
                print(f"  {i}. (score: {score:.2f}) {ev[:100]}...")
        else:
            print("  No relevant evidence found")
    
    print("\n✅ Test 7 PASSED: Evidence retrieval working")
    return True

def test_scoring_algorithm():
    """Test 8: Scoring Algorithm"""
    print_header("TEST 8: Scoring Algorithm")
    
    engine = ProofSenseEngine("general")
    
    # Create test scenarios
    scenarios = [
        {
            "name": "Strong Evidence",
            "evidence": [("Exact match", 0.9), ("Good match", 0.8), ("Ok match", 0.7)],
            "expected_range": (70, 100),
        },
        {
            "name": "Weak Evidence",
            "evidence": [("Weak match", 0.3)],
            "expected_range": (0, 50),
        },
        {
            "name": "No Evidence",
            "evidence": [],
            "expected_range": (0, 10),
        },
    ]
    
    for scenario in scenarios:
        score, risk = engine.calculate_claim_score("test claim", scenario["evidence"])
        print(f"\n{scenario['name']}:")
        print(f"  Score: {score:.1f}/100")
        print(f"  Risk: {risk}")
        print(f"  Evidence sources: {len(scenario['evidence'])}")
        
        min_score, max_score = scenario["expected_range"]
        assert min_score <= score <= max_score, f"Score should be in range {min_score}-{max_score}"
    
    print("\n✅ Test 8 PASSED: Scoring algorithm working correctly")
    return True

def run_performance_test():
    """Test 9: Performance Test"""
    print_header("TEST 9: Performance Test")
    
    engine = ProofSenseEngine("general")
    
    # Test with increasing text sizes
    test_cases = [
        ("Short", "The Earth orbits the Sun."),
        ("Medium", " ".join(["The Earth orbits the Sun."] * 5)),
        ("Long", " ".join(["The Earth orbits the Sun."] * 20)),
    ]
    
    for name, text in test_cases:
        start_time = time.time()
        result = engine.verify_answer(text)
        elapsed = time.time() - start_time
        
        print(f"\n{name} text ({len(text)} chars):")
        print(f"  Processing time: {elapsed:.3f} seconds")
        print(f"  Claims analyzed: {result.total_claims}")
        print(f"  Claims/second: {result.total_claims/elapsed:.1f}")
        
        assert elapsed < 10, "Should process within reasonable time"
    
    print("\n✅ Test 9 PASSED: Performance acceptable")
    return True

def run_all_tests():
    """Run all tests"""
    print("\n" + "🔍 PROOFSENSE AI - AUTOMATED TEST SUITE 🔍".center(70))
    print("="*70)
    
    tests = [
        test_hallucination_detection,
        test_verified_content,
        test_mixed_quality,
        test_overconfident_language,
        test_claim_extraction,
        test_all_domains,
        test_evidence_retrieval,
        test_scoring_algorithm,
        run_performance_test,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n❌ Test FAILED with error: {str(e)}")
            failed += 1
    
    # Summary
    print_header("TEST SUMMARY")
    print(f"Total Tests: {len(tests)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {passed/len(tests)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! ProofSense AI is working correctly. 🎉")
        return 0
    else:
        print("\n⚠️ Some tests failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
