Mit dieser Applikation möchten wir Mitarbeitende der kantonalen Verwaltung dabei unterstützen, ihre Kommunikation noch verständlicher aufzubereiten.

## Wichtig

- Die App ist ausschliesslich für Mitarbeitende der kantonalen Verwaltung.
- Du darfst die App ausschliesslich für dienstliche Zwecke nutzen.
- Mit der App kannst du vertrauliche Informationen verarbeiten.
- Die App speichert keine Texte und keine Ergebnisse.
- Die App liefert lediglich einen Entwurf. Überprüfe das Ergebnis immer und passe es an, wenn nötig.

## Was macht diese App?

**Diese App vereinfacht einen von dir eingegebenen Text.**

Dein Text wird dazu in der App aufbereitet und an ein sogenanntes grosses Sprachmodell (LLM, Large Language Model) eines kommerziellen Anbieters geschickt. Diese Sprachmodelle sind in der Lage, Texte nach Anweisungen umzuformulieren und dabei zu vereinfachen.

Die App bietet dir drei verschiedene Grade der Vereinfachung:

- **Verständlichere Sprache**: Vereinfachung nach gängigen Sprachregeln für bessere Textverständlichkeit. Zielniveau etwa B2.
- **Einfache Sprache**: Vereinfachung nach den [Regeln für Einfache Sprache des Kantons Zürich](https://www.zh.ch/de/webangebote-entwickeln-und-gestalten/inhalt/inhalte-gestalten/informationen-bereitstellen/umgang-mit-sprache.html). Zielniveau B1 bis A2.
- **Leichte Sprache**: Vereinfachung nach den [Regeln für Leichte Sprache des Kantons Zürich](https://www.zh.ch/de/webangebote-entwickeln-und-gestalten/inhalt/barrierefreiheit/regeln-fuer-leichte-sprache.html). Zielniveau A2 bis A1.

**Die Texte werden teils in sehr guter Qualität vereinfacht. Sie sind aber nie 100% korrekt. Die App liefert lediglich einen Entwurf. Die Texte müssen immer von dir überprüft und angepasst werden.**

### Was sind die verschiedenen Sprachmodelle?

Momentan kannst du eins von 4 Sprachmodellen wählen:

- [Llama 3.1 Nemotron](https://huggingface.co/nvidia/Llama-3.1-Nemotron-70B-Instruct)
- [Llama 3.1 «Sauerkraut»](https://huggingface.co/VAGOsolutions/Llama-3.1-SauerkrautLM-70b-Instruct)
- [Gemma 2](https://huggingface.co/google/gemma-2-27b)
- [Phi-4](https://huggingface.co/microsoft/phi-4)

Speziell für Leichte Sprache eignet sich::

- [Llama 3.3](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct)

Alle Modelle analysieren und schreiben unterschiedlich und sind alle einen Versuch wert.

### Wie funktioniert die Bewertung der Verständlichkeit?

Wir haben einen Algorithmus entwickelt, der die Verständlichkeit von Texten automatisch in Punkten auf einer Skala von -10 bis +10 bewertet. Dieser Algorithmus basiert auf 5 Textmerkmalen: Der Wortlänge, der Satzlänge, dem [Lesbarkeitsindex RIX](https://www.jstor.org/stable/40031755), der Häufigkeit von viel genutzten Worten sowie dem Anteil von Worten aus dem offiziellen Vokabular A1 bis B2 des Goethe Instituts. Wir haben diese Merkmale systematisch ermittelt, indem wir geschaut haben, welche Merkmale am aussagekräftigsten für Verwaltungs- und Rechtssprache und deren Vereinfachung sind.

Die Bewertung kannst du so interpretieren:

- **Sehr schwer verständliche Texte** wie Rechts- oder Verwaltungstexte haben meist Werte von **-10 bis -2**.
- **Durchschnittlich verständliche Texte** wie Nachrichtentexte, Wikipediaartikel oder Bücher haben Werte von etwa **-2 bis 0**.
- **Gut verständliche Texte im Bereich Einfacher Sprache und Leichter Sprache** haben Werte von etwa **0 oder höher**.

Wir zeigen dir zusätzlich eine grobe Schätzung des Sprachniveaus gemäss [CEFR (Common European Framework of Reference for Languages)](https://www.coe.int/en/web/common-european-framework-reference-languages/level-descriptions) von A1 bis C2 an.  

### Image ###

Die Bewertung ist bei weitem nicht perfekt, aber sie ist ein guter Anhaltspunkt. Wir arbeiten daran, die Bewertung weiter zu verbessern.

## Wie geht es weiter?

Wir möchten das System kontinuierlich nach Nutzungsbedürfnissen verbessern. Wir sind für Rückmeldungen und Anregungen jeglicher Art jederzeit dankbar und nehmen diese gern [per Mail entgegen](mailto:patrick.arnecke@statistik.ji.zh.ch).

## Versionsverlauf

- **v0.1** 31.01.2025 - *Erste Version der App.*
