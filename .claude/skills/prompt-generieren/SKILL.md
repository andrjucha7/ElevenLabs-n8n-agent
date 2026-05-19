# Skill: Prompt Generieren

## Zweck
Dieser Skill steuert den Ablauf zur Erstellung eines fertigen ElevenLabs 
Voice AI Prompts basierend auf der Nutzerbeschreibung.

## Auslöser
Aktivierung wenn der Nutzer einen neuen Agenten-Prompt erstellen möchte:
- "Erstelle mir einen Prompt für..."
- "Ich brauche einen Agenten für..."
- "Baue mir einen Voice Agent für..."

## Ablauf

### Phase 1 — Informationssammlung
Lies zuerst CLAUDE.md, /plattform-guides/elevenlabs.md und alle Dateien 
in /vorlagen/.

Pflichtfelder — stelle gezielte Fragen für folgende Punkte:
- Unternehmensname
- Branche / Was bietet das Unternehmen an?
- Use Case (Inbound FAQ / Terminbuchung / Outbound / Kundenservice / Sonstiges)
- Ziel des Anrufs (was soll am Ende des Gesprächs erreicht sein?)
- Gewünschter Ton (formell mit "Sie" / informell mit "du")
- Name des Agenten
- Welche Tools werden benötigt? (z.B. Kalender-API, Buchungssystem, CRM)

Optionale Felder (nur fragen wenn relevant für den Use Case):
- Dynamische Variablen die per API übergeben werden (z.B. Name, Fahrzeugdaten)
- Standorte und Öffnungszeiten
- Eskalationsnummer für transfer_to_number
- Verbotene Themen oder besondere Einschränkungen
- Kontakt-E-Mail oder Telefon für Weiterleitungshinweise

### Phase 2 — Vorlage auswählen
- Inbound FAQ → /vorlagen/inbound-faq.md
- Terminbuchung → /vorlagen/terminbuchung.md
- Outbound → /vorlagen/outbound-leadgen.md
- Kundenservice → /vorlagen/kundenservice.md
- Sonstiges → Prompt von Grund auf nach der Struktur in elevenlabs.md erstellen

### Phase 3 — Prompt befüllen
Ersetze alle Platzhalter mit den gesammelten Informationen. Passe die 
Schritt-Struktur an den konkreten Use Case an — füge Schritte hinzu oder 
entferne überflüssige. Stelle sicher dass:
- Jeder Gesprächspfad mit hangup endet
- Nach jeder Frage <wait for user response> steht
- Alle Tools im Tools-Abschnitt aufgelistet sind
- Zahlen und Daten ausgeschrieben sind
- Kein Markdown im gesprochenen Text verwendet wird

### Phase 4 — Speichern und ausgeben
Speichere unter: /output-prompts/[unternehmensname]-[use-case].md

Gib den vollständigen Prompt im Chat aus. Weise danach explizit auf 
folgende manuelle Schritte hin:
1. First Message im ElevenLabs Dashboard eintragen (aus dem letzten 
   Abschnitt des Prompts)
2. Tools im Dashboard anlegen und mit den im Prompt genannten Namen verknüpfen
3. Dynamische Variablen in den Agent-Einstellungen konfigurieren (falls vorhanden)
