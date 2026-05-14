# 🚀 Deployment — Online-Speisekarten QA Tool

Deploye das QA Tool kostenlos online auf **Railway.app** oder **Render.com**.

## Option 1: Railway.app (EMPFOHLEN) ⭐

Railway ist einfach und kostenlos für Hobby-Projekte.

### 1. Account erstellen

Gehe zu: https://railway.app

- Sign up (GitHub Login empfohlen)
- Verifiziere deinen Account

### 2. Neues Projekt erstellen

```
Dashboard → New Project → Deploy from GitHub
```

### 3. GitHub verbinden

- Authorize Railway mit deinem GitHub
- Wähle das Repository: `Atlas-KuK/mp1877-speisekarte`
- Branch: `claude/review-menu-quality-etxbF` (oder main)

### 4. Environment-Variablen setzen

Im Railway Dashboard:

```
Variables → Add Variable
```

Füge hinzu:
```
ANTHROPIC_API_KEY = sk-ant-dein-api-key-hier
FLASK_HOST = 0.0.0.0
FLASK_PORT = 5000
```

### 5. Deploy starten

Railway erkennt automatisch das `Dockerfile` und deployed es.

Nach 2-3 Minuten siehst du:
```
✅ Deployment erfolgreich
🌐 https://dein-app-name.up.railway.app
```

### 6. Online nutzen

Öffne einfach:
```
https://dein-app-name.up.railway.app
```

Fertig! 🎉

---

## Option 2: Render.com

Auch kostenlos, ähnlich einfach wie Railway.

### 1. Account erstellen

https://render.com → Sign up

### 2. New Web Service

```
Dashboard → New → Web Service
```

### 3. GitHub verbinden

- Authorize Render
- Wähle Repository
- Wähle Branch

### 4. Konfiguration

```
Name:             speisekarten-qa
Environment:      Docker
Region:           Europe (Frankfurt)
```

### 5. Environment-Variablen

Unter "Environment":
```
ANTHROPIC_API_KEY = sk-ant-...
FLASK_HOST = 0.0.0.0
```

### 6. Deploy

Click "Create Web Service"

Nach 3-5 Minuten live! 🚀

---

## Option 3: Heroku (Kostenpflichtig)

Heroku war kostenlos, jetzt kostenpflichtig (~$5/Monat).

Falls du Heroku nutzen möchtest:

```bash
# Install Heroku CLI
brew install heroku

# Login
heroku login

# Create app
heroku create dein-app-name

# Set variables
heroku config:set ANTHROPIC_API_KEY=sk-ant-...

# Deploy
git push heroku claude/review-menu-quality-etxbF:main

# Open
heroku open
```

---

## 🔑 API-Key Sicherheit

⚠️ **WICHTIG:** Schütze deinen Anthropic API Key!

```
NIEMALS ins Git committen!
NUR über Platform-Secrets setzen (Railway/Render UI)
```

Überprüfe:
```bash
grep -r "sk-ant" .  # Sollte nichts finden!
```

Falls du versehentlich gepusht hast:
1. Key sofort deaktivieren (console.anthropic.com)
2. Neuen Key erstellen
3. In Railway/Render aktualisieren

---

## 💰 Kosten

### Railway.app
- **Free Tier:** $5/Monat credits
- Für dieses Tool: **kostenlos** (passt locker rein)

### Render.com
- **Free Tier:** 1 Web Service (Dormancy nach 15 min Inaktivität)
- Für dieses Tool: **kostenlos**

### Heroku
- **Starter:** ~$5/Monat

---

## 🛠️ Troubleshooting

### Deploy schlägt fehl

```
❌ Build failed
```

Überprüfe:
1. ✅ Dockerfile existiert?
2. ✅ requirements.txt aktuell?
3. ✅ API Key gesetzt?
4. Logs anschauen (Platform zeigt Details)

### App ist langsam / reagiert nicht

- **Problem:** OCR auf Tesseract braucht Zeit
- **Lösung:** 
  - First upload kann 10-20 Sek dauern
  - Free-Tier Server sind nicht schnell
  - Upgrade auf bezahlten Tier für schneller

### Speicherplatz voll

- Temp-Dateien werden nicht gelöscht
- Lösungs-Code in `menu_qa_app.py` anpassen:

```python
# Nach Verarbeitung:
try:
    os.remove(filepath)
except:
    pass
```

---

## 📋 Checkliste vor Deploy

- [ ] Dockerfile existiert
- [ ] requirements.txt aktuell
- [ ] `.env` NICHT ins Git
- [ ] API Key sicher gespeichert (nur via Platform)
- [ ] Branch gepusht (`claude/review-menu-quality-etxbF`)
- [ ] Railway/Render Account erstellt
- [ ] GitHub Authorization konfiguriert

---

## 🌐 Nach dem Deploy

### URL teilen

```
Deine App läuft unter:
https://dein-app-name.up.railway.app
```

Teile diese URL mit:
- Team-Mitgliedern
- Testern
- Kunden

### Monitoring

Railway/Render zeigen:
- ✅ Deployment Status
- 📊 CPU / Memory Usage
- 📋 Logs in Echtzeit
- 🔄 Auto-Redeploy bei Push

---

## 🆘 Support

Falls etwas nicht funktioniert:

1. **Logs überprüfen** (Platform Dashboard)
2. **API Key überprüfen** (gültig, nicht abgelaufen?)
3. **OCR-Fehler?** → Tesseract funktioniert auf diesem Server
4. **PDF-Fehler?** → Poppler installation überprüfen

---

**Ready to go live?** 🚀

Wähle deine Plattform und los geht's!
