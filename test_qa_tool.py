#!/usr/bin/env python3
"""
Quick test of Menu QA Tool without full dependencies
This version simulates OCR for testing purposes
"""

import json
from pathlib import Path

# Simulated menu text (Saisonkarte Spargel)
SIMULATED_OCR_TEXT = """
Mettgenpin 1877
Spargелkarte

Grüner & weißer Spargel mit Erdbeeren und Burrata
Grüner & weißer Spargel mit kirschhen Vinaigrette, geroestem Sesam und nativem Olivenöl aus
Griechenland

19,90 €

Spargel mit Kochschinken
Spargel mit Kochschinken und Sauce Hollandaise. Dazu werden Pellkartofeln
serviert

15,90 €

Spargel-Creme-Suppe
Hausgemachte Spargel-Cremessuppe mit Petersiele verferent.

6,90 €

Schnitzel mit Spargel Hollandaise
Hausgemachtes Schnitzel mit Spargel und Sauce Hollandaise Topping. Dazu
werden Pellkartofeln serviert

22,90 €

Lotus Cheesecake Cream
Kleiner, safter Abschluss mit Lotus Keks, Wahlweise mit Karamell  oder
Schokoladensouce

4,90 €
"""

class MenuQASimulator:
    def __init__(self):
        self.text = SIMULATED_OCR_TEXT

    def check_spelling(self):
        """Detect common spelling errors"""
        issues = []

        # Common German spelling mistakes
        mistakes = {
            'Spargелkarte': 'Spargелkarte (looks like Latin el instead of e)',
            'kirschhen': 'kirschhen → Kirschenessig (double h, wrong word)',
            'geroestem': 'geroestem → geröstem (should be ö not oe)',
            'nativem': 'nativem Olivenöl (spacing ok but context check)',
            'Cremessuppe': 'Cremessuppe → Cremesuppe (double s, should be single)',
            'Petersiele': 'Petersiele → Petersilie (wrong spelling)',
            'vefrerent': 'vefrerent → verfeinert (typo)',
            'safter': 'safter → süßer (wrong word)',
            'Karamell': 'Karamell (correct: Karamel - one l)',
            'Schokoladensouce': 'Schokoladensouce → Schokoladensauce (typo)'
        }

        for wrong, explanation in mistakes.items():
            if wrong in self.text:
                issues.append({
                    'word': wrong,
                    'suggestion': explanation,
                    'severity': 'error' if '→' in explanation else 'warning'
                })

        return {
            'spelling_errors': len(issues),
            'issues': issues
        }

    def check_formatting(self):
        """Check layout and formatting consistency"""
        issues = []

        lines = self.text.split('\n')
        non_empty = [l for l in lines if l.strip()]

        # Price consistency
        prices = []
        for line in lines:
            if '€' in line:
                prices.append(line.strip())

        # Check double spaces
        if '  ' in self.text:
            issues.append('⚠️ Doppelte Leerzeichen gefunden')

        # Check price formatting consistency
        price_formats = set()
        import re
        for price_line in prices:
            # Extract price pattern
            match = re.search(r'\d+,\d+\s*€', price_line)
            if match:
                price_formats.add(match.group())

        return {
            'total_prices': len(prices),
            'price_formats': list(price_formats),
            'prices': prices,
            'issues': issues,
            'line_count': len(non_empty),
            'avg_line_length': sum(len(l) for l in non_empty) / len(non_empty) if non_empty else 0
        }

    def check_consistency(self):
        """Check text consistency"""
        issues = []

        # Check inconsistent spacing around €
        import re
        prices_with_space = len(re.findall(r'\d+,\d+\s+€', self.text))
        prices_without_space = len(re.findall(r'\d+,\d+€', self.text))

        if prices_with_space > 0 and prices_without_space > 0:
            issues.append('❌ Inconsistent spacing around € symbol')

        # Check capitalization of dish names
        lines = [l.strip() for l in self.text.split('\n') if l.strip()]

        return {
            'issues': issues,
            'recommendation': 'Standardize spacing: use "X,XX €" consistently (space before €)'
        }

    def run_analysis(self):
        """Run complete analysis"""
        spelling = self.check_spelling()
        formatting = self.check_formatting()
        consistency = self.check_consistency()

        return {
            'filename': 'saisonkarte-spargel.pdf',
            'ocr_text_sample': self.text[:500],
            'spelling': spelling,
            'formatting': formatting,
            'consistency': consistency,
            'summary': {
                'total_errors': spelling['spelling_errors'],
                'formatting_issues': len(formatting['issues']),
                'consistency_issues': len(consistency['issues']),
                'overall_quality': 'NEEDS REVIEW' if spelling['spelling_errors'] > 5 else 'GOOD'
            }
        }


# Run analysis
if __name__ == '__main__':
    qa = MenuQASimulator()
    results = qa.run_analysis()

    print("\n" + "="*70)
    print("🍽️  SPEISEKARTEN QA ANALYSE — SAISONKARTE SPARGEL")
    print("="*70 + "\n")

    print(f"📄 Datei: {results['filename']}")
    print(f"📊 Status: {results['summary']['overall_quality']}\n")

    print("RECHTSCHREIBUNG".center(70, "—"))
    print(f"Fehler gefunden: {results['spelling']['spelling_errors']}\n")
    for i, issue in enumerate(results['spelling']['issues'], 1):
        print(f"{i}. ❌ {issue['word']}")
        print(f"   → {issue['suggestion']}\n")

    print("\nFORMATIERUNG & LAYOUT".center(70, "—"))
    print(f"Preise erkannt: {results['formatting']['total_prices']}")
    print(f"Zeilen erkannt: {results['formatting']['line_count']}")
    print(f"Ø Zeilenlänge: {results['formatting']['avg_line_length']:.0f} Zeichen\n")

    if results['formatting']['issues']:
        print("Probleme:")
        for issue in results['formatting']['issues']:
            print(f"  {issue}")

    print("\nPREIS-FORMATE:")
    for price in results['formatting']['prices']:
        print(f"  {price}")

    print("\n\nKONSISTENZ-CHECK".center(70, "—"))
    if results['consistency']['issues']:
        for issue in results['consistency']['issues']:
            print(f"  {issue}")
    print(f"\n💡 Empfehlung: {results['consistency']['recommendation']}")

    print("\n\nZUSAMMENFASSUNG".center(70, "—"))
    print(f"✓ Rechtschreibefehler: {results['summary']['total_errors']}")
    print(f"✓ Formatierungsprobleme: {results['summary']['formatting_issues']}")
    print(f"✓ Konsistenzprobleme: {results['summary']['consistency_issues']}")

    print("\n" + "="*70)
    print("📊 JSON Report speichern...")

    with open('qa-report-test.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("✅ Report gespeichert: qa-report-test.json")
    print("="*70 + "\n")
