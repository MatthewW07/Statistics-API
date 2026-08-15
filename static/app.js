const state = { file: null, heatmap: null, numerical: null, categorical: null, selectedCell: null };
const $ = (selector) => document.querySelector(selector);

function format(value) {
  if (value === null || value === undefined) return "—";
  if (typeof value === "number") return Number.isInteger(value) ? value.toLocaleString() : value.toLocaleString(undefined, { maximumFractionDigits: 4 });
  if (typeof value === "object") return `${Object.keys(value).length} categories`;
  return String(value);
}

async function request(url, options) {
  const res = await fetch(url, options);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || "Request failed");
  return data;
}

function relationshipColor(value) {
  if (value === null || Number.isNaN(value)) return "#d9ded9";
  const n = Math.max(-1, Math.min(1, value));
  const low = n < 0 ? [36, 82, 166] : [220, 91, 63];
  const t = Math.abs(n);
  const base = [245, 244, 239];
  return `rgb(${base.map((v, i) => Math.round(v + (low[i] - v) * t)).join(",")})`;
}

function getPair(x, y) {
  return state.heatmap.pair_details[`${x}|${y}`] || state.heatmap.pair_details[`${y}|${x}`];
}

function showPair(x, y, value, button) {
  if (state.selectedCell) state.selectedCell.classList.remove("selected");
  state.selectedCell = button;
  button.classList.add("selected");
  const pair = getPair(x, y);
  const metrics = Object.entries(pair.metrics).map(([name, metric]) => `<li><span>${name.replaceAll("-", " ")}</span><strong>${format(metric)}</strong></li>`).join("");
  $("#pair-detail").innerHTML = `<p class="eyebrow">${pair.type.replaceAll("_", " ")}</p><h3>${x} × ${y}</h3><p class="muted">Displayed association: <strong>${format(value)}</strong></p><ul class="metric-list">${metrics}</ul>`;
}

function renderHeatmap() {
  const { variables, correlation_matrix: matrix } = state.heatmap;
  const grid = $("#heatmap-grid");
  grid.className = "heat-grid";
  grid.style.gridTemplateColumns = `125px repeat(${variables.length}, 31px)`;
  grid.innerHTML = '<div class="hm-label top"></div>' + variables.map((name) => `<div class="hm-label top" title="${name}">${name}</div>`).join("");
  variables.forEach((x, i) => {
    grid.insertAdjacentHTML("beforeend", `<div class="hm-label left" title="${x}">${x}</div>`);
    variables.forEach((y, j) => {
      const value = matrix[i][j];
      const cell = document.createElement("button");
      cell.className = "hm-cell";
      cell.style.background = relationshipColor(value);
      cell.title = `${x} × ${y}: ${format(value)}`;
      cell.setAttribute("aria-label", cell.title);
      cell.addEventListener("click", () => showPair(x, y, value, cell));
      grid.appendChild(cell);
    });
  });
}

function renderTable(tableId, data) {
  const table = document.getElementById(tableId);
  const columns = data.columns;
  const rows = data.variables.map((variable) => ({ variable, ...data.statistics[variable] }));
  let sort = { key: "variable", direction: 1 };

  function draw(filter = "") {
    const filtered = rows.filter((row) => row.variable.toLowerCase().includes(filter.toLowerCase()));
    filtered.sort((a, b) => {
      const left = a[sort.key], right = b[sort.key];
      return typeof left === "number" && typeof right === "number" ? sort.direction * (left - right) : sort.direction * String(left ?? "").localeCompare(String(right ?? ""));
    });
    table.innerHTML = `<thead><tr><th><button data-key="variable">Variable</button></th>${columns.map((c) => `<th title="${c.description || ""}"><button data-key="${c.key}">${c.label} ${sort.key === c.key ? (sort.direction === 1 ? "↑" : "↓") : ""}</button></th>`).join("")}</tr></thead><tbody>${filtered.map((row) => `<tr><td>${row.variable}</td>${columns.map((c) => `<td>${c.key === "categories" && typeof row[c.key] === "object" ? `<span class="category-pill">${format(row[c.key])}</span>` : format(row[c.key])}</td>`).join("")}</tr>`).join("") || `<tr><td colspan="${columns.length + 1}">No matching variables.</td></tr>`}</tbody>`;
    table.querySelectorAll("button[data-key]").forEach((button) => button.addEventListener("click", () => {
      const key = button.dataset.key;
      sort = { key, direction: sort.key === key ? -sort.direction : 1 };
      draw(document.querySelector(`[data-table="${tableId}"]`).value);
    }));
  }
  draw();
  document.querySelector(`[data-table="${tableId}"]`).oninput = (event) => draw(event.target.value);
}

async function analyze(file) {
  $("#analyze-button").textContent = "Analyzing…";
  $("#analyze-button").disabled = true;
  const form = new FormData(); form.append("file", file);
  const uploaded = await request("/upload", { method: "POST", body: form });
  state.file = uploaded.file;
  const arg = `?file=${encodeURIComponent(state.file)}`;
  [state.heatmap, state.numerical, state.categorical] = await Promise.all([request(`/heatmap${arg}`), request(`/num_table${arg}`), request(`/cat_table${arg}`)]);
  $("#dataset-name").textContent = uploaded.original_filename;
  renderHeatmap(); renderTable("numerical-table", state.numerical); renderTable("categorical-table", state.categorical);
  $("#upload-view").hidden = true; $("#analysis-view").hidden = false;
}

const input = $("#csv-file"), zone = $("#drop-zone"), form = $("#upload-form");
input.addEventListener("change", () => { $("#analyze-button").disabled = !input.files.length; if (input.files.length) zone.querySelector("strong").textContent = input.files[0].name; });
["dragenter", "dragover"].forEach((event) => zone.addEventListener(event, (e) => { e.preventDefault(); zone.classList.add("dragging"); }));
["dragleave", "drop"].forEach((event) => zone.addEventListener(event, (e) => { e.preventDefault(); zone.classList.remove("dragging"); }));
zone.addEventListener("drop", (event) => { input.files = event.dataTransfer.files; input.dispatchEvent(new Event("change")); });
form.addEventListener("submit", async (event) => { event.preventDefault(); $("#upload-error").textContent = ""; try { await analyze(input.files[0]); } catch (error) { $("#upload-error").textContent = error.message; $("#analyze-button").textContent = "Analyze dataset →"; $("#analyze-button").disabled = false; } });
$("#new-file").addEventListener("click", () => { $("#analysis-view").hidden = true; $("#upload-view").hidden = false; input.value = ""; zone.querySelector("strong").textContent = "Choose a CSV"; });
document.querySelectorAll(".tab").forEach((tab) => tab.addEventListener("click", () => { document.querySelectorAll(".tab,.panel").forEach((el) => el.classList.remove("active")); tab.classList.add("active"); document.getElementById(tab.dataset.view).classList.add("active"); }));
