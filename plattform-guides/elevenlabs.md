# ElevenLabs — Plattform-Konventionen

## Systemvariablen
Folgende Variablen stehen im Prompt zur Verfügung:
- `{{system__time}}` — aktuelle Uhrzeit
- `{{system__agent_id}}` — ID des Agenten
- `{{name}}` — Name des Angerufenen (wenn via API übergeben)
- Eigene Variablen können beim Anrufstart via API als dynamische Parameter
  übergeben werden, z.B. `{{marke}}`, `{{modell}}`, `{{tuev_datum}}`

## Gesprächssteuerung mit <wait for user response>
Bei strukturierten Gesprächsabläufen den Tag `<wait for user response>` 
nach jeder Frage einfügen. Dies signalisiert dem Agenten, dass er auf eine 
Antwort warten soll, bevor er weitermacht. Ohne diesen Tag besteht das 
Risiko, dass der Agent mehrere Schritte hintereinander abarbeitet ohne auf 
den Kunden zu warten.

## Gesprächsstruktur
Komplexe Prompts immer in nummerierte Schritte unterteilen:
- ## Schritt 1, ## Schritt 2 usw.
- Mit klar benannten Verzweigungen:
  "### Bei Interesse:" / "### Bei Ablehnung:" / "### Bei Unsicherheit:"
- Jede Verzweigung führt entweder zum nächsten Schritt oder zum Abschluss
- Keine offenen Enden — jeder Pfad endet mit hangup

## Erste Nachricht (First Message)
- ElevenLabs-Agenten haben eine statische "First Message", die vor dem
  Systemprompt gesprochen wird
- Diese wird NICHT im Systemprompt definiert, sondern separat im Dashboard
  oder via API eingetragen
- Im generierten Prompt wird die empfohlene First Message als eigener
  Abschnitt am Ende ausgegeben:
  `## Empfohlene Erste Nachricht (First Message — separat im Dashboard eintragen)`
- Bei Outbound-Agenten: First Message leer lassen oder auf eine kurze neutrale
  Begrüssung setzen — der eigentliche Einstieg erfolgt über Schritt 1

## Gesprächsende
- Zum Beenden des Anrufs wird die Funktion `hangup` verwendet
- Immer am Ende jedes Gesprächspfads eintragen — kein Pfad ohne hangup
- Beispiel im Prompt: "Beende den Anruf mit hangup."

## Anrufweiterleitung
- Weiterleitung an einen Menschen oder eine andere Nummer: `transfer_to_number`
- Beispiel: "Bei komplexen Anliegen leite den Anruf weiter mit transfer_to_number."

## Tools-Abschnitt
Jeden verwendeten Tool-Aufruf unter einem eigenen Abschnitt "# Tools" auflisten 
mit Beschreibung des Zwecks. Reihenfolge:
1. Funktionale Tools (z.B. kalenderCheck, terminBuchen)
2. hangup immer zuletzt

## Ton & Stil Abschnitt
Jeden Prompt mit einem eigenen "# Ton & Stil" Abschnitt versehen:
- Sie-Form oder du-Form explizit festlegen
- Natürliche Füllwörter definieren (z.B. "Okay", "Alles klar", "Wunderbar")
- Hinweis auf kurze, klare Sätze
- Hinweis auf kein Druck / keine Hektik bei Outbound

## Wichtige Eigenheiten
- ElevenLabs liest den Systemprompt vollständig — halte ihn klar strukturiert
  und vermeide redundante Wiederholungen
- Vermeide Markdown-Formatierung (**, Listen mit -) im gesprochenen Text,
  da diese vom TTS vorgelesen werden können
- Halte Anweisungen imperativisch: "Frage nach dem Namen." statt
  "Du solltest versuchen, nach dem Namen zu fragen."
- Zahlen immer ausschreiben wenn sie gesprochen werden sollen:
  "achtzehn Uhr" statt "18:00 Uhr"
- Daten natürlich formulieren: "Am fünfzehnten März" statt "15.03."
- Das LLM Modell 'Gemini 2.0 Flash' existiert in der Platform nicht, nutze daher'Gemini 2.5 Flash'

## Empfohlene Prompt-Gesamtstruktur
# Rolle
# Kontext
# Spezifikationen
# Hauptaufgabe: [TITEL]
  ## Schritt 1: ...
  ## Schritt 2: ...
  ## Schritt N: Abschluss bei Erfolg
  ## Schritt N+1: Abschluss bei Ablehnung
# Tools
# Ton & Stil
# Wichtige Hinweise
# Notizen
