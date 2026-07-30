// Core State
let ventures = [];
let currentSortMode = "score_desc";
let currentSearchFilter = "";
let currentViewMode = "cards";

// DOM Elements
const ventureGrid = document.getElementById("ventureGrid");
const ventureTableContainer = document.getElementById("ventureTableContainer");
const ventureTableBody = document.getElementById("ventureTableBody");
const viewCardBtn = document.getElementById("viewCardBtn");
const viewTableBtn = document.getElementById("viewTableBtn");
const loadingState = document.getElementById("loadingState");
const emptyState = document.getElementById("emptyState");
const searchInput = document.getElementById("searchInput");
const sortSelect = document.getElementById("sortSelect");
const suggestionsContainer = document.getElementById("suggestionsContainer");
const addVentureBtn = document.getElementById("addVentureBtn");

const detailModal = document.getElementById("detailModal");
const closeDetailBtn = document.getElementById("closeDetailBtn");
const detailModalBody = document.getElementById("detailModalBody");

const addModal = document.getElementById("addModal");
const closeAddBtn = document.getElementById("closeAddBtn");
const cancelAddBtn = document.getElementById("cancelAddBtn");
const addVentureForm = document.getElementById("addVentureForm");
const addLoadingState = document.getElementById("addLoadingState");
const submitVentureBtn = document.getElementById("submitVentureBtn");

const guideBtn = document.getElementById("guideBtn");

// API Base URL (Dynamic for local vs Cloudflare/Cloud Run deployments)
const isLocal =
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1";
const API_BASE = isLocal
  ? "/api/ventures"
  : "https://asme-ventures-backend-963557792569.us-central1.run.app/api/ventures";

// Score mappings
const SCORE_COLORS = {
  exceptional: "#10b981", // green
  strong: "#06b6d4", // cyan
  promising: "#8b5cf6", // purple
  average: "#f59e0b", // yellow
  weak: "#f97316", // orange
  poor: "#ef4444", // red
};

function getScoreColor(score) {
  if (score >= 4.5) return SCORE_COLORS.exceptional;
  if (score >= 4.0) return SCORE_COLORS.strong;
  if (score >= 3.5) return SCORE_COLORS.promising;
  if (score >= 2.5) return SCORE_COLORS.average;
  if (score >= 1.5) return SCORE_COLORS.weak;
  return SCORE_COLORS.poor;
}

function getScoreLabel(score) {
  if (score >= 4.5) return "Exceptional";
  if (score >= 4.0) return "Strong";
  if (score >= 3.5) return "Promising";
  if (score >= 2.5) return "Average";
  if (score >= 1.5) return "Weak";
  return "Poor";
}

// Format sub-score names
const SCORE_LABELS = {
  focus_area_alignment: "Focus Area Alignment",
  built_world_impact: "Built World Impact",
  engineering_innovation: "Engineering Innovation",
  early_stage_fit: "Early-Stage Fit",
  asme_synergy: "ASME Synergy",
};

// Event Listeners
document.addEventListener("DOMContentLoaded", fetchVentures);
searchInput.addEventListener("input", (e) => {
  currentSearchFilter = e.target.value.toLowerCase();
  renderVentures();
});
sortSelect.addEventListener("change", (e) => {
  currentSortMode = e.target.value;
  sortVentures();
  renderVentures();
});

document.querySelectorAll(".suggestion-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const name = btn.getAttribute("data-name");
    const url = btn.getAttribute("data-url");
    btn.disabled = true;
    btn.textContent = "Analyzing...";
    analyzeVentureTrigger(name, url, "").then(() => {
        btn.style.display = "none";
    });
  });
});
addVentureBtn.addEventListener("click", openAddForm);

closeDetailBtn.addEventListener("click", closeModal);
closeAddBtn.addEventListener("click", closeModal);
cancelAddBtn.addEventListener("click", closeModal);
// Interactive Tour setup
const driver = window.driver.js.driver;
const tour = driver({
  showProgress: true,
  animate: true,
  steps: [
    {
      popover: {
        title: 'Augmenting Venture Intelligence',
        description: `
          <div style="margin-bottom: 16px;">
            By automating the initial scanning, identification, and screening phases, human decision-makers can spend more time reviewing high-quality candidates instead of sifting through the noise.
            <br><br>
            <span style="color: var(--text-muted); font-size: 13.5px; font-style: italic;">
              Future versions of this prototype could be upgraded to run 24 hours a day, continuously analyzing hundreds of organizations and autonomously notifying you when a candidate scores high enough for human review.
            </span>
          </div>
          <div class="flow-graphic">
            <div class="flow-step">
              <span class="icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
              </span>
              <span class="text">1. Input URL</span>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-step">
              <span class="icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>
              </span>
              <span class="text">2. AI Researches & Grades</span>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-step highlight">
              <span class="icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
              </span>
              <span class="text">3. Human Review</span>
            </div>
          </div>
        `,
        side: "over",
        align: 'center'
      }
    },
    {
      element: '#suggestionsContainer',
      popover: {
        title: '1. Try an Example',
        description: 'Click one of these highlighted suggestions to watch the AI instantly crawl the web and fully analyze the company in real-time.',
        side: "bottom",
        align: 'start'
      }
    },
    {
      element: '#addVentureBtn',
      popover: {
        title: '2. Add Custom Venture',
        description: 'Or, click here to add any custom startup you want. Give it a name and URL, and the AI will do the rest!',
        side: "bottom",
        align: 'end'
      }
    }
  ]
});

guideBtn.addEventListener("click", () => {
  tour.drive();
});

// Close modals on backdrop click
document.querySelectorAll(".modal-backdrop").forEach((backdrop) => {
  backdrop.addEventListener("click", closeModal);
});

viewCardBtn.addEventListener("click", () => setViewMode("cards"));
viewTableBtn.addEventListener("click", () => setViewMode("table"));

// Check if user has seen guide
if (!localStorage.getItem("hasSeenTour")) {
  localStorage.setItem("hasSeenTour", "true");
  setTimeout(() => tour.drive(), 500);
}

addVentureForm.addEventListener("submit", submitVenture);

// Core Functions
async function fetchVentures() {
  showLoading(true);
  try {
    const response = await fetch(API_BASE);
    if (response.ok) {
      const data = await response.json();
      ventures = data.ventures || [];
      sortVentures();
      renderVentures();
    } else {
      console.error("Failed to fetch ventures");
      ventures = [];
      renderVentures();
    }
  } catch (error) {
    console.error("Error fetching ventures:", error);
    ventures = [];
    renderVentures();
  } finally {
    showLoading(false);
  }
}

function sortVentures() {
  ventures.sort((a, b) => {
    // Pending items always go to the bottom unless sorting specifically puts them elsewhere, but usually we just handle missing scores
    const scoreA = a.overall_score || 0;
    const scoreB = b.overall_score || 0;

    switch (currentSortMode) {
      case "score_desc":
        return scoreB - scoreA;
      case "score_asc":
        return scoreA - scoreB;
      case "name_asc":
        return a.name.localeCompare(b.name);
      case "sector":
        const secA = a.sector || "";
        const secB = b.sector || "";
        return secA.localeCompare(secB);
      default:
        return 0;
    }
  });
}

function renderVentures() {
  updateSuggestionsVisibility();

  const filtered = ventures.filter((v) => {
    const searchStr = currentSearchFilter;
    if (!searchStr) return true;
    const nameMatch = v.name && v.name.toLowerCase().includes(searchStr);
    const sectorMatch = v.sector && v.sector.toLowerCase().includes(searchStr);
    return nameMatch || sectorMatch;
  });

  ventureGrid.innerHTML = "";
  ventureTableBody.innerHTML = "";

  if (filtered.length === 0) {
    if (ventures.length === 0) {
      emptyState.classList.remove("hidden");
    } else {
      emptyState.classList.add("hidden");
      ventureGrid.innerHTML =
        '<p style="color:var(--text-secondary); grid-column: 1/-1; text-align: center;">No matches found.</p>';
      ventureTableBody.innerHTML =
        '<tr><td colspan="5" style="text-align: center;">No matches found.</td></tr>';
    }
    return;
  }

  emptyState.classList.add("hidden");
  filtered.forEach((venture) => {
    ventureGrid.appendChild(createCardElement(venture));
    ventureTableBody.appendChild(createTableRowElement(venture));
  });
}

function setViewMode(mode) {
  currentViewMode = mode;
  if (mode === "cards") {
    viewCardBtn.classList.add("active");
    viewTableBtn.classList.remove("active");
    ventureGrid.classList.remove("hidden");
    ventureTableContainer.classList.add("hidden");
  } else {
    viewTableBtn.classList.add("active");
    viewCardBtn.classList.remove("active");
    ventureTableContainer.classList.remove("hidden");
    ventureGrid.classList.add("hidden");
  }
}

function createCardElement(venture) {
  const card = document.createElement("div");
  card.className = "card";
  card.onclick = () => openDetail(venture.id);

  const isPending = venture.status === "pending" || !venture.overall_score;
  let scoreHtml = "";

  if (isPending) {
    scoreHtml = `<div class="score-badge" style="background-color: var(--text-muted)">Pending</div>`;
  } else {
    const score = parseFloat(venture.overall_score).toFixed(1);
    const color = getScoreColor(score);
    const label = getScoreLabel(score);
    scoreHtml = `<div class="score-badge" style="background-color: ${color}">${score} — ${label}</div>`;
  }

  card.innerHTML = `
        <div class="card-header">
            <h3 class="card-title" style="margin-bottom: 0;">${escapeHtml(venture.name)}</h3>
            ${scoreHtml}
        </div>
        <div class="card-sector">
            ${escapeHtml(venture.sector || "Unknown Sector")}
        </div>
        <div class="card-meta">
            ${escapeHtml(venture.location || "Unknown Location")} • Founded ${venture.founding_year || "Unknown"} • ${escapeHtml(venture.funding_stage || "Unknown Stage")}
        </div>
        <div class="card-rationale">
            ${isPending ? "Analysis in progress..." : escapeHtml(venture.rationale || "No rationale available.")}
        </div>
    `;

  return card;
}

function createTableRowElement(venture) {
  const tr = document.createElement("tr");
  tr.onclick = () => openDetail(venture.id);

  const isPending = venture.status === "pending" || !venture.overall_score;
  let scoreHtml = "";

  if (isPending) {
    scoreHtml = `<div class="score-badge" style="background-color: var(--text-muted); display: inline-block;">Pending</div>`;
  } else {
    const score = parseFloat(venture.overall_score).toFixed(1);
    const color = getScoreColor(score);
    const label = getScoreLabel(score);
    scoreHtml = `<div class="score-badge" style="background-color: ${color}; display: inline-block;">${score} — ${label}</div>`;
  }

  tr.innerHTML = `
        <td style="font-weight: 500;">${escapeHtml(venture.name)}</td>
        <td>${escapeHtml(venture.sector || "-")}</td>
        <td style="color: var(--text-secondary); max-width: 300px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${escapeHtml(venture.rationale || (isPending ? "Analysis in progress..." : "-"))}</td>
        <td>${scoreHtml}</td>
    `;
  return tr;
}

async function openDetail(ventureId) {
  const venture = ventures.find((v) => v.id === ventureId);
  if (!venture) return;

  // Optional: Fetch latest detail if API provides more info
  // const res = await fetch(`${API_BASE}/${ventureId}`);
  // const fullVenture = await res.json();

  renderDetailModal(venture);
  detailModal.classList.remove("hidden");
}

function renderDetailModal(venture) {
  const isPending = venture.status === "pending" || !venture.overall_score;

  let scoreHeaderHtml = "";
  if (isPending) {
    scoreHeaderHtml = `<div class="score-badge detail-score-large" style="background-color: var(--text-muted)">Pending Analysis</div>`;
  } else {
    const score = parseFloat(venture.overall_score).toFixed(1);
    const color = getScoreColor(score);
    const label = getScoreLabel(score);
    scoreHeaderHtml = `<div class="score-badge detail-score-large" style="background-color: ${color}">${score} — ${label}</div>`;
  }

  let scoresHtml = "";
  if (!isPending && venture.scores) {
    let scoresObj = venture.scores;
    if (typeof scoresObj === "string") {
      try {
        scoresObj = JSON.parse(scoresObj);
      } catch (e) {}
    }

    for (const [key, val] of Object.entries(scoresObj)) {
      const labelName = SCORE_LABELS[key] || key;
      const scoreVal = parseInt(val) || 0;
      const barColor = getScoreColor(scoreVal);

      let bars = "";
      for (let i = 1; i <= 5; i++) {
        if (i <= scoreVal) {
          bars += `<div class="subscore-bar-segment filled" style="background-color: ${barColor}"></div>`;
        } else {
          bars += `<div class="subscore-bar-segment"></div>`;
        }
      }

      scoresHtml += `
                <div class="subscore-item">
                    <div class="subscore-header">
                        <span>${escapeHtml(labelName)}</span>
                        <strong>${scoreVal}/5</strong>
                    </div>
                    <div class="subscore-bars">
                        ${bars}
                    </div>
                </div>
            `;
    }
  }

  let strengthsHtml = "";
  if (venture.strengths) {
    let stArr = venture.strengths;
    if (typeof stArr === "string") {
      try {
        stArr = JSON.parse(stArr);
      } catch (e) {
        stArr = [stArr];
      }
    }
    if (Array.isArray(stArr) && stArr.length > 0) {
      strengthsHtml = `<ul class="bullet-list">${stArr.map((s) => `<li>${escapeHtml(s)}</li>`).join("")}</ul>`;
    }
  }

  let weaknessesHtml = "";
  if (venture.weaknesses) {
    let wkArr = venture.weaknesses;
    if (typeof wkArr === "string") {
      try {
        wkArr = JSON.parse(wkArr);
      } catch (e) {
        wkArr = [wkArr];
      }
    }
    if (Array.isArray(wkArr) && wkArr.length > 0) {
      weaknessesHtml = `<ul class="bullet-list">${wkArr.map((w) => `<li>${escapeHtml(w)}</li>`).join("")}</ul>`;
    }
  }

  detailModalBody.innerHTML = `
        <div class="detail-header">
            <div>
                <div style="display: flex; align-items: center; gap: 12px;">
                    <h2 class="detail-title">${escapeHtml(venture.name)}</h2>
                    <button class="btn btn-secondary" style="padding: 4px 12px; font-size: 12px; border-color: #ef4444; color: #ef4444;" onclick="deleteVenture(${venture.id})">Delete</button>
                </div>
                ${venture.website ? `<a href="${escapeHtml(venture.website)}" target="_blank" class="detail-website">${escapeHtml(venture.website)}</a>` : ""}
                <div class="detail-meta">
                    <span>${escapeHtml(venture.sector || "Unknown")}</span>
                    <span>${escapeHtml(venture.location || "Unknown")}</span>
                    <span>Team: ${venture.team_size || "Unknown"}</span>
                    <span>Stage: ${escapeHtml(venture.funding_stage || "Unknown")}</span>
                </div>
            </div>
            ${scoreHeaderHtml}
        </div>
        
        ${
          isPending
            ? '<div class="detail-section"><p>This venture is currently being analyzed.</p></div>'
            : `
            <div class="detail-section" style="display: grid; grid-template-columns: 1fr 1fr; gap: 32px;">
                <div>
                    <h3>Overall Rationale</h3>
                    <p style="font-size: 15px;">${escapeHtml(venture.rationale || "N/A")}</p>
                </div>
                <div>
                    <h3>Scoring Breakdown</h3>
                    ${scoresHtml}
                </div>
            </div>

            <div class="detail-section" style="display: grid; grid-template-columns: 1fr 1fr; gap: 32px;">
                <div>
                    <h3>Strengths</h3>
                    ${strengthsHtml || '<p class="text-muted">None identified.</p>'}
                </div>
                <div>
                    <h3>Weaknesses / Risks</h3>
                    ${weaknessesHtml || '<p class="text-muted">None identified.</p>'}
                </div>
            </div>
            
            <div class="detail-section" style="margin-top: 24px; padding-top: 24px; border-top: 1px solid var(--border-color);">
                <h3>Deep Dive: Assessment Data</h3>
                <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 16px;">
                    Structured data extracted by the AI model.
                </p>
                <div style="background: var(--bg-dark); padding: 16px; border-radius: 8px; font-size: 14px; font-family: monospace; white-space: pre-wrap; color: var(--text-secondary); max-height: 200px; overflow-y: auto; margin-bottom: 16px;">
                    ${venture.enrichment_data ? escapeHtml(typeof venture.enrichment_data === "string" ? venture.enrichment_data : JSON.stringify(venture.enrichment_data, null, 2)) : "No structured data available."}
                </div>
                
                <button class="btn btn-secondary" onclick="document.getElementById('rawTavilyData-${venture.id}').classList.toggle('hidden')" style="width: 100%; margin-bottom: 12px; font-size: 14px;">
                    👁️ Reveal Raw Tavily Search Data
                </button>
                <div id="rawTavilyData-${venture.id}" class="hidden" style="background: #111827; border: 1px solid #374151; padding: 16px; border-radius: 8px; font-size: 12px; font-family: monospace; white-space: pre-wrap; color: #9ca3af; max-height: 400px; overflow-y: auto;">
                    ${venture.enrichment_data && venture.enrichment_data.raw_tavily_data ? escapeHtml(venture.enrichment_data.raw_tavily_data) : "No raw search data available. (You may need to re-analyze this venture)."}
                </div>
            </div>
        `
        }
    `;
}

function openAddForm() {
  addVentureForm.reset();
  addLoadingState.classList.add("hidden");
  submitVentureBtn.disabled = false;
  addModal.classList.remove("hidden");
}

function closeModal() {
  detailModal.classList.add("hidden");
  addModal.classList.add("hidden");
}

async function analyzeVentureTrigger(name, website, description) {
  // Create a temporary pending venture card instantly
  const tempId = Date.now();
  const pendingVenture = {
    id: tempId,
    name: name,
    website: website,
    sector: "AI Analysis in progress...",
    rationale: "Crawling the web, extracting signals, and grading against ASME criteria...",
    status: "pending",
    overall_score: null
  };
  
  ventures.unshift(pendingVenture);
  renderVentures();

  try {
    const res = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, website, description: description || "" }),
    });

    if (res.ok) {
      const updatedVenture = await res.json();
      ventures = ventures.map(v => v.id === tempId ? updatedVenture : v);
      sortVentures();
      renderVentures();
    } else {
      alert("Error analyzing venture.");
      ventures = ventures.filter(v => v.id !== tempId);
      renderVentures();
    }
  } catch (err) {
    console.error(err);
    alert("Network error analyzing venture.");
    ventures = ventures.filter(v => v.id !== tempId);
    renderVentures();
  }
}

async function submitVenture(e) {
  e.preventDefault();
  const name = document.getElementById("ventureName").value;
  const website = document.getElementById("ventureWebsite").value;
  const description = document.getElementById("ventureDescription").value;

  closeModal();
  analyzeVentureTrigger(name, website, description);
}

// Removed seedVentures logic for stakeholder demo

async function deleteVenture(id) {
  if (!confirm("Are you sure you want to delete this venture?")) return;

  try {
    const res = await fetch(`${API_BASE}/${id}`, { method: "DELETE" });
    if (res.ok) {
      closeModal();
      await fetchVentures();
    } else {
      alert("Failed to delete venture.");
    }
  } catch (err) {
    console.error(err);
    alert("Error deleting venture.");
  }
}

// Utils
function showLoading(show) {
  if (show) {
    loadingState.classList.remove("hidden");
    ventureGrid.classList.add("hidden");
    emptyState.classList.add("hidden");
  } else {
    loadingState.classList.add("hidden");
    ventureGrid.classList.remove("hidden");
  }
}

function escapeHtml(unsafe) {
  if (!unsafe) return "";
  return unsafe
    .toString()
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function updateSuggestionsVisibility() {
  if (!suggestionsContainer) return;
  const existingNames = ventures.map(v => v.name.toLowerCase());
  const suggestionBtns = document.querySelectorAll(".suggestion-btn");
  let anyVisible = false;
  
  suggestionBtns.forEach(btn => {
    const btnName = btn.getAttribute("data-name").toLowerCase();
    if (existingNames.includes(btnName)) {
      btn.style.display = "none";
    } else {
      btn.style.display = "inline-block";
      anyVisible = true;
    }
  });
  
  if (!anyVisible) {
    suggestionsContainer.style.display = "none";
  } else {
    suggestionsContainer.style.display = "flex";
  }
}
