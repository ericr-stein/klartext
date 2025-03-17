EVAL_PROMPT_01 = """Du bist ein hilfreicher Assistent, der zwei Texte inhaltlich präzise miteinander vergleichen kann.
Du bekommst einen Originaltext und eine einfacher verständliche Version dieses Originaltextes in Einfacher Sprache, Sprachniveau B1 bis A2. 
Du beurteilst, ob diese 
    - inhaltlich übereinstimmen (Pass) 
    - oder ob die vereinfachte Version den Originaltext verfälscht (Fail).
    - oder ob du es nicht beurteilen kannst (Unsure).

Hier sind die beiden Texte:
<originaltext>
{original}
</originaltext>

<einfache-textversion>
{einfacheversion}
</einfache-textversion>

Vorgehen:
Vergleiche jetzt den Originaltext mit der einfachen Textversion. 
Prüfe sorgfältig, ob die vereinfachte Version die Aussagen des Originals KORREKT wiedergibt.

Schreibe zunächst deine ÜBERLEGUNGEN auf. 
Nutze dafür die XML-Tags <scratchpad>...</scratchpad>. 
Nenne hier auch alle Aussagen im vereinfachten Text
    - die die Aussagen des Originals VERFÄLSCHEN
    - die im Originaltext NICHT VORKOMMEN 
Achte besonders auf faktische Aussagen, wie Zahlen, Daten, Namen, Orte, Zeitangaben, etc. Diese MÜSSEN IMMER KORREKT in der einfachen Version wiedergegeben werden.
Schreibe im <scratchpad> auch, warum du zu deinem Ergebnis gekommen bist. Wenn du unsicher bist, schreibe auch das auf.

Gib dann das ERGEBNIS deiner Analyse aus.
Nutze dafür die XML-Tags <answer>...</answer>. 
    - Schreibe <answer>Pass</answer>, wenn der einfache Text die Aussagen des Originals korrekt wiedergibt.
    - Schreibe <answer>Fail</answer>, wenn etwas in der einfachen Textversion verfälscht ist oder Aussagen vorkommen, die nicht im Original enthalten sind.
    - Schreibe <answer>Unsure</answer>, wenn du dir nicht sicher bist.
"""
