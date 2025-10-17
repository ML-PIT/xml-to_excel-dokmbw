# dokmbw_komplett_Auto-v1-3.py Neu

 1. Konfigurations-Menü (Button "⚙️ Konfiguration")

  - E-Mail Tab: E-Mail-Adressen, Passwörter, SMTP-Host, Empfänger, Betreff & Text bearbeitbar
  - Zeitplanung Tab: Abrufzeit einstellbar + Server-Wochentag-Konfiguration (z.B. Server 01 nur Mo+Mi, Server 02 nur Fr)
  - Kürzel-Mapping Tab: Seminartitel → Kürzel Zuordnung vollständig editierbar, neue hinzufügen möglich

  2. Server-Wochentag-Konfiguration

  - Für jeden Server (01-10) individuell einstellbar an welchen Wochentagen (Mo-So) er abgerufen wird
  - Wenn nichts konfiguriert: Standard Mo-Fr wie bisher

  3. SQLite-Datenbank (dokmbw_bewertungen.db)

  - Speichert alle Bewertungen automatisch
  - Berechnet Gesamtnote pro Bewertung

  4. Statistik-Fenster (Button "📊 Statistiken")

  - Zeigt Gesamtnotendurchschnitt pro Trainer
  - Anzahl Bewertungen, beste & schlechteste Note
  - Button "📊 Details anzeigen": Zeigt vollständige beste/schlechteste Bewertung mit allen Kommentaren

  5. Konfigurationsdatei (dokmbw_config.json)

  - Alle Einstellungen werden persistent gespeichert
  - Kann manuell bearbeitet werden

  Die bestehenden Funktionen (manuelle Serverauswahl, automatischer Abruf, Präsenzmodus) bleiben vollständig erhalten.