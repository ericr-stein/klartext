Mit dieser Applikation möchten wir Mitarbeitende dabei unterstützen, noch verständlicher zu kommunizieren.

## Wichtig

- **Mit der App kannst du öffentliche, interne und vertrauliche Daten / Informationen verarbeiten.**
- **Geheime Daten darfst du nicht in die App eingeben.**
- **Die App speichert keine Texte und keine Ergebnisse. Alle Daten werden auf einem KI-Server beim AFI in einem eigenen kantonalen Rechenzentrum *(on premise)* verarbeitet.**
- **Sprachmodelle machen Fehler. Die App liefert lediglich einen Entwurf. Überprüfe das Ergebnis immer und passe es an, wenn nötig.**
- Die App ist ausschliesslich für Mitarbeitende der kantonalen Verwaltung.
- Du darfst die App ausschliesslich für dienstliche Zwecke nutzen.

## Was macht diese App?

**Diese App vereinfacht einen von dir eingegebenen Text.**

Dein Text wird dazu in der App aufbereitet und an ein sogenanntes grosses Sprachmodell (LLM, Large Language Model) auf einem AFI KI-Server geschickt. Diese Sprachmodelle sind in der Lage, Texte nach Anweisungen umzuformulieren und dabei zu vereinfachen.

Die App bietet dir drei verschiedene Grade der Vereinfachung:

- **Verständliche Sprache**: Vereinfachung nach gängigen Sprachregeln für bessere Textverständlichkeit. Zielniveau etwa B2.
- **Einfache Sprache**: Vereinfachung nach den [Regeln für Einfache Sprache des Kantons Zürich](https://www.zh.ch/de/webangebote-entwickeln-und-gestalten/inhalt/inhalte-gestalten/informationen-bereitstellen/umgang-mit-sprache.html). Zielniveau B1 bis A2.
- **Leichte Sprache**: Vereinfachung nach den [Regeln für Leichte Sprache des Kantons Zürich](https://www.zh.ch/de/webangebote-entwickeln-und-gestalten/inhalt/barrierefreiheit/regeln-fuer-leichte-sprache.html). Zielniveau A2 bis A1.

**Die Texte werden teils in guter Qualität vereinfacht. Sprachmodelle machen aber auch Fehler. Die App liefert lediglich einen Entwurf. Die Texte müssen immer von dir überprüft werden. Du bleibst für die Ergebnisse immer verantwortlich.**

### Welches Sprachmodell wird in der App verwendet?

Wir setzen das Open-Source-Sprachmodell [**Phi-4** von Microsoft](https://huggingface.co/microsoft/phi-4) ein. Das Modell können wir lokal betreiben und haben es zudem mit einem sog. Finetuning spezifisch auf unsere Sprachleitfäden optimiert.


### Wie funktioniert die Bewertung der Verständlichkeit?

Wir haben einen Algorithmus entwickelt, der die Verständlichkeit von Texten misst. Damit können wir das Sprachniveaus gemäss [CEFR (Common European Framework of Reference for Languages)](https://www.coe.int/en/web/common-european-framework-reference-languages/level-descriptions) von A1 bis C2 einschätzen. Wir zeigen dir das Sprachniveau für deinen Ausgangstext und das Ergebnis an. Die Bewertung ist nicht 100% exakt, aber sie ist ein guter Anhaltspunkt.

## Wie geht es weiter?

Wir möchten das System kontinuierlich nach Nutzungsbedürfnissen verbessern. Wir sind für Rückmeldungen und Anregungen jeglicher Art jederzeit dankbar und nehmen diese gern [per Mail entgegen](mailto:patrick.arnecke@statistik.ji.zh.ch).

## Versionsverlauf

- **v1.0.0** 22.07.2025 - *Optimiertes Sprachmodell Phi-4 KTZH. Neues einfacheres UI. Ergebnisse werden gestreamt.*
- **v0.2.0** 05.05.2025 - *Verbesserte Prompts und Modelle. Einfachere Bedienung der App.*
- **v0.1.0** 24.03.2025 - *Erste Version der App.*
