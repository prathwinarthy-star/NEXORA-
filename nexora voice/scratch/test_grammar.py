import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from grammar_analyzer import analyze_grammar

sample_flawed = (
    "Good morning. He are speaking today and they has went to the conference. "
    "We discuss about a honest mistake because she don't know nothing. "
    "Between you and I, I am gonna explain you the problem."
)

res = analyze_grammar([], sample_flawed, 30.0)
print(f"Grammar Score: {res['grammar_score']}/100")
print(f"Fluency Rating: {res['fluency_rating']}")
print(f"Total Errors Found: {res['error_count']}")
print(f"Points Deducted: {res['points_deducted']} pts")
print("\nDetected Grammar Issues:")
for idx, iss in enumerate(res['issues'], start=1):
    print(f" [{idx}] {iss['error_type']} (Severity {iss['severity']}):")
    print(f"     Original : '{iss['original_text']}'")
    print(f"     Corrected: '{iss['corrected_text']}'")
    print(f"     Why      : {iss['why']}")
    print(f"     Points   : -{iss['points_deducted']} pts")

print("\nCorrected Full Transcript:")
print(res['corrected_transcript'])

sample_clean = (
    "Good morning esteemed judges and guests. Today I stand before you to explore "
    "the transformative power of deliberate communication. When we speak with unwavering "
    "clarity, our message resonates deeply. Mastering the strategic pause empowers every word."
)
res_clean = analyze_grammar([], sample_clean, 30.0)
print(f"\n[Clean Speech Test] Grammar Score: {res_clean['grammar_score']}/100, Errors: {res_clean['error_count']}")
