#!/usr/bin/env python3
"""Przycina nagrania odpalania i gaszenia silnika (np. z ElevenLabs) tak, żeby pasowały do pętli jałowego z generatora.

  node tools/render.js wav <pętle> v4 eng_petrol_idle eng_diesel_idle eng_small_idle eng_radial_idle eng_ww1_idle \
       eng_v8_petrol_idle eng_v8_diesel_idle eng_v12_petrol_idle eng_v12_diesel_idle
  python3 tools/fit_engine_events.py <katalog_wejściowy> <katalog_wyjściowy> <pętle>

Dla każdego pliku (wav/mp3/ogg):
  1. mono 44,1 kHz, usunięcie składowej stałej i ciszy na początku,
  2. rozpoznanie: odpalanie (głośny początek, potem równy jałowy) albo gaszenie (jałowy, potem spadek),
  3. przypisanie do konkretnej pętli: paliwo z nazwy pliku, tempo zapłonów i barwa jałowego,
  4. odpalanie: od początku do ~1 s po ustabilizowaniu się jałowego + wyciszenie 0,35 s (przejście w pętlę);
     gaszenie: od 0,7 s przed gaśnięciem (wejście 0,25 s, przejście z pętli) do zgaśnięcia,
  5. korekcja barwy jałowego do pętli (krzywa 1/3 oktawy, wygładzona, maks. ±6 dB, filtr liniowofazowy),
  6. głośność jałowego = głośność pętli (LUFS wg BS.1770), szczyt ≤ −1,5 dBFS (łagodny limiter),
  7. zapis WAV 16-bit i OGG.
"""
import os, sys, glob, json, subprocess, wave
import numpy as np
from scipy.signal import sosfilt, butter, lfilter

SR = 44100


def load(path):
    out = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype=np.int16).astype(np.float64) / 32768


def save(path, x):
    w = wave.open(path, 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()


def kweight(x):
    # BS.1770: półka wysokich + górnoprzepustowy (współczynniki dla 44,1 kHz wyliczone jak w generatorze)
    G, Q, fc = 3.999843853973347, 0.7071752369554196, 1681.974450955533
    A = 10 ** (G / 40); w0 = 2 * np.pi * fc / SR; al = np.sin(w0) / (2 * Q); c = np.cos(w0); sA = np.sqrt(A)
    b = [A * ((A + 1) + (A - 1) * c + 2 * sA * al), -2 * A * ((A - 1) + (A + 1) * c), A * ((A + 1) + (A - 1) * c - 2 * sA * al)]
    a = [(A + 1) - (A - 1) * c + 2 * sA * al, 2 * ((A - 1) - (A + 1) * c), (A + 1) - (A - 1) * c - 2 * sA * al]
    y = lfilter(np.array(b) / a[0], np.array(a) / a[0], x)
    Q2, fc2 = 0.5003270373238773, 38.13547087602444; w0 = 2 * np.pi * fc2 / SR; al = np.sin(w0) / (2 * Q2); c = np.cos(w0)
    b = [(1 + c) / 2, -(1 + c), (1 + c) / 2]; a = [1 + al, -2 * c, 1 - al]
    return lfilter(np.array(b) / a[0], np.array(a) / a[0], y)


def lufs(x):
    k = kweight(x); return -0.691 + 10 * np.log10(np.mean(k * k) + 1e-12)


def env_db(x, win=0.05):
    h = int(win * SR); k = len(x) // h
    return 20 * np.log10(np.sqrt((x[:k * h].reshape(k, h) ** 2).mean(1)) + 1e-9), win


BANDS = np.geomspace(31.5, 16000, 28)


def band_spec(x):
    n = 1 << int(np.ceil(np.log2(len(x))))
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)), n)) ** 2; f = np.fft.rfftfreq(n, 1 / SR)
    return np.array([10 * np.log10(X[(f >= b / 2 ** (1 / 6)) & (f < b * 2 ** (1 / 6))].mean() + 1e-20) for b in BANDS])


def firing_hz(x):
    """tempo zapłonów na jałowym: najsilniejszy rytm obwiedni 20-75 Hz; gdy rytm cyklu (10-20 Hz) dominuje - jego podwojenie"""
    from scipy.signal import sosfiltfilt
    e = np.abs(sosfiltfilt(butter(4, [60, 2500], 'bp', fs=SR, output='sos'), x)); e = sosfiltfilt(butter(4, 200, 'lp', fs=SR, output='sos'), e); e -= e.mean()
    n = 1 << (int(np.ceil(np.log2(len(e)))) + 1); E = np.abs(np.fft.rfft(e * np.hanning(len(e)), n)); f = np.fft.rfftfreq(n, 1 / SR)
    lo = (f >= 10) & (f < 20); hi = (f >= 20) & (f < 75)
    fl, El = f[lo][np.argmax(E[lo])], E[lo].max(); fh, Eh = f[hi][np.argmax(E[hi])], E[hi].max()
    return 2 * fl if (El > Eh and abs(2 * fl - fh) / fh > 0.12 and 2 * fl < 75) else fh


def eq_match(x, src_seg, ref, maxdb=4.0):
    d = band_spec(ref) - band_spec(src_seg); d -= np.median(d)           # tylko kształt; poziom osobno
    d = np.convolve(np.pad(d, 2, mode='edge'), np.ones(5) / 5, 'valid')   # wygładzenie
    d = np.clip(d, -maxdb, maxdb)
    n = 4096; f = np.fft.rfftfreq(n, 1 / SR)
    g = 10 ** (np.interp(np.log(np.maximum(f, 20)), np.log(BANDS), d) / 20)
    h = np.fft.irfft(g, n); h = np.roll(h, n // 2) * np.hanning(n)        # liniowofazowy FIR
    y = np.convolve(x, h)[n // 2: n // 2 + len(x)]
    return y, d


def limit(x, thr):
    a = np.abs(x); g = np.minimum(1, thr / (a + 1e-12)); L = int(0.006 * SR) | 1
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    gs = np.minimum(uniform_filter1d(minimum_filter1d(g, L), L), g)
    return x * gs


def compress(x, thr_db=-7.0, ratio=2.0, att=0.004, rel=0.18):
    """łagodny kompresor (śledzenie szczytu: szybki atak, wolne puszczanie) - przegazowanie zostaje głośne, ale nie "zduszone" """
    thr = 10 ** (thr_db / 20); a1 = np.exp(-1 / (att * SR)); r1 = np.exp(-1 / (rel * SR))
    env = np.empty(len(x)); e = 0.0; ax = np.abs(x)
    for i in range(len(x)):
        v = ax[i]; e = a1 * e + (1 - a1) * v if v > e else r1 * e + (1 - r1) * v; env[i] = e
    g = np.ones(len(x)); m = env > thr
    g[m] = (thr * (env[m] / thr) ** (1 / ratio)) / env[m]
    return x * g


def fade(n, a, b):
    t = np.arange(n) / SR; e = np.ones(n)
    if a > 0: e *= 0.5 - 0.5 * np.cos(np.pi * np.clip(t / a, 0, 1))
    if b > 0: e *= 0.5 + 0.5 * np.cos(np.pi * np.clip((t - (t[-1] - b)) / b, 0, 1))
    return e


PETROL = ('petrol', 'v8_petrol', 'v12_petrol', 'small', 'radial', 'ww1')
DIESEL = ('diesel', 'v8_diesel', 'v12_diesel')


def main(src, dst, refdir):
    """refdir: katalog z pętlami jałowego z generatora, np. eng_v8_petrol_idle_1.v4.wav (node tools/render.js wav <dir> v4 eng_*_idle)"""
    os.makedirs(dst, exist_ok=True)
    refs = {}
    for pth in sorted(glob.glob(os.path.join(refdir, 'eng_*_idle*.wav'))):
        k = os.path.basename(pth).split('_idle')[0][4:]
        if k != 'turbine': refs[k] = load(pth)
    ref_fire = {k: firing_hz(v) for k, v in refs.items()}
    ref_lufs = {k: lufs(v) for k, v in refs.items()}
    files = sorted(f for f in glob.glob(os.path.join(src, '*')) if f.lower().endswith(('.wav', '.mp3', '.ogg', '.flac')))
    report, cnt = [], {}
    for f in files:
        x = load(f); x = x - x.mean()
        x = sosfilt(butter(2, 20, 'hp', fs=SR, output='sos'), x)
        pk = np.abs(x).max(); i0 = int(np.argmax(np.abs(x) > pk * 10 ** (-45 / 20))); x = x[max(0, i0 - int(0.002 * SR)):]
        e, w = env_db(x)
        # koniec "prawdziwego" dźwięku: przed automatycznym wyciszeniem ElevenLabs
        idle_lvl = np.median(e[len(e) // 3: int(len(e) * 0.8)])
        first = e[:int(2.0 / w)].max(); kind = 'start' if first > idle_lvl + 4 else 'stop'   # rozruch/zaskoczenie wyraźnie głośniejsze od jałowego
        if kind == 'start':
            imax = int(np.argmax(e[:int(2.5 / w)]))
            settle = None
            for i in range(imax, len(e) - int(0.6 / w)):
                if np.all(np.abs(e[i:i + int(0.6 / w)] - idle_lvl) < 2.5): settle = i; break
            settle = settle if settle is not None else imax + int(0.5 / w)
            t_end = min(len(x) / SR, (settle * w) + 1.0 + 0.35)
            seg = x[:int(t_end * SR)]
            ia, ib = int(settle * w * SR), min(len(seg), int((settle * w + 1.0) * SR))
            # rozrusznik ciszej niż praca silnika: kręcenie do chwili zaskoczenia ~8 dB pod jałowym, potem wyraźny skok
            lo_i = int(0.3 / w); imax2 = lo_i + int(np.argmax(e[lo_i:max(lo_i + 1, settle)])) if settle > lo_i else imax
            tc = max(0.25, imax2 * w - 0.12)
            crank_db = 10 * np.log10(np.mean(seg[:int(tc * SR)] ** 2) + 1e-12)
            gdb = min(0.0, (idle_lvl - 8) - crank_db)
            t = np.arange(len(seg)) / SR
            cg = 10 ** (np.interp(t, [0, max(0.0, tc - 0.12), tc, t[-1] + 1], [gdb, gdb, 0, 0]) / 20)
            seg = seg * cg
            env = fade(len(seg), 0.005, 0.35)
        else:
            stop = None
            for i in range(int(0.5 / w), len(e) - int(0.2 / w)):
                if np.all(e[i:i + int(0.2 / w)] < idle_lvl - 3): stop = i; break
            stop = stop if stop is not None else int(len(e) * 0.7)
            t0 = max(0, stop * w - 0.7)
            # koniec: gdzie obwiednia spada 40 dB pod jałowy (albo koniec pliku)
            tail = np.where(e[stop:] < idle_lvl - 40)[0]; t1 = (stop + (tail[0] if len(tail) else len(e) - stop)) * w
            seg = x[int(t0 * SR): int(min(t1 + 0.05, len(x) / SR) * SR)]
            ia, ib = 0, int((stop * w - t0) * SR)
            env = fade(len(seg), 0.25, 0.03)
        # przypisanie do pętli: bliższa barwa jałowego (kształt widma)
        idle = seg[ia:ib]
        sp = band_spec(idle); sp -= np.median(sp)
        dist = {k: np.mean(np.abs((band_spec(v) - np.median(band_spec(v))) - sp)) for k, v in refs.items()}
        low = os.path.basename(f).lower()
        if 'dies' in low: cand = DIESEL                                           # nazwa pliku z ElevenLabs = początek promptu
        elif 'petr' in low or 'benz' in low: cand = PETROL
        elif 'v8' in low: cand = ('petrol', 'v8_petrol', 'v8_diesel')
        else: cand = tuple(refs)
        fh = firing_hz(idle)
        score = {k: abs(np.log2(fh / ref_fire[k])) * 12 + 0.5 * dist[k] for k in cand if k in refs}   # tempo zapłonów + barwa
        typ = min(score, key=score.get)
        y, curve = eq_match(seg, idle, refs[typ])
        # głośność: jałowy jak w pętli
        idle_eq = y[ia:ib]
        gain = 10 ** ((ref_lufs[typ] - lufs(idle_eq)) / 20)
        pre = np.abs(y * gain).max()
        y = limit(compress(y * gain), 10 ** (-1.5 / 20)) * env
        key = kind + '_' + typ; cnt[key] = cnt.get(key, 0) + 1
        name = 'eng_%s_%s_%d' % (kind, typ, cnt[key])
        save(os.path.join(dst, name + '.wav'), y)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', os.path.join(dst, name + '.wav'), '-c:a', 'libvorbis', '-q:a', '6', os.path.join(dst, name + '.ogg')], check=True)
        report.append({'plik': name, 'zrodlo': os.path.basename(f), 'rodzaj': kind, 'petla': 'eng_' + typ + '_idle', 'tempo_zaplonow_hz': round(float(fh), 1), 'tempo_petli_hz': round(float(ref_fire[typ]), 1), 'dlugosc_s': round(len(y) / SR, 2),
                       'jalowy_od_s': round(settle * w, 2) if kind == 'start' else 0.0, 'gaszenie_od_s': round(0.7, 2) if kind == 'stop' else None,
                       'lufs_jalowego': round(lufs(idle_eq * gain), 1), 'lufs_petli': round(ref_lufs[typ], 1),
                       'szczyt_db': round(20 * np.log10(np.abs(y).max() + 1e-12), 1), 'limiter_db': round(max(0.0, 20 * np.log10(pre / 10 ** (-1.5 / 20))), 1), 'korekcja_db_min_max': [round(float(curve.min()), 1), round(float(curve.max()), 1)]})
        print(json.dumps(report[-1], ensure_ascii=False))
    json.dump(report, open(os.path.join(dst, 'raport.json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main(*sys.argv[1:4])
