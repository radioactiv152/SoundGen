"""Test: "groźniejsze" i donośniejsze wersje dźwięków silników wyrenderowanych z generatora.

  node tools/render.js wav <we> v4 eng_petrol_idle eng_petrol_mid ...
  python3 tools/menace_engines.py <we> <wy> [poziom 0..1.5, domyślnie 1]

Każdy plik przechodzi przez:
  1. obniżenie o ~1,4 półtonu (resampling FFT: pętla zostaje okresowa, więc szew się nie psuje),
  2. więcej dołu (pompa wydechu 60-120 Hz) i szczekania wydechu ~1,7 kHz (donośność),
  3. charczenie: równoległe nasycenie pasma 120-1500 Hz,
  4. zagęszczenie: równoległa kompresja (niższy crest factor = donośniej przy tym samym szczycie),
  5. głośność: pętle +2,5 dB LUFS względem oryginału (zdarzenia +1,5 dB), limiter -1,5 dBFS.
Pętle (nazwa zawiera _idle/_mid/_high) są przetwarzane cyklicznie, bez szwu na końcu.
"""
import os, sys, glob, json, subprocess
import numpy as np
from scipy.signal import butter, sosfiltfilt, resample
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fit_engine_events import load, save, lufs, limit, SR


def peq(x, f0, db, q):
    """filtr szczytowy (RBJ), zerofazowy"""
    a = 10 ** (db / 40); w = 2 * np.pi * f0 / SR; al = np.sin(w) / (2 * q)
    b = [1 + al * a, -2 * np.cos(w), 1 - al * a]; d = [1 + al / a, -2 * np.cos(w), 1 - al / a]
    sos = np.array([[b[0] / d[0], b[1] / d[0], b[2] / d[0], 1, d[1] / d[0], d[2] / d[0]]])
    return sosfiltfilt(sos, x)


def env_follow(x, att, rel):
    g = np.abs(x); out = np.empty_like(g); a1 = np.exp(-1 / (att * SR)); r1 = np.exp(-1 / (rel * SR)); s = 0.0
    for i, v in enumerate(g):
        c = a1 if v > s else r1; s = c * s + (1 - c) * v; out[i] = s
    return out


def menace(x, amt, loop):
    # 1. niżej (resampling FFT jest okresowy: pętla po zmianie długości nadal domyka się bez szwu)
    x = resample(x, int(round(len(x) / (1 - 0.077 * amt))))
    n0 = len(x)
    if loop: x = np.tile(x, 3)                                      # cyklicznie: filtry i kompresor "widzą" pętlę z obu stron
    # 2. barwa
    x = peq(x, 75, 4.5 * amt, 0.9); x = peq(x, 240, 1.0 * amt, 1.0); x = peq(x, 1700, 3.0 * amt, 0.9)   # dół + szczekanie, które niesie się daleko
    x = sosfiltfilt(butter(2, 25, 'hp', fs=SR, output='sos'), x)
    # 3. charczenie
    band = sosfiltfilt(butter(2, [120, 1500], 'bp', fs=SR, output='sos'), x)
    rms = np.sqrt(np.mean(band ** 2)) + 1e-9
    grit = np.tanh(band / rms * 0.9) * rms
    grit = sosfiltfilt(butter(2, 2600, 'lp', fs=SR, output='sos'), grit)          # bez jasnego "piasku"
    x = x + grit * 0.55 * amt
    # 4. równoległa kompresja
    e = env_follow(x, 0.003, 0.12); thr = np.percentile(e, 60)
    g = np.minimum(1.0, (thr / np.maximum(e, 1e-9)) ** 0.75)
    x = x + x * g * 0.8 * amt
    if loop:
        x = x[n0:2 * n0]
    return x, n0


def main(src, dst, amt=1.0):
    os.makedirs(dst, exist_ok=True); rep = []
    for f in sorted(glob.glob(os.path.join(src, '*.wav'))):
        name = os.path.basename(f).replace('.v4.wav', '').replace('_1', '', 1) if f.endswith('_1.v4.wav') else os.path.basename(f)[:-4]
        loop = any(k in name for k in ('_idle', '_mid', '_high'))
        x = load(f); l0 = lufs(x)
        seam0 = 20 * np.log10(abs(x[0] - x[-1]) / (np.sqrt(np.mean(x ** 2)) + 1e-12) + 1e-12)
        y, _ = menace(x, amt, loop)
        tgt = l0 + (2.5 if loop else 1.5) * amt
        y = y * 10 ** ((tgt - lufs(y)) / 20)
        pre = np.abs(y).max()
        y = limit(y, 10 ** (-1.5 / 20))
        out = os.path.join(dst, name + '_grozny.wav'); save(out, y)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', out, '-c:a', 'libvorbis', '-q:a', '6', out[:-4] + '.ogg'], check=True)
        seam = 20 * np.log10(abs(y[0] - y[-1]) / (np.sqrt(np.mean(y ** 2)) + 1e-12) + 1e-12) if loop else None
        crest = lambda z: 20 * np.log10(np.abs(z).max() / np.sqrt(np.mean(z ** 2)))
        rep.append({'plik': name + '_grozny', 'petla': loop, 'lufs_przed': round(l0, 1), 'lufs_po': round(lufs(y), 1),
                    'crest_przed_db': round(crest(x), 1), 'crest_po_db': round(crest(y), 1),
                    'limiter_db': round(max(0, 20 * np.log10(pre / 10 ** (-1.5 / 20))), 1), 'szew_db_wzgl_rms': None if seam is None else [round(seam0, 1), round(seam, 1)]})
        print(json.dumps(rep[-1], ensure_ascii=False))
    json.dump(rep, open(os.path.join(dst, 'raport.json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 1.0)
