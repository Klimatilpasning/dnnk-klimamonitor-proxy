# DNNK klimamonitor

## Når KP refererer til en sag fra klimamonitoren
Når KP nævner en sag fra klimamonitoren, ugemailen eller "ugens fund" (fx "Kolding-pumpeslusen" eller "det med Lufthavnsdiget"):

1. Slå den op i `ugevurdering.json` på branchen `claude/ugevurdering` (`git fetch origin claude/ugevurdering && git show origin/claude/ugevurdering:ugevurdering.json`). Hvert punkt har titel, url, kilde, dato, farve og begrundelse. Ældre uger ligger i git-historikken for filen.
2. Brug punktets præcise URL som udgangspunkt for svaret, ikke en ny websøgning.
3. Log et signal i `kriterier.md` på branchen `claude/ugevurdering` under "Signaler" i formatet: `- ÅÅÅÅ-MM-DD - [titel](url) - farve i rapporten - hvad KP gjorde`. Commit og push til `claude/ugevurdering`. KP skal ikke gøre noget for at signalet logges.

Skriv på dansk, brug kun "-" (ingen lange tankestreger), og skriv "klimatilpasning", ikke "klimasikring" (titler fra kilder må citeres uændret).
