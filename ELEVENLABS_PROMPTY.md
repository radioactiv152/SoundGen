# Prompty ElevenLabs (Sound Effects): wszystkie grupy poza pętlami silników

Dźwięki, z którymi proceduralny generator ma najwięcej problemów: brzmią syntetycznie, mimo kolejnych poprawek.
Do podmiany na nagrania lub generację. Prompty są po angielsku, bo ElevenLabs najlepiej rozumie angielski.

## Ustawienia i obróbka

- **Duration**: ustaw ręcznie na wartość z kolumny „czas” (automat często daje za długie lub za krótkie).
- **Prompt influence**: ~0,5–0,7. Wyżej = dokładniej według opisu, ale mniej naturalnie.
- Generuj po 3–4 wersje i wybieraj. Warianty (`_1`, `_2`, `_3`) to różne udane generacje tego samego promptu.
- Po wygenerowaniu (żeby pasowały do reszty paczki):
  - mono, 44,1 kHz,
  - przytnij ciszę na początku (atak od pierwszej próbki),
  - krótkie wyciszenie końca (~15 ms),
  - głośność: −14 LUFS (short-term), szczyt −1,5 dBFS,
  - zapisz pod nazwą z kolumny „plik”, np. `cannon_m_fire_1.ogg`.
- Jeśli ElevenLabs dorzuca muzykę lub głosy, dopisz na końcu promptu: `no music, no voices`.
- Na brzmienie „z beczki” lub „z hangaru” dopisz: `open field, no indoor reverb, natural outdoor echo`.

## Wystrzały (warstwa „sucha”; długi ogon to osobny plik `shot_tail`)

| plik | czas | prompt |
|---|---|---|
| `mg_shot` | 1,0 s | `Single gunshot from a WWII belt-fed machine gun (MG42 style, 7.92 mm), close perspective, open field. Sharp supersonic crack, punchy mid-range muzzle blast, short metallic bolt clack, then a brief natural outdoor echo from distant trees. One shot only, no burst, no music, no voices.` |
| `hmg_shot` | 1,2 s | `Single shot from a WWII heavy machine gun (.50 cal Browning M2), close perspective, outdoors. Deep, heavy muzzle boom with a hard supersonic crack, mechanical receiver clank, short natural echo from a tree line. One shot only, no burst, no music.` |
| `autocannon_shot` | 1,4 s | `Single shot from a 20 mm anti-aircraft autocannon on a vehicle, close outdoor perspective. Loud sharp bang with strong low-mid punch, metallic breech clack right after, short rolling outdoor echo. One round only, no music.` |
| `cannon_s_fire` | 1,8 s | `Single shot from a light WWII tank cannon (37 mm), recorded close outside the tank in an open field. Hard explosive crack, powerful muzzle blast, short clunk of the recoil mechanism, brief echo from distant hills. One shot, dry, no indoor reverb, no music.` |
| `cannon_m_fire` | 2,2 s | `Single shot from a WWII medium tank main gun (75 mm, Sherman or Panzer IV), recorded close in an open field. Massive explosive boom with a sharp supersonic crack, chest-hitting low end, heavy metal clunk of the recoiling breech, then a natural outdoor echo rolling off a tree line. One shot, open field, no indoor reverb, no music.` |
| `cannon_l_fire` | 2,6 s | `Single shot from a WWII heavy tank gun (88 mm Tiger), close outdoor perspective. Enormous concussive blast, sharp crack, deep pressure-wave thump, steel recoil clank, the tank hull shudders, then a long natural echo across open countryside. One shot only, no music, no voices.` |
| `howitzer_fire` | 2,8 s | `Single shot from a WWII 105 mm field howitzer, recorded nearby in an open field. Deep, booming, concussive blast with a softer crack than a tank gun, heavy low-frequency pressure wave, recoil clank, long rolling outdoor echo. One shot, no music.` |
| `recoilless_fire` | 1,4 s | `Single shot from a recoilless rifle, close outdoor perspective. Very loud sharp bang combined with a violent roaring backblast of gas rushing out behind the weapon, debris and dust kicked up, short outdoor echo. One shot, no music.` |
| `atgm_launch` | 2,5 s | `Wire-guided anti-tank missile launch outdoors: a sharp ejection pop, then the rocket motor ignites with a harsh fluttering roar that quickly flies away into the distance and fades. Close perspective at launch, open field, no music.` |
| `shot_tail` (stereo) | 2,5 s | `Distant echo tail of a large tank cannon shot in open countryside, without the initial blast: deep rolling thunder-like reverberation bouncing off hills and forest, several distinct delayed echoes, slowly fading. Stereo, outdoor, no music.` |

## Trafienia

| plik | czas | prompt |
|---|---|---|
| `hit_nonpen_thin` | 1,2 s | `An armor-piercing shell strikes the thin side armor of a WWII light tank and bounces off: violent explosive bang, sharp high-pitched steel crack, short metallic ring, sparks and fragments scatter. Heard from outside, open field, short natural echo. No music.` |
| `hit_nonpen_thick` | 1,5 s | `A tank shell slams into thick frontal armor of a heavy tank and fails to penetrate: enormous explosive bang like a cannon shot, deep heavy steel impact, brief harsh metallic crack, fragments rattling off, short outdoor echo. Massive and dry, not a bell, no music.` |
| `hit_pen_thin` | 1,5 s | `An armor-piercing shell punches through the thin armor of a light tank: sharp explosive bang, tearing crunch of steel being sheared, muffled thump inside the hull, spall fragments clattering inside. Heard from outside, open field, no music.` |
| `hit_pen_thick` | 1,5 s | `A heavy armor-piercing shell penetrates thick tank armor: huge concussive impact boom, violent crunch of steel tearing, deep muffled blast inside the hull, metal fragments rattling inside. Heavy, brutal, heard from outside in an open field, no music.` |
| `hit_ricochet` | 1,2 s | `A tank shell glances off sloped steel armor and ricochets away: hard explosive clang, sparks, then the deflected shell tumbles away with a fast whirring, fading whoosh. Outdoors, close perspective, no music.` |
| `hit_mg` | 0,8 s | `Rifle-caliber machine gun bullet hits tank armor: sharp bright "spak" of a bullet splattering on thick steel, tiny metallic ping, fragments spraying, very short. Single impact, outdoors, no music.` |
| `hit_spall` | 1,0 s | `A handful of small steel nuts and bolts thrown hard against a thick steel wall in a small metal room, a fast burst of sharp metallic clinks and clatters that quickly dies down. Dry, close-up, no music.` (alternatywy w sekcji „hit_spall: warianty”) |
| `hit_rivets` | 0,6 s | `Inside an old riveted WWII tank hit by a shell: rivet heads snap off the inner armor and fly across the compartment, several sharp metallic pops and clinks against steel walls. Short, dry interior. No music.` |
| `hit_he` | 3,5 s | `A high-explosive artillery shell explodes on a tank: powerful detonation with a sharp crack and deep boom, heavy shockwave, steel debris and dirt raining down for a moment, long rolling echo across open terrain. Outdoor, no music.` |
| `hit_heat` | 1,4 s | `A shaped-charge HEAT round detonates on tank armor: sharp concentrated explosion, a hissing jet of molten metal cutting through steel, crackling sparks and spall. Outdoors, close perspective, no music.` |
| `hit_module` | 0,7 s | `A shell hits a tank engine compartment: heavy blunt impact on cast iron machinery, cracking metal parts, loose components rattling. Heard from outside, dry, short. No music.` |
| `hit_crew` | 0,3 s | `Short muffled blunt impact of a fragment hitting gear and padding inside a cramped tank interior, dull and soft, no metal ring. No voices, no screams, no music.` |
| `hit_ground` | 1,4 s | `An armor-piercing shell misses and slams into the dirt next to a tank: heavy dull thud, spray of earth, clods and small stones falling back to the ground. Outdoors, no explosion, no music.` |
| `shell_flyby` | 0,8 s | `A tank shell flies past very close overhead: sharp supersonic crack followed by a fast tearing whoosh that passes from left to right and fades, Doppler effect. Outdoors, no explosion, no music.` |
| `cookoff` | 5,0 s | `Ammunition cook-off inside a destroyed WWII tank: a huge initial explosion, roaring fireball, then a series of smaller secondary detonations and popping rounds, burning propellant hissing, metal debris and hatches crashing down. Outdoors, no music, no voices.` |
| `hull_torn` | 3,0 s | `A tank hull is torn apart by a massive internal explosion: deep powerful blast, screeching and tearing of thick steel plates, heavy armor panels crashing to the ground, debris falling. Outdoors, no music.` |

### hit_spall: warianty (pierwotny prompt nie działał: „spall” i „ricocheting” myliły model, a „Inside a tank” dodawało silnik)

Prompt influence ~0,7–0,8, czas 1 s:

1. `A handful of small steel nuts and bolts thrown hard against a thick steel wall in a small metal room, a fast burst of sharp metallic clinks and clatters that quickly dies down. Dry, close-up, no music.`
2. `A loud metallic bang followed by dozens of small sharp steel fragments striking metal walls in a cramped steel box, a quick clattering rattle lasting under one second. Dry, no ringing, no music.`
3. `Shrapnel striking the inside of an armored steel compartment: a sudden sharp impact, then a rapid scatter of small metal pieces bouncing and rattling off steel surfaces. Short, dry, no whistle, no music.`
4. `Short burst of metal debris clattering on a steel floor and steel walls, like a bucket of steel scraps dropped at once. One second, dry, realistic, no music.`

Awaryjnie można złożyć dwie warstwy: odpryski (1 lub 4) nałożone 10–20 ms po krótkim huku
`short muffled metallic thump inside a steel box, dry`, całość przycięta do ~0,8 s.

## Podwozie i teren

Te dźwięki nakładają się w grze na pętle silnika, dlatego w każdym prompcie jest `no engine sound`.
Bez tego model zwykle dokłada silnik.

**Pętle (`loop: tak`)**:
- w ElevenLabs włącz **Loop**, jeśli jest dostępne;
- jeśli nie: generuj 8–12 s, wytnij fragment o równym rytmie i zszyj końce przenikaniem (crossfade ~50–100 ms);
- pętla może być dłuższa niż w specyfikacji (2–3 s), bo silnik gry zapętla dowolną długość, a dłuższa mniej się powtarza;
- głośność pętli: −18 LUFS (integrated).

| plik | czas | pętla | prompt |
|---|---|---|---|
| `track_steel` | 8–10 s | tak | `Steel tank tracks of a WWII tank rolling at steady moderate speed on a dirt road, heard close from the side: rhythmic heavy clanking of track links over the sprocket, rattling track pins, squeaking road wheels, low rumble. Constant speed, no engine sound, no music.` |
| `track_rubber` | 8–10 s | tak | `Rubber-padded tank tracks rolling steadily on an asphalt road, close perspective: dull rhythmic thumping of track pads, soft rattle, rolling road wheels, low rumble. Much softer than steel tracks, constant speed, no engine sound, no music.` |
| `track_ww1` | 10–12 s | tak | `Very slow, heavy WWI tank tracks crawling over muddy ground: slow, loud, irregular clanking of huge steel track plates, chain-like rattling and squealing, creaking, heavy low rumble. Constant slow speed, no engine sound, no music.` |
| `wheels_road` | 8–10 s | tak | `Heavy WWII armored car with large rubber tires driving steadily on a cobblestone and gravel road, close perspective: tire roar and hum, gravel crunching and popping under the tires, rhythmic bumps over joints, loose metal parts rattling. No engine sound, no music.` |
| `halftrack_roll` | 8–10 s | tak | `WWII half-track vehicle rolling steadily on a dirt road: rubber band tracks thumping rhythmically, front tires rolling on gravel, rattling suspension and loose equipment. Close perspective, constant speed, no engine sound, no music.` |
| `track_spin` | 6–8 s | tak | `Tank tracks spinning in place without traction in mud and gravel: fast continuous clattering of steel track links, mud and stones being thrown and spattering, grinding scrape. Close perspective, no engine sound, no music.` |
| `surf_mud` | 8–10 s | tak | `Heavy tank tracks churning through thick wet mud at slow speed: deep squelching, sucking and slapping mud with every track link, wet splatter, low rumble. Close perspective, no engine sound, no music.` |
| `surf_sand` | 8–10 s | tak | `Tank tracks rolling over dry sand and fine gravel: continuous soft crunching and hissing of sand under the tracks in a steady rhythm, muffled clanking of links. Close perspective, no engine sound, no music.` |
| `surf_water` | 8–10 s | tak | `A heavy tank fording a shallow river at slow speed: water sloshing and splashing against the hull, tracks churning water, bubbling and gurgling, waves lapping. Close perspective, no engine sound, no music.` |
| `water_enter` | 2 s | nie | `A heavy tank drives fast into a river: a big heavy splash as the hull hits the water, a wall of water crashing down, bubbles, then waves slapping against the hull and settling. One event, no engine sound, no music.` |
| `susp_bump` | 0,6 s | nie | `A heavy tank drives over a bump: one deep heavy thud of the vehicle mass, metallic clunk of the suspension hitting the bump stop, a short spring rebound, loose tools and equipment rattling on the hull. Single event, no engine sound, no music.` |
| `step_hit` | 0,8 s | nie | `A heavy tank drops off a ledge and its front slams into the ground: massive heavy thud, steel tracks clanking, suspension clunk, rattling equipment, clods of earth falling. Single event, no engine sound, no music.` |
| `belly_scrape` | 1,2 s | nie | `The steel belly of a tank scrapes over rocks and hard ground: heavy grinding friction, harsh metallic screeching scrape, stones knocking against the hull, gravel crunching. Short event, no engine sound, no music.` |
| `brake` | 1,6 s | nie | `A heavy WWII tank brakes hard to a stop: steel tracks clank slower and slower, a metallic brake squeal, a low groan of friction just before stopping, then the hull rocks forward and back on its suspension with a heavy clunk. No engine sound, no music.` |
| `hull_creak` | 1,5 s | nie | `Thick steel plates of a tank hull creaking and groaning under stress: slow metallic stick-slip creak, deep groan of the hull, no impacts. Close perspective, no engine sound, no music.` |

## Ambienty (tła, stereo)

Pliki w specyfikacji są 40-sekundowe (`amb_battle`: 15 s). Maksymalna długość w ElevenLabs bywa krótsza
(sprawdź limit w swoim planie), więc:
- generuj najdłużej, jak się da, z **Loop** (jeśli dostępne);
- albo złóż 2 różne generacje tego samego promptu z przenikaniem ~1–2 s i zszyj koniec z początkiem;
- głośność ambientów: −23 LUFS (integrated), stereo.

| plik | prompt |
|---|---|
| `amb_battle` | `Distant WWII battlefield ambience heard from a quiet position: far-off artillery explosions with long rolling echoes, distant machine gun bursts, occasional rifle shots, a shell whistling high overhead, a tank rumbling far away, light wind. Wide stereo, distant, no music, no voices.` |
| `amb_range` | `Military proving ground on a calm summer day: gentle wind over open grassland, birds singing in the distance, occasional far-off tank cannon test shots echoing across the hills, a tank rumbling faintly in the distance. Wide stereo, peaceful, no music, no voices.` |
| `amb_town` | `Small industrial town in the 1940s heard from an open office window: distant street noise, an old truck passing by, a blacksmith hammering on an anvil far away, birds, light wind, a factory steam whistle in the distance once. Wide stereo, calm, no modern cars, no music, no voices.` |
| `amb_office` | `1940s engineering design office interior: quiet room tone, a wall clock ticking, an old mechanical typewriter typing in bursts with a carriage bell and return, paper rustling, a muffled factory press thumping behind the wall. Calm, no music, no voices, no modern electronics.` |
| `fire_loop` | `A burning destroyed tank close up: roaring fire, crackling and popping flames, hissing, occasional small pops of burning ammunition, metal ticking from heat. Constant intensity, loopable, no explosions, no music, no voices.` |

## Obsługa broni

| plik | czas | pętla | prompt |
|---|---|---|---|
| `gun_breech_1` | 1,2 s | nie | `Inside a WWII tank turret: the heavy sliding-wedge breech of the main gun drops open with a solid steel clack, and a large empty brass shell casing slides out and clangs onto the steel floor. Close, dry, cramped metal interior, no gunshot, no music, no voices.` |
| `gun_breech_2` | 1,2 s | nie | `Inside a WWII tank turret: a heavy tank shell is pushed into the gun chamber with a metallic slide, then the steel breech block slams shut with a heavy clank and a sharp latch click. Close, dry, cramped metal interior, no gunshot, no music, no voices.` |
| `shell_casing_1` | 1,0 s | nie | `A large empty brass tank shell casing drops onto a steel floor: bright ringing clang, a few bounces getting faster and quieter, then it rolls briefly with a hollow brass ring. Close, dry, no music.` |
| `shell_casing_2` | 1,0 s | nie | `A large empty brass shell casing falls onto packed dirt: a short dull clunk, one small bounce, muted brass ring that dies quickly. Outdoors, close, no music.` |
| `shell_casing_3` | 1,0 s | nie | `A heavy brass artillery shell casing hits a steel deck, bounces several times with a deep resonant ring, then rolls away rattling across the metal floor. Close, dry, no music.` |
| `turret_traverse` | 6–8 s | tak | `A WWII tank turret rotating steadily: smooth whine of the electric traverse motor, gear whine of the turret ring drive, deep low rumble of the heavy turret turning on its ball bearing ring, faint metal friction. Constant speed, smooth, no crackling, no engine sound, no music.` |

Do `turret_traverse`: jeśli wychodzi trzeszczący szum (brzmiało już raz „jak spawanie”), dopisz
`smooth tonal motor hum, no static, no crackle, no welding sound`.

## Wojna i meldunki

`ace` i `report_defeat` to krótkie sygnały muzyczne (w specyfikacji „szkic”). Jeśli generator efektów
robi z nich hałas, lepiej wygenerować je w **ElevenLabs Music** albo nagrać.

| plik | czas | prompt |
|---|---|---|
| `report_open` | 1,2 s | `A 1940s military teleprinter or telegraph receiving a message: rapid mechanical clattering of typebars for about one second, then a single small bell ding as the line ends. Close, dry office, no music, no voices.` |
| `stamp` | 0,4 s | `A heavy rubber stamp pressed firmly onto paper on a wooden desk: one solid dull thump with a slight wooden knock. Close, dry, single hit, no music.` |
| `ace` | 2,5 s | `Short triumphant military sting: a crisp snare drum roll building for one second, a cymbal crash, then a bold two-note brass fanfare rising, with a timpani hit. 1940s military band style, no voices.` |
| `report_defeat` | 2,0 s | `Short somber military sting: three slow, heavy, muffled bass drum hits with a low rumble underneath, dark and mournful, fading out. No melody, no voices.` |
| `war_start` | 3,0 s | `Outbreak of war in a 1940s town: an air-raid siren winding up and wailing, a second siren further away slightly out of tune, long echo between buildings, and three distant heavy explosions rumbling in the background. Outdoor, no music, no voices.` |
| `hangar_arrive` | 2,5 s | `A WWII tank drives slowly into a large hangar and stops: steel tracks clanking on concrete slowing down, a heavy final clunk as it halts, then the engine idles with a low rumble, echoing in the big hall. No music, no voices.` |

`amb_battle` (z grupy „Wojna i meldunki”) jest wyżej, w sekcji „Ambienty”.

## Silniki: zdarzenia

Pętle silników (`eng_*_idle/mid/high`) zostają z generatora. Tu są tylko zdarzenia jednorazowe.

| plik | czas | prompt |
|---|---|---|
| `eng_start` | 3,2 s | `A big WWII tank petrol V8 engine starting from cold, close outdoor perspective: a solenoid clack, the electric starter motor whines and cranks the engine slowly with rhythmic compression strokes, the engine catches with a few uneven coughs, revs up briefly, then settles into a rough, burbling idle. No music, no voices.` |
| `eng_stall` | 1,8 s | `A big WWII tank engine stalls: the idle stumbles and misfires, revs drop quickly with uneven chugging, a last couple of heavy compression thumps, then silence with a slight metallic clunk as the engine rocks on its mounts. Close outdoor perspective, no music.` |
| `eng_stop` (nowy, brak w generatorze) | 3,5 s | `Engine shutdown of a heavy WWII tank: a deep, lumpy V8 idle rumbling steadily for one second, then the engine is turned off and the rumble dies away over about one second in a few slow, heavy, uneven chugs, ending with one soft clunk. Then silence. Close, outdoors, no starting, no revving, no music.` (warianty niżej) |
| `gear_shift` | 0,5 s | `Heavy WWII tank transmission gear change: a short grinding of gears meshing, a solid metallic clunk as the gear engages, a jolt through the drivetrain. Close, from inside the hull, dry, no engine revving, no music.` |
| `eng_backfire` | 0,4 s | `Single loud backfire from the exhaust of a big petrol tank engine: a sharp explosive pop with a short flame burst, ringing exhaust pipe, followed by two or three small crackles. Close outdoor perspective, no music.` |

Warianty `eng_stop`, gdy główny prompt nie działa (czas 3–4 s, prompt influence ~0,7):
- prostszy: `A large diesel tank engine idling, then switched off: the rumble slows down and stops within a second with a few heavy final thumps. Close, outdoors, no music.`
- gdy model odpala silnik zamiast go gasić: `Sound of an engine stopping, not starting: idling truck-sized engine shuts off, chugs slowing down to silence, a final mechanical clunk. No starter motor, no revving, no music.`
- bez idle na początku (do sklejenia z pętlą `eng_*_idle`): `A heavy tank engine shutting down: three or four slowing, heavy, uneven chugs fading to silence, a soft final clunk. Short, close, outdoors, no music.`

`eng_stop` (zwykłe zgaszenie silnika, w odróżnieniu od `eng_stall`, czyli zgaśnięcia) nie istnieje dziś w
specyfikacji. Jeśli ma trafić do gry, trzeba dodać go także po stronie gry. Mogę go też dorobić w generatorze.

## Poligon i próby

| plik | czas | prompt |
|---|---|---|
| `trial_start` | 0,6 s | `A referee's pea whistle blown once firmly outdoors: a bright shrill trilling whistle about half a second long. No music, no voices.` |
| `trial_pass` | 0,8 s | `Two-note bell chime signalling success: a clear bright metal bell strikes a lower note then a higher note, natural ringing decay. Clean, short, no music, no voices.` |
| `trial_fail` | 0,8 s | `Two-tone old electric buzzer signalling failure: a harsh low buzz, then a second lower buzz. 1940s electromechanical buzzer, dry, short, no music, no voices.` |
| `series_done` | 0,6 s | `A sheet of paper slid quickly off a clipboard with a soft whoosh, followed by one small bright desk bell ding. Close, dry, no music.` |

## Firma

| plik | czas | prompt |
|---|---|---|
| `month_next` | 0,8 s | `Tearing a page off a 1940s paper wall calendar: a quick crisp paper rip, followed by a single warm mechanical desk bell chime. Close, dry office, no music.` |
| `money_in` | 0,7 s | `An old mechanical cash register: a bright bell ring as the drawer opens, and a few metal coins dropping and clinking onto a wooden counter. Close, dry, no music, no voices.` |
| `tender_won` | 2,0 s | `Short triumphant victory fanfare: bright brass trumpets play a rising arpeggio ending on a long high note, with timpani hits and a cymbal crash at the end. 1940s military band style, no voices.` |
| `tender_lost` | 1,5 s | `Short disappointed sting: muted brass trombones play four slowly descending notes, the last one sagging flat. Sad, comic, 1940s style, no voices.` |
| `research_done` | 1,2 s | `An old mechanical typewriter typing a short line in quick bursts, then a single clear desk bell ding. Close, dry office, no music, no voices.` |
| `research_start` | 0,5 s | `Feeding a sheet of paper into an old typewriter: the platen knob ratchets with several small clicks while the paper slides in with a soft rustle. Close, dry, no music.` |
| `bid_submit` | 0,6 s | `A rubber stamp pressed hard onto a document on a wooden desk, followed by the paper being slid away across the desk. Close, dry office, no music.` |
| `newspaper` | 1,0 s | `A 1940s newspaper being unfolded with two crisp paper rustles, then slapped down onto a wooden desk. Close, dry, no music, no voices.` |
| `medal` | 1,5 s | `Short military award sting: a crisp snare drum roll, then a bright metal medal chime ringing out with a soft cymbal. Ceremonial, 1940s military style, no voices.` |
| `factory_up` | 2,5 s | `A 1940s factory starting up: a steam whistle blows once, then heavy machinery starts and gains speed, rhythmic thumping of a mechanical press getting faster, the deep rumble of the hall growing. No music, no voices.` |
| `delivery_done` | 2,5 s | `A 1940s steam freight train leaving a factory siding with a delivery: a short whistle, slow heavy steam chuffs speeding up, wagon couplings clanking, rolling away into the distance. No music, no voices.` |
| `deadline` | 1,2 s | `An old mechanical wall clock ticking four times, tick-tock with a wooden case resonance, the last tick slightly louder. Close, dry, no music.` |
| `order_cancel` | 0,7 s | `A sheet of paper being torn in half quickly and crumpled. Close, dry office, no music, no voices.` |
| `bankrupt` | 2,5 s | `A heavy iron factory gate slamming shut in an empty industrial hall: a deep booming metallic clang with a long hollow echo, chains rattling down, debris settling. Gloomy, no music, no voices.` |

## Kreator (warsztat i biuro konstrukcyjne)

Wspólny kontekst: montaż czołgu w hali fabrycznej. Każdy prompt ma `factory hall` i `no machine-gun, no engine`,
żeby model nie dodawał walki ani silnika.

| plik | czas | prompt |
|---|---|---|
| `ed_place` | 0,5 s | `A heavy steel tank part is set down onto a steel frame in a factory hall: a solid dull metal clunk with a short damped ring, then one or two bolts being tightened with small metal clicks. Close, short, no engine, no music.` |
| `ed_remove` | 0,5 s | `Removing a steel part in a factory workshop: a ratchet wrench clicks four times, the part slides off with a short metal scrape, then is set aside with a light clunk. Close, dry, no engine, no music.` |
| `ed_swap` | 0,8 s | `Swapping a steel component in a workshop: a quick ratchet and metal scrape as one part is removed, then another heavy steel part is set into place with a solid clunk. Close, factory hall, no engine, no music.` |
| `ed_armor` | 0,8 s | `A thick steel armor plate is lowered onto a tank hull in a factory hall: a short scrape of the edge, then a massive heavy low steel thud with a brief damped ring as it settles. Close, no engine, no music.` |
| `ed_turret` | 1,2 s | `A heavy tank turret is lowered by a crane onto the turret ring in a factory hall: a grinding of the ring, a deep heavy metallic clunk as it seats, then the loose crane chain rattles. No engine, no music.` |
| `ed_hull` | 1,5 s | `A massive tank hull is set down by an overhead crane onto a factory floor: a huge deep metallic thud shaking the floor, echoing in a large hall, then the crane chain slackens and rattles. No engine, no music.` |
| `ed_autofill` | 1,8 s | `Several heavy steel parts are placed onto a tank one after another in quick succession in a factory hall: five solid metal clunks of different sizes in a steady rhythm, with small bolt clicks. Close, no engine, no music.` |
| `ed_weld` | 1,2 s | `Electric arc welding on thick steel in a factory: the arc strikes and sizzles with a steady frying crackle and hiss, then stops. Close, no music, no voices.` |
| `ed_rivet` | 1,0 s | `A pneumatic rivet gun hammering a rivet into a steel plate: a rapid burst of loud metallic hammer blows at about 16 hits per second, compressed air hissing, in a factory hall. No music.` |
| `ed_stage_done` | 0,4 s | `A short pneumatic air hiss followed by a solid satisfying metal latch clunk and click. Close, factory, no music.` |
| `ed_undo` | 0,2 s | `A quick soft paper swoosh, like a drawing sheet slid back across a drafting table. Very short, close, dry, no music.` |

## Interfejs (UI)

Styl spójny z resztą gry: przedmioty z biura lat 40. (bakelit, drewniane biurko, papier, pieczątka, dzwonek,
brzęczyk), bez cyfrowych „bipów”.

Bardzo krótkie dźwięki (`ui_click` 0,08 s, `ui_slider` 0,03 s) generuj w najkrótszym czasie, jaki pozwala
ElevenLabs (zwykle ~0,5 s), i przytnij do samego uderzenia (atak od pierwszej próbki, wyciszenie ~5 ms).
Głośność UI: −20 LUFS (short-term), szczyt −1,5 dBFS.

| plik | czas docelowy | prompt |
|---|---|---|
| `ui_click_1` | 0,08 s | `A single click of an old bakelite toggle switch: a short, crisp, dry mechanical snap with a tiny spring sound. Very short, close, no reverb, no music.` |
| `ui_click_2` | 0,08 s | `A single press of a 1940s bakelite push button: short dry plastic click with a soft mechanical body. Very short, close, no reverb, no music.` |
| `ui_tab_1` | 0,25 s | `Quickly flipping a single cardboard index card tab forward in a wooden file box: a short paper flick ending with a soft wooden tap. Close, dry, no music.` |
| `ui_tab_2` | 0,25 s | `Flipping a single cardboard file tab backward: a short paper flick, slightly lower in tone, ending with a soft wooden tap. Close, dry, no music.` |
| `ui_error` | 0,35 s | `Two quick dull knocks of a knuckle on a wooden desk, the second slightly lower and quieter. Close, dry, no music, no voices.` |
| `ui_confirm_1` | 0,4 s | `A rubber stamp pressed onto paper on a wooden desk: one firm, short, satisfying thump. Close, dry, no music.` |
| `ui_confirm_2` | 0,4 s | `A heavy rubber stamp pressed hard onto a document: deeper, more solid thump on a wooden desk. Close, dry, no music.` |
| `ui_toast` | 0,6 s | `A single small desk service bell tapped once: a clear bright ding with a natural ringing decay. Close, dry room, no music.` |
| `ui_warning` | 0,6 s | `An old electromechanical warning buzzer sounding twice in quick succession: two short harsh low buzzes. 1940s style, dry, no music, no voices.` |
| `ui_modal` | 0,4 s | `A sheet of paper slid quickly out of a folder with a rising whoosh, then laid down on a wooden desk with a soft tap. Close, dry, no music.` |
| `ui_expand` | 0,2 s | `A quick short paper rustle as a folded document is opened, ending with a tiny wooden tap. Very short, close, dry, no music.` |
| `ui_drawer` | 0,4 s | `A small wooden desk drawer sliding open smoothly with a soft wood-on-wood friction sound, stopping with a gentle wooden knock. Close, dry, no music.` |
| `ui_slider` | 0,03 s | `A single tiny dry metal detent tick of a 1940s radio tuning knob. Extremely short, close, no reverb, no music.` |

Jeśli model dodaje dźwięki cyfrowe lub komputerowe, dopisz `analog, mechanical, no electronic beeps, no computer sounds`.

## Wskazówki, gdy wynik jest zły

- **Za mało mocy**: dopisz `massive, concussive, chest-hitting low end, close perspective`.
- **Brzmi jak dzwon albo garnek**: dopisz `dry, not a bell, no ringing, short metallic crack`.
- **Za dużo pogłosu**: dopisz `dry, close-up, minimal reverb, open field`.
- **Dodaje serię strzałów**: dopisz `single shot only, one impact, no burst`.
- **Zbyt filmowe** (whoosh przed strzałem, efekty „trailerowe”): dopisz `realistic field recording, no cinematic whoosh, no build-up`.
- **Dokłada silnik do gąsienic lub terenu**: dopisz `no engine sound, no engine noise` (czasem pomaga też `recorded with the engine off, coasting`).
- **Rytm gąsienic za szybki lub za wolny**: dopisz `slow walking pace` / `moderate speed` / `fast speed`.
- **W ambiencie są współczesne dźwięki**: dopisz `1940s, no modern cars, no airplanes, no electronics`.
- **Sygnał muzyczny brzmi jak hałas**: użyj ElevenLabs Music albo dopisz `clean, short musical sting, military band instruments`.
