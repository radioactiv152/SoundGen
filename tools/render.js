#!/usr/bin/env node
/* Render pętli silników poza przeglądarką (ten sam silnik co w index.html).
 *
 *   node tools/render.js list                               - lista silników i stanów
 *   node tools/render.js wav <out_dir> [id[_stan]]...        - zapis WAV (brak id = wszystko)
 *   node tools/render.js custom <out_dir> <id> <rpm> <load>  - własne obroty i obciążenie (0-1)
 *   node tools/render.js check                               - render wszystkiego: błędy, NaN, LUFS, szczyt, szew pętli
 * Opcje: --loud=equal (wyrównana głośność), --seed=N, --dur=S
 */
'use strict';
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const m = html.match(/<script id="engine" type="text\/plain">([\s\S]*?)<\/script>/);
if (!m) throw new Error('nie znaleziono skryptu silnika');
const E = new Function(m[1] + ';return {REG:REG,ENGINES:ENGINES,specEntries:specEntries,specStem:specStem,renderOne:renderOne,SR:SR};')();

function wav(chs, sr) {
  const n = chs[0].length, nc = chs.length, b = Buffer.alloc(44 + n * nc * 2);
  b.write('RIFF', 0); b.writeUInt32LE(36 + n * nc * 2, 4); b.write('WAVEfmt ', 8); b.writeUInt32LE(16, 16); b.writeUInt16LE(1, 20);
  b.writeUInt16LE(nc, 22); b.writeUInt32LE(sr, 24); b.writeUInt32LE(sr * nc * 2, 28); b.writeUInt16LE(nc * 2, 32); b.writeUInt16LE(16, 34);
  b.write('data', 36); b.writeUInt32LE(n * nc * 2, 40);
  let o = 44;
  for (let i = 0; i < n; i++) for (let c = 0; c < nc; c++) { b.writeInt16LE(Math.round(Math.max(-1, Math.min(1, chs[c][i])) * 32767), o); o += 2; }
  return b;
}
const argv = process.argv.slice(2), opts = {};
const args = argv.filter((a) => { const mm = a.match(/^--(\w+)=(.*)$/); if (mm) { opts[mm[1]] = mm[2]; return false; } return true; });
const base = { seed: +(opts.seed || 0), loud: opts.loud || 'natural', dur: opts.dur ? +opts.dur : undefined };
function allTasks(keys) {
  const out = [];
  E.REG.forEach((s) => E.specEntries(s).forEach((e) => {
    const k = s.id + '_' + e.sub;
    if (!keys.length || keys.includes(k) || keys.includes(s.id)) out.push(Object.assign({ id: s.id, sub: e.sub, v: e.v, name: E.specStem(s, e.sub, e.v, false) }, base));
  }));
  return out;
}
function run(tasks, out) {
  if (out) fs.mkdirSync(out, { recursive: true });
  let bad = 0;
  tasks.forEach((t) => {
    const t0 = Date.now();
    try {
      const r = E.renderOne(t), finite = r.channels.every((c) => c.every(Number.isFinite));
      const warn = !finite || r.rep.peak_db > -1.4 || r.rep.seam > 3;
      if (warn) bad++;
      if (out) fs.writeFileSync(path.join(out, t.name + '.wav'), wav(r.channels, E.SR));
      console.log((warn ? '!! ' : '   ') + t.name.padEnd(26) + JSON.stringify(r.rep) + ' ' + (Date.now() - t0) + ' ms');
    } catch (err) { bad++; console.log('XX ' + t.name + ' ' + err.message); }
  });
  return bad;
}
const [cmd, ...rest] = args;
if (cmd === 'list') {
  E.REG.forEach((s) => console.log(s.id.padEnd(16) + (s.eng ? s.eng.rpm.join('/') + ' obr/min  ' : '').padEnd(22) + s.name + ' (' + s.veh + ')'));
} else if (cmd === 'wav') {
  run(allTasks(rest.slice(1)), rest[0]);
} else if (cmd === 'custom') {
  const [out, id, rpm, load] = rest;
  run([Object.assign({ id: id, sub: 'mid', v: 0, rpm: +rpm, load: +load, name: id + '_' + rpm + 'rpm_' + Math.round(+load * 100) + 'pct' }, base)], out);
} else if (cmd === 'check') {
  const bad = run(allTasks([]), null);
  console.log(bad ? bad + ' problemów' : 'OK');
  process.exit(bad ? 1 : 0);
} else {
  console.log('użycie: list | wav <out> [id]... | custom <out> <id> <rpm> <load> | check   [--loud=equal] [--seed=N] [--dur=S]');
}
