# 🍽️ Speisekarten QA Tool — Setup-Anleitung

Ein automatisiertes Tool zur Überprüfung von Speisekarten-PDFs und -Bildern auf Rechtschreibung, Grammatik, Formatierung und Layout.

## Features

✅ **OCR-Texterkennung** aus PDFs und Bildern (Deutsch-optimiert)
✅ **Automatische Rechtschreib-Checks** (deutsche Regeln)
✅ **Grammatik-Überprüfung** (LanguageTool)
✅ **Layout-Analyse** (Abstände, Konsistenz, Formatierung)
✅ **KI-Review mit Claude** (Haiku, Sonnet, Opus)
✅ **Drag & Drop Upload** + Datei-Explorer
✅ **Report-Export** (JSON)

## Voraussetzungen

### System-Abhängigkeiten

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip tesseract-ocr poppler-utils
```

**macOS (Homebrew):**
```bash
brew install tesseract poppler
```

**Windows:**
- Download & install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
- Download & install Poppler: https://github.com/oschwartz10612/poppler-windows/releases/

### Python-Abhängigkeiten

Python 3.8+

## Installation

### 1. Virtual Environment erstellen

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# oder
venv\Scripts\activate  # Windows
```

### 2. Python-Pakete installieren

```bash
pip install -r requirements.txt
```

### 3. API-Key konfigurieren

Die Claude AI-Review braucht einen Anthropic API Key:

```bash
# Kopiere .env.example zu .env
cp .env.example .env

# Editiere .env und setze deinen API Key
# ANTHROPIC_API_KEY=sk-ant-YOUR-KEY-HERE
```

**API Key holen:** https://console.anthropic.com/

### 4. Tesseract-Pfad (Windows nur)

Falls Tesseract nicht in PATH ist, muss der Pfad gesetzt werden:

```python
# In menu_qa_app.py nach den Imports hinzufügen:
import pytesseract
pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## Verwendung

### Dashboard starten

```bash
python menu_qa_app.py
```

Öffne dann: **http://localhost:5000**

### Workflow

1. **Upload** → PDF oder Bild hochladen (Drag & Drop oder Dateiauswahl)
2. **OCR** → Text wird automatisch extrahiert
3. **Automatische Checks** → Rechtschreibung, Grammatik, Layout werden analysiert
4. **KI-Review** → Optional Claude-basierte detaillierte Überprüfung
5. **Export** → Report als JSON herunterladen

## Unterstützte Dateitypen

- **PDF** (.pdf) → mit OCR verarbeitet
- **Bilder** (.png, .jpg, .jpeg, .gif, .bmp) → direkt mit OCR verarbeitet

Max. Dateigröße: **50 MB**

## Was wird überprüft?

### Automatische Checks
- ✅ Doppelte Leerzeichen
- ✅ Zeilenstruktur & -längen
- ✅ Grammatische Fehler (Deutsch)
- ✅ Konsistenz von Abstände

### KI-Review (Claude)
- ✅ Detaillierte Rechtschreib- & Grammatik-Analyse
- ✅ Formatierungs-Konsistenz (Preise, Einheiten, Schreibweisen)
- ✅ Layout-Bewertung (ist alles ordentlich arrangiert?)
- ✅ Lesbarkeits-Analyse
- ✅ Spezifische Empfehlungen

## Claude-Modelle

Wähle das beste Modell für deine Anforderungen:

| Modell | Geschwindigkeit | Qualität | Kosten | Ideal für |
|--------|----------------|----------|--------|-----------|
| **Haiku** | ⚡⚡⚡ | ⭐⭐ | € | Schnelle Vorprüfung |
| **Sonnet** | ⚡⚡ | ⭐⭐⭐⭐ | €€ | Standard-Review |
| **Opus** | ⚡ | ⭐⭐⭐⭐⭐ | €€€ | Detaillierte Analyse |

## Troubleshooting

### OCR funktioniert nicht
```bash
# Tesseract neu installieren
sudo apt-get remove tesseract-ocr
sudo apt-get install tesseract-ocr
```

### PDF2Image Fehler
```bash
# Poppler neu installieren
sudo apt-get install poppler-utils
```

### Claude-Review zeigt Fehler
- ✅ Überprüfe, dass ANTHROPIC_API_KEY in .env gesetzt ist
- ✅ API Key muss gültig und aktiv sein
- ✅ Rate-Limits beachten (siehe Anthropic Docs)

### Port 5000 ist belegt
```bash
# Port ändern in menu_qa_app.py:
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Oder anderer Port
```

## Performance-Tipps

- **Große PDFs:** Teile sie in mehrere Dateien
- **Schnelle Vorprüfung:** Nutze Haiku-Modell statt Opus
- **Batch-Verarbeitung:** Mehrere Dateien nacheinander hochladen

## Datenschutz

- ✅ Dateiverarbeitung erfolgt lokal auf diesem Server
- ✅ Nur der extrahierte Text wird zu Claude gesendet (falls AI-Review aktiv)
- ✅ Hochgeladene Dateien werden nach Verarbeitung gelöscht
- ⚠️ Text wird an Anthropic API übertragen bei Claude-Review

## Kostenübersicht (Claude API)

Ungefähre Kosten für 100 Speisekarten-Reviews:

- **Haiku:** ~$0.05
- **Sonnet:** ~$0.50
- **Opus:** ~$5.00

(Preise können variieren, siehe https://www.anthropic.com/pricing)

## Häufige Fragen

**F: Kann ich auch Handschrift erkennen?**
A: OCR mit Tesseract funktioniert best bei gedrucktem Text. Handschrift wird nicht gut erkannt.

**F: Wie lange dauert eine Überprüfung?**
A: OCR/Checks: 2-5 Sek. | Claude-Review: 10-30 Sek. (abhängig von Modell)

**F: Kann ich mehrere Dateien gleichzeitig hochladen?**
A: Derzeit eine nach der anderen. Batch-Upload könnte in zukünftigen Versionen hinzugefügt werden.

**F: Wie kann ich meine eigenen Custom-Checks hinzufügen?**
A: Editiere die `check_*`-Funktionen in `menu_qa_app.py`

## Support

Bei Fragen oder Problemen:
1. Überprüfe das Troubleshooting-Kapitel oben
2. Sieh dir die App-Logs an
3. Erstelle ein GitHub Issue

---

**Version:** 1.0  
**Letzte Aktualisierung:** 2024-05-14  
**Mettgenpin 1877 GmbH**
