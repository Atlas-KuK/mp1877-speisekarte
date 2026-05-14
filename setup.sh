#!/bin/bash
# Speisekarten QA Tool — Setup-Skript

set -e

echo "🍽️  Speisekarten QA Tool — Installation"
echo "======================================="

# Überprüfe Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nicht gefunden. Bitte installieren."
    exit 1
fi
echo "✅ Python3 gefunden: $(python3 --version)"

# Überprüfe System-Abhängigkeiten
echo ""
echo "Überprüfe System-Abhängigkeiten..."

if command -v tesseract &> /dev/null; then
    echo "✅ Tesseract gefunden: $(tesseract --version | head -1)"
else
    echo "❌ Tesseract nicht gefunden. Bitte installieren:"
    echo "   Ubuntu/Debian: sudo apt-get install tesseract-ocr"
    echo "   macOS: brew install tesseract"
    echo "   Windows: https://github.com/UB-Mannheim/tesseract/wiki"
    exit 1
fi

if command -v pdftoppm &> /dev/null; then
    echo "✅ Poppler gefunden"
else
    echo "❌ Poppler nicht gefunden. Bitte installieren:"
    echo "   Ubuntu/Debian: sudo apt-get install poppler-utils"
    echo "   macOS: brew install poppler"
    exit 1
fi

# Erstelle Virtual Environment
echo ""
echo "Erstelle Python Virtual Environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual Environment erstellt"
else
    echo "ℹ️  Virtual Environment existiert bereits"
fi

# Aktiviere Virtual Environment
source venv/bin/activate
echo "✅ Virtual Environment aktiviert"

# Installiere Python-Pakete
echo ""
echo "Installiere Python-Pakete..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt

echo "✅ Python-Pakete installiert"

# Überprüfe .env
echo ""
echo "Überprüfe Konfiguration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  .env erstellt. Bitte Anthropic API Key eintragen:"
    echo "   Bearbeite: .env"
    echo "   Setze: ANTHROPIC_API_KEY=sk-ant-YOUR-KEY"
else
    echo "✅ .env existiert"
fi

# Zusammenfassung
echo ""
echo "======================================="
echo "✅ Installation abgeschlossen!"
echo "======================================="
echo ""
echo "Nächste Schritte:"
echo "1. Anthropic API Key setzen:"
echo "   nano .env  (oder Editor deiner Wahl)"
echo ""
echo "2. Dashboard starten:"
echo "   python menu_qa_app.py"
echo ""
echo "3. Im Browser öffnen:"
echo "   http://localhost:5000"
echo ""
