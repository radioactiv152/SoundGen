# Prompty ElevenLabs (Sound Effects): wystrzały i trafienia

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
| `hit_spall` | 0,8 s | `Inside a WWII tank: metal spall fragments fly around the crew compartment after a hit, a rapid cluster of sharp metallic impacts ricocheting off steel walls, cramped dry metal interior. No music, no voices.` |
| `hit_rivets` | 0,6 s | `Inside an old riveted WWII tank hit by a shell: rivet heads snap off the inner armor and fly across the compartment, several sharp metallic pops and clinks against steel walls. Short, dry interior. No music.` |
| `hit_he` | 3,5 s | `A high-explosive artillery shell explodes on a tank: powerful detonation with a sharp crack and deep boom, heavy shockwave, steel debris and dirt raining down for a moment, long rolling echo across open terrain. Outdoor, no music.` |
| `hit_heat` | 1,4 s | `A shaped-charge HEAT round detonates on tank armor: sharp concentrated explosion, a hissing jet of molten metal cutting through steel, crackling sparks and spall. Outdoors, close perspective, no music.` |
| `hit_module` | 0,7 s | `A shell hits a tank engine compartment: heavy blunt impact on cast iron machinery, cracking metal parts, loose components rattling. Heard from outside, dry, short. No music.` |
| `hit_crew` | 0,3 s | `Short muffled blunt impact of a fragment hitting gear and padding inside a cramped tank interior, dull and soft, no metal ring. No voices, no screams, no music.` |
| `hit_ground` | 1,4 s | `An armor-piercing shell misses and slams into the dirt next to a tank: heavy dull thud, spray of earth, clods and small stones falling back to the ground. Outdoors, no explosion, no music.` |
| `shell_flyby` | 0,8 s | `A tank shell flies past very close overhead: sharp supersonic crack followed by a fast tearing whoosh that passes from left to right and fades, Doppler effect. Outdoors, no explosion, no music.` |
| `cookoff` | 5,0 s | `Ammunition cook-off inside a destroyed WWII tank: a huge initial explosion, roaring fireball, then a series of smaller secondary detonations and popping rounds, burning propellant hissing, metal debris and hatches crashing down. Outdoors, no music, no voices.` |
| `hull_torn` | 3,0 s | `A tank hull is torn apart by a massive internal explosion: deep powerful blast, screeching and tearing of thick steel plates, heavy armor panels crashing to the ground, debris falling. Outdoors, no music.` |

## Wskazówki, gdy wynik jest zły

- **Za mało mocy**: dopisz `massive, concussive, chest-hitting low end, close perspective`.
- **Brzmi jak dzwon albo garnek**: dopisz `dry, not a bell, no ringing, short metallic crack`.
- **Za dużo pogłosu**: dopisz `dry, close-up, minimal reverb, open field`.
- **Dodaje serię strzałów**: dopisz `single shot only, one impact, no burst`.
- **Zbyt filmowe** (whoosh przed strzałem, efekty „trailerowe”): dopisz `realistic field recording, no cinematic whoosh, no build-up`.
