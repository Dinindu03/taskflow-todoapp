const state = { tasks: [], filter: "all", editingId: null };
const $ = (selector) => document.querySelector(selector);

function csrfToken() {
  return document.cookie.split("; ").find((cookie) => cookie.startsWith("taskflow_csrf="))?.split("=")[1] || "";
}

function showMessage(text, type = "error") {
  const element = $("#dashboard-message");
  element.textContent = text;
  element.className = `mb-6 rounded-xl border px-4 py-3 text-sm ${type === "success" ? "border-emerald-200 bg-emerald-50 text-emerald-700" : "border-red-200 bg-red-50 text-red-700"}`;
}

function clearMessage() {
  $("#dashboard-message").className = "mb-6 hidden rounded-xl border px-4 py-3 text-sm";
}

async function api(path, options = {}) {
  const headers = { ...(options.body ? { "Content-Type": "application/json" } : {}), ...(options.headers || {}) };
  if (options.method && options.method !== "GET") {
    headers["X-CSRF-Token"] = decodeURIComponent(csrfToken());
  }
  const response = await fetch(path, { ...options, headers, credentials: "include" });
  if (response.status === 401) {
    window.location.href = "/";
    throw new Error("Your session has expired.");
  }
  if (!response.ok) {
    let detail = "Unable to complete that request.";
    try {
      const body = await response.json();
      detail = body.error?.message || (typeof body.detail === "string" ? body.detail : detail);
    } catch {
      // Keep the user-facing fallback for non-JSON responses.
    }
    throw new Error(detail);
  }
  return response.status === 204 ? null : response.json();
}

function renderStats(stats) {
  $("#total-count").textContent = stats.total;
  $("#pending-count").textContent = stats.pending;
  $("#completed-count").textContent = stats.completed;
}

async function refreshStats() {
  renderStats(await api("/api/dashboard/stats"));
}

function visibleTasks() {
  return state.tasks.filter((task) => state.filter === "all" || (state.filter === "completed" ? task.completed : !task.completed));
}

function renderTasks() {
  const list = $("#task-list");
  const tasks = visibleTasks();
  $("#task-loading").classList.add("hidden");
  $("#empty-state").classList.toggle("hidden", tasks.length !== 0);
  list.innerHTML = tasks.map((task) => `
    <article class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:p-5">
      <div class="flex items-start gap-3">
        <button data-action="toggle" data-id="${task.id}" type="button" class="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full border-2 ${task.completed ? "border-emerald-500 bg-emerald-500 text-white" : "border-slate-300 text-transparent"}" aria-label="${task.completed ? "Mark task pending" : "Mark task complete"}">✓</button>
        <div class="min-w-0 flex-1">
          <h4 class="${task.completed ? "text-slate-400 line-through" : "text-slate-900"} break-words font-semibold">${escapeHtml(task.title)}</h4>
          ${task.description ? `<p class="mt-1 break-words text-sm text-slate-500">${escapeHtml(task.description)}</p>` : ""}
        </div>
        <div class="flex shrink-0 gap-1">
          <button data-action="edit" data-id="${task.id}" type="button" class="rounded-lg px-2 py-1.5 text-sm font-medium text-slate-500 hover:bg-violet-50 hover:text-violet-700">Edit</button>
          <button data-action="delete" data-id="${task.id}" type="button" class="rounded-lg px-2 py-1.5 text-sm font-medium text-slate-500 hover:bg-red-50 hover:text-red-600">Delete</button>
        </div>
      </div>
    </article>`).join("");
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" })[character]);
}

function openForm(task = null) {
  state.editingId = task?.id || null;
  $("#task-form-title").textContent = task ? "Edit task" : "Create a task";
  $("#save-task-label").textContent = task ? "Save changes" : "Save task";
  $("#task-title").value = task?.title || "";
  $("#task-description").value = task?.description || "";
  $("#task-title-error").classList.add("hidden");
  $("#task-form-section").classList.remove("hidden");
  $("#task-title").focus();
}

function closeForm() {
  state.editingId = null;
  $("#task-form-section").classList.add("hidden");
  $("#task-form").reset();
}

async function loadDashboard() {
  try {
    const [user, stats, tasks] = await Promise.all([api("/api/auth/me"), api("/api/dashboard/stats"), api("/api/todos")]);
    $("#sidebar-user").textContent = `${user.name} · ${user.email}`;
    $("#header-user").textContent = user.name;
    renderStats(stats);
    state.tasks = tasks;
    renderTasks();
  } catch (error) {
    if (error.message !== "Your session has expired.") showMessage(error.message);
  }
}

async function saveTask(event) {
  event.preventDefault();
  const title = $("#task-title").value.trim();
  if (!title) {
    $("#task-title-error").textContent = "Please enter a task title.";
    $("#task-title-error").classList.remove("hidden");
    return;
  }
  $("#save-task-button").disabled = true;
  $("#save-task-spinner").classList.remove("hidden");
  const editing = Boolean(state.editingId);
  try {
    const payload = { title, description: $("#task-description").value.trim() };
    const task = await api(editing ? `/api/todos/${state.editingId}` : "/api/todos", { method: editing ? "PUT" : "POST", body: JSON.stringify(payload) });
    if (editing) state.tasks = state.tasks.map((item) => item.id === task.id ? task : item);
    else state.tasks.unshift(task);
    closeForm();
    renderTasks();
    await refreshStats();
    showMessage(editing ? "Task updated." : "Task created.", "success");
  } catch (error) {
    showMessage(error.message);
  } finally {
    $("#save-task-button").disabled = false;
    $("#save-task-spinner").classList.add("hidden");
  }
}

async function handleTaskAction(event) {
  const button = event.target.closest("button[data-action]");
  if (!button) return;
  const task = state.tasks.find((item) => item.id === button.dataset.id);
  if (!task) return;
  try {
    if (button.dataset.action === "edit") return openForm(task);
    if (button.dataset.action === "delete") {
      if (!window.confirm(`Delete "${task.title}"?`)) return;
      await api(`/api/todos/${task.id}`, { method: "DELETE" });
      state.tasks = state.tasks.filter((item) => item.id !== task.id);
      showMessage("Task deleted.", "success");
    } else {
      const updated = await api(`/api/todos/${task.id}/${task.completed ? "pending" : "complete"}`, { method: "PATCH" });
      state.tasks = state.tasks.map((item) => item.id === updated.id ? updated : item);
    }
    renderTasks();
    await refreshStats();
  } catch (error) {
    showMessage(error.message);
  }
}

async function logout() {
  try {
    await api("/api/auth/logout", { method: "POST" });
    window.location.href = "/";
  } catch (error) {
    showMessage(error.message);
  }
}

$("#new-task-button").addEventListener("click", () => openForm());
$("#cancel-task-button").addEventListener("click", closeForm);
$("#cancel-task-button-bottom").addEventListener("click", closeForm);
$("#task-form").addEventListener("submit", saveTask);
$("#task-list").addEventListener("click", handleTaskAction);
$("#logout-button").addEventListener("click", logout);
$("#header-logout").addEventListener("click", logout);
document.querySelectorAll(".filter-button").forEach((button) => button.addEventListener("click", () => {
  state.filter = button.dataset.filter;
  document.querySelectorAll(".filter-button").forEach((item) => item.className = "filter-button rounded-lg px-3 py-1.5 text-sm font-semibold text-slate-500 hover:bg-slate-50");
  button.className = "filter-button rounded-lg bg-violet-100 px-3 py-1.5 text-sm font-semibold text-violet-700";
  renderTasks();
}));

const sidebar = $("#sidebar");
const backdrop = $("#sidebar-backdrop");
function toggleSidebar(open) {
  sidebar.classList.toggle("-translate-x-full", !open);
  backdrop.classList.toggle("hidden", !open);
}
$("#open-sidebar").addEventListener("click", () => toggleSidebar(true));
$("#close-sidebar").addEventListener("click", () => toggleSidebar(false));
backdrop.addEventListener("click", () => toggleSidebar(false));
loadDashboard();
