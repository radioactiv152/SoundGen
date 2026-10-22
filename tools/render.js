#!/usr/bin/env node
/* Render dźwięków poza przeglądarką (ten sam silnik co w index.html).
 *
 *   node tools/render.js list                              - lista id
 *   node tools/render.js wav <out_dir> <ver> <id[_sub]>... - zapis WAV (wszystkie warianty)
 *   node tools/render.js check [ver]                       - render wszystkiego: błędy, NaN, LUFS, szczyt, szew pętli
 */
'use strict';
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const m = html.match(/<script id="engine" type="text\/plain">([\s\S]*?)<\/script>/);
if (!m) throw new Error('nie znaleziono skryptu silnika');
const E = new Function(m[1] + ';markV3();return {REG:REG,specEntries:specEntries,specStem:specStem,renderOne:renderOne,SR:SR};')();

function wav(chs, sr) {
  const n = chs[0].length, nc = chs.length, b = Buffer.alloc(44 + n * nc * 2);
  b.write('RIFF', 0); b.writeUInt32LE(36 + n * nc * 2, 4); b.write('WAVEfmt ', 8); b.writeUInt32LE(16, 16); b.writeUInt16LE(1, 20);
  b.writeUInt16LE(nc, 22); b.writeUInt32LE(sr, 24); b.writeUInt32LE(sr * nc * 2, 28); b.writeUInt16LE(nc * 2, 32); b.writeUInt16LE(16, 34);
  b.write('data', 36); b.writeUInt32LE(n * nc * 2, 40);
  let o = 44;
  for (let i = 0; i < n; i++) for (let c = 0; c < nc; c++) { b.writeInt16LE(Math.round(Math.max(-1, Math.min(1, chs[c][i])) * 32767), o); o += 2; }
  return b;
}
function tasksFor(key) {
  const s = E.REG.find((x) => key === x.id || (x.subs.length && x.subs.some((sb) => key === x.id + '_' + sb)));
  if (!s) throw new Error('brak id: ' + key);
  const sub = key === s.id ? null : key.slice(s.id.length + 1);
  return E.specEntries(s).filter((e) => !sub || e.sub === sub).map((e) => ({ spec: s, sub: e.sub, v: e.v }));
}

const [cmd, ...args] = process.argv.slice(2);
if (cmd === 'list') {
  E.REG.forEach((s) => console.log(s.id + (s.subs.length ? ' [' + s.subs.join(',') + ']' : '') + ' x' + s.var + (s.fn2 ? ' (' + (s.v3 ? 'v3' : 'v2') + ')' : '')));
} else if (cmd === 'wav') {
  const [out, ver, ...keys] = args;
  fs.mkdirSync(out, { recursive: true });
  keys.forEach((k) => tasksFor(k).forEach((t) => {
    const t0 = Date.now(), r = E.renderOne({ id: t.spec.id, sub: t.sub, v: t.v, seed: 0, ver: ver });
    const name = E.specStem(t.spec, t.sub, t.v, false) + '.' + ver + '.wav';
    fs.writeFileSync(path.join(out, name), wav(r.channels, E.SR));
    console.log(name, JSON.stringify(r.rep), (Date.now() - t0) + ' ms');
  }));
} else if (cmd === 'check') {
  const ver = args[0] || 'v4';
  let bad = 0;
  E.REG.forEach((s) => E.specEntries(s).forEach((e) => {
    const name = E.specStem(s, e.sub, e.v, false);
    try {
      const t0 = Date.now(), r = E.renderOne({ id: s.id, sub: e.sub, v: e.v, seed: 0, ver: ver });
      const finite = r.channels.every((c) => c.every(Number.isFinite));
      const warn = !finite || r.rep.peak_db > -1.4 || (s.loop && r.rep.seam > 3);
      if (warn) bad++;
      console.log((warn ? '!! ' : '   ') + name.padEnd(28) + JSON.stringify(r.rep) + ' ' + (Date.now() - t0) + ' ms');
    } catch (err) { bad++; console.log('XX ' + name + ' ' + err.message); }
  }));
  console.log(bad ? bad + ' problemów' : 'OK');
  process.exit(bad ? 1 : 0);
} else {
  console.log('użycie: list | wav <out> <ver> <id>... | check [ver]');
}
