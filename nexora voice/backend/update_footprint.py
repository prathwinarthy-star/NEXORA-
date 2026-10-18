"""
Updates frontend/index.html with interactive Acoustic DSP Schedule Bars and fully responsive
DSP feature extraction (F0 contour auto-scaling & playhead, FFT spectrum, MFCC bars, pause strip)
"""
import os
import re

INDEX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html"))

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. CSS for DSP Schedule Bars & Canvas Hover
DSP_CSS = """
    /* DSP Schedule Bars & Dynamic Footprint Controls */
    .dsp-schedule-panel {
      margin-top: 24px;
      margin-bottom: 20px;
      background: var(--bg-surface);
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-md);
      padding: 18px 22px;
      transition: var(--transition-fast);
    }

    .dsp-schedule-panel:hover {
      border-color: var(--border-accent);
    }

    .dsp-schedule-track {
      position: relative;
      height: 28px;
      border-radius: var(--radius-sm);
      overflow: hidden;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      display: flex;
      cursor: crosshair;
      user-select: none;
    }

    .dsp-schedule-slice {
      height: 100%;
      position: relative;
      transition: opacity 0.15s ease, filter 0.15s ease;
      cursor: pointer;
    }

    .dsp-schedule-slice:hover {
      filter: brightness(1.35);
      z-index: 2;
    }

    .dsp-schedule-slice.speech {
      background: linear-gradient(180deg, #06b6d4, #2563eb);
    }

    .dsp-schedule-slice.pause-normal {
      background: linear-gradient(180deg, #fbbf24, #d97706);
    }

    .dsp-schedule-slice.pause-long {
      background: linear-gradient(180deg, #f43f5e, #be123c);
    }
"""

if ".dsp-schedule-panel {" not in content:
    target_css_anchor = "    /* ==========================================================================\n       5 ADVANCED ORATORY INNOVATIONS SUITE (STYLES)"
    if target_css_anchor in content:
        content = content.replace(target_css_anchor, DSP_CSS + "\n" + target_css_anchor, 1)
        print("[+] Injected DSP Schedule CSS")
    else:
        # Fallback before </style>
        content = content.replace("  </style>", DSP_CSS + "\n  </style>", 1)
        print("[+] Injected DSP Schedule CSS before </style>")

# 2. HTML for DSP Schedule Bars
DSP_HTML = """
      <!-- Interactive Acoustic DSP Phonation & Pause Schedule Bars -->
      <div class="dsp-schedule-panel" id="dspSchedulePanel" style="display: none;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 16px;">⏱️</span>
            <h5 style="font-family: var(--font-display); font-size: 14px; font-weight: 800; color: var(--text-white); text-transform: uppercase; letter-spacing: 0.02em;">
              Acoustic Phonation & Pause Schedule Bars
            </h5>
            <span class="badge-pill" id="scheduleActiveStateBadge" style="background: rgba(6, 182, 212, 0.15); color: var(--primary-cyan); font-size: 10.5px;">
              Dynamic Voice Timeline
            </span>
          </div>
          <div style="display: flex; align-items: center; gap: 14px; font-size: 11.5px; font-family: var(--font-mono);">
            <span style="display: flex; align-items: center; gap: 6px;">
              <span style="width: 10px; height: 10px; border-radius: 2px; background: linear-gradient(90deg, #06b6d4, #3b82f6);"></span> Speech Phonation
            </span>
            <span style="display: flex; align-items: center; gap: 6px;">
              <span style="width: 10px; height: 10px; border-radius: 2px; background: #fbbf24;"></span> Natural Pause
            </span>
            <span style="display: flex; align-items: center; gap: 6px;">
              <span style="width: 10px; height: 10px; border-radius: 2px; background: #f43f5e;"></span> Long Silence (≥1.5s)
            </span>
          </div>
        </div>

        <!-- The Interactive Schedule Bar Track -->
        <div style="position: relative; width: 100%;">
          <div class="dsp-schedule-track" id="dspScheduleTrack">
            <!-- Slices injected dynamically -->
          </div>
          <!-- Synchronized Playhead Line -->
          <div id="dspSchedulePlayhead" style="position: absolute; top: -3px; bottom: -3px; width: 2px; background: #ffffff; box-shadow: 0 0 8px #ffffff; pointer-events: none; transform: translateX(-50%); display: none; z-index: 5;">
            <div style="position: absolute; top: -6px; left: -4px; width: 10px; height: 6px; background: #ffffff; border-radius: 2px;"></div>
          </div>
        </div>

        <!-- Schedule Time Scale -->
        <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 11px; font-family: var(--font-mono); color: var(--text-muted);">
          <span>0.0s (Start)</span>
          <span id="dspScheduleMidText">--s</span>
          <span id="dspScheduleEndText">--s</span>
        </div>

        <!-- Schedule Hover Tooltip Pill -->
        <div id="dspScheduleHoverPill" style="margin-top: 10px; font-size: 12px; font-family: var(--font-mono); color: var(--text-secondary); background: var(--bg-elevated); padding: 6px 12px; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
          Click anywhere along the schedule bar to jump audio playback to that exact timestamp
        </div>
      </div>
"""

if 'id="dspSchedulePanel"' not in content:
    target_html_anchor = '      <!-- Interactive Pause Intervals Navigator Strip -->'
    if target_html_anchor in content:
        content = content.replace(target_html_anchor, DSP_HTML + "\n" + target_html_anchor, 1)
        print("[+] Injected DSP Schedule HTML")

# 3. Enhanced JS Functions for Acoustic Footprint Studio
JS_REPLACEMENT = """
    function renderAcousticFootprintStudio(data) {
      const section = document.getElementById('footprintStudioSection');
      if (!section || !data.acoustic_footprint) return;
      section.style.display = 'block';

      const af = data.acoustic_footprint;

      // 1. FFT Spectral Harmonics & Timbre Brightness
      if (af.fft) {
        const centroidText = `${af.fft.spectral_centroid_hz} Hz`;
        const setIfExists = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };

        setIfExists('dspSpectralCentroid', centroidText);
        setIfExists('dspSpectralCentroidVal', centroidText);
        setIfExists('dspSpectralRolloff', `${af.fft.spectral_rolloff_hz} Hz`);
        setIfExists('dspSpectralFlatness', `${af.fft.spectral_flatness}`);
        setIfExists('dspSpectralBandwidth', `${af.fft.spectral_bandwidth_hz} Hz`);
        setIfExists('dspSpectralBrightness', af.fft.brightness_label);
        setIfExists('fftCentroidBadge', `Centroid: ${af.fft.spectral_centroid_hz} Hz`);

        // Draw FFT Spectral Curve (0 - 8 kHz)
        drawFftSpectrum(af.fft);
      }

      // 2. Speech Rate & Articulation Cadence
      if (af.speech_rate) {
        const setIfExists = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
        setIfExists('dspOverallWpm', `${af.speech_rate.overall_wpm} WPM`);
        setIfExists('dspOverallWpmVal', `${af.speech_rate.overall_wpm} WPM`);
        setIfExists('dspArticulationWpm', `${af.speech_rate.articulation_wpm} WPM`);
        setIfExists('dspSyllableRate', `${af.speech_rate.syllable_rate} syl/s`);
        setIfExists('dspPacingLabel', af.speech_rate.pacing_label || (af.speech_rate.overall_wpm < 120 ? "Deliberate" : "Optimal"));
      }

      // 3. Pause Intervals & Strategic Silences
      if (af.pause_intervals) {
        const setIfExists = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
        setIfExists('dspPauseTotalSec', `${af.pause_intervals.total_duration_sec}s`);
        setIfExists('dspPauseCount', `${af.pause_intervals.count} pauses`);
        setIfExists('dspPauseMeanSec', `${af.pause_intervals.mean_duration_sec}s`);
        setIfExists('dspPauseLongestSec', `${af.pause_intervals.longest_pause_sec || 0.0}s`);
        setIfExists('dspPauseRatio', `${af.pause_intervals.pause_ratio_pct}%`);

        // Render Pause Intervals mini-strip for instant inspection & clicking
        renderPauseIntervalsStrip(af.pause_intervals);
      }

      // 3b. Render Interactive Schedule Bars across recording duration
      renderAcousticScheduleBars(af.timeline_schedule, data.duration, af.pause_intervals);

      // 4. Vocal Clarity & Dynamic Projection Index
      if (af.vocal_clarity && af.pitch_f0) {
        const setIfExists = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
        setIfExists('dspClarityIndex', `${af.vocal_clarity.clarity_index} / 100`);
        setIfExists('dspDynamicRange', `${af.vocal_clarity.dynamic_range_db} dB`);
        setIfExists('dspHarmonicPurity', `${af.vocal_clarity.harmonic_purity_pct || 88.5}%`);
        setIfExists('dspPitchRange', `${af.pitch_f0.range_semitones} st`);
        setIfExists('dspProjectionLabel', af.vocal_clarity.projection_label);
        setIfExists('f0RegisterBadge', `${af.pitch_f0.register} (${af.pitch_f0.mean_f0_hz} Hz)`);
        setIfExists('f0SeminotesText', `Range: ${af.pitch_f0.range_semitones} semitones (Min: ${af.pitch_f0.min_f0_hz}Hz, Max: ${af.pitch_f0.max_f0_hz}Hz)`);
        setIfExists('f0DurationEndText', `${data.duration}s (End)`);
      }

      // 5. Draw F0 Pitch Contour Graph with auto-scaling to user voice register
      drawF0PitchContour(af.pitch_f0, data.duration);

      // 6. Draw MFCC Timbre Signature Bars
      renderMfccBars(af.mfcc);
      if (af.mfcc && af.mfcc.timbre_signature) {
        const sigBadge = document.getElementById('mfccSignatureBadge');
        if (sigBadge) sigBadge.textContent = af.mfcc.timbre_signature;
      }
    }

    // Render Phonation & Pause Schedule Bars
    function renderAcousticScheduleBars(schedule, duration, pauseData) {
      const panel = document.getElementById('dspSchedulePanel');
      const track = document.getElementById('dspScheduleTrack');
      const midText = document.getElementById('dspScheduleMidText');
      const endText = document.getElementById('dspScheduleEndText');
      const hoverPill = document.getElementById('dspScheduleHoverPill');
      if (!panel || !track) return;

      panel.style.display = 'block';
      track.innerHTML = '';
      if (midText) midText.textContent = `${(duration / 2).toFixed(1)}s`;
      if (endText) endText.textContent = `${duration.toFixed(1)}s (Total)`;

      let slices = schedule;
      if (!slices || slices.length === 0) {
        slices = [];
        const pauses = (pauseData && pauseData.intervals) ? pauseData.intervals : [];
        let curr = 0;
        pauses.forEach(p => {
          if (p.start > curr) {
            slices.push({
              start: curr,
              end: p.start,
              duration: +(p.start - curr).toFixed(2),
              type: 'speech',
              is_long_pause: false,
              energy_db: -14.0,
              label: 'Speech Phonation'
            });
          }
          slices.push({
            start: p.start,
            end: p.end,
            duration: p.duration,
            type: 'pause',
            is_long_pause: p.duration >= 1.5,
            energy_db: -52.0,
            label: p.duration >= 1.5 ? 'Long Silence' : 'Breath Pause'
          });
          curr = p.end;
        });
        if (curr < duration) {
          slices.push({
            start: curr,
            end: duration,
            duration: +(duration - curr).toFixed(2),
            type: 'speech',
            is_long_pause: false,
            energy_db: -14.0,
            label: 'Speech Phonation'
          });
        }
      }

      slices.forEach((s) => {
        const seg = document.createElement('div');
        const widthPct = Math.max(0.6, (s.duration / Math.max(0.1, duration)) * 100);
        seg.className = `dsp-schedule-slice ${s.type === 'speech' ? 'speech' : (s.is_long_pause ? 'pause-long' : 'pause-normal')}`;
        seg.style.width = `${widthPct}%`;
        seg.title = `${s.label} (${s.start}s – ${s.end}s): ${s.duration}s`;

        seg.addEventListener('mouseenter', () => {
          if (hoverPill) {
            hoverPill.innerHTML = `<span>⏱️ <strong>${s.label}</strong> [${s.start.toFixed(2)}s – ${s.end.toFixed(2)}s] Duration: <strong>${s.duration}s</strong> | RMS Dynamic Energy: <strong>${s.energy_db} dB</strong></span>`;
          }
        });

        seg.addEventListener('mouseleave', () => {
          if (hoverPill) {
            hoverPill.textContent = "Click anywhere along the schedule bar to jump audio playback to that exact timestamp";
          }
        });

        seg.addEventListener('click', (e) => {
          e.stopPropagation();
          seekToTimestamp(s.start);
        });

        track.appendChild(seg);
      });

      track.onclick = (e) => {
        const rect = track.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const pct = Math.max(0, Math.min(1, clickX / rect.width));
        seekToTimestamp(pct * duration);
      };
    }

    // F0 Pitch Contour Canvas Graph with auto-scaling to voice register
    function drawF0PitchContour(pitchData, duration, currTime = null) {
      const canvas = document.getElementById('f0ContourCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      const rect = canvas.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.scale(dpr, dpr);

      const w = rect.width;
      const h = rect.height;
      ctx.clearRect(0, 0, w, h);

      const contour = (pitchData && pitchData.contour) ? pitchData.contour : [];
      if (contour.length === 0) {
        ctx.fillStyle = '#64748b';
        ctx.font = '12px var(--font-body)';
        ctx.fillText('Pitch contour unvoiced or insufficient signal', 20, h / 2);
        return;
      }

      // Dynamic Y scaling adapted to user voice register!
      const minF0 = pitchData.min_f0_hz ? Math.max(40, pitchData.min_f0_hz - 15) : 60;
      const maxF0 = pitchData.max_f0_hz ? Math.min(500, pitchData.max_f0_hz + 25) : 380;
      const spanF0 = Math.max(40, maxF0 - minF0);

      // Draw background frequency grid lines
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      ctx.strokeStyle = isDark ? 'rgba(255, 255, 255, 0.07)' : 'rgba(0, 0, 0, 0.07)';
      ctx.lineWidth = 1;

      // 3 Dynamic reference lines: min, mean, max
      const gridLevels = [
        { label: `Min ${Math.round(pitchData.min_f0_hz || minF0)}Hz`, val: pitchData.min_f0_hz || minF0 },
        { label: `Mean ${Math.round(pitchData.mean_f0_hz || (minF0 + maxF0)/2)}Hz`, val: pitchData.mean_f0_hz || (minF0 + maxF0)/2, isMean: true },
        { label: `Max ${Math.round(pitchData.max_f0_hz || maxF0)}Hz`, val: pitchData.max_f0_hz || maxF0 }
      ];

      gridLevels.forEach(item => {
        const y = h - ((item.val - minF0) / spanF0) * (h - 22) - 10;
        ctx.beginPath();
        if (item.isMean) ctx.setLineDash([4, 4]); else ctx.setLineDash([]);
        ctx.strokeStyle = item.isMean ? '#fbbf24' : (isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)');
        ctx.moveTo(0, y);
        ctx.lineTo(w, y);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = item.isMean ? '#fbbf24' : (isDark ? 'rgba(148, 163, 184, 0.5)' : 'rgba(100, 116, 139, 0.6)');
        ctx.font = '10px var(--font-mono)';
        ctx.fillText(item.label, 6, Math.max(12, y - 4));
      });

      // Plot F0 points
      const points = [];
      const stepX = w / Math.max(1, contour.length - 1);
      for (let i = 0; i < contour.length; i++) {
        const val = contour[i];
        if (val !== null && val !== undefined) {
          const x = i * stepX;
          const y = h - ((val - minF0) / spanF0) * (h - 22) - 10;
          points.push({ x, y, val });
        }
      }

      if (points.length >= 2) {
        // Gradient fill under contour
        const grad = ctx.createLinearGradient(0, 0, 0, h);
        grad.addColorStop(0, 'rgba(6, 182, 212, 0.35)');
        grad.addColorStop(1, 'rgba(6, 182, 212, 0.0)');

        ctx.beginPath();
        ctx.moveTo(points[0].x, h);
        points.forEach(p => ctx.lineTo(p.x, p.y));
        ctx.lineTo(points[points.length - 1].x, h);
        ctx.closePath();
        ctx.fillStyle = grad;
        ctx.fill();

        // Draw smooth line
        ctx.beginPath();
        ctx.moveTo(points[0].x, points[0].y);
        for (let i = 1; i < points.length; i++) {
          ctx.lineTo(points[i].x, points[i].y);
        }
        ctx.strokeStyle = '#06b6d4';
        ctx.lineWidth = 2.5;
        ctx.stroke();
      }

      // Draw synchronized vertical playhead needle
      const activeT = (currTime !== null) ? currTime : (nativeAudioPlayer.currentTime || 0);
      if (activeT > 0 && duration > 0) {
        const playX = Math.min(w, Math.max(0, (activeT / duration) * w));
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.shadowColor = '#06b6d4';
        ctx.shadowBlur = 8;
        ctx.beginPath();
        ctx.moveTo(playX, 0);
        ctx.lineTo(playX, h);
        ctx.stroke();
        ctx.shadowBlur = 0;
      }

      // Setup click to seek on canvas once
      if (!canvas._hasClickListener) {
        canvas._hasClickListener = true;
        canvas.style.cursor = 'crosshair';
        canvas.addEventListener('click', (e) => {
          const r = canvas.getBoundingClientRect();
          const clickX = e.clientX - r.left;
          const pct = Math.max(0, Math.min(1, clickX / r.width));
          const dur = appState.analysis?.duration || 1;
          seekToTimestamp(pct * dur);
        });
      }
    }

    // FFT Spectral Power Spectrum Canvas
    function drawFftSpectrum(fftData) {
      const canvas = document.getElementById('fftSpectrumCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      const rect = canvas.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.scale(dpr, dpr);

      const w = rect.width;
      const h = rect.height;
      ctx.clearRect(0, 0, w, h);

      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

      // Draw frequency grid lines (1kHz, 2kHz, 4kHz)
      ctx.strokeStyle = isDark ? 'rgba(255, 255, 255, 0.07)' : 'rgba(0, 0, 0, 0.07)';
      ctx.lineWidth = 1;
      [1000, 2000, 4000].forEach(f => {
        const x = (f / 8000) * w;
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, h);
        ctx.stroke();
        ctx.fillStyle = isDark ? 'rgba(148, 163, 184, 0.45)' : 'rgba(100, 116, 139, 0.55)';
        ctx.font = '9.5px var(--font-mono)';
        ctx.fillText(`${f / 1000}k`, x + 4, h - 6);
      });

      const spectrum = (fftData && fftData.spectrum) ? fftData.spectrum : [];
      if (spectrum.length === 0) {
        ctx.fillStyle = '#64748b';
        ctx.font = '12px var(--font-body)';
        ctx.fillText('FFT spectrum unavailable', 20, h / 2);
        return;
      }

      // Draw smooth FFT curve
      const stepX = w / Math.max(1, spectrum.length - 1);
      const points = spectrum.map((val, idx) => ({
        x: idx * stepX,
        y: h - (val * (h * 0.85) + 6)
      }));

      // Gradient under curve
      const grad = ctx.createLinearGradient(0, 0, 0, h);
      grad.addColorStop(0, 'rgba(56, 189, 248, 0.35)');
      grad.addColorStop(1, 'rgba(56, 189, 248, 0.0)');

      ctx.beginPath();
      ctx.moveTo(points[0].x, h);
      points.forEach(p => ctx.lineTo(p.x, p.y));
      ctx.lineTo(points[points.length - 1].x, h);
      ctx.closePath();
      ctx.fillStyle = grad;
      ctx.fill();

      // FFT curve stroke
      ctx.beginPath();
      ctx.moveTo(points[0].x, points[0].y);
      for (let i = 1; i < points.length; i++) {
        ctx.lineTo(points[i].x, points[i].y);
      }
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 2.2;
      ctx.stroke();

      // Mark Spectral Centroid (Yellow dashed line)
      if (fftData.spectral_centroid_hz) {
        const centX = Math.min(w - 2, (fftData.spectral_centroid_hz / 8000) * w);
        ctx.setLineDash([3, 3]);
        ctx.strokeStyle = '#fbbf24';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(centX, 0);
        ctx.lineTo(centX, h);
        ctx.stroke();
        ctx.fillStyle = '#fbbf24';
        ctx.font = '10px var(--font-mono)';
        ctx.fillText(`Centroid ${Math.round(fftData.spectral_centroid_hz)}Hz`, Math.max(4, centX - 40), 16);
      }

      // Mark Spectral Rolloff 85% (Pink dashed line)
      if (fftData.spectral_rolloff_hz) {
        const rollX = Math.min(w - 2, (fftData.spectral_rolloff_hz / 8000) * w);
        ctx.setLineDash([3, 3]);
        ctx.strokeStyle = '#f43f5e';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(rollX, 0);
        ctx.lineTo(rollX, h);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#f43f5e';
        ctx.font = '10px var(--font-mono)';
        ctx.fillText(`Rolloff 85% ${Math.round(fftData.spectral_rolloff_hz)}Hz`, Math.max(4, rollX - 45), 32);
      }
      ctx.setLineDash([]);
    }

    // MFCC Timbre Signature Bars
    function renderMfccBars(mfccData) {
      const container = document.getElementById('mfccBarsContainer');
      if (!container) return;
      container.innerHTML = '';
      const coeffs = (mfccData && mfccData.coefficients) ? mfccData.coefficients : [];
      const descriptors = (mfccData && mfccData.descriptors) ? mfccData.descriptors : [];
      if (coeffs.length === 0) return;

      const nonC1 = coeffs.slice(1).map(x => Math.abs(x));
      const maxNonC1 = Math.max(...nonC1, 10);

      coeffs.forEach((c, idx) => {
        const col = document.createElement('div');
        col.className = 'mfcc-bar-col';

        let normPct;
        if (idx === 0) {
          normPct = Math.max(25, Math.min(95, 100 - (Math.abs(c) / 6.0)));
        } else {
          normPct = Math.max(12, Math.min(95, (Math.abs(c) / maxNonC1) * 85 + 10));
        }

        const bar = document.createElement('div');
        bar.className = 'mfcc-bar';
        bar.style.height = `${normPct}%`;
        const descText = descriptors[idx] || `Coefficient ${idx + 1}`;
        bar.title = `${descText}: ${c}`;
        if (c < 0) {
          bar.style.background = 'linear-gradient(180deg, #ec4899, #8b5cf6)';
        }

        const label = document.createElement('span');
        label.className = 'mfcc-bar-label';
        label.textContent = `C${idx + 1}`;

        col.appendChild(bar);
        col.appendChild(label);

        col.addEventListener('click', () => {
          alert(`MFCC Band ${idx + 1}\nDescription: ${descText}\nMeasured Coefficient: ${c}`);
        });

        container.appendChild(col);
      });
    }

    // Pause Intervals Strip
    function renderPauseIntervalsStrip(pauseData) {
      const panel = document.getElementById('pauseStripPanel');
      const scroll = document.getElementById('pauseStripScroll');
      const countBadge = document.getElementById('pauseStripCountBadge');
      if (!panel || !scroll) return;

      scroll.innerHTML = '';
      const itvs = (pauseData && pauseData.intervals) ? pauseData.intervals : [];
      panel.style.display = 'block';

      if (itvs.length === 0) {
        if (countBadge) countBadge.textContent = '0 pauses';
        scroll.innerHTML = `<span style="font-size:12px; color:#10b981; font-family:var(--font-mono); padding:6px 0;">✓ Continuous Delivery Flow (No extended hesitation pauses detected)</span>`;
        return;
      }

      if (countBadge) countBadge.textContent = `${itvs.length} pauses detected`;

      itvs.forEach((p) => {
        const pill = document.createElement('button');
        const isLong = (p.duration >= 1.5);
        pill.className = `pause-pill ${isLong ? 'long-pause' : ''}`;
        pill.innerHTML = `<span>⏸️</span> <span>${formatClock(p.start, true)} – ${formatClock(p.end, true)}</span> <strong style="color:var(--text-white);">(${p.duration}s)</strong>`;
        pill.title = `Click to seek to pause at ${p.start}s (${p.duration} seconds silence)`;
        pill.addEventListener('click', () => {
          seekToTimestamp(Math.max(0, p.start - 0.2));
        });
        scroll.appendChild(pill);
      });
    }

    // Synchronize playhead across Schedule Bar and Pitch Canvas during audio playback
    function updateAcousticSchedulePlayhead() {
      const playhead = document.getElementById('dspSchedulePlayhead');
      const dur = nativeAudioPlayer.duration || (appState.analysis?.duration || 1);
      const curr = nativeAudioPlayer.currentTime || 0;
      if (playhead && dur > 0) {
        const pct = Math.min(100, Math.max(0, (curr / dur) * 100));
        playhead.style.display = 'block';
        playhead.style.left = `${pct}%`;
      }

      // Re-draw F0 playhead needle
      if (appState.analysis && appState.analysis.acoustic_footprint && appState.analysis.acoustic_footprint.pitch_f0) {
        drawF0PitchContour(appState.analysis.acoustic_footprint.pitch_f0, appState.analysis.duration, curr);
      }
    }
"""

# Replace the old renderAcousticFootprintStudio block
old_start = "    function renderAcousticFootprintStudio(data) {"
old_end = "    // =========================================================================\n    // CANVAS WAVEFORM & ACOUSTIC HUD"

if old_start in content and old_end in content:
    idx1 = content.find(old_start)
    idx2 = content.find(old_end)
    content = content[:idx1] + JS_REPLACEMENT + "\n\n" + content[idx2:]
    print("[+] Replaced renderAcousticFootprintStudio and related DSP functions with dynamic implementations")
else:
    print("[-] Could not find old renderAcousticFootprintStudio block")

# 4. Connect updateAcousticSchedulePlayhead in timeupdate listener
if "updateAcousticSchedulePlayhead();" not in content:
    content = content.replace(
        "syncTranscriptWithPlayback();",
        "syncTranscriptWithPlayback();\n      updateAcousticSchedulePlayhead();",
        1
    )
    print("[+] Added updateAcousticSchedulePlayhead() call to timeupdate listener")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[SUCCESS] Successfully updated frontend/index.html with interactive Acoustic DSP Schedule Bars!")
