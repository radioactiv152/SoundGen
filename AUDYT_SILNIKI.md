# Audyt: jak naprawdę brzmią silniki czołgów i jak je generować

Zakres: wyłącznie pętle pracy silnika (bieg jałowy, średnie i wysokie obroty). Odpalanie, gaszenie i wszystkie
pozostałe dźwięki gry zostały z generatora usunięte. Generator (`index.html`, model v5) jest napisany od nowa
na podstawie tego audytu; stary kod (v1–v4) jest w historii repozytorium.

## 1. Co decyduje o brzmieniu silnika tłokowego

### 1.1 Rytm: częstotliwość zapłonów

Jedyna liczba, którą ucho „liczy” od razu, to tempo zapłonów. Dla czterosuwu każdy cylinder strzela co dwa
obroty, więc:

    f_zapłonów [Hz] = obroty/60 × liczba cylindrów / 2        (dwusuw: bez dzielenia przez 2)

| silnik (pojazd) | układ | obroty: jałowe / średnie / maks. | f zapłonów [Hz] |
|---|---|---|---|
| Maybach HL 230 P30 (Panther, Tiger II) | V12 60°, 23,1 l, benzyna | 650 / 1700 / 2800 (3000) | 65 / 170 / 280 |
| W-2-34 (T-34, KW) | V12 60°, 38,8 l, diesel DI | 550 / 1200 / 1750 (1800) | 55 / 120 / 175 |
| Ford GAA (M4A3) | V8 60°, płaski wał, 18 l, benzyna | 600 / 1600 / 2600 | 40 / 107 / 173 |
| SPA 8T M40 (M13/40) | V8, 11,1 l, diesel | 550 / 1150 / 1800 | 37 / 77 / 120 |
| Maybach HL 120 TRM (Pz III/IV) | V12 60°, 11,9 l, benzyna | 650 / 1800 / 2800 (3000) | 65 / 180 / 280 |
| GM 6046 (M4A2) | 2 × R6 dwusuw 6-71, 13,9 l, diesel | 500 / 1300 / 2100 | 100 / 260 / 420 |
| Maybach HL 62 TRM (Pz II) | R6, 6,2 l, benzyna | 700 / 1800 / 2600 | 35 / 90 / 130 |
| Continental R-975 C1 (M4, M4A1) | gwiazda 9 cyl., 15,9 l, benzyna | 550 / 1500 / 2400 | 41 / 112 / 180 |
| Ricardo 150 KM (Mark V) | R6, 19 l, benzyna | 330 / 750 / 1200 | 16 / 37 / 60 |

Obroty maksymalne pochodzą z danych fabrycznych (źródła niżej). **Obrotów jałowych żadne z dostępnych źródeł
nie podaje** – przyjęte wartości (500–700 obr/min dla silników WWII, 330 dla WW1) to typowe liczby dla
wolnoobrotowych jednostek o dużej pojemności; w generatorze są jawnym parametrem i łatwo je zmienić.

### 1.2 Odstępy zapłonów (charakter)

Ucho rozróżnia nie tylko tempo, ale i równość odstępów:

* **V12 60°** (Maybach, W-2, Meteor): równe 60° wału, w każdym rzędzie równe 120°. Gładki, „jedwabisty” warkot.
* **Ford GAA**: widlak 60° z **płaskim** wałem – kolejność R1-L2-R3-L1-R4-L3-R2-L4; każdy rząd pracuje jak
  osobna czwórka (równe 180°), ale rzędy są przesunięte o 60°, więc w sumie odstępy wynoszą
  60°-120°-60°-120°… Wydech brzmi „parami”: na jałowym bulgotanie, przy obrotach warkot z podtonem połowy
  częstotliwości zapłonów.
* **V8 90° z wałem krzyżowym**: ogólnie równe 90°, ale w jednym kolektorze 90-180-270-180° – znany „galop”
  amerykańskich V8.
* **Gwiazda 9 cyl.**: zapłon co 80° w kolejności 1-3-5-7-9-2-4-6-8; wszystkie cylindry w jeden pierścień
  zbiorczy; krótkie rury, duża zmienność między cylindrami: suchy, trzaskliwy chrzęst.
* **GM 6046 (dwusuw)**: 12 cylindrów, zapłon w każdym co obrót → 12 wydmuchów na obrót (420 Hz przy 2100).
  Stąd „Screaming Jimmy”: bzyczący, gęsty ryk plus wycie dmuchawy Roots.
* **Ricardo**: 6 ogromnych cylindrów przy 330 obr/min: 16 „puff” na sekundę, każdy słyszalny osobno.

### 1.3 Źródła dźwięku (od najgłośniejszego na zewnątrz)

1. **Wydech.** Po otwarciu zaworu wydechowego gaz pod ciśnieniem 3–5 bar wyrywa się z cylindra („wydmuch”,
   ok. 40–60° wału), potem tłok wypycha resztę (ok. 180°). Czas trwania impulsu jest stały **w stopniach wału**,
   więc w sekundach skaluje się z 1/obroty. Siła wydmuchu rośnie z obciążeniem (ciśnienie w cylindrze), siła
   wypychania z obrotami. Dalej impulsy idą przez kolektor (objętość = dolnoprzepustowy + rezonans
   Helmholtza 100–200 Hz), rurę (rezonator ćwierćfalowy: nieparzyste harmoniczne c/4L; przy 1,3 m i gorącym
   gazie ~100 Hz), tłumik (komora rozprężna: tłumienie góry powyżej ~1–1,5 kHz) i wylot (promieniowanie:
   małe częstotliwości słabną ~6 dB/okt). W widmie: **grzebień harmonicznych częstotliwości zapłonów**,
   najsilniejszy między 60 a 600 Hz, opadający 6–10 dB/okt powyżej ~800 Hz.
2. **Stuk spalania (klekot).** Gwałtowny skok ciśnienia po zapłonie (diesel z wtryskiem bezpośrednim:
   bardzo stromy, zwłaszcza na jałowym, gdy zwłoka zapłonu jest długa) pobudza blok i głowice; promieniują
   mody 800–4000 Hz z zanikiem 10–30 ms. W dieslu na jałowym to składnik dominujący, w benzyniaku ledwo
   słyszalny; pod obciążeniem w dieslu maleje względem wydechu.
3. **Mechanika.** Siadanie zaworów (2 stuki na cylinder na cykl, 2–6 kHz), pompa wtryskowa (ostry tik tuż przed
   zapłonem), koła zębate rozrządu i napędu wentylatorów (ton = obroty/60 × liczba zębów, wyraźny w Maybachach),
   luzy i łańcuchy w starych konstrukcjach (WW1).
4. **Wentylator i wlot.** Szum łopatek rośnie z obrotami jak ~obroty^2,5 (przy pełnych obrotach porównywalny
   z wydechem u silników chłodzonych powietrzem – R-975 ma wentylator na kole zamachowym); wlot gaźnika/filtra
   pulsuje w rytm zapłonów, słyszalny pod obciążeniem.
5. **Kadłub.** Silnik stoi w stalowej skrzyni z żaluzjami: góra tłumiona (powyżej ~1 kHz opada), bas
   dociążony (50–150 Hz), krótkie odbicia od ziemi i płyt. Dlatego czołg z zewnątrz brzmi ciemniej niż
   ten sam silnik na hamowni.

### 1.4 Obroty, obciążenie, nierówność

* **Jałowy**: słaby wydmuch (małe ciśnienie), długie impulsy, nierówne cykle (zmienność siły zapłonu 15–30 %,
  pojedyncze słabe zapłony w gaźnikowych), pływanie obrotów 2–5 % w rytmie 1–3 Hz (regulator). W dieslu
  klekot głośniejszy od wydechu.
* **Obciążenie** (jazda) zmienia barwę bardziej niż obroty: wydmuch 3–4× silniejszy, wydech ostrzejszy
  (nieliniowość gorącego gazu), wlot głośniejszy; klekot diesla względnie cichszy.
* **Głośność**: od jałowego do pełnej mocy różnica ok. 8–12 dB. Pętle wyrównane do jednej głośności brzmią
  nienaturalnie, jeśli gra nie dodaje własnych wzmocnień.

## 2. Pomiary nagrań referencyjnych

Nagrania z archive.org (w tej sesji: `tank.wav` – przejazd czołgu benzynowego, `diesel.wav` – duży diesel
na stałych obrotach), 1/3-oktawy względem pasma 500 Hz:

| nagranie, fragment | 63 | 125 | 250 | 500 | 1 k | 2 k | 4 k | 8 k | tempo modulacji |
|---|---|---|---|---|---|---|---|---|---|
| tank.wav 8–20 s (jałowy, blisko) | −3 | +6 | +6 | 0 | −6 | −1 | −14 | −15 | 9 Hz (cykl), 18 Hz (zapłony) |
| tank.wav 36–48 s (jazda, dalej) | −21 | −20 | −5 | 0 | −15 | −16 | −29 | −37 | 38 Hz, harmoniczne 75, 113 |
| diesel.wav 10–40 s (stałe obroty) | +8 | −2 | 0 | 0 | −10 | −12 | −16 | −29 | wolny rytm 3,3 / 6,6 Hz |

Wnioski: energia skupiona 60–600 Hz; powyżej 1 kHz spadek 10–30 dB; na spektrogramie wyraźne linie
harmonicznych zapłonów do ~1 kHz, nad nimi rzadkie pionowe „kreski” stuków mechanicznych (jałowy z bliska:
tiki sięgają 3,5 kHz, głośnością porównywalne z całością). Współczynnik szczytu 12–13 dB.

## 3. Błędy starego generatora (v4)

1. **Impulsy wydechu o stałej długości w sekundach** (osobne liczby dla idle/mid/high) zamiast długości w
   stopniach wału – barwa nie wynikała z fizyki, każdy poziom był strojony ręcznie.
2. **Brak obciążenia jako parametru** – wysokie obroty bez obciążenia i pod obciążeniem brzmiały tak samo.
3. **Za jasne, szumowe widmo**: turbulencja, iskrzące ziarna, wentylator i wlot zalewały grzebień harmonicznych;
   tiki rozrządu były krótkie (0,2 ms narastania) i słyszalne jako „strzelanie”.
4. **Silniki nie odpowiadały rzeczywistym jednostkom**: „petrol” był V8 z wałem krzyżowym (żaden czołg WWII go nie
   miał), „diesel” generycznym V12, nowe V8/V12 wariantami tych samych parametrów. Brak dwusuwu GM 6046,
   brak płaskiego wału Forda GAA, brak różnic kolektorów.
5. **Wszystkie pętle wyrównane do −18 LUFS** – jałowy tak samo głośny jak pełna moc.
6. Kadłub jako bank dzwoniących modów („garnek”) i plenerowy pogłos z chmurą odbić – w pętli silnika zbędne.

## 4. Nowy generator (v5)

### 4.1 Tor sygnału (jeden przebieg, okresowy w pętli)

```
obroty(t) = obroty × (1 + pływanie regulatora + drgania)      → kąt wału θ(t) = ∫ obroty
tabela zapłonów (kąt, rząd) ──► zdarzenia zapłonów (czas, cylinder, siła)
   siła = cecha cylindra × zmienność cyklu × wolna zmiana obciążenia × (słabe zapłony na jałowym)
   │
   ├─► impuls przepływu wydechu (wydmuch 7°↑ 42°↓ + wypychanie 200°; w sekundach ∝ 1/obroty) + turbulencja wylotu
   │     → kolektor rzędu (LP 2,6 kHz + Helmholtz) → rura ćwierćfalowa (c=520 m/s, L z tabeli) → tłumik (LP, komora)
   │     → promieniowanie (pochodna poniżej 120 Hz) → nieliniowość gorącego gazu
   ├─► stuk spalania: ziarno 0,9 ms → 44 mody bloku 500–4000 Hz (T60 25 ms) → LP 3,2 kHz; diesel ≫ benzyna
   ├─► tłok (diesel, jałowy), zawory (2/cyl/cykl), pompa wtryskowa, łańcuchy (WW1)
   ├─► koła zębate (ton obroty/60 × Z, FM 2,3 Hz), wentylator (szum ∝ obroty^2,5 + ton łopatek), dmuchawa Roots
   └─► wlot (szum 150–1800 Hz pulsujący z zapłonami)
   Σ → żaluzje (LP 5 kHz, −6 dB/okt powyżej 700 Hz) → bas kadłuba (+LP 110 Hz) → odbicia (3,2 i 7,1 ms, krótki ogon 0,11 s)
   → mastering: LUFS (naturalna: −24,8 jałowy … −16,5 pełna moc; lub wyrównana −18), szczyt −1,5 dBFS
```

Pętla ma całkowitą liczbę cykli silnika (obroty dopasowane o ułamek procenta), pływanie obrotów i tony są
okresowe w długości pętli, wszystkie filtry liczone cyklicznie – pętla domyka się co do próbki (szew ≤ 0,7
w mierze generatora, próg ostrzeżenia 3).

### 4.2 Parametry silnika (tabela `ENGINES` w `index.html`)

`fire` (tabela zapłonów), `cyl`, `disp` (l), `rpm` i `load` dla idle/mid/high, `pipeL` (długość rur rzędów, m),
`muf` (0 = otwarte rury … 1 = ciężki tłumik), `manF` (Helmholtz kolektora), `cool`/`fan`/`fanZ`
(wentylator), `gear`/`gearZ` (koła zębate), `knock` (stuk spalania), `valve`, `intake`, `inj` (pompa
wtryskowa), `slap` (tłok), `blower`/`blowerZ` (Roots), `chain`, `cylVar` (różnice cylindrów), `wob`
(pływanie obrotów), `ccv` (zmienność cyklu), `miss` (słabe zapłony).

Suwaki „własne obroty i obciążenie” przy każdym silniku renderują dowolny punkt pracy (np. 1400 obr/min bez
obciążenia = zwalnianie, 1400 pod obciążeniem = podjazd).

### 4.3 Wynik pomiarów (pętle v5, 1/1-oktawy względem maksimum)

| pętla | 63 | 125 | 250 | 500 | 1 k | 2 k | 4 k | 8 k | tempo modulacji [Hz] (oczekiwane) |
|---|---|---|---|---|---|---|---|---|---|
| HL 230 high (2800) | −27 | −21 | 0 | −10 | −13 | −25 | −33 | −42 | 280 (280) |
| HL 230 idle (650) | 0 | −12/0 | −15 | −17 | −19 | −34 | −44 | −54 | 65 (65) |
| W-2 high (1750) | −15 | −16 | −8 | −2 | −4 | −12 | −19 | −35 | 175 (175) |
| W-2 idle (550) | 0 | −6 | −16 | −14 | −12 | −20 | −30 | −47 | 54 (55) |
| GAA high (2600) | −26 | −3 | 0 | −13 | −15 | −26 | −34 | −44 | 173 (173) |
| GM 6046 high (2100) | −19 | −9 | −2 | −5 | −6 | −17 | −26 | −41 | 140/279/420 (420) |
| R-975 high (2400) | −17 | −12 | −7 | −5 | −6 | −17 | −24 | −34 | 180 (180) |
| Ricardo idle (330) | 0 | −10 | −18 | −10 | −10 | −16 | −25 | −36 | 16 (16,5) |

Kształt widma odpowiada nagraniom (maksimum 60–500 Hz, spadek 20–40 dB do 4–8 kHz), tempa modulacji zgadzają
się z częstotliwością zapłonów każdego silnika, klekot diesli sięga 3–4 kHz jak w nagraniu z bliska, benzyniaki
są ciemniejsze. Tiki mechaniczne są 20–35 dB pod poziomem całości (w nagraniu z bliska bywają głośniejsze –
parametr `valve`). Współczynnik szczytu 9–14 dB (nagrania: 12–13).

### 4.4 Czego audyt nie rozstrzyga

* Obroty jałowe i kąt rozwidlenia SPA 8T nie są udokumentowane w dostępnych źródłach – to założenia.
* Generator jest strojony pomiarami (widmo, tempo, szczyty), nie odsłuchem – ostateczny sąd należy do ucha;
  każdy parametr jest w jednej tabeli i można go zmienić bez ruszania modelu.
* Turbina gazowa nie jest napędem WWII; zostawiona jako prosty model (tony sprężarki, strumień, pomruk), bo
  gra ma taki silnik.

## 5. Źródła

* Ford GAA: [Wikipedia](https://en.wikipedia.org/wiki/Ford_GAA_engine), [karta danych GAA/GAF/GAN 1945 (theshermantank.com)](https://www.theshermantank.com/wp-content/uploads/Ford-GAA-V8-Data-Sheet-beta13.pdf), [EngineLabs o płaskim wale](https://www.enginelabs.com/?p=290828)
* Maybach HL 230 / HL 120: [Wikipedia HL230](https://en.wikipedia.org/wiki/Maybach_HL230), [Panzerworld – silniki niemieckie](https://panzerworld.com/german-armor-engines), [Lone Sentry – Pz IV](https://www.lonesentry.com/ordnance/?p=3048)
* W-2: [Wikipedia](https://en.wikipedia.org/wiki/Kharkiv_model_V-2), [tankhistoria.com](https://tankhistoria.com/cold-war/v-2-engine/)
* GM 6046 / Detroit 6-71: [theshermantank.com – silniki](https://www.theshermantank.com/sherman/the-motors-four-motors-made-it-into-production), [Wikipedia Series 71](https://www.wikiwand.com/en/articles/Series_71)
* Continental/Wright R-975: [Wikipedia](https://en.wikipedia.org/wiki/Wright_R-975_Whirlwind)
* SPA 8T: [Wikipedia M13/40](https://en.wikipedia.org/wiki/M13/40_tank), [Tanks Encyclopedia](https://www.tanks-encyclopedia.com/ww2/italy/Carro_Armato_Medio_M13-40.php)
* Ricardo 150 KM: [Wikipedia Mark V](https://en.wikipedia.org/wiki/Mark_V_tank), [Harry Ricardo](https://en.wikipedia.org/wiki/Harry_Ricardo)
* Odstępy zapłonów a barwa: [Car Throttle – A Musician's Analysis of Engine Notes](https://www.carthrottle.com/news/musicians-analysis-engine-notes), [F1technical – what causes an engine's character](https://www.f1technical.net/forum/viewtopic.php?p=715979)
* Hałas spalania: [Anderton – I.C. engine combustion noise (IOA)](https://www.ioa.org.uk/system/files/publications/D%20ANDERTON%20I.C.%20ENGINE%20COMBUSTION%20NOISE%20AND%20METHODS%20FOR%20ITS%20REDUCTION.pdf), [Springer 2016 – combustion noise](https://link.springer.com/article/10.1007/s41104-016-0001-5), [SAE 2004-32-0071](https://saemobilus.sae.org/papers/combustion-induced-noise-single-cylinder-diesel-engines-2004-32-0071)
