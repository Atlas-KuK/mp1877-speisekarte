# 📱 Speisekarten QA Tool — Handy-Setup

Das QA Tool kannst du auf deinem **Handy, Tablet oder anderen Geräten** im gleichen WLAN-Netzwerk nutzen!

## Setup für Handy-Zugriff

### 1. Server starten (Computer)

```bash
python menu_qa_app.py
```

Du siehst dann:
```
🌐 Lokal (dieser Computer): http://localhost:5000
📱 Handy/anderes Gerät:      http://192.168.1.100:5000
```

**Merke dir die Handy-IP!** (z.B. `192.168.1.100:5000`)

### 2. Im Handy-Browser öffnen

Öffne in deinem Handy-Browser (Chrome, Safari, etc.):
```
http://192.168.1.100:5000
```
(Ersetze `192.168.1.100` mit deiner tatsächlichen IP)

## ✨ Features auf dem Handy

✅ Drag & Drop Upload (auf touch-fähigen Geräten)  
✅ Dateibrowser zum Auswählen  
✅ Responsive Design (passt sich ans Handy an)  
✅ Alle QA-Checks funktionieren  
✅ Claude AI-Review auf dem Handy  

## 🔍 IP-Adresse ermitteln

Wenn du die IP oben nicht siehst:

**Linux/macOS:**
```bash
hostname -I
# oder
ifconfig | grep "inet "
```

**Windows:**
```cmd
ipconfig
# Suche: "IPv4-Adresse"
```

## 🛡️ Sicherheits-Tipps

⚠️ **Wichtig:** Der Server läuft auf **0.0.0.0** (alle Netzwerk-Interfaces)

- ✅ Verwende nur im **privaten Heimnetzwerk** / **Restaurant-WLAN**
- ✅ Nicht über das **Internet** exponieren
- ✅ Passwort-Schutz optional (siehe unten)

### Optional: Lokal-only (sicherer)

Wenn du das Tool **nur lokal** (Computer) brauchst:

```bash
# In .env setzen:
FLASK_HOST=localhost
FLASK_PORT=5000
```

Dann nur erreichbar unter: `http://localhost:5000`

## 🚀 Workflow mit Handy

1. **Am Server:** Terminal laufen lassen
   ```bash
   python menu_qa_app.py
   ```

2. **Am Handy:** Browser öffnen
   ```
   http://192.168.X.X:5000
   ```

3. **Menü-Foto/PDF** hochladen
   - Kamera-Foto machen
   - Oder Datei aus Galerie wählen

4. **Sofort Analyse** sehen

5. **Report exportieren** (JSON)

## 📷 Best Practices für Handy-Fotos

- 📸 Gutes Licht, scharfes Bild
- 📐 Flach fotografieren (keine Winkel)
- 📏 Ganzes Dokument im Frame
- ⚪ Weißer Hintergrund hilft OCR

## ❓ Troubleshooting

**Problem:** Handy kann nicht auf IP zugreifen

**Lösungen:**
1. ✅ Handy und Computer im **gleichen WLAN**?
2. ✅ Firewall blockiert Port 5000?
   ```bash
   # Linux/macOS:
   sudo ufw allow 5000
   ```
3. ✅ Router erlaubt Device-to-Device?
   (Manchmal "Gastnetzwerk" deaktiviert das)

**Problem:** Upload funktioniert nicht

- ✅ Größe < 50 MB?
- ✅ Format unterstützt? (PDF, PNG, JPG, GIF, BMP)
- ✅ Server-Logs überprüfen

**Problem:** Langsam/reagiert nicht

- ✅ Handy <-> Computer Verbindung stabil?
- ✅ WLAN-Signal stark?
- ✅ Server ist nicht überlastet?

## 🌐 Optional: Im Internet nutzbar

⚠️ **Achtung:** Nur wenn du weißt, was du tust!

Mit **ngrok** oder **tunneling service** kannst du das Tool auch übers Internet nutzen:

```bash
# Installation
brew install ngrok  # oder Download von ngrok.com

# Tunnel öffnen (während menu_qa_app.py läuft)
ngrok http 5000
```

Dann URL teilen, die ngrok zeigt (z.B. `https://abc123.ngrok.io`)

⚠️ Aber: **Speicherkarten werden zu ngrok übertragen** → Datenschutz!

---

**Hinweis:** Für Produktionseinsatz im Restaurant empfehlen wir:
- Feste IP-Adresse für den Server
- Optional: HTTPS mit self-signed Zertifikat
- Optional: Basic Authentication hinzufügen
