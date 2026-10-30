# SoundGen — generator dźwięków silników (Das Panzer)

`index.html` – jednoplikowa aplikacja (bez serwera): fizyczna synteza pętli silników czołgów (jałowy / średnie /
wysokie obroty), odsłuch, własne obroty i obciążenie, eksport ZIP (OGG Vorbis lub WAV). Otwórz plik w przeglądarce.

`AUDYT_SILNIKI.md` – jak brzmią prawdziwe silniki, pomiary nagrań, opis modelu i parametrów.

`tools/render.js` – render z wiersza poleceń (Node): `node tools/render.js list | wav <katalog> [id]... | custom <katalog> <id> <obr/min> <obciążenie 0-1> | check`.
