// ============================================
// TRATAMIENTOS.JS - Gestión de Tratamientos
// ============================================

const API = "http://127.0.0.1:8000";
let tratamientoAEliminar = null;

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
    try {
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
    } catch (error) {
        console.error(`❌ Error en API ${method} ${path}:`, error);
        throw error;
    }
}

// ── Cargar tratamientos ──────────────────────────────────────────────────
async function cargarTratamientos() {
    try {
        console.log("🔄 Cargando tratamientos...");
        const lista = await api("GET", "/tratamientos");
        console.log("✅ Tratamientos cargados:", lista.length);
        renderTabla(lista);
    } catch (error) {
        console.error("❌ Error al cargar tratamientos:", error);
        toast("❌ No se pudo conectar con la API", "error");
        document.getElementById("tablaTratamientos").innerHTML = `
            <tr>
                <td colspan="5" style="text-align:center;padding:30px;color:var(--text-muted)">
                    ❌ Error al cargar los datos: ${error.message}
                </td>
            </tr>
        `;
    }
}
window.cargarTratamientos = cargarTratamientos;

// ── Renderizar tabla (con números consecutivos) ────────────────────────────
function renderTabla(lista) {
    const tbody = document.getElementById("tablaTratamientos");
    
    if (!lista || !lista.length) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;padding:30px;color:var(--text-muted)">Sin tratamientos registrados</td></tr>`;
        return;
    }

    // Ordenar por ID para mantener consistencia
    lista.sort((a, b) => a.id_tratamiento - b.id_tratamiento);

    tbody.innerHTML = lista.map((t, index) => `
        <tr>
            <td><strong>${index + 1}</strong></td>
            <td><strong>${t.nombre}</strong></td>
            <td>${t.descripcion || '—'}</td>
            <td>$${(t.costo || 0).toLocaleString('es-CO')}</td>
            <td>
                <button class="btn-icon" title="Editar" onclick="editarTratamiento(${t.id_tratamiento})">
                    <span class="material-symbols-outlined">edit</span>
                </button>
                <button class="btn-danger" title="Eliminar" onclick="abrirConfirmModal(${t.id_tratamiento}, '${t.nombre}', ${t.costo || 0})">
                    <span class="material-symbols-outlined">delete</span>
                </button>
            </td>
        </tr>
    `).join("");
}

// ── Modal ──────────────────────────────────────────────────────────────────
function abrirModal() {
    document.getElementById("editId").value = "";
    document.getElementById("modalTitulo").textContent = "Nuevo Tratamiento";
    document.getElementById("inNombre").value = "";
    document.getElementById("inDescripcion").value = "";
    document.getElementById("inPrecio").value = "";
    document.getElementById("btnGuardarTratamiento").disabled = false;
    document.getElementById("btnGuardarTratamiento").innerHTML = '<span class="material-symbols-outlined">save</span> Guardar';
    document.getElementById("modalTrat").classList.add("open");
}
window.abrirModal = abrirModal;

function cerrarModal() {
    document.getElementById("modalTrat").classList.remove("open");
}
window.cerrarModal = cerrarModal;

// ── Editar tratamiento ────────────────────────────────────────────────────
async function editarTratamiento(id) {
    try {
        const t = await api("GET", `/tratamientos/${id}`);
        document.getElementById("editId").value = t.id_tratamiento;
        document.getElementById("modalTitulo").textContent = "Editar Tratamiento";
        document.getElementById("inNombre").value = t.nombre;
        document.getElementById("inDescripcion").value = t.descripcion || "";
        document.getElementById("inPrecio").value = t.costo || 0;
        document.getElementById("btnGuardarTratamiento").disabled = false;
        document.getElementById("btnGuardarTratamiento").innerHTML = '<span class="material-symbols-outlined">save</span> Guardar';
        document.getElementById("modalTrat").classList.add("open");
    } catch (error) {
        toast("❌ Error al cargar el tratamiento", "error");
        console.error(error);
    }
}
window.editarTratamiento = editarTratamiento;

// ── Guardar tratamiento ──────────────────────────────────────────────────
async function guardarTratamiento() {
    const id = document.getElementById("editId").value;
    const nombre = document.getElementById("inNombre").value.trim();
    const descripcion = document.getElementById("inDescripcion").value.trim();
    const costo = parseFloat(document.getElementById("inPrecio").value) || 0;
    const btn = document.getElementById("btnGuardarTratamiento");

    if (!nombre) {
        toast("⚠️ Por favor, ingresa el nombre del tratamiento", "warning");
        document.getElementById("inNombre").focus();
        return;
    }
    if (costo <= 0) {
        toast("⚠️ Por favor, ingresa un precio válido", "warning");
        document.getElementById("inPrecio").focus();
        return;
    }

    btn.disabled = true;
    btn.innerHTML = `<span class="material-symbols-outlined spinner">progress_activity</span> Guardando...`;

    try {
        const data = {
            nombre: nombre,
            descripcion: descripcion,
            costo: costo
        };
        
        if (id) {
            await api("PUT", `/tratamientos/${id}`, data);
            toast("✅ Tratamiento actualizado correctamente", "success");
        } else {
            await api("POST", "/tratamientos", data);
            toast("✅ Tratamiento creado correctamente", "success");
        }
        
        cerrarModal();
        cargarTratamientos();
    } catch (error) {
        toast(`❌ ${error.message || "Error al guardar"}`, "error");
        btn.disabled = false;
        btn.innerHTML = `<span class="material-symbols-outlined">save</span> Guardar`;
    }
}
window.guardarTratamiento = guardarTratamiento;

// ── ABRIR MODAL DE CONFIRMACIÓN PARA ELIMINAR ──────────────────────────
function abrirConfirmModal(id, nombre, precio) {
    tratamientoAEliminar = id;
    
    document.getElementById("confirmIcon").textContent = "warning";
    document.getElementById("confirmIcon").className = "material-symbols-outlined confirm-icon warning";
    document.getElementById("confirmTitulo").textContent = "¿Eliminar este tratamiento?";
    document.getElementById("confirmMensaje").textContent = "Esta acción no se puede deshacer. El tratamiento será eliminado permanentemente del sistema.";
    
    document.getElementById("confirmNombre").textContent = nombre || '—';
    document.getElementById("confirmPrecio").textContent = `$${(precio || 0).toLocaleString('es-CO')}`;
    
    const btn = document.getElementById("btnConfirmEliminar");
    btn.disabled = false;
    btn.className = "btn-confirm-eliminar";
    btn.innerHTML = '<span class="material-symbols-outlined">delete</span> Eliminar';
    btn.onclick = function() { confirmarEliminar(); };
    
    document.getElementById("confirmModal").classList.add("open");
}
window.abrirConfirmModal = abrirConfirmModal;

function cerrarConfirmModal() {
    document.getElementById("confirmModal").classList.remove("open");
    tratamientoAEliminar = null;
}
window.cerrarConfirmModal = cerrarConfirmModal;

// ── CONFIRMAR ELIMINAR TRATAMIENTO ──────────────────────────────────────
async function confirmarEliminar() {
    if (!tratamientoAEliminar) return;
    
    const btn = document.getElementById("btnConfirmEliminar");
    btn.disabled = true;
    btn.innerHTML = `<span class="material-symbols-outlined spinner">progress_activity</span> Eliminando...`;

    try {
        await api("DELETE", `/tratamientos/${tratamientoAEliminar}`);
        toast("✅ Tratamiento eliminado correctamente", "success");
        cerrarConfirmModal();
        cargarTratamientos();
    } catch (error) {
        console.error("❌ Error al eliminar:", error);
        toast(`❌ ${error.message || "Error al eliminar"}`, "error");
        btn.disabled = false;
        btn.innerHTML = '<span class="material-symbols-outlined">delete</span> Eliminar';
    }
}
window.confirmarEliminar = confirmarEliminar;

// ── Verificar sesión ─────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
    const usuarioActual = JSON.parse(localStorage.getItem('usuario_actual') || 'null');
    if (!usuarioActual) {
        window.location.href = "../login.html";
        return;
    }
    cargarTratamientos();

    // Evento para el botón guardar
    document.getElementById('btnGuardarTratamiento')?.addEventListener('click', guardarTratamiento);
});