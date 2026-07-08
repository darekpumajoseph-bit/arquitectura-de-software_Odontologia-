// ============================================
// PROVEEDORES.JS - Gestión de Proveedores
// ============================================

const API = "http://127.0.0.1:8000";

// ── Toast ──────────────────────────────────────────────────────────────────
function toast(msg, tipo = "success") {
  const t = document.getElementById("toast");
  if (!t) return;
  t.textContent = msg;
  t.className = `toast show ${tipo}`;
  setTimeout(() => t.classList.remove("show"), 3500);
}
window.toast = toast;

// ── API ──────────────────────────────────────────────────────────────────
async function api(method, path, body = null) {
  const res = await fetch(`${API}${path}`, {
    method,
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : null,
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Error ${res.status}`);
  }
  return res.status === 204 ? null : res.json();
}

// ── Cargar proveedores ──────────────────────────────────────────────────
async function cargarProveedores() {
  try {
    const lista = await api("GET", "/proveedores");
    const tbody = document.getElementById("tablaProveedores");
    const colores = { "Vigente": "green", "Vencido": "red", "Suspendido": "yellow" };
    
    if (!lista.length) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:30px;color:var(--text-muted)">Sin proveedores registrados</td></tr>`;
      return;
    }
    
    tbody.innerHTML = lista.map(p => `
      <tr>
        <td><strong>${p.empresa}</strong></td>
        <td>${p.contacto_asesor || '—'}</td>
        <td>${p.telefono || '—'}</td>
        <td>${p.suministro || '—'}</td>
        <td><span class="badge ${colores[p.estado_convenio] || 'green'}">${p.estado_convenio}</span></td>
        <td>
          <button class="btn-icon" onclick="editarProveedor(${p.id})"><span class="material-symbols-outlined">edit</span></button>
          <button class="btn-danger" onclick="eliminarProveedor(${p.id})"><span class="material-symbols-outlined">delete</span></button>
        </td>
      </tr>
    `).join("");
  } catch (error) {
    toast("❌ No se pudo conectar con la API", "error");
    console.error(error);
  }
}

// ── Modal ──────────────────────────────────────────────────────────────────
function abrirModal() {
  document.getElementById("editId").value = "";
  document.getElementById("modalTitulo").textContent = "Registrar Proveedor";
  ["inEmpresa","inContacto","inTelefono","inSuministro"].forEach(id => document.getElementById(id).value = "");
  document.getElementById("inEstado").value = "Vigente";
  document.getElementById("modalProveedor").classList.add("open");
}
window.abrirModal = abrirModal;

function cerrarModal() {
  document.getElementById("modalProveedor").classList.remove("open");
}
window.cerrarModal = cerrarModal;

// ── Editar proveedor ──────────────────────────────────────────────────────
async function editarProveedor(id) {
  try {
    const p = await api("GET", `/proveedores/${id}`);
    document.getElementById("editId").value = p.id;
    document.getElementById("modalTitulo").textContent = "Editar Proveedor";
    document.getElementById("inEmpresa").value = p.empresa;
    document.getElementById("inContacto").value = p.contacto_asesor || "";
    document.getElementById("inTelefono").value = p.telefono || "";
    document.getElementById("inSuministro").value = p.suministro || "";
    document.getElementById("inEstado").value = p.estado_convenio;
    document.getElementById("modalProveedor").classList.add("open");
  } catch (error) {
    toast("❌ Error al cargar el proveedor", "error");
  }
}
window.editarProveedor = editarProveedor;

// ── Guardar proveedor ──────────────────────────────────────────────────────
async function guardarProveedor() {
  const id = document.getElementById("editId").value;
  const data = {
    empresa: document.getElementById("inEmpresa").value,
    contacto_asesor: document.getElementById("inContacto").value,
    telefono: document.getElementById("inTelefono").value,
    suministro: document.getElementById("inSuministro").value,
    estado_convenio: document.getElementById("inEstado").value
  };
  
  try {
    if (id) {
      await api("PUT", `/proveedores/${id}`, data);
      toast("✅ Proveedor actualizado correctamente");
    } else {
      await api("POST", "/proveedores", data);
      toast("✅ Proveedor registrado correctamente");
    }
    cerrarModal();
    cargarProveedores();
  } catch(error) {
    toast(`❌ ${error.message}`, "error");
  }
}
window.guardarProveedor = guardarProveedor;

// ── Eliminar proveedor ──────────────────────────────────────────────────
async function eliminarProveedor(id) {
  if (!confirm("¿Eliminar este proveedor?")) return;
  try {
    await api("DELETE", `/proveedores/${id}`);
    toast("✅ Proveedor eliminado correctamente");
    cargarProveedores();
  } catch(error) {
    toast(`❌ ${error.message}`, "error");
  }
}
window.eliminarProveedor = eliminarProveedor;

// ── Inicio ─────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
  const usuarioActual = JSON.parse(localStorage.getItem('usuario_actual') || 'null');
  if (!usuarioActual) {
    window.location.href = "login.html";
  }
  cargarProveedores();
});