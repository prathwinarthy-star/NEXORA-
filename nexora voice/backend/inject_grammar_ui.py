"""
Injects Dynamic Score Calibration HUD and Spoken Grammar Analysis Studio into frontend/index.html
"""
import os
import re

INDEX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html"))

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. CSS Styles
CSS_INJECTION = """
    /* ==========================================================================
       DYNAMIC FAULT-DRIVEN SCORE CALIBRATION & GRAMMAR STUDIO (STYLES)
       ========================================================================== */
    .score-audit-panel {
      margin-top: 20px;
      margin-bottom: 24px;
      background: var(--bg-surface);
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-lg);
      padding: 22px 26px;
      box-shadow: var(--shadow-surface);
      transition: var(--transition-fast);
    }

    .score-audit-panel:hover {
      border-color: var(--border-accent);
    }

    .score-waterfall-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 16px;
      margin-top: 16px;
      margin-bottom: 18px;
    }

    .score-waterfall-card {
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 16px 18px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .score-waterfall-card.final {
      border-color: var(--primary-cyan);
      background: linear-gradient(145deg, rgba(6,182,212,0.12), rgba(59,130,246,0.06));
    }

    .score-waterfall-label {
      font-size: 11.5px;
      font-weight: 700;
      color: var(--text-secondary);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .score-waterfall-val {
      font-family: var(--font-display);
      font-size: 26px;
      font-weight: 900;
      line-height: 1.1;
    }

    .score-waterfall-sub {
      font-size: 11.5px;
      color: var(--text-muted);
    }

    .deductions-toggle-btn {
      background: var(--bg-elevated);
      border: 1px solid var(--border-medium);
      color: var(--text-primary);
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 12.5px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: var(--transition-fast);
    }

    .deductions-toggle-btn:hover {
      background: var(--bg-glass-hover);
      border-color: var(--primary-cyan);
      color: var(--primary-cyan);
    }

    .deductions-drawer {
      margin-top: 16px;
      background: var(--bg-void);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      overflow: hidden;
      max-height: 380px;
      overflow-y: auto;
    }

    .deductions-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12.5px;
    }

    .deductions-table th {
      background: var(--bg-elevated);
      color: var(--text-secondary);
      font-weight: 700;
      padding: 10px 14px;
      text-align: left;
      border-bottom: 1px solid var(--border-subtle);
      font-size: 11.5px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .deductions-table td {
      padding: 10px 14px;
      border-bottom: 1px solid var(--border-subtle);
      color: var(--text-primary);
    }

    .deductions-table tr:hover td {
      background: rgba(255, 255, 255, 0.02);
    }

    /* Grammar Studio Styles */
    .grammar-studio-section {
      margin-top: 36px;
      margin-bottom: 36px;
      background: var(--bg-glass);
      backdrop-filter: var(--glass-blur);
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-xl);
      padding: 30px;
      box-shadow: var(--shadow-surface);
      position: relative;
    }

    .grammar-hero-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 22px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border-subtle);
      flex-wrap: wrap;
      gap: 14px;
    }

    .grammar-metrics-strip {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 14px;
      margin-bottom: 24px;
    }

    .grammar-stat-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .grammar-cards-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 14px;
      margin-top: 14px;
    }

    .grammar-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-md);
      padding: 20px 22px;
      transition: var(--transition-fast);
      position: relative;
    }

    .grammar-card:hover {
      border-color: var(--border-accent);
      transform: translateY(-2px);
    }

    .grammar-diff-box {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      background: var(--bg-void);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 14px 16px;
      margin: 12px 0;
    }

    @media (max-width: 768px) {
      .grammar-diff-box {
        grid-template-columns: 1fr;
      }
    }

    .grammar-diff-col {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .grammar-diff-label {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .grammar-original-text {
      color: #f43f5e;
      text-decoration: line-through;
      font-weight: 600;
      font-family: var(--font-body);
      font-size: 14px;
    }

    .grammar-corrected-text {
      color: #10b981;
      font-weight: 700;
      font-family: var(--font-body);
      font-size: 14px;
    }

    .grammar-sentences-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 14px;
      max-height: 420px;
      overflow-y: auto;
    }

    .grammar-sentence-row {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 14px 18px;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 16px;
    }

    .grammar-sentence-row.clean {
      border-left: 4px solid #10b981;
    }

    .grammar-sentence-row.has-faults {
      border-left: 4px solid #f43f5e;
    }
"""

if "/* DYNAMIC FAULT-DRIVEN SCORE CALIBRATION & GRAMMAR STUDIO (STYLES) */" not in content:
    content = content.replace("</style>", CSS_INJECTION + "\n  </style>")

# 2. HTML Injection for Score Audit HUD (right below coachingCard)
SCORE_AUDIT_HTML = """
    <!-- DYNAMIC FAULT-DRIVEN SCORE CALIBRATION & PENALTY HUD -->
    <div class="score-audit-panel" id="scoreAuditPanel" style="display: none;">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <span style="font-size: 20px;">⚡</span>
          <div>
            <h4 style="font-family: var(--font-display); font-size: 17px; font-weight: 800; color: var(--text-white); margin: 0;">
              Fault-Calibrated Delivery Score HUD
            </h4>
            <p style="font-size: 12px; color: var(--text-secondary); margin: 2px 0 0 0;" id="scoreFormulaDesc">
              Your overall score changes dynamically based on detected delivery and grammatical faults.
            </p>
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
          <span class="badge-pill" id="deliveryGradeBadge" style="background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.4); font-size: 12px; font-weight: 700; padding: 5px 14px;">
            Grade: A+
          </span>
          <button class="deductions-toggle-btn" id="btnToggleDeductions">
            <span>📋 View Deductions Breakdown</span>
            <span id="deductionsArrow">▼</span>
          </button>
        </div>
      </div>

      <!-- Waterfall Metrics -->
      <div class="score-waterfall-grid">
        <div class="score-waterfall-card">
          <span class="score-waterfall-label">Base Starting Score</span>
          <span class="score-waterfall-val" style="color: var(--text-white);">100 pts</span>
          <span class="score-waterfall-sub">Flawless oratory baseline</span>
        </div>
        <div class="score-waterfall-card">
          <span class="score-waterfall-label">Acoustic Fault Penalty</span>
          <span class="score-waterfall-val" id="auditAcousticDeduct" style="color: #f43f5e;">-0 pts</span>
          <span class="score-waterfall-sub" id="auditAcousticCount">0 delivery flaws detected</span>
        </div>
        <div class="score-waterfall-card">
          <span class="score-waterfall-label">Grammar & Syntax Penalty</span>
          <span class="score-waterfall-val" id="auditGrammarDeduct" style="color: #fbbf24;">-0 pts</span>
          <span class="score-waterfall-sub" id="auditGrammarCount">0 grammatical slips detected</span>
        </div>
        <div class="score-waterfall-card final">
          <span class="score-waterfall-label">Final Dynamic Score</span>
          <span class="score-waterfall-val" id="auditFinalScore" style="color: var(--primary-cyan);">100/100</span>
          <span class="score-waterfall-sub" id="auditScoreDelta">100% mastery retained</span>
        </div>
      </div>

      <!-- Collapsible Deductions Log Drawer -->
      <div class="deductions-drawer" id="deductionsDrawer" style="display: none;">
        <table class="deductions-table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Criterion / Category</th>
              <th>Fault Description</th>
              <th>Severity</th>
              <th>Score Impact</th>
            </tr>
          </thead>
          <tbody id="deductionsTableBody">
            <!-- Injected dynamically -->
          </tbody>
        </table>
      </div>
    </div>
"""

# 3. HTML Injection for Spoken Grammar Studio (after innovationsSuiteSection)
GRAMMAR_STUDIO_HTML = """
    <!-- =========================================================================
         SPOKEN GRAMMAR & SYNTACTIC ANALYSIS STUDIO
         ========================================================================= -->
    <div class="grammar-studio-section" id="grammarStudioSection" style="display: none;">
      <div class="grammar-hero-header">
        <div style="display: flex; flex-direction: column; gap: 4px;">
          <h3 style="font-family: var(--font-display); font-size: 22px; font-weight: 800; color: var(--text-white); display: flex; align-items: center; gap: 10px; margin: 0;">
            <span>📝</span> <span>Spoken Grammar & Syntactic Analysis Studio</span>
          </h3>
          <p style="font-size: 13.5px; color: var(--text-secondary); margin: 0; max-width: 820px; line-height: 1.5;">
            Automated linguistic evaluation inspecting subject-verb agreement, irregular verb tenses, article usage, prepositions, double negatives, colloquial slang, and spoken run-on clauses.
          </p>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
          <span class="badge-pill" id="grammarFluencyBadge" style="background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.4); font-size: 12.5px; padding: 6px 14px; font-weight: 700;">
            Fluency: Native / Pristine
          </span>
        </div>
      </div>

      <!-- Grammar Metrics Strip -->
      <div class="grammar-metrics-strip">
        <div class="grammar-stat-card">
          <span style="font-size: 11.5px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase;">Grammar Score</span>
          <span style="font-family: var(--font-display); font-size: 28px; font-weight: 900; color: var(--primary-cyan);" id="statGrammarScore">100/100</span>
          <span style="font-size: 11px; color: var(--text-muted);">Weighted by flaw severity</span>
        </div>
        <div class="grammar-stat-card">
          <span style="font-size: 11.5px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase;">Grammar Faults Found</span>
          <span style="font-family: var(--font-display); font-size: 28px; font-weight: 900; color: #f43f5e;" id="statGrammarFaults">0</span>
          <span style="font-size: 11px; color: var(--text-muted);" id="statGrammarPointsDeducted">-0 pts deducted</span>
        </div>
        <div class="grammar-stat-card">
          <span style="font-size: 11.5px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase;">Error Density</span>
          <span style="font-family: var(--font-display); font-size: 28px; font-weight: 900; color: #fbbf24;" id="statErrorDensity">0.0%</span>
          <span style="font-size: 11px; color: var(--text-muted);">Errors per 100 spoken words</span>
        </div>
        <div class="grammar-stat-card">
          <span style="font-size: 11.5px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase;">Analyzed Words</span>
          <span style="font-family: var(--font-display); font-size: 28px; font-weight: 900; color: var(--text-white);" id="statTotalSpokenWords">0</span>
          <span style="font-size: 11px; color: var(--text-muted);" id="statSentenceCount">0 sentences evaluated</span>
        </div>
      </div>

      <!-- Navigation Tabs for Grammar Studio -->
      <div class="inno-nav-tabs" id="grammarNavTabs" style="margin-bottom: 18px;">
        <button class="inno-tab-btn active" data-gtab="faults">
          <span>🔍</span> <span>1. Grammar Faults & Corrections</span>
        </button>
        <button class="inno-tab-btn" data-gtab="sentences">
          <span>📜</span> <span>2. Sentence-by-Sentence Audit</span>
        </button>
        <button class="inno-tab-btn" data-gtab="reconstructed">
          <span>✨</span> <span>3. Polished Reconstructed Keynote</span>
        </button>
      </div>

      <!-- TAB 1: FAULTS & BEFORE-VS-AFTER CORRECTIONS -->
      <div class="inno-tab-panel active" id="gTabFaults">
        <div id="grammarEmptyState" style="text-align: center; padding: 36px 20px; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); display: none;">
          <span style="font-size: 32px;">🌟</span>
          <h4 style="font-family: var(--font-display); font-size: 17px; font-weight: 800; color: var(--text-white); margin: 8px 0;">
            Immaculate Spoken Grammar
          </h4>
          <p style="font-size: 13px; color: var(--text-secondary); margin: 0 auto; max-width: 500px;">
            No grammatical inconsistencies, agreement mismatches, or informal contractions were detected in this speech recording.
          </p>
        </div>
        <div class="grammar-cards-grid" id="grammarCardsGrid">
          <!-- Injected dynamically -->
        </div>
      </div>

      <!-- TAB 2: SENTENCE-BY-SENTENCE AUDIT -->
      <div class="inno-tab-panel" id="gTabSentences" style="display: none;">
        <div class="grammar-sentences-list" id="grammarSentencesList">
          <!-- Injected dynamically -->
        </div>
      </div>

      <!-- TAB 3: POLISHED RECONSTRUCTED KEYNOTE -->
      <div class="inno-tab-panel" id="gTabReconstructed" style="display: none;">
        <div style="background: var(--bg-surface); border: 1px solid var(--border-medium); border-radius: var(--radius-md); padding: 22px 26px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <h5 style="font-family: var(--font-display); font-size: 15px; font-weight: 800; color: var(--text-white); margin: 0;">
              Grammatically Enhanced Spoken Transcript
            </h5>
            <span class="badge-pill" style="background: rgba(6,182,212,0.15); color: var(--primary-cyan); font-size: 11.5px;">
              Executive Keynote Standard
            </span>
          </div>
          <p style="font-size: 14.5px; line-height: 1.7; color: var(--text-primary); margin: 0;" id="txtReconstructedTranscript">
            --
          </p>
        </div>
      </div>
    </div>
"""

# Insert Score Audit HTML after coachingCard
if 'id="scoreAuditPanel"' not in content:
    target_needle = '</div>\n\n    <!-- 8 Criteria Scorecards Grid -->'
    if target_needle in content:
        content = content.replace(target_needle, '</div>\n' + SCORE_AUDIT_HTML + '\n    <!-- 8 Criteria Scorecards Grid -->')

# Insert Grammar Studio HTML after innovationsSuiteSection
if 'id="grammarStudioSection"' not in content:
    content = content.replace('</div>\n\n  </div>\n\n  <!-- APPLICATION LOGIC & MULTILINGUAL LOCALIZATION -->', '</div>\n' + GRAMMAR_STUDIO_HTML + '\n  </div>\n\n  <!-- APPLICATION LOGIC & MULTILINGUAL LOCALIZATION -->')

# 4. JavaScript Rendering Logic
JS_FUNCTIONS = """
    // =========================================================================
    // DYNAMIC FAULT-DRIVEN SCORE CALIBRATION & GRAMMAR STUDIO (LOGIC)
    // =========================================================================

    // 1. Render Score Fault Audit HUD
    function renderScoreFaultAudit(audit, scores) {
      const panel = document.getElementById('scoreAuditPanel');
      if (!panel) return;
      panel.style.display = 'block';

      const aDeduct = document.getElementById('auditAcousticDeduct');
      const gDeduct = document.getElementById('auditGrammarDeduct');
      const fScore = document.getElementById('auditFinalScore');
      const aCount = document.getElementById('auditAcousticCount');
      const gCount = document.getElementById('auditGrammarCount');
      const gradeBadge = document.getElementById('deliveryGradeBadge');
      const deltaSub = document.getElementById('auditScoreDelta');
      const tbody = document.getElementById('deductionsTableBody');

      if (!audit) {
        aDeduct.textContent = '-0 pts';
        gDeduct.textContent = '-0 pts';
        fScore.textContent = '100/100';
        return;
      }

      aDeduct.textContent = `-${audit.acoustic_deduction || 0} pts`;
      gDeduct.textContent = `-${audit.grammar_deduction || 0} pts`;
      fScore.textContent = `${audit.overall_score || 100}/100`;

      aCount.textContent = `${audit.fault_count || 0} acoustic flaws tracked`;
      gCount.textContent = `${audit.grammar_deduction ? 'Grammar faults penalized' : '0 grammar slips'}`;
      gradeBadge.textContent = `Grade: ${audit.delivery_grade || 'A+'}`;

      const totalLost = audit.total_deduction || 0;
      deltaSub.textContent = totalLost > 0 ? `-${totalLost} pts total deduction` : '100% mastery retained';

      // Deductions table rows
      tbody.innerHTML = '';
      const logs = audit.deduction_log || [];
      if (logs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--text-muted); padding:16px;">Zero delivery faults detected. Score remains at pristine 100/100 baseline.</td></tr>';
      } else {
        logs.forEach(l => {
          const tr = document.createElement('tr');
          const sevColor = l.severity === 3 ? 'var(--sev-serious)' : (l.severity === 2 ? 'var(--sev-moderate)' : 'var(--primary-cyan)');
          const sevLabel = l.severity === 3 ? 'Major (Level 3)' : (l.severity === 2 ? 'Moderate (Level 2)' : 'Minor (Level 1)');
          tr.innerHTML = `
            <td style="font-family:var(--font-mono); font-size:11.5px; color:var(--text-muted);">${l.start.toFixed(1)}s - ${l.end.toFixed(1)}s</td>
            <td><span class="badge-pill" style="background:var(--bg-elevated); font-size:11px;">${l.category.replace(/_/g, ' ')}</span></td>
            <td><strong style="color:var(--text-white);">${l.what}</strong><br><span style="font-size:11px; color:var(--text-secondary);">${l.explanation}</span></td>
            <td><span class="badge-pill" style="background:${sevColor}22; color:${sevColor}; border:1px solid ${sevColor}55; font-size:11px;">${sevLabel}</span></td>
            <td style="font-family:var(--font-mono); font-weight:700; color:#f43f5e;">-${l.points_deducted} pts</td>
          `;
          tbody.appendChild(tr);
        });
      }
    }

    // Toggle Deductions Drawer
    const btnToggleDeductions = document.getElementById('btnToggleDeductions');
    const deductionsDrawer = document.getElementById('deductionsDrawer');
    const deductionsArrow = document.getElementById('deductionsArrow');
    if (btnToggleDeductions && deductionsDrawer) {
      btnToggleDeductions.addEventListener('click', () => {
        const isHidden = deductionsDrawer.style.display === 'none';
        deductionsDrawer.style.display = isHidden ? 'block' : 'none';
        deductionsArrow.textContent = isHidden ? '▲' : '▼';
      });
    }

    // 2. Render Spoken Grammar Analysis Studio
    function renderGrammarStudio(grammarData) {
      const gSection = document.getElementById('grammarStudioSection');
      if (!gSection) return;
      gSection.style.display = 'block';

      if (!grammarData) return;

      const scoreEl = document.getElementById('statGrammarScore');
      const faultsEl = document.getElementById('statGrammarFaults');
      const deductEl = document.getElementById('statGrammarPointsDeducted');
      const densityEl = document.getElementById('statErrorDensity');
      const wordsEl = document.getElementById('statTotalSpokenWords');
      const sentCountEl = document.getElementById('statSentenceCount');
      const fluencyBadge = document.getElementById('grammarFluencyBadge');

      scoreEl.textContent = `${grammarData.grammar_score || 100}/100`;
      faultsEl.textContent = grammarData.error_count || 0;
      deductEl.textContent = `-${grammarData.points_deducted || 0} pts deducted`;
      densityEl.textContent = `${grammarData.error_density_per_100_words || 0}%`;
      wordsEl.textContent = grammarData.total_words || 0;
      sentCountEl.textContent = `${(grammarData.sentences || []).length} sentences evaluated`;

      fluencyBadge.textContent = `Fluency: ${grammarData.fluency_rating || 'Pristine'}`;
      fluencyBadge.style.color = grammarData.fluency_color || '#10b981';
      fluencyBadge.style.borderColor = `${grammarData.fluency_color || '#10b981'}55`;

      // Render Cards Grid
      const cardsGrid = document.getElementById('grammarCardsGrid');
      const emptyState = document.getElementById('grammarEmptyState');
      cardsGrid.innerHTML = '';

      const issues = grammarData.issues || [];
      if (issues.length === 0) {
        emptyState.style.display = 'block';
      } else {
        emptyState.style.display = 'none';
        issues.forEach((iss, idx) => {
          const card = document.createElement('div');
          card.className = 'grammar-card';
          const sevColor = iss.severity === 3 ? 'var(--sev-serious)' : (iss.severity === 2 ? 'var(--sev-moderate)' : 'var(--primary-cyan)');
          card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
              <div style="display:flex; align-items:center; gap:8px;">
                <span class="badge-pill" style="background:var(--bg-elevated); font-size:11px; color:var(--primary-cyan);">#${idx + 1} ${iss.error_type}</span>
                <span style="font-family:var(--font-mono); font-size:11.5px; color:var(--text-muted);">⏱️ ${iss.start.toFixed(2)}s – ${iss.end.toFixed(2)}s</span>
              </div>
              <div style="display:flex; align-items:center; gap:8px;">
                <span class="badge-pill" style="background:${sevColor}22; color:${sevColor}; font-size:11px; border:1px solid ${sevColor}44;">
                  Severity ${iss.severity} (-${iss.points_deducted} pts)
                </span>
                <button class="btn btn-icon" style="padding:4px 10px; font-size:11px; height:auto; gap:4px;" onclick="seekToTimestamp(${iss.start})">
                  🔊 Jump to Audio
                </button>
              </div>
            </div>

            <!-- Before vs After Diff Box -->
            <div class="grammar-diff-box">
              <div class="grammar-diff-col">
                <span class="grammar-diff-label" style="color:#f43f5e;">❌ Spoken Excerpt (User Speech):</span>
                <span class="grammar-original-text">"${iss.original_text}"</span>
              </div>
              <div class="grammar-diff-col">
                <span class="grammar-diff-label" style="color:#10b981;">✓ Suggested Correction:</span>
                <span class="grammar-corrected-text">"${iss.corrected_text}"</span>
              </div>
            </div>

            <div style="font-size:12.5px; color:var(--text-secondary); line-height:1.5;">
              <strong>Linguistic Rationale:</strong> ${iss.why || iss.explanation}
            </div>
            <div style="font-size:12px; color:var(--primary-cyan); margin-top:6px;">
              💡 <strong>Actionable Rule:</strong> ${iss.how}
            </div>
          `;
          cardsGrid.appendChild(card);
        });
      }

      // Render Sentences Audit
      const sList = document.getElementById('grammarSentencesList');
      sList.innerHTML = '';
      (grammarData.sentences || []).forEach(s => {
        const sRow = document.createElement('div');
        sRow.className = `grammar-sentence-row ${s.has_faults ? 'has-faults' : 'clean'}`;
        sRow.innerHTML = `
          <div style="flex:1;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              <span class="badge-pill" style="background:var(--bg-elevated); font-size:10.5px;">Sentence #${s.id}</span>
              ${s.has_faults ? `<span class="badge-pill" style="background:rgba(244,63,94,0.15); color:var(--sev-serious); font-size:10.5px;">⚠️ ${s.faults_count} Syntax Slips</span>` : `<span class="badge-pill" style="background:rgba(16,185,129,0.15); color:#10b981; font-size:10.5px;">✓ Clean Syntax</span>`}
            </div>
            <div style="font-size:13.5px; line-height:1.6; color:var(--text-primary);">
              ${s.highlighted_html}
            </div>
          </div>
          <button class="btn btn-icon" style="padding:4px 8px; font-size:11px; height:auto;" onclick="seekToTimestamp(${s.start})">
            ▶ Play
          </button>
        `;
        sList.appendChild(sRow);
      });

      // Render Reconstructed Transcript
      const rTxt = document.getElementById('txtReconstructedTranscript');
      if (rTxt) {
        rTxt.textContent = grammarData.corrected_transcript || appState.analysis?.full_text || 'No transcript available.';
      }
    }

    // Grammar Tabs Switching
    const gTabs = document.querySelectorAll('#grammarNavTabs button');
    gTabs.forEach(btn => {
      btn.addEventListener('click', () => {
        gTabs.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const target = btn.getAttribute('data-gtab');
        document.getElementById('gTabFaults').style.display = target === 'faults' ? 'block' : 'none';
        document.getElementById('gTabSentences').style.display = target === 'sentences' ? 'block' : 'none';
        document.getElementById('gTabReconstructed').style.display = target === 'reconstructed' ? 'block' : 'none';
      });
    });
"""

# Append JS Functions and update renderCompleteTelemetry
if "function renderScoreFaultAudit" not in content:
    content = content.replace("initTheme();", JS_FUNCTIONS + "\n    initTheme();")

# Update renderCompleteTelemetry to call renderScoreFaultAudit and renderGrammarStudio
if "renderScoreFaultAudit(data.score_audit" not in content:
    needle = "valReadiness.textContent = `${overallAvg}/100`;"
    repl = """valReadiness.textContent = `${data.overall_score || overallAvg}/100`;

      // Render Dynamic Fault-Driven Score HUD
      renderScoreFaultAudit(data.score_audit, data.scores);

      // Render Spoken Grammar & Syntactic Analysis Studio
      renderGrammarStudio(data.grammar);"""
    content = content.replace(needle, repl)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[+] Successfully injected Score Audit HUD and Grammar Analysis Studio into frontend/index.html!")
