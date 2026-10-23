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
4. **A/B nie działał na pętlach.** `abPlay` wywoływał `src.stop()` przed `src.start()`, przez co przy każdym
   dźwięku zapętlonym (silniki, gąsienice, otoczenie) wyskakiwał błąd zamiast porównania. Poprawione.
5. **Trzaski w silnikach v4** („strzelanie oscylatora”). Zmierzone detektorem kliknięć: skoki w paśmie
   >4 kHz ponad 5× RMS otoczenia, 40–120 na sekundę, w rytmie zapłonów. Źródła:
   - ucięty kernel impulsu wydechu (skok sygnału po 20 ms),
   - natychmiastowe narastanie impulsu (0,25 ms),
   - surowe ziarno stuku spalania dodawane bez filtru, i to samo ziarno wzbudzające mody bloku bez ataku,
   - zbyt ostre ziarna zaworów, grzechotu i łańcuchów (WW1).

   Poprawka: kernel 40+ ms z łagodnym wygaszeniem, narastanie ~1 ms, zdarzenia mechaniczne z atakiem 2–4 ms
   i obcięte powyżej ~3,5 kHz. Wynik: 0–3 kliknięć/s (pozostałe to celowe pojedyncze stuki,
   np. metaliczny stuk w `eng_stall`).

### Architektura i utrzymanie (opisane, nie zmieniane)

6. **„Poprzednie (v2)” nie jest historyczną v2.** `sfxV2()` wywołano dwa razy dla tych samych id
   (np. `mg_shot`, `cannon_*_fire`, `hit_*`, `cookoff`, silniki): druga rejestracja nadpisuje `fn2`.
   W efekcie opcja v2 renderuje funkcje z sekcji „v3” z wyłączonymi gałęziami `RV === 'v3'`, a `gunV2()`
   i pierwsze definicje trafień to martwy kod. Etykiety v2/v3 i przycisk A/B sugerują coś innego, niż słychać.
7. **Wersjonowanie przez globalną zmienną `RV`**, sprawdzaną głęboko we współdzielonych helperach
   (`plateModes`, `plateHit`, `blast2`, `petrolV8P`, `eng_ww1`…). To kruche: zmiana helpera „dla v3” po cichu
   zmienia inne dźwięki. v4 omija to celowo: ma osobne funkcje i własny rejestr (`fn4`, `dur4`), a dźwięki
   bez v4 renderują się dokładnie jak v3.
8. **Nakładające się warstwy.** v1, v2 i v3 żyją obok siebie (≈1300 linii, z czego część martwa). Jeśli
   starsze wersje nie są już potrzebne do porównań, warto je usunąć.
9. `markV3()` działa tylko w wątku głównym. Workery go nie potrzebują, ale to pułapka przy rozbudowie.
10. `window.__cancel` jest globalną flagą. Anulowanie eksportu (`cancelAll`) przerywa też trwający odsłuch.

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

## Runda 3: strzały, obrót wieży, trafienia

Diagnoza (pomiar energii w pasmach, porównanie z salwami i ostrzałem z płyt WWII):
- **Strzały v3** (`mg_shot` … `howitzer_fire`): widmo zdominowane przez < 100 Hz. Karabin maszynowy brzmiał jak
  stopa perkusji, a działa miały środek −30 dB i urywały się w ciszę po 0,4–0,5 s.
- **Ogon pleneru v4** (wspólny dla wszystkich dźwięków v4) był na hertz ~10 dB ciemniejszy w basie
  (szum różowy plus najdłuższy zanik basu) i dokładał +12 dB w 20–100 Hz każdemu dźwiękowi z otoczeniem.
  Poprawione: równa gęstość widma, góra nadal gaśnie szybciej. To rozjaśniło też wybuchy i trafienia.
- **Obrót wieży v3**: praktycznie szum z maksimum 500 Hz, bez silnika, przekładni i wieńca.

Nowe w v4:
- `gunshot4` (wszystkie strzały): podmuch wylotowy (przesterowany szum 150 Hz – 8 kHz, ciemniejący,
  chropawy), trzask N-fali pocisku, impuls ciśnienia i „bum” tylko jako dodatek, mechanika
  (zamek kb: `boltClack`; odrzut działa, powrót lufy i kołysanie pojazdu: `recoilMech`), plener.
  `recoilless_fire` ma ryk gazów do tyłu, `atgm_launch` oddalający się silnik rakiety.
- `shot_tail` (stereo): rozproszony, toczący się pogłos z 6 wyraźnymi, rozmytymi echami rozłożonymi w panoramie.
- `turret_traverse`: silnik z harmonicznymi i wyciem, chropawe zazębienie wieńca w rytmie zębów, pomruk łożyska,
  skrzypienie, zabarwienie kadłubem. Pętla bez szwu.
- Trafienia: nowe `hit_mg` (jasny „spak” blachy, rozprysk, warianty z rykoszetem i podwójnym trafieniem),
  `hit_rivets`, `hit_crew`, `shell_flyby` (szum z Dopplerem i trzaskiem fali uderzeniowej zamiast gwizdka).

Bilans pasm (dB względem 300–1000 Hz, 40–100 / 100–300 / 1–3k / 3–5k):

| | 40–100 | 100–300 | 1–3k | 3–5k |
|---|---|---|---|---|
| salwa z nagrania | −5…−2 | 0…+1,5 | −3…+3,5 | −10…−3 |
| `cannon_m_fire` v4 | +0,4 | +2,5 | −0,6 | −2,6 |
| `cannon_l_fire` v4 | +0,2 | −1,5 | +0,3 | −2,6 |
