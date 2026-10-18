"""
Helper script to inject the 5 Advanced Oratory Innovations Suite into frontend/index.html
"""
import os
import re

INDEX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html"))

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. CSS STYLES TO INJECT INTO <style>
CSS_INJECTION = """
    /* ==========================================================================
       5 ADVANCED ORATORY INNOVATIONS SUITE (STYLES)
       ========================================================================== */
    .innovations-suite-section {
      margin-top: 38px;
      margin-bottom: 40px;
      background: var(--bg-glass);
      backdrop-filter: var(--glass-blur);
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-xl);
      padding: 32px;
      box-shadow: var(--shadow-surface);
      position: relative;
      overflow: hidden;
    }

    .inno-hero-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 24px;
      padding-bottom: 18px;
      border-bottom: 1px solid var(--border-subtle);
      flex-wrap: wrap;
      gap: 14px;
    }

    .inno-title-cluster h3 {
      font-family: var(--font-display);
      font-size: 22px;
      font-weight: 800;
      color: var(--text-white);
      display: flex;
      align-items: center;
      gap: 10px;
      letter-spacing: -0.01em;
    }

    .inno-title-cluster p {
      font-size: 13.5px;
      color: var(--text-secondary);
      margin-top: 4px;
      max-width: 860px;
      line-height: 1.5;
    }

    .inno-nav-tabs {
      display: flex;
      gap: 8px;
      background: var(--bg-surface);
      padding: 6px;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-subtle);
      margin-bottom: 26px;
      overflow-x: auto;
      scrollbar-width: thin;
    }

    .inno-tab-btn {
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 700;
      padding: 10px 18px;
      border-radius: var(--radius-sm);
      border: 1px solid transparent;
      background: transparent;
      color: var(--text-secondary);
      cursor: pointer;
      white-space: nowrap;
      transition: var(--transition-fast);
      display: flex;
      align-items: center;
      gap: 8px;
      user-select: none;
    }

    .inno-tab-btn:hover {
      color: var(--text-white);
      background: var(--bg-elevated);
    }

    .inno-tab-btn.active {
      background: var(--primary-gradient);
      color: #ffffff;
      border-color: rgba(255, 255, 255, 0.2);
      box-shadow: 0 4px 14px var(--glow-cyan);
    }

    .inno-tab-panel {
      display: none;
      animation: fadeInTab 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    .inno-tab-panel.active {
      display: block;
    }

    @keyframes fadeInTab {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Innovation 1: Severity Spectrum */
    .spectrum-bar-wrap {
      background: var(--bg-surface);
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-md);
      padding: 20px 24px;
      margin-bottom: 24px;
    }

    .spectrum-bar-track {
      height: 16px;
      border-radius: 99px;
      overflow: hidden;
      display: flex;
      margin: 14px 0 16px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
    }

    .spectrum-seg {
      height: 100%;
      transition: width 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .spectrum-legend {
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
      font-size: 12px;
    }

    .spectrum-legend-item {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .spectrum-legend-dot {
      width: 11px;
      height: 11px;
      border-radius: 50%;
    }

    .calib-rubric-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
      gap: 16px;
      margin-top: 18px;
    }

    .calib-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 16px 18px;
      transition: var(--transition-fast);
    }

    .calib-card:hover {
      border-color: var(--border-accent);
      transform: translateY(-2px);
      box-shadow: 0 8px 20px -6px rgba(0,0,0,0.4);
    }

    .calib-card-title {
      font-family: var(--font-display);
      font-weight: 700;
      font-size: 14px;
      color: var(--text-white);
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }

    .calib-card-rationale {
      font-size: 11.5px;
      color: var(--text-secondary);
      line-height: 1.45;
      margin-bottom: 12px;
    }

    .calib-levels-mini {
      display: flex;
      flex-direction: column;
      gap: 5px;
      font-size: 11px;
      font-family: var(--font-mono);
    }

    .calib-lvl-row {
      display: flex;
      justify-content: space-between;
      padding: 4px 8px;
      border-radius: 4px;
      background: var(--bg-elevated);
      align-items: center;
    }

    .calib-lvl-row.lvl-0 { border-left: 3px solid #10b981; }
    .calib-lvl-row.lvl-1 { border-left: 3px solid #38bdf8; }
    .calib-lvl-row.lvl-2 { border-left: 3px solid #fbbf24; }
    .calib-lvl-row.lvl-3 { border-left: 3px solid #f43f5e; }

    /* Innovation 2: Same Text Contrastive */
    .contrast-header-banner {
      background: linear-gradient(135deg, rgba(6, 182, 212, 0.12), rgba(59, 130, 246, 0.08));
      border: 1px solid rgba(6, 182, 212, 0.35);
      border-radius: var(--radius-md);
      padding: 20px;
      margin-bottom: 22px;
    }

    .norm-factors-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      margin: 18px 0;
    }

    .norm-factor-pill {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 12px 14px;
      font-size: 12px;
      line-height: 1.45;
    }

    .norm-factor-pill h5 {
      font-family: var(--font-display);
      font-weight: 700;
      color: var(--primary-cyan);
      margin-bottom: 5px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .contrast-metrics-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 14px;
      margin-bottom: 22px;
    }

    .contrast-metric-tile {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 16px;
      transition: var(--transition-fast);
    }

    .contrast-metric-tile:hover {
      border-color: var(--border-accent);
    }

    .contrast-tile-title {
      font-size: 12px;
      color: var(--text-secondary);
      margin-bottom: 6px;
    }

    .contrast-tile-main {
      font-family: var(--font-mono);
      font-size: 18px;
      font-weight: 800;
      color: var(--text-white);
      display: flex;
      align-items: baseline;
      gap: 8px;
    }

    .contrast-tile-sub {
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 4px;
      font-family: var(--font-mono);
    }

    .phrase-contrast-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12.5px;
      margin-top: 14px;
      border-radius: var(--radius-sm);
      overflow: hidden;
    }

    .phrase-contrast-table th {
      text-align: left;
      padding: 10px 14px;
      background: var(--bg-elevated);
      color: var(--text-secondary);
      font-family: var(--font-mono);
      font-size: 11px;
      border-bottom: 1px solid var(--border-medium);
    }

    .phrase-contrast-table td {
      padding: 12px 14px;
      border-bottom: 1px solid var(--border-subtle);
      background: var(--bg-surface);
    }

    /* Innovation 3: Rhetorical Emphasis */
    .showcase-persuasive-box {
      background: radial-gradient(circle at 10% 10%, rgba(99, 102, 241, 0.15), transparent 60%), var(--bg-surface);
      border: 1px solid rgba(99, 102, 241, 0.4);
      border-radius: var(--radius-lg);
      padding: 24px;
      margin-bottom: 26px;
    }

    .showcase-btns-row {
      display: flex;
      gap: 10px;
      margin: 14px 0;
      flex-wrap: wrap;
    }

    .btn-showcase-toggle {
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 700;
      padding: 9px 18px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-medium);
      background: var(--bg-elevated);
      color: var(--text-primary);
      cursor: pointer;
      transition: var(--transition-fast);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .btn-showcase-toggle.active {
      background: var(--primary-gradient);
      color: #ffffff;
      border-color: transparent;
      box-shadow: 0 4px 14px var(--glow-blue);
    }

    .focal-eval-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
      gap: 14px;
      margin-top: 18px;
    }

    .focal-eval-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 16px;
      transition: var(--transition-fast);
    }

    .focal-eval-card:hover {
      border-color: var(--primary-cyan);
      transform: translateY(-2px);
      box-shadow: 0 6px 20px -6px rgba(0,0,0,0.4);
    }

    .focal-card-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }

    .focal-word-badge {
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 800;
      color: #ffffff;
      background: rgba(6, 182, 212, 0.15);
      border: 1px solid rgba(6, 182, 212, 0.4);
      padding: 3px 10px;
      border-radius: var(--radius-sm);
    }

    .focal-metrics-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 11.5px;
      color: var(--text-secondary);
    }

    .focal-metrics-list span strong {
      color: var(--text-primary);
      font-family: var(--font-mono);
    }

    /* Innovation 4: Judge Consistency */
    .judge-philosophy-callout {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.12), rgba(244, 63, 94, 0.08));
      border: 1px solid rgba(245, 158, 11, 0.4);
      border-radius: var(--radius-md);
      padding: 18px 22px;
      margin-bottom: 22px;
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .judge-panel-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-bottom: 22px;
    }

    .judge-panel-tile {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 16px;
      text-align: center;
      transition: var(--transition-fast);
    }

    .judge-panel-tile.ai {
      border-color: var(--primary-cyan);
      background: rgba(6, 182, 212, 0.08);
      box-shadow: 0 0 15px rgba(6, 182, 212, 0.15);
    }

    .discrepancy-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      margin-top: 14px;
      border-radius: var(--radius-sm);
      overflow: hidden;
    }

    .discrepancy-table th {
      padding: 10px 12px;
      background: var(--bg-elevated);
      color: var(--text-secondary);
      font-family: var(--font-mono);
      text-align: left;
      border-bottom: 1px solid var(--border-medium);
    }

    .discrepancy-table td {
      padding: 12px;
      border-bottom: 1px solid var(--border-subtle);
      background: var(--bg-surface);
    }

    /* Innovation 5: Personalized Practice */
    .drills-stack {
      display: flex;
      flex-direction: column;
      gap: 16px;
      margin-bottom: 26px;
    }

    .drill-prescription-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-md);
      padding: 22px;
      position: relative;
      transition: var(--transition-fast);
    }

    .drill-prescription-card:hover {
      border-color: var(--border-accent);
      box-shadow: 0 10px 28px -6px rgba(0,0,0,0.4);
      transform: translateY(-2px);
    }

    .drill-prescription-card.p1 {
      border-left: 5px solid var(--sev-serious);
    }

    .drill-prescription-card.p2 {
      border-left: 5px solid var(--sev-moderate);
    }

    .drill-prescription-card.p3 {
      border-left: 5px solid var(--sev-minor);
    }

    .drill-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      flex-wrap: wrap;
      gap: 8px;
    }

    .drill-instructions-box {
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 14px 18px;
      margin: 12px 0;
      font-size: 13px;
      line-height: 1.55;
      color: var(--text-primary);
    }

    .roadmap-steps-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      margin-top: 16px;
    }

    .roadmap-step-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 16px;
    }

    @media (max-width: 900px) {
      .norm-factors-row, .judge-panel-grid, .roadmap-steps-row {
        grid-template-columns: 1fr;
      }
    }
"""

# 2. HTML MARKUP FOR INNOVATIONS SUITE
HTML_INJECTION = """
    <!-- =========================================================================
         5 ADVANCED ORATORY INNOVATIONS SUITE (AT DASHBOARD END)
         ========================================================================= -->
    <div class="innovations-suite-section" id="innovationsSuiteSection" style="display: none;">
      <!-- Hero Section Header -->
      <div class="inno-hero-header">
        <div class="inno-title-cluster">
          <h3>
            <span>🌟</span> <span>5 Oratory Innovations & Objective Speech Analytics</span>
          </h3>
          <p>
            Grounded in calibrated acoustic rubrics, reference normalization, persuasive rhetorical emphasis detection, multi-judge consistency tracking, and participant-specific rehearsal prescriptions.
          </p>
        </div>
        <span class="badge-pill" style="background: rgba(99, 102, 241, 0.15); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.4); font-size: 11.5px; padding: 4px 12px;">
          Advanced Oratory Intelligence
        </span>
      </div>

      <!-- Innovations Navigation Tabs -->
      <div class="inno-nav-tabs" id="innoNavTabs">
        <button class="inno-tab-btn active" data-tab="severity">
          <span>📊</span> <span>1. Severity Grading</span>
        </button>
        <button class="inno-tab-btn" data-tab="contrast">
          <span>⚖️</span> <span>2. Same-Text Contrast</span>
        </button>
        <button class="inno-tab-btn" data-tab="rhetorical">
          <span>🎯</span> <span>3. Rhetorical Emphasis</span>
        </button>
        <button class="inno-tab-btn" data-tab="consistency">
          <span>👥</span> <span>4. Judge Consistency</span>
        </button>
        <button class="inno-tab-btn" data-tab="practice">
          <span>⚡</span> <span>5. Personalized Drills</span>
        </button>
      </div>

      <!-- TAB 1: SEVERITY GRADING SPECTRUM -->
      <div class="inno-tab-panel active" id="innoTabSeverity">
        <div class="spectrum-bar-wrap">
          <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 8px;">
            <h4 style="font-family: var(--font-display); font-size: 16px; font-weight: 800; color: var(--text-white);">
              Delivery Flaw Spectrum & Calibrated Severity Distribution
            </h4>
            <span id="spectrumOptimalRatio" style="font-family: var(--font-mono); font-size: 13px; font-weight: 700; color: #10b981;">
              Level 0 (No Significant Deviation): --%
            </span>
          </div>
          <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 4px;">
            Instead of classifying flaws as merely present or absent, each moment is graded across 4 distinct levels calibrated against human-reviewed oratorical benchmarks.
          </p>

          <!-- Segmented Progress Bar -->
          <div class="spectrum-bar-track" id="spectrumBarTrack">
            <div class="spectrum-seg" id="segLvl0" style="width: 50%; background: #10b981;" title="Level 0: No significant deviation detected"></div>
            <div class="spectrum-seg" id="segLvl1" style="width: 20%; background: #38bdf8;" title="Level 1: Minor deviation"></div>
            <div class="spectrum-seg" id="segLvl2" style="width: 15%; background: #fbbf24;" title="Level 2: Moderate deviation"></div>
            <div class="spectrum-seg" id="segLvl3" style="width: 15%; background: #f43f5e;" title="Level 3: Major deviation"></div>
          </div>

          <!-- Spectrum Legend -->
          <div class="spectrum-legend">
            <div class="spectrum-legend-item">
              <span class="spectrum-legend-dot" style="background: #10b981;"></span>
              <span><strong>Level 0:</strong> No significant deviation detected (<span id="countLvl0">--</span>)</span>
            </div>
            <div class="spectrum-legend-item">
              <span class="spectrum-legend-dot" style="background: #38bdf8;"></span>
              <span><strong>Level 1:</strong> Minor deviation (<span id="countLvl1">--</span>)</span>
            </div>
            <div class="spectrum-legend-item">
              <span class="spectrum-legend-dot" style="background: #fbbf24;"></span>
              <span><strong>Level 2:</strong> Moderate deviation (<span id="countLvl2">--</span>)</span>
            </div>
            <div class="spectrum-legend-item">
              <span class="spectrum-legend-dot" style="background: #f43f5e;"></span>
              <span><strong>Level 3:</strong> Major deviation (<span id="countLvl3">--</span>)</span>
            </div>
          </div>
        </div>

        <!-- Rubric-Specific Calibrated Thresholds Matrix -->
        <h5 style="font-family: var(--font-display); font-size: 14.5px; font-weight: 800; color: var(--text-white); margin-top: 24px;">
          Calibrated Human-Reviewed Threshold Rubrics (8 Delivery Dimensions)
        </h5>
        <div class="calib-rubric-grid" id="calibRubricGrid">
          <!-- Injected dynamically -->
        </div>

        <!-- Classified Flaws Breakdown in User Speech -->
        <h5 style="font-family: var(--font-display); font-size: 14.5px; font-weight: 800; color: var(--text-white); margin-top: 28px; margin-bottom: 12px;">
          Classified Flaw Instances in This Speech Recording (<span id="classifiedIssuesCount">0</span>)
        </h5>
        <div class="issues-container" id="classifiedIssuesList" style="max-height: 420px; overflow-y: auto;">
          <!-- Injected dynamically -->
        </div>
      </div>

      <!-- TAB 2: SAME-TEXT CONTRASTIVE COMPARISON -->
      <div class="inno-tab-panel" id="innoTabContrast">
        <div class="contrast-header-banner">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
              <span class="badge-pill" style="background: rgba(6, 182, 212, 0.2); color: var(--primary-cyan); font-size: 11px;">Reference Passage Benchmark</span>
              <h4 style="font-family: var(--font-display); font-size: 17px; font-weight: 800; color: var(--text-white); margin-top: 6px;" id="refPassageTitle">
                Deliberate Communication Keynote (Standard Benchmark)
              </h4>
            </div>
            <div style="text-align: right;">
              <span style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-family: var(--font-mono);">Alignment Index</span>
              <div style="font-family: var(--font-mono); font-size: 24px; font-weight: 800; color: #10b981;" id="contrastAlignmentIdx">--%</div>
              <span id="contrastAlignmentLabel" style="font-size: 11px; color: var(--text-secondary);">Cadence Alignment</span>
            </div>
          </div>
          <p style="font-size: 12.5px; color: var(--text-secondary); margin-top: 10px; line-height: 1.45;" id="refPassageSnippet">
            "Good morning esteemed judges and guests. Today I stand before you to explore the transformative power of deliberate communication..."
          </p>
        </div>

        <!-- Normalization Engine Indicators -->
        <div class="norm-factors-row">
          <div class="norm-factor-pill">
            <h5><span>👤</span> <span>Speaker Identity Normalization</span></h5>
            <p style="color: var(--text-secondary);">Transposed fundamental frequency (F0) into semitone delta relative to median pitch. Bass and soprano vocal registers are compared fairly without pitch bias.</p>
          </div>
          <div class="norm-factor-pill">
            <h5><span>🎙️</span> <span>Acoustic Room & Mic Normalization</span></h5>
            <p style="color: var(--text-secondary);">Normalized RMS dynamic range (z-score dB dynamic range) and noise floor decoupling. Removes microphone distance, preamp gain, and room reverberation discrepancies.</p>
          </div>
          <div class="norm-factor-pill">
            <h5><span>🗣️</span> <span>Accent & Style Decoupling</span></h5>
            <p style="color: var(--text-secondary);">Evaluates cadence phrasing, pause syntax, and dynamic stress excursions rather than phonetic dialect variants or phoneme acoustics.</p>
          </div>
        </div>

        <!-- Contrastive Metrics Quad -->
        <div class="contrast-metrics-grid" id="contrastMetricsGrid">
          <!-- Injected dynamically -->
        </div>

        <!-- Phrase-by-Phrase Landmark Comparison -->
        <h5 style="font-family: var(--font-display); font-size: 14px; font-weight: 800; color: var(--text-white); margin-top: 20px;">
          Phrase-by-Phrase Delivery Pacing & Pitch Contour Contrast
        </h5>
        <div style="overflow-x: auto;">
          <table class="phrase-contrast-table">
            <thead>
              <tr>
                <th>Keynote Landmark Phrase</th>
                <th>Participant Duration</th>
                <th>Reference Duration</th>
                <th>Participant Pitch Excursion</th>
                <th>Reference Pitch Spike</th>
                <th>Cadence Verdict</th>
              </tr>
            </thead>
            <tbody id="phraseContrastTbody">
              <!-- Injected dynamically -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- TAB 3: RHETORICAL EMPHASIS DETECTION -->
      <div class="inno-tab-panel" id="innoTabRhetorical">
        <div class="showcase-persuasive-box">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
            <div>
              <span class="badge-pill" style="background: rgba(99, 102, 241, 0.2); color: #818cf8; font-size: 11px;">Persuasive Declamation Philosophy</span>
              <h4 style="font-family: var(--font-display); font-size: 17px; font-weight: 800; color: var(--text-white); margin-top: 6px;">
                Showcase: Contrastive Intent in Persuasive Oratory
              </h4>
            </div>
            <span style="font-size: 12px; font-family: var(--font-mono); color: var(--primary-cyan);">"We need change today."</span>
          </div>

          <p style="font-size: 13px; color: var(--text-secondary); margin-top: 8px; line-height: 1.5;">
            In persuasive public speaking, sentence meaning shifts completely depending on which focal word carries acoustic weight. The system evaluates whether delivery supports the intended rhetorical effect, rather than assuming a single universally correct pitch curve.
          </p>

          <div class="showcase-btns-row">
            <button class="btn-showcase-toggle active" id="btnShowcaseChange">
              <span>🎯</span> <span>Emphasize "change" (Ideological Urgency)</span>
            </button>
            <button class="btn-showcase-toggle" id="btnShowcaseToday">
              <span>⏱️</span> <span>Emphasize "today" (Temporal Immediacy)</span>
            </button>
          </div>

          <div id="showcaseDetailsCard" style="background: var(--bg-surface); border: 1px solid var(--border-medium); border-radius: var(--radius-sm); padding: 16px; font-size: 13px;">
            <!-- Injected dynamically -->
          </div>
        </div>

        <!-- Detected Focal Words in Speech -->
        <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 8px; margin-top: 24px;">
          <div>
            <h5 style="font-family: var(--font-display); font-size: 15px; font-weight: 800; color: var(--text-white);">
              Rhetorical Emphasis Footprint on Key Focal Words
            </h5>
            <p style="font-size: 12.5px; color: var(--text-secondary);">
              Analyzes Pitch Movement, Intensity Boost, Vowel Elongation, and Framing Pauses on salient words.
            </p>
          </div>
          <span class="badge-pill" id="focalCountBadge" style="background: var(--bg-elevated); border: 1px solid var(--border-medium); font-size: 11px;">
            0 Focal Words Analyzed
          </span>
        </div>

        <div class="focal-eval-grid" id="focalEvalGrid">
          <!-- Injected dynamically -->
        </div>
      </div>

      <!-- TAB 4: JUDGE CONSISTENCY MODE -->
      <div class="inno-tab-panel" id="innoTabConsistency">
        <!-- Defensible Objective Alert Callout -->
        <div class="judge-philosophy-callout">
          <span style="font-size: 26px;">⚖️</span>
          <div>
            <h5 style="font-family: var(--font-display); font-size: 14.5px; font-weight: 800; color: #fbbf24;">
              Defensible Objective: Explicit, Measurable & Reproducible Criteria
            </h5>
            <p style="font-size: 12.5px; color: var(--text-primary); margin-top: 2px; line-height: 1.45;">
              <strong>We do not claim that AI eliminates subjectivity.</strong> Human adjudication naturally reflects divergent perspectives. The objective of Nexora Voice is to make evaluation criteria explicit, measurable, and reproducible across adjudicator panels.
            </p>
          </div>
        </div>

        <!-- Inter-Rater Reliability Scoreboard -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 8px;">
          <h5 style="font-family: var(--font-display); font-size: 15px; font-weight: 800; color: var(--text-white);">
            Shared Rubric Multi-Judge Evaluation Panel
          </h5>
          <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 12px; color: var(--text-secondary);">Inter-Rater Agreement Index:</span>
            <span id="judgeAgreementIndex" style="font-family: var(--font-mono); font-size: 17px; font-weight: 800; color: #10b981;">0.97 / 1.00</span>
            <span id="judgeAgreementLabel" class="badge-pill" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4); font-size: 11px;">Strong Consistency</span>
          </div>
        </div>

        <div class="judge-panel-grid" id="judgePanelGrid">
          <!-- Injected dynamically -->
        </div>

        <!-- Rubric Interpretation Discrepancy Heatmap -->
        <h5 style="font-family: var(--font-display); font-size: 14px; font-weight: 800; color: var(--text-white); margin-top: 22px;">
          Rubric Interpretation Discrepancy Heatmap (Consensus vs Ambiguity Zones)
        </h5>
        <div style="overflow-x: auto;">
          <table class="discrepancy-table">
            <thead>
              <tr>
                <th>Evaluation Criterion</th>
                <th>AI DSP Benchmark</th>
                <th>Judge 1 (Coach)</th>
                <th>Judge 2 (Debate)</th>
                <th>Judge 3 (Audience)</th>
                <th>Spread</th>
                <th>Consensus Status</th>
                <th>Diagnostic Interpretation</th>
              </tr>
            </thead>
            <tbody id="discrepancyTbody">
              <!-- Injected dynamically -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- TAB 5: PERSONALIZED PRACTICE RECOMMENDATIONS -->
      <div class="inno-tab-panel" id="innoTabPractice">
        <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 8px; margin-bottom: 18px;">
          <div>
            <h4 style="font-family: var(--font-display); font-size: 17px; font-weight: 800; color: var(--text-white);">
              Ranked Bottleneck Rehearsal Prescription
            </h4>
            <p style="font-size: 13px; color: var(--text-secondary); margin-top: 2px;">
              Prioritizing the participant's most significant delivery flaws detected directly in this recording, with tailored vocal drills and target metrics.
            </p>
          </div>
          <span id="speakerReadinessBadge" class="badge-pill" style="background: rgba(244, 63, 94, 0.15); color: var(--sev-serious); border: 1px solid var(--sev-serious-border); font-size: 11.5px; padding: 4px 12px;">
            Targeted Coaching Required
          </span>
        </div>

        <!-- Prioritized Drill Stack -->
        <div class="drills-stack" id="drillsStack">
          <!-- Injected dynamically -->
        </div>

        <!-- 3-Step Actionable Roadmap -->
        <h5 style="font-family: var(--font-display); font-size: 14.5px; font-weight: 800; color: var(--text-white); margin-top: 26px;">
          Structured 20-Minute Rehearsal Roadmap
        </h5>
        <div class="roadmap-steps-row" id="roadmapStepsRow">
          <!-- Injected dynamically -->
        </div>
      </div>
    </div>
"""

# 3. JAVASCRIPT FUNCTIONS TO INJECT INTO <script>
JS_INJECTION = """
    // =========================================================================
    // 5 ADVANCED ORATORY INNOVATIONS SUITE CONTROLLER
    // =========================================================================
    function renderInnovationsSuite(data) {
      const suiteSection = document.getElementById('innovationsSuiteSection');
      if (!suiteSection) return;

      const inn = data.innovations;
      if (!inn || inn.error) {
        suiteSection.style.display = 'none';
        return;
      }

      suiteSection.style.display = 'block';

      // Setup Tab Switcher
      setupInnovationTabs();

      // 1. Severity Grading Spectrum
      renderSeverityGrading(inn.severity_grading);

      // 2. Same-Text Contrastive Comparison
      renderSameTextContrast(inn.same_text_contrast);

      // 3. Rhetorical Emphasis Detection
      renderRhetoricalEmphasis(inn.rhetorical_emphasis);

      // 4. Judge Consistency Mode
      renderJudgeConsistency(inn.judge_consistency);

      // 5. Personalized Practice Recommendations
      renderPersonalizedPractice(inn.personalized_practice);
    }

    function setupInnovationTabs() {
      const tabBtns = document.querySelectorAll('.inno-tab-btn');
      tabBtns.forEach(btn => {
        btn.onclick = () => {
          tabBtns.forEach(b => b.classList.remove('active'));
          document.querySelectorAll('.inno-tab-panel').forEach(p => p.classList.remove('active'));

          btn.classList.add('active');
          const tabId = btn.getAttribute('data-tab');
          const panelMap = {
            'severity': 'innoTabSeverity',
            'contrast': 'innoTabContrast',
            'rhetorical': 'innoTabRhetorical',
            'consistency': 'innoTabConsistency',
            'practice': 'innoTabPractice'
          };
          const targetPanel = document.getElementById(panelMap[tabId]);
          if (targetPanel) targetPanel.classList.add('active');
        };
      });
    }

    // 1. Render Severity Grading Spectrum
    function renderSeverityGrading(sevData) {
      if (!sevData) return;

      const counts = sevData.level_counts || {0:0, 1:0, 2:0, 3:0};
      const total = Math.max(1, counts[0] + counts[1] + counts[2] + counts[3]);

      const pct0 = Math.round((counts[0] / total) * 100);
      const pct1 = Math.round((counts[1] / total) * 100);
      const pct2 = Math.round((counts[2] / total) * 100);
      const pct3 = Math.max(0, 100 - (pct0 + pct1 + pct2));

      document.getElementById('segLvl0').style.width = `${pct0}%`;
      document.getElementById('segLvl1').style.width = `${pct1}%`;
      document.getElementById('segLvl2').style.width = `${pct2}%`;
      document.getElementById('segLvl3').style.width = `${pct3}%`;

      document.getElementById('countLvl0').textContent = `${counts[0]} segments (${pct0}%)`;
      document.getElementById('countLvl1').textContent = `${counts[1]} (${pct1}%)`;
      document.getElementById('countLvl2').textContent = `${counts[2]} (${pct2}%)`;
      document.getElementById('countLvl3').textContent = `${counts[3]} (${pct3}%)`;

      document.getElementById('spectrumOptimalRatio').textContent = `Level 0 Optimal Time: ${sevData.optimal_ratio_pct}% (${sevData.optimal_time_sec}s / ${sevData.total_time_sec}s)`;

      // Render Rubric Calibration Grid
      const rubricGrid = document.getElementById('calibRubricGrid');
      rubricGrid.innerHTML = '';
      const rubrics = sevData.rubric_calibration || {};
      for (const [key, r] of Object.entries(rubrics)) {
        const card = document.createElement('div');
        card.className = 'calib-card';
        card.innerHTML = `
          <div class="calib-card-title">
            <span>${r.title}</span>
            <span class="badge-pill" style="font-size:10px; background:var(--bg-elevated);">${r.unit}</span>
          </div>
          <p class="calib-card-rationale">${r.calibration_rationale || ''}</p>
          <div class="calib-levels-mini">
            <div class="calib-lvl-row lvl-0"><span>L0: Optimal</span><strong>${r.levels[0].range}</strong></div>
            <div class="calib-lvl-row lvl-1"><span>L1: Minor</span><strong>${r.levels[1].range}</strong></div>
            <div class="calib-lvl-row lvl-2"><span>L2: Moderate</span><strong>${r.levels[2].range}</strong></div>
            <div class="calib-lvl-row lvl-3"><span>L3: Major</span><strong>${r.levels[3].range}</strong></div>
          </div>
        `;
        rubricGrid.appendChild(card);
      }

      // Render Classified Issues List
      const issContainer = document.getElementById('classifiedIssuesList');
      issContainer.innerHTML = '';
      const issues = sevData.classified_issues || [];
      document.getElementById('classifiedIssuesCount').textContent = issues.length;

      if (!issues.length) {
        issContainer.innerHTML = `<p style="color:var(--text-muted); font-size:13px;">No significant delivery flaws detected across the spectrum! Pristine execution.</p>`;
        return;
      }

      issues.forEach(iss => {
        const card = document.createElement('div');
        card.className = `issue-card sev-${iss.level}`;
        card.innerHTML = `
          <div class="issue-header-line">
            <div class="issue-badge-group">
              <span class="badge-pill" style="background:${iss.level_color}22; color:${iss.level_color}; border:1px solid ${iss.level_color}66;">
                ${iss.level_label}
              </span>
              <span class="badge-pill" style="background:var(--bg-elevated); color:var(--text-secondary); border:1px solid var(--border-subtle);">
                ${iss.category.replace('_', ' ').toUpperCase()}
              </span>
            </div>
            <button class="ts-seek-button" onclick="seekAudioTime(${iss.start})">
              ⏱️ ${iss.start.toFixed(2)}s – ${iss.end.toFixed(2)}s (${iss.duration}s)
            </button>
          </div>
          <div style="font-size: 13.5px; font-weight: 700; color: var(--text-white); margin-bottom: 6px;">
            ${iss.what}
          </div>
          <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 8px;">
            <strong>Rubric Calibration:</strong> ${iss.level_desc} <span style="font-family:var(--font-mono); color:${iss.level_color};">(${iss.threshold_range})</span>
          </div>
          <div style="font-size: 12px; color: var(--text-muted); line-height: 1.45;">
            <strong>WHY:</strong> ${iss.why}
          </div>
          <div style="font-size: 12px; color: var(--primary-cyan); margin-top: 4px;">
            <strong>HOW TO FIX:</strong> ${iss.how}
          </div>
        `;
        issContainer.appendChild(card);
      });
    }

    // 2. Render Same-Text Contrastive Comparison
    function renderSameTextContrast(contrastData) {
      if (!contrastData) return;

      document.getElementById('refPassageTitle').textContent = contrastData.reference_title || 'Keynote Benchmark';
      document.getElementById('refPassageSnippet').textContent = `"${contrastData.target_text || ''}"`;
      document.getElementById('contrastAlignmentIdx').textContent = `${contrastData.alignment_index || 85}%`;
      document.getElementById('contrastAlignmentLabel').textContent = contrastData.alignment_label || 'Cadence Alignment';

      // Render Metrics Quad
      const mGrid = document.getElementById('contrastMetricsGrid');
      mGrid.innerHTML = '';
      const metrics = contrastData.metrics_comparison || {};
      for (const [key, m] of Object.entries(metrics)) {
        const tile = document.createElement('div');
        tile.className = 'contrast-metric-tile';
        const ratioStr = m.ratio !== undefined ? `Ratio: ${m.ratio}x` : `Delta: ${m.delta > 0 ? '+' : ''}${m.delta}s`;
        tile.innerHTML = `
          <div class="contrast-tile-title">${m.label}</div>
          <div class="contrast-tile-main">
            <span>${m.user}</span>
            <span style="font-size:12px; color:var(--text-muted); font-weight:normal;">vs ref ${m.ref}</span>
          </div>
          <div class="contrast-tile-sub" style="display:flex; justify-content:space-between; margin-top:6px;">
            <span style="color:var(--primary-cyan);">${ratioStr}</span>
            <span class="badge-pill" style="font-size:10px; background:var(--bg-elevated);">${m.status}</span>
          </div>
        `;
        mGrid.appendChild(tile);
      }

      // Render Phrase Breakdown Table
      const tbody = document.getElementById('phraseContrastTbody');
      tbody.innerHTML = '';
      (contrastData.phrase_breakdown || []).forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${p.phrase}</strong></td>
          <td style="font-family:var(--font-mono);">${p.user_duration}s</td>
          <td style="font-family:var(--font-mono); color:var(--text-muted);">${p.ref_duration}s</td>
          <td style="font-family:var(--font-mono); color:var(--primary-cyan);">${p.user_pitch_spike > 0 ? '+' : ''}${p.user_pitch_spike} st</td>
          <td style="font-family:var(--font-mono); color:var(--text-muted);">${p.ref_pitch_spike > 0 ? '+' : ''}${p.ref_pitch_spike} st</td>
          <td><span class="badge-pill" style="background:${p.status_color}22; color:${p.status_color}; border:1px solid ${p.status_color}55;">${p.status}</span></td>
        `;
        tbody.appendChild(tr);
      });
    }

    // 3. Render Rhetorical Emphasis Detection
    function renderRhetoricalEmphasis(rhetData) {
      if (!rhetData) return;

      const showcase = rhetData.sentence_showcase;
      const detailsCard = document.getElementById('showcaseDetailsCard');
      const btnChange = document.getElementById('btnShowcaseChange');
      const btnToday = document.getElementById('btnShowcaseToday');

      const renderShowcaseCase = (caseIndex) => {
        if (!showcase || !showcase.cases) return;
        const c = showcase.cases[caseIndex];
        detailsCard.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-family:var(--font-display); font-size:15px; font-weight:800; color:var(--primary-cyan);">
              Focal Accent: "${c.focal_word}"
            </span>
            <span class="badge-pill" style="background:var(--bg-elevated); font-size:10.5px;">Acoustic Persuasion Profile</span>
          </div>
          <div style="font-weight:600; color:var(--text-primary); margin-bottom:6px;">${c.interpretation}</div>
          <div style="font-size:12px; color:var(--text-secondary); font-family:var(--font-mono); line-height:1.5;">
            <strong>Acoustic Footprint:</strong> ${c.acoustic_footprint}
          </div>
        `;
      };

      if (btnChange && btnToday) {
        btnChange.onclick = () => {
          btnChange.classList.add('active');
          btnToday.classList.remove('active');
          renderShowcaseCase(0);
        };
        btnToday.onclick = () => {
          btnToday.classList.add('active');
          btnChange.classList.remove('active');
          renderShowcaseCase(1);
        };
        renderShowcaseCase(0);
      }

      // Render Focal Words Grid
      const fGrid = document.getElementById('focalEvalGrid');
      fGrid.innerHTML = '';
      const focals = rhetData.focal_evaluations || [];
      document.getElementById('focalCountBadge').textContent = `${focals.length} Focal Words Analyzed`;

      if (!focals.length) {
        fGrid.innerHTML = `<p style="color:var(--text-muted); font-size:13px;">No explicit focal targets detected. Review full transcript for emphasis annotations.</p>`;
        return;
      }

      focals.forEach(f => {
        const card = document.createElement('div');
        card.className = 'focal-eval-card';
        card.innerHTML = `
          <div class="focal-card-head">
            <span class="focal-word-badge">"${f.word}"</span>
            <span class="badge-pill" style="background:${f.verdict_color}22; color:${f.verdict_color}; border:1px solid ${f.verdict_color}66; font-size:10.5px;">
              ${f.punch_score}/100 Punch
            </span>
          </div>
          <div style="font-size:12px; font-weight:700; color:${f.verdict_color}; margin-bottom:8px;">
            ${f.verdict}
          </div>
          <div class="focal-metrics-list">
            <span>Pitch Movement: <strong>+${f.pitch_movement_st} semitones</strong></span>
            <span>Intensity Boost: <strong>+${f.intensity_boost_db} dB</strong></span>
            <span>Duration Expansion: <strong>${f.duration_factor}x factor</strong></span>
            <span>Framing Pauses: <strong>pre: ${f.pre_pause_sec}s | post: ${f.post_pause_sec}s</strong></span>
          </div>
          <div style="margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
            <button class="btn" style="padding:3px 8px; font-size:11px;" onclick="seekAudioTime(${f.start})">
              ▶️ Play Focal Word (${f.timestamp})
            </button>
          </div>
        `;
        fGrid.appendChild(card);
      });
    }

    // 4. Render Judge Consistency Mode
    function renderJudgeConsistency(jData) {
      if (!jData) return;

      document.getElementById('judgeAgreementIndex').textContent = `${jData.inter_rater_agreement_index} / 1.00`;
      document.getElementById('judgeAgreementLabel').textContent = jData.agreement_label || 'High Panel Consistency';

      // Render 4 Panel Tiles
      const pGrid = document.getElementById('judgePanelGrid');
      pGrid.innerHTML = '';
      const judges = jData.judge_scores || {};

      for (const [name, scs] of Object.entries(judges)) {
        const vals = Object.values(scs);
        const avg = vals.length ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : 0;
        const isAi = name.includes('AI');

        const tile = document.createElement('div');
        tile.className = `judge-panel-tile ${isAi ? 'ai' : ''}`;
        tile.innerHTML = `
          <div style="font-size:11px; text-transform:uppercase; color:var(--text-muted); font-family:var(--font-mono); margin-bottom:4px;">
            ${isAi ? 'Objective DSP Sensor' : 'Human Adjudicator'}
          </div>
          <h5 style="font-family:var(--font-display); font-size:14px; font-weight:700; color:var(--text-white); margin-bottom:8px;">
            ${name}
          </h5>
          <div style="font-family:var(--font-mono); font-size:24px; font-weight:800; color:${isAi ? 'var(--primary-cyan)' : 'var(--text-white)'};">
            ${avg}/100
          </div>
          <div style="font-size:11px; color:var(--text-secondary); margin-top:4px;">
            Panel Average
          </div>
        `;
        pGrid.appendChild(tile);
      }

      // Render Discrepancy Heatmap Table
      const tbody = document.getElementById('discrepancyTbody');
      tbody.innerHTML = '';
      (jData.discrepancy_heatmap || []).forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${row.criterion}</strong></td>
          <td style="font-family:var(--font-mono); color:var(--primary-cyan); font-weight:700;">${row.ai_score}</td>
          <td style="font-family:var(--font-mono);">${row.j1_score}</td>
          <td style="font-family:var(--font-mono);">${row.j2_score}</td>
          <td style="font-family:var(--font-mono);">${row.j3_score}</td>
          <td style="font-family:var(--font-mono); font-weight:700;">${row.spread} pts</td>
          <td>
            <span class="badge-pill" style="background:${row.consensus_color}22; color:${row.consensus_color}; border:1px solid ${row.consensus_color}55;">
              ${row.consensus_level}
            </span>
          </td>
          <td style="font-size:11px; color:var(--text-secondary); max-width:280px;">${row.interpretation}</td>
        `;
        tbody.appendChild(tr);
      });
    }

    // 5. Render Personalized Practice Recommendations
    function renderPersonalizedPractice(pData) {
      if (!pData) return;

      const badge = document.getElementById('speakerReadinessBadge');
      badge.textContent = pData.speaker_readiness_status || 'Targeted Coaching Prescribed';

      const dStack = document.getElementById('drillsStack');
      dStack.innerHTML = '';
      const drills = pData.prioritized_drills || [];

      drills.forEach((d, idx) => {
        const card = document.createElement('div');
        card.className = `drill-prescription-card p${idx + 1}`;
        card.innerHTML = `
          <div class="drill-header">
            <div style="display:flex; align-items:center; gap:10px;">
              <span class="badge-pill" style="background:var(--bg-elevated); border:1px solid var(--border-medium); font-size:11px; color:var(--primary-cyan);">
                Priority #${d.priority} Bottleneck
              </span>
              <h4 style="font-family:var(--font-display); font-size:16px; font-weight:800; color:var(--text-white);">
                ${d.drill_name}
              </h4>
            </div>
            <span class="badge-pill" style="background:rgba(244,63,94,0.15); color:var(--sev-serious); font-size:11px;">
              Flaw: ${d.flaw_type} (Impact Weight: ${d.impact_weight})
            </span>
          </div>

          <div style="font-size:12.5px; color:var(--text-secondary); margin-bottom:8px;">
            <strong>Objective:</strong> ${d.objective}
          </div>

          <div class="drill-instructions-box">
            <strong>Exercise Instructions:</strong> ${d.instructions}
          </div>

          <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; color:var(--text-muted); flex-wrap:wrap; gap:8px;">
            <span>⏱️ <strong>Frequency:</strong> ${d.frequency}</span>
            <span style="color:#10b981; font-family:var(--font-mono);">🎯 <strong>Target Metric on Take 2:</strong> ${d.target_metric}</span>
          </div>
        `;
        dStack.appendChild(card);
      });

      // Render Roadmap Steps
      const rRow = document.getElementById('roadmapStepsRow');
      rRow.innerHTML = '';
      (pData.rehearsal_roadmap || []).forEach(s => {
        const stepCard = document.createElement('div');
        stepCard.className = 'roadmap-step-card';
        stepCard.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="badge-pill" style="background:var(--primary-gradient); color:#ffffff; font-size:10.5px;">${s.step}</span>
            <span style="font-family:var(--font-mono); font-size:11px; color:var(--text-muted);">${s.est_time}</span>
          </div>
          <p style="font-size:12.5px; color:var(--text-primary); line-height:1.45;">${s.action}</p>
        `;
        rRow.appendChild(stepCard);
      });
    }
"""

# Apply CSS injection before </style>
if "</style>" in content:
    content = content.replace("  </style>", CSS_INJECTION + "\n  </style>", 1)
    print("[+] Injected CSS styles into index.html")
else:
    print("[-] Could not find </style> in index.html")

# Apply HTML injection before </div> <!-- end app-wrapper -->
target_wrapper_end = "      <!-- Interactive Pause Intervals Navigator Strip -->"
if "</div>\n    </div>\n  </div>\n\n  <!-- APPLICATION LOGIC" in content:
    content = content.replace("    </div>\n  </div>\n\n  <!-- APPLICATION LOGIC", "    </div>\n" + HTML_INJECTION + "\n  </div>\n\n  <!-- APPLICATION LOGIC", 1)
    print("[+] Injected HTML markup into index.html")
elif "</div>\n  </div>\n\n  <!-- APPLICATION LOGIC" in content:
    content = content.replace("</div>\n  </div>\n\n  <!-- APPLICATION LOGIC", "</div>\n" + HTML_INJECTION + "\n  </div>\n\n  <!-- APPLICATION LOGIC", 1)
    print("[+] Injected HTML markup into index.html (alt)")
else:
    # Try regex search
    pattern = r'(    </div>\s*</div>\s*<!-- APPLICATION LOGIC)'
    if re.search(pattern, content):
        content = re.sub(pattern, HTML_INJECTION + r"\n    </div>\n  </div>\n\n  <!-- APPLICATION LOGIC", content, count=1)
        print("[+] Injected HTML markup with regex")
    else:
        print("[-] Could not find insertion point for HTML")

# Apply renderCompleteTelemetry call
if "renderAcousticFootprintStudio(data);" in content:
    content = content.replace(
        "renderAcousticFootprintStudio(data);",
        "renderAcousticFootprintStudio(data);\n\n      // Render 5 Advanced Oratory Innovations\n      renderInnovationsSuite(data);",
        1
    )
    print("[+] Added renderInnovationsSuite(data) call inside renderCompleteTelemetry")

# Apply JS injection before initTheme();
if "initTheme();" in content:
    content = content.replace("    initTheme();", JS_INJECTION + "\n    initTheme();", 1)
    print("[+] Injected JavaScript controller into index.html")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[SUCCESS] Completed injection into frontend/index.html")
