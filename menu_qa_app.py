#!/usr/bin/env python3
"""
Menu QA Tool - Automated quality checks for restaurant menus
Supports PDF & image uploads with OCR, spell check, grammar check, and AI review
"""

import os
import json
import base64
from pathlib import Path
from typing import Optional
import tempfile
import traceback

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# Optional imports with fallbacks
try:
    import pytesseract
    from PIL import Image
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

try:
    import pdf2image
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    from language_tool_python import LanguageTool
    HAS_GRAMMAR = True
except ImportError:
    HAS_GRAMMAR = False

try:
    from anthropic import Anthropic
    HAS_CLAUDE = True
except ImportError:
    HAS_CLAUDE = False

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_image(image_path: str) -> str:
    """Extract text from image using OCR"""
    if not HAS_OCR:
        return "⚠️ OCR nicht installiert (pip install pytesseract pillow)"

    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='deu')
        return text
    except Exception as e:
        return f"❌ OCR-Fehler: {str(e)}"

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF"""
    if not HAS_PDF:
        return "⚠️ PDF-Verarbeitung nicht installiert (pip install pdf2image)"

    try:
        images = pdf2image.convert_from_path(pdf_path)
        all_text = ""
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang='deu')
            all_text += f"\n--- Seite {i+1} ---\n{text}"
        return all_text
    except Exception as e:
        return f"❌ PDF-Fehler: {str(e)}"

def check_spelling_basic(text: str) -> dict:
    """Basic spelling checks using common German rules"""
    issues = []

    # Common German spelling mistakes
    common_mistakes = {
        'ss': ('ß', 'Doppel-S sollte ß sein'),
        'ae': ('ä', 'ae sollte ä sein'),
        'oe': ('ö', 'oe sollte ö sein'),
        'ue': ('ü', 'ue sollte ü sein'),
    }

    # Very basic checks
    if '  ' in text:  # Double spaces
        issues.append({'type': 'spacing', 'issue': 'Doppelte Leerzeichen gefunden', 'severity': 'warning'})

    return {
        'spelling_issues': issues,
        'total_issues': len(issues)
    }

def check_grammar(text: str) -> dict:
    """Check grammar using LanguageTool if available"""
    if not HAS_GRAMMAR:
        return {'status': 'unavailable', 'message': 'LanguageTool nicht installiert'}

    try:
        tool = LanguageTool('de')
        matches = tool.check(text)

        issues = []
        for match in matches[:20]:  # Limit to 20 issues
            issues.append({
                'message': match.message,
                'ruleId': match.ruleId,
                'offset': match.offset,
                'length': match.length
            })

        return {
            'grammar_issues': issues,
            'total_issues': len(matches)
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def analyze_layout(text: str, file_info: dict) -> dict:
    """Analyze text layout and formatting"""
    lines = text.split('\n')
    non_empty_lines = [l for l in lines if l.strip()]

    # Basic layout analysis
    analysis = {
        'total_lines': len(lines),
        'non_empty_lines': len(non_empty_lines),
        'avg_line_length': sum(len(l) for l in non_empty_lines) / len(non_empty_lines) if non_empty_lines else 0,
        'has_inconsistent_spacing': '  ' in text,
        'file_size_mb': file_info.get('size_mb', 0),
        'estimated_pages': max(1, len(non_empty_lines) // 40)  # Rough estimate
    }

    return analysis

def send_to_claude(text: str, model: str = 'claude-3-5-haiku-20241022') -> dict:
    """Send extracted text to Claude for AI review"""
    if not HAS_CLAUDE:
        return {
            'status': 'unavailable',
            'message': 'Claude API nicht konfiguriert. Setze ANTHROPIC_API_KEY env var.'
        }

    try:
        client = Anthropic()

        prompt = f"""Du bist ein Experte für Speisekarten-Qualität. Überprüfe diese Speisekarte auf:

1. **Rechtschreibung & Grammatik** - Fehler im Text
2. **Formatierung** - Konsistenz in Schreibweisen, Preisformatierung, Abstände
3. **Layout** - Ist alles ordentlich angeordnet, zentriert, ausgerichtet?
4. **Konsistenz** - Einheitliche Schreibweisen, Mengenangaben, Einheiten
5. **Lesbarkeit** - Sind Abstände und Strukturen klar?

Extrahierter Text der Speisekarte:
---
{text[:3000]}
---

Gib eine strukturierte Bewertung mit:
- KRITISCHE FEHLER (rot)
- WICHTIGE HINWEISE (gelb)
- EMPFEHLUNGEN (blau)

Sei prägnant und praktisch."""

        message = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return {
            'status': 'success',
            'model': model,
            'review': message.content[0].text
        }
    except Exception as e:
        return {'status': 'error', 'message': f'Claude-Fehler: {str(e)}'}

@app.route('/')
def index():
    return render_template('qa_dashboard.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and analysis"""
    if 'file' not in request.files:
        return jsonify({'error': 'Keine Datei ausgewählt'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Keine Datei ausgewählt'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Dateiformat nicht unterstützt'}), 400

    try:
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Get file info
        file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
        file_ext = filename.rsplit('.', 1)[1].lower()

        # Extract text
        if file_ext == 'pdf':
            extracted_text = extract_text_from_pdf(filepath)
        else:
            extracted_text = extract_text_from_image(filepath)

        # Run checks
        results = {
            'filename': filename,
            'file_size_mb': round(file_size_mb, 2),
            'extracted_text': extracted_text[:2000],  # First 2000 chars
            'spelling': check_spelling_basic(extracted_text),
            'layout': analyze_layout(extracted_text, {'size_mb': file_size_mb})
        }

        # Optional: Grammar check
        if HAS_GRAMMAR:
            results['grammar'] = check_grammar(extracted_text)

        # Cleanup
        os.remove(filepath)

        return jsonify(results)

    except Exception as e:
        return jsonify({
            'error': f'Verarbeitungsfehler: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/ai-review', methods=['POST'])
def ai_review():
    """Send text to Claude for AI review"""
    data = request.get_json()
    text = data.get('text', '')
    model = data.get('model', 'claude-3-5-haiku-20241022')

    if not text:
        return jsonify({'error': 'Kein Text zur Überprüfung'}), 400

    result = send_to_claude(text, model)
    return jsonify(result)

@app.route('/api/status', methods=['GET'])
def status():
    """Check system status and available features"""
    return jsonify({
        'ocr_available': HAS_OCR,
        'pdf_available': HAS_PDF,
        'grammar_available': HAS_GRAMMAR,
        'claude_available': HAS_CLAUDE,
        'claude_api_key_set': bool(os.getenv('ANTHROPIC_API_KEY')),
        'message': '✅ Alle Features aktiviert!' if all([HAS_OCR, HAS_PDF, HAS_GRAMMAR, HAS_CLAUDE]) else '⚠️ Einige Features nicht verfügbar'
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, port=5000)
