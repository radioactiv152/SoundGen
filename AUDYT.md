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

## Runda 4: „beczka” w strzałach, spawanie w wieży, przegląd wszystkiego poza silnikami

**„Beczka” w strzałach**, przyczyny zmierzone:
1. Rozproszony ogon pleneru zaczynał się po ~20 ms. Gęste odbicia w pierwszych 5–80 ms ucho odbiera jako
   zamkniętą przestrzeń. Na otwartym terenie po dźwięku bezpośrednim jest tylko słabe, ciemne odbicie od ziemi,
   a ogon lasu/terenu zaczyna się po ~80 ms i narasta powoli (`outdoorIr`, tryb otwarty; silniki zostały
   przy starym, bliskim trybie `open: false`).
2. Ogon był o ~18 dB głośniejszy niż wybrzmienie samego strzału (hala). Strzały to warstwa „sucha”,
   długi ogon daje `shot_tail`, więc poziomy pogłosu zmniejszone ~2×. Trafienia też.
3. Mechanika odrzutu dzwoniła modami blachy i kadłuba z zanikiem 0,2–0,3 s. W wybrzmieniu działa
   były wąskie piki rezonansowe +17–18 dB (w nagraniach 11–16 dB). Teraz to tłumiony stuk masy.

**Obrót wieży „jak spawanie”**: szum szerokopasmowy z szybką losową modulacją (40 Hz, 20 Hz) i syk 3–9 kHz.
Teraz to gładki ton silnika napędu z harmonicznymi, wycie przekładni z biciem wałka, pomruk łożyska wieńca
i ciche tarcie. Powyżej 4 kHz zostało −60 dB (wcześniej −17 dB), bez trzasków.

**Przegląd grup (bez silników):**

| Grupa | Co było nie tak | Co zrobione |
|---|---|---|
| Obsługa broni | `gun_breech`: czyste tony urywane w ciszę; `shell_casing`: cienkie „pingi” | zamek klinowy (masywna stal, ślizg, wyrzut łuski, zatrzask) we wnętrzu wieży; łuska jako mosiężna rura (tryby pierścieniowe w rozstrojonych parach = dudnienie), odbicia, toczenie |
| Podwozie i teren | `hull_creak` 41–44 trzasków/s (twarde bramkowanie); `belly_scrape`, `track_spin` „spawające” (szum z modulacją 110/25 Hz); `surf_sand` syczący; `water_enter` ucięty | skrzypienie stick-slip na łagodnych impulsach (0 trzasków/s); szorowanie: niskie tarcie, żwir, uderzenia w kamień; piach: gęsty, drobny chrzęst z ogniwami; buksowanie: miękka ziemia; wjazd do wody z falami o burty (2 s) |
| Kreator | `ed_armor`: ton 137 Hz wystający o 47 dB; `ed_remove`/`ed_swap` ucinane z piszczącym tonem; „bum”-sinusy | spójny warsztat: masywna stal (tłumione, gęste mody), śruby, grzechotka klucza, łańcuch dźwigu, młot pneumatyczny na wspólnych modach blachy, spawanie z łagodnym zapaleniem/zgaśnięciem, pogłos hali |
| Interfejs | `ui_click`/`ui_slider` = czysty sinus; `ui_drawer` = szum modulowany 20–30 Hz; „knock” = sinus-bębenek; twarde cięcia | bakelitowy przełącznik, zapadka, drewniane stuknięcia (tłumione mody deski), szuflada z tarciem drewna i rezonansem pudła; wyciszanie zamiast cięć |
| Firma, poligon | `research_start` ucięty syk; `deadline` tonalne kliki; `trial_start` czysty sinus | wkładanie kartki do maszyny (zapadka wałka + papier), zegar z wychwytem (tik-tak) w drewnianej obudowie, gwizdek z kulką i oddechem |
| Wojna | `amb_battle`: 6 sinusowych „bumów”, zdarzenia przy końcu pętli ucinane (dziura w pętli); `war_start`: czysty sweep | front z daleka: artyleria (wybuchy v4 z pochłanianiem powietrza i długim ogonem stereo, ostre ataki jak w nagraniu), wystrzały, serie km (różne tempa), pojedyncze strzały, wszystko zawijane w pętli; syrena z wirnikiem + odległe wybuchy |

Zostawione bez zmian: stylizowane sygnały muzyczne i dzwonki (`tender_*`, `medal`, `ace`, `money_in`, `month_next`…
oznaczone w specyfikacji jako szkice do podmiany na nagrania), `fire_loop`, `report_open`, `stamp`, gąsienice
(trzaski ogniw to prawdziwe transjenty metalu).

## Runda 5: szelest w strzałach i trafieniach, gąsienice, zawieszenie, ambienty

**„Zgniatana reklamówka” w strzałach i trafieniach**, trzy źródła:
1. Echa od lasu/zabudowy były 50-ms „chmurkami” szumu: ostry trzask przepuszczony przez szum to szelest.
   Teraz echo to kilka wyraźnych, przyciemnionych kopii dźwięku (odbicia od kilku powierzchni).
2. Ogon pleneru narastał przez 150 ms po ciszy i był jasny (1,4–6 kHz). Po krótkim trafieniu dawało to osobne „szszsz”.
   Teraz startuje po 50 ms, narasta 40 ms, potem tylko gaśnie, jest ciemniejszy, a w trafieniach i karabinach ~2× cichszy.
3. Szybka losowa modulacja (120 Hz w podmuchu, 60 Hz w wybuchu, 90/300 Hz w zgrzytach) przez cały zanik
   (`earlyRough` ogranicza ją do ataku), iskry jako rzadkie losowe ziarna (teraz gładki, krótki syk), roje
   odprysków 140–200/s z szumowych brzęków (teraz ~45/s, metaliczne).

Miara „szelestu” (szybkie wahania obwiedni 1–6 kHz): gładki szum 1,3 dB, nagrania 1,9–2,8 dB, działa v4 1,7–2,2 dB.

**Gąsienice „jak kapiąca woda”**: każde ogniwo było kilkoma czystymi tonami o losowej wysokości, czyli kroplami.
`trackSet4`: kilka typów ogniw o stałej barwie (powtarzalny wzór), ciężkie tłumione uderzenia stali (koło
napędowe i napinające), grzechot sworzni, pomruk w rytmie ogniw, toczenie kół jezdnych, lekki pisk, zabarwienie
kadłubem. Dotyczy `track_steel`, `track_ww1`, `track_rubber`, `halftrack_roll`, `track_spin`. Wystające piki
9–11 dB (poziom szumu), bez tonalności.

**Zawieszenie i reszta podwozia**: `susp_bump`/`step_hit` to masa pojazdu (szum, nie sinus), odbojnik,
sprężyna, grzechot wyposażenia (+ grudy ziemi w `step_hit`). `brake`: zwalniające ogniwa, pisk taśmy
z drżeniem, pojazd kiwa się na zawieszeniu. `belly_scrape`: metaliczny zgrzyt stick-slip. `hull_creak`: ciche tarcie.

**Ambienty**: `amb_range` (wiatr z płynnymi porywami, ptaki: tryle, dwutony, świergot, odległe strzały prób,
daleki czołg), `amb_town` (szum ulicy, kuźnia, ciężarówka, parowy gwizd fabryczny; usunięty sztuczny brum
100 Hz), `amb_office` (szum pokoju, prasa za ścianą, zegar z wychwytem, maszyna do pisania z dzwonkiem
i powrotem karetki, kartki), `amb_battle` (+ przeloty pocisków, daleki czołg, wiatr). `war_start`: dwie
rozstrojone syreny z sekaniem wirnika i echem zabudowy, odległe wybuchy.

Silniki: bez zmian (tryb bliski pleneru zachowany; render bajt w bajt identyczny z poprzednią wersją).

## Runda 6: wystrzały, hamowanie, trafienia wg nagrania terenowego

Nowe referencje (archive.org): nagranie terenowe strzałów z karabinu nad rzeką (pełne pasmo, naturalne otoczenie),
pojedynczy strzał karabinowy z bliska, płyta z efektami wystrzałów.

**Wnioski z nagrania terenowego:**
- ogon strzału w plenerze to gęstniejący ciąg wyraźnych odbić (drzewa, brzegi): pierwsze rzadkie, kolejne
  coraz gęstsze i ciemniejsze, nie gładki szum;
- ogon jest głośny i długi: energia w 50–500 ms ≈ +2 dB względem samego strzału (0–30 ms), w 0,5–1,5 s ≈ −9 dB;
- widmo karabinu ma maksimum ~500 Hz, płaskie 30 Hz – 3 kHz, góra powyżej 5 kHz gaśnie w ~0,3 s.

v4 przed zmianą: kb −13 dB w 50–500 ms i nic później (za suche, „zabawkowe”), działo −1/−17 dB; kb z basem
~10 dB za mocnym.

**Zmiany:**
- `echoCloud`: ogon jako chmura dyskretnych odbić (gęstość 20 → 220/s, coraz ciemniejsze, na końcu ciemne
  „zlanie się”). Używana w strzałach, trafieniach i wybuchach. Silniki bez zmian (sprawdzone bajt w bajt).
- Kalibracja ogona strzałów do nagrania (50–500 ms / 0,5–1,5 s, dB względem strzału):

| | 50–500 ms | 0,5–1,5 s |
|---|---|---|
| nagranie terenowe | +1,7 | −9,6 |
| `mg_shot` | +1,8 | −12,8 |
| `hmg_shot` | +1,8 | −11,9 |
| `cannon_m_fire` | −0,4 | −9,6 |
| `cannon_l_fire` | −1,3 | −8,7 |

- Karabiny: środek podmuchu niżej (850–1200 / 650–900 Hz), mniej basu, dłuższe pliki (1,0 / 1,2 s).
  Działa 1,8–2,8 s.
- Trafienia: chmura odbić, grube trafienia mniej dudnią, a więcej brzęczą. Rezonanse kadłuba to teraz gęsty,
  losowy zestaw modów (tępe „bum” bez wysokości). Najniższe mody płyty są tłumione mocowaniem, a dzwonienie
  pancerza skrócone. Wystające piki spadły z 20–23 dB do 13–17 dB.
- `brake`: gąsienica zwalnia płynnie (tempo ogniw ~ prędkość), toczenie zamiera, ślizg po podłożu, pisk bębna
  z nieregularnym narastaniem i przeskokiem na drugi ton, jęk tarcia tuż przed zatrzymaniem, przód nurkuje
  na zawieszeniu i odbija do tyłu (1,6 s).

## Runda 7: trafienia „jak w garnku / gotowane ziemniaki”, strzały „w pustym hangarze”

Przyczyny:
- Kalibracja ogona do nagrania terenowego była błędem kierunku. Tamten strzał nagrano z daleka, więc pogłosu
  jest w nim naturalnie dużo więcej niż przy strzale z bliska. Stąd „hangar”.
- Gęsty ciąg ciemnych, dyskretnych odbić (20–220/s) brzmiał jak bulgotanie: każde odbicie to „plop” bąbla.
- Trafienia oparte były na dzwoniących modach blachy i rezonansach pustego kadłuba, czyli garnek/beczka.
  Trafienie pocisku w pancerz to przede wszystkim huk (fala ciśnienia), a metal jest krótki.

Zmiany:
- `echoCloud`: tylko kilka wyraźnych odbić w pierwszych ~0,35 s, dalej gładki, ciemny pomruk (bez pojedynczych zdarzeń).
- Strzały: ogon ~8–10 dB cichszy (50–500 ms ≈ −3…−6 dB, 0,5–1,5 s ≈ −17…−27 dB względem strzału).
- `armorStrike`: rdzeń trafienia = podmuch jak wystrzał (`gunshot4`, suchy) + krótki trzask stali (płyta 0,05–0,1 s,
  bez modów kadłuba) + gładki syk iskier. Używany w `hit_nonpen`, `hit_pen`, `hit_ricochet`, `hit_module`.
- `hit_he`, `hit_heat`: warstwa stali krótka (0,08–0,09 s), bez „garnka”. `hit_spall`, `hit_rivets`, `hit_module`:
  usunięte rezonanse pustego kadłuba (`hullBox`). Plener trafień: odbicia ~3× słabsze.
- Wystające piki w trafieniach: 10–16 dB (poziom szumu), szorstkość 1,8–3,2 dB. Silniki bez zmian.

## Runda 8: nowe silniki V8 i V12 (benzyna, diesel)

Cztery nowe pętle (idle / mid / high, po 4 s) na tym samym modelu co pozostałe silniki v4 (`engineCore4`):

| id | charakter | obroty (idle/mid/high) |
|---|---|---|
| `eng_v8_petrol` | V8 cross-plane (np. Ford GAA): nierówne grupy zapłonów w rzędach = bulgotanie, głęboki wydech | 560 / 1500 / 2700 |
| `eng_v8_diesel` | V8 cross-plane + stuk spalania diesla, bardziej nierówny niż V12 | 480 / 1200 / 2000 |
| `eng_v12_petrol` | V12 (np. Maybach HL230): równe zapłony naprzemiennie w rzędach, gładki, mocne wentylatory | 600 / 1700 / 3000 |
| `eng_v12_diesel` | V12 diesel (np. W-2): aluminiowy blok, więcej klekotu, głośny wlot i wentylator | 600 / 1400 / 2000 |

Każdy ma własne, stałe cechy cylindrów, inne długości rur w rzędach i inne rezonanse bloku. Bilans pasm na
jałowym jest zbliżony do nagrań referencyjnych (czołg z II wojny, diesel V12). Bez trzasków, szwy pętli czyste.
Na liście są zaraz za pozostałymi pętlami silników, z oznaczeniem „nowy” (bez A/B, bo nie mają starszej wersji).
Dotychczasowe silniki bez zmian.
