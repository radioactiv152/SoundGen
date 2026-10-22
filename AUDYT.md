# Audyt: Das Panzer — generator dźwięków (`index.html`)

## Co to jest

Jednoplikowa aplikacja (≈3,5 tys. linii, bez zależności). Syntetyzuje ok. 110 efektów dźwiękowych
(≈190 plików z wariantami i poziomami obrotów) w przeglądarce i eksportuje je do ZIP-a (OGG Vorbis albo WAV).
Ma też manifest JSON i raport głośności.

| Warstwa | Zawartość |
|---|---|
| `<script id="engine">` | FFT (radix-2, mieszany radix, Bluestein), własny koder Vorbis, ZIP, DSP (Butterworth, rezonatory, filtry STFT, szum okresowy, pogłos), mastering (LUFS wg BS.1770, limiter z wyprzedzeniem), rejestr `sfx()` i wersje brzmień v1 / v2 / v3 (teraz też v4) |
| drugi `<script>` | interfejs: lista, filtry, odsłuch, A/B, pula Web Workerów (kod silnika przekazywany jako Blob), eksport |

Mocne strony: deterministyczne ziarna (`crc32(id:sub:v)` + ziarno globalne), pętle liczone okresowo
(szum z FFT, filtry z „potrójnym” buforem, splot kołowy), więc szwy są czyste. Działa offline, ma awaryjny
tryb bez workerów, mastering do LUFS z limiterem, a najdłuższe zadania eksportu idą na początek kolejki.

## Znalezione problemy

### Błędy w kodzie (poprawione)

1. **Wyścig przy odsłuchu.** `playVar`/`abPlay` uruchamiały dźwięk po zakończeniu renderu, nie sprawdzając,
   czy użytkownik w międzyczasie kliknął *Stop* albo inny dźwięk. Skutek: grały dwa dźwięki naraz, a *Stop*
   nie zatrzymywał dźwięku, który jeszcze się renderował. Poprawka: żeton `playTok` unieważniany w `stopAudio()`.
2. **Wyciek pamięci w pamięci podręcznej.** `ensure()` doklejała surowe kanały audio (`Float32Array`) do obiektu
   wyniku w `results`, także do już zapisanego wpisu z bajtami OGG. Każdy odsłuch trwale trzymał w pamięci
   pełny PCM (w trybie WAV dotyczyło to każdego pliku). Poprawka: kanały trafiają tylko do zwracanej kopii.
3. **Manifest** zapisywał `duration` ze specyfikacji, nawet gdy wersja ma inną długość. Teraz bierze długość
   wersji v4.

### Architektura i utrzymanie (opisane, nie zmieniane)

4. **„Poprzednie (v2)” nie jest historyczną v2.** `sfxV2()` wywołano dwa razy dla tych samych id
   (np. `mg_shot`, `cannon_*_fire`, `hit_*`, `cookoff`, silniki): druga rejestracja nadpisuje `fn2`.
   W efekcie opcja v2 renderuje funkcje z sekcji „v3” z wyłączonymi gałęziami `RV === 'v3'`, a `gunV2()`
   i pierwsze definicje trafień to martwy kod. Etykiety v2/v3 i przycisk A/B sugerują coś innego, niż słychać.
5. **Wersjonowanie przez globalną zmienną `RV`**, sprawdzaną głęboko we współdzielonych helperach
   (`plateModes`, `plateHit`, `blast2`, `petrolV8P`, `eng_ww1`…). To kruche: zmiana helpera „dla v3” po cichu
   zmienia inne dźwięki. v4 omija to celowo: ma osobne funkcje i własny rejestr (`fn4`, `dur4`), a dźwięki
   bez v4 renderują się dokładnie jak v3.
6. **Nakładające się warstwy.** v1, v2 i v3 żyją obok siebie (≈1300 linii, z czego część martwa). Jeśli
   starsze wersje nie są już potrzebne do porównań, warto je usunąć.
7. `markV3()` działa tylko w wątku głównym. Workery go nie potrzebują, ale to pułapka przy rozbudowie.
8. `window.__cancel` jest globalną flagą. Anulowanie eksportu (`cancelAll`) przerywa też trwający odsłuch.

### Brzmienie (powód przeróbek)

Zmierzone na v3 (`node tools/render.js check v3` + spektrogramy) i porównane z prawdziwymi nagraniami
(archive.org: płyty efektów WWII: rozruch i jałowy czołgu, ostrzał artyleryjski, salwy 16"; diesel V12 na jałowym):

| Grupa | Problem w v3 | Skąd „sztuczność” |
|---|---|---|
| Wybuchy (`hit_he`, `cookoff`, `hull_torn`) | spadek do −60 dB w ~0,6 s, maksimum widma ~60 Hz | w nagraniach ogon trwa 3+ s (odbicia od terenu), maksimum 150–500 Hz. W v3 bas to sinus z opadającą wysokością (`thump`), czyli „stopa perkusji” |
| Trafienia w pancerz | suche (~0,15 s), kilka strojonych trybów (wyraźne piki), głośność −26…−28 LUFS przy celu −14 | brzmi jak dzwonek/kowadło, nie jak masywna płyta. Sam transjent bez „ciała” sprawia, że limiter nie dociąga głośności i trafienia są o ~12 dB cichsze od wybuchów |
| Silniki | rezonans rury pokrywał się z częstotliwością zapłonu (diesel: 52 Hz), zbyt regularne zapłony, za mało klekotu 1–4 kHz | jeden „buczący” ton i równe, syntetyczne pulsowanie zamiast nierównego, „żywego” silnika |
| Wszystko plenerowe | zero otoczenia | nagrania zawsze mają odbicie od ziemi i echo otoczenia |

Uwaga do masteringu: krótkie transjenty normalizowane do −14 LUFS i tak kończą na *limiter-max* (szczyt
−1,5 dBFS), więc realna głośność efektów jest przypadkowa. W v4 trafienia mają więcej energii po transjencie
i lądują w okolicach −14…−20 LUFS. Docelowo warto rozważyć osobne cele LUFS na kategorię (np. kb −18,
działa −14, wybuchy −12) zamiast jednego dla wszystkich.

## Co zmienia v4 (domyślna w UI)

Nowe klocki DSP:
- `modeBank`: szybki bank rezonatorów dwubiegunowych (także w trybie pętli),
- `plateSet`: mody płyty o **stałej gęstości w Hz** (jak w fizyce płyt), z amplitudami z rozkładu Rayleigha
  i zanikiem malejącym z częstotliwością, zamiast kilku strojonych trybów,
- `outdoorIr` / `outdoor`: dźwięk bezpośredni, odbicie od ziemi, echa (las, zabudowa) i rozproszony ogon,
  w którym wysokie tony gasną szybciej,
- `explosion4`: impuls Friedlandera, ognisko z filtrem opadającym w czasie (jasne → ciemne), turbulencja,
  niskie „łup” z szumu (bez sinusa), toczący się pomruk, przester transjentu, N-fala, opóźniony deszcz grud
  i piachu (`dirtFall`), plener,
- `impact4`: kontakt (czas kontaktu → jasność), gęste mody płyty, rezonanse kadłuba, tępy udar masy,
  huk powietrza, iskry,
- `engineCore4`: per-cylindrowe stałe różnice (amplituda, czas, barwa), zmienność cykl-do-cyklu, słabe zapłony
  na jałowym, rury ćwierćfalowe dla każdego rzędu (V8/V12 dudnią), tłumik, stuk spalania pobudzający bank
  modów bloku (diesel klekocze), zawory, wlot, luzy/łańcuchy (WW1), wentylator i przekładnia, plener.

Przerobione dźwięki: `eng_petrol/diesel/small/radial/ww1/turbine` (×3 poziomy), `eng_start`, `eng_stall`,
`hit_he`, `cookoff`, `hull_torn`, `hit_ground`, `hit_nonpen`, `hit_pen`, `hit_ricochet`, `hit_mg`, `hit_heat`,
`hit_spall`, `hit_module`. Wybuchy i część trafień dostały dłuższy czas trwania w v4 (`dur4`), żeby ogon się
zmieścił. Starsze wersje mają nadal swoje długości.

## Narzędzia

`tools/render.js` to ten sam silnik uruchamiany w Node:

```
node tools/render.js list
node tools/render.js wav out/ v4 hit_he eng_diesel_idle
node tools/render.js check v4      # render wszystkiego: błędy, NaN, LUFS, szczyt, szew pętli
```

## Ograniczenia

Dźwięki strojono na podstawie analizy widm i porównania z nagraniami referencyjnymi, nie odsłuchu.
Ostateczną ocenę trzeba zrobić uchem (przycisk A/B: v3 → v4). Parametry są zebrane w `ENG4` oraz w wywołaniach
`impact4`/`explosion4`, więc łatwo je podkręcić.
