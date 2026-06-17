<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OdontoSoft - Usuarios</title>
  <link rel="stylesheet" href="../css/style.css">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0"/>
</head>
<body>

<div id="toast" class="toast"></div>

<!-- Modal Crear/Editar Usuario -->
<div id="modalUsuario" class="modal-overlay">
  <div class="modal">
    <h3 id="modalTitulo">Nuevo Usuario</h3>
    <input type="hidden" id="editId">
    <div class="form-group">
      <label>Nombre Completo</label>
      <input type="text" id="inNombre" placeholder="Dr. Juan Pérez">
    </div>
    <div class="form-group">
      <label>Correo Electrónico</label>
      <input type="email" id="inCorreo" placeholder="juan@dental.com">
    </div>
    <div class="form-group">
      <label>Identificación</label>
      <input type="text" id="inIdentificacion" placeholder="CC 12345678">
    </div>
    <div class="form-group">
      <label>Contraseña</label>
      <input type="password" id="inPassword" placeholder="••••••••">
    </div>
    <div class="form-group">
      <label>Rol</label>
      <select id="inRol"></select>
    </div>
    <div class="form-group">
      <label>Estado</label>
      <select id="inEstado">
        <option value="Activo">Activo</option>
        <option value="Inactivo">Inactivo</option>
      </select>
    </div>
    <div class="modal-footer">
      <button class="btn-secondary" onclick="cerrarModal()">Cancelar</button>
      <button class="btn-primary" onclick="guardarUsuario()">
        <span class="material-symbols-outlined">save</span> Guardar
      </button>
    </div>
  </div>
</div>

<div class="dashboard-container">
  <aside class="sidebar">
    <div class="sidebar-brand">
      <span class="material-symbols-outlined">dentistry</span>
      <span>OdontoSoft</span>
    </div>
    <nav class="sidebar-menu">
      <a href="panel.html" class="active"><span class="material-symbols-outlined">group</span> Usuarios</a>
      <a href="roles.html"><span class="material-symbols-outlined">manage_accounts</span> Roles</a>
      <a href="tratamientos.html"><span class="material-symbols-outlined">medical_services</span> Tratamientos</a>
      <a href="citas.html"><span class="material-symbols-outlined">calendar_month</span> Citas</a>
      <a href="proveedores.html"><span class="material-symbols-outlined">local_shipping</span> Proveedores</a>
      <a href="panel_cliente.html"><span class="material-symbols-outlined">account_circle</span> Portal Paciente</a>
      <a href="login.html"><span class="material-symbols-outlined">logout</span> Salir</a>
    </nav>
  </aside>

  <main class="main-content">
    <header class="content-header">
      <div>
        <h2>Gestión de Usuarios</h2>
        <p style="color:var(--text-muted)">Clínica e Historial del Personal</p>
      </div>
      <button class="btn-primary" onclick="abrirModal()">
        <span class="material-symbols-outlined">person_add</span> Nuevo Usuario
      </button>
    </header>

    <section class="metrics-grid">
      <div class="metric-card">
        <div class="metric-icon"><span class="material-symbols-outlined">badge</span></div>
        <div class="metric-data"><h3 id="cntOdontologos">—</h3><p>Odontólogos Activos</p></div>
      </div>
      <div class="metric-card">
        <div class="metric-icon" style="background:#dcfce7;color:var(--success)">
          <span class="material-symbols-outlined">patient_list</span>
        </div>
        <div class="metric-data"><h3 id="cntPacientes">—</h3><p>Pacientes Registrados</p></div>
      </div>
    </section>

    <section class="table-container">
      <table>
        <thead>
          <tr>
            <th>Nombre Completo</th>
            <th>Correo</th>
            <th>Identificación</th>
            <th>Rol</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody id="tablaUsuarios">
          <tr><td colspan="6" style="text-align:center;padding:30px;color:var(--text-muted)">Cargando...</td></tr>
        </tbody>
      </table>
    </section>
  </main>
</div>

<script type="module">
  const API = "http://127.0.0.1:8000";

  // ── Utilidades ─────────────────────────────────────────────────────────────
  function toast(msg, tipo = "success") {
    const t = document.getElementById("toast");
    t.textContent = msg;
    t.className = `toast show ${tipo}`;
    setTimeout(() => t.classList.remove("show"), 3000);
  }

  async function api(method, path, body = null) {
    const res = await fetch(`${API}${path}`, {
      method,
      headers: { "Content-Type": "application/json" },
      body: body ? JSON.stringify(body) : null,
    });
    if (!res.ok) { const e = await res.json(); throw new Error(e.detail || "Error"); }
    return res.status === 204 ? null : res.json();
  }

  // ── Cargar roles en el select ──────────────────────────────────────────────
  async function cargarRoles() {
    const roles = await api("GET", "/roles");
    const sel = document.getElementById("inRol");
    sel.innerHTML = roles.map(r => `<option value="${r.id}">${r.nombre}</option>`).join("");
    return roles;
  }

  // ── Renderizar tabla ───────────────────────────────────────────────────────
  function renderTabla(usuarios) {
    const colores = { "Odontólogo": "blue", "Paciente": "yellow", "Administrador": "red" };
    const tbody = document.getElementById("tablaUsuarios");
    if (!usuarios.length) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:30px;color:var(--text-muted)">Sin usuarios registrados</td></tr>`;
      return;
    }
    tbody.innerHTML = usuarios.map(u => `
      <tr>
        <td><strong>${u.nombre}</strong></td>
        <td>${u.correo}</td>
        <td>${u.identificacion}</td>
        <td><span class="badge ${colores[u.rol?.nombre] || 'blue'}">${u.rol?.nombre || '—'}</span></td>
        <td><span class="badge ${u.estado === 'Activo' ? 'green' : 'yellow'}">${u.estado}</span></td>
        <td>
          <button class="btn-icon" title="Editar" onclick="window.editarUsuario(${u.id})">
            <span class="material-symbols-outlined">edit</span>
          </button>
          <button class="btn-danger" title="Eliminar" onclick="window.eliminarUsuario(${u.id})">
            <span class="material-symbols-outlined">delete</span>
          </button>
        </td>
      </tr>
    `).join("");

    // Métricas
    document.getElementById("cntOdontologos").textContent =
      usuarios.filter(u => u.rol?.nombre === "Odontólogo").length;
    document.getElementById("cntPacientes").textContent =
      usuarios.filter(u => u.rol?.nombre === "Paciente").length;
  }

  // ── Cargar usuarios ────────────────────────────────────────────────────────
  async function cargarUsuarios() {
    try {
      const usuarios = await api("GET", "/usuarios");
      renderTabla(usuarios);
    } catch (e) {
      toast("No se pudo conectar con la API. ¿Está corriendo el backend?", "error");
    }
  }

  // ── Modal ──────────────────────────────────────────────────────────────────
  window.abrirModal = async () => {
    document.getElementById("editId").value = "";
    document.getElementById("modalTitulo").textContent = "Nuevo Usuario";
    document.getElementById("inNombre").value = "";
    document.getElementById("inCorreo").value = "";
    document.getElementById("inIdentificacion").value = "";
    document.getElementById("inPassword").value = "";
    document.getElementById("inEstado").value = "Activo";
    await cargarRoles();
    document.getElementById("modalUsuario").classList.add("open");
  };

  window.cerrarModal = () => {
    document.getElementById("modalUsuario").classList.remove("open");
  };

  window.editarUsuario = async (id) => {
    const roles = await cargarRoles();
    const u = await api("GET", `/usuarios/${id}`);
    document.getElementById("editId").value = u.id;
    document.getElementById("modalTitulo").textContent = "Editar Usuario";
    document.getElementById("inNombre").value = u.nombre;
    document.getElementById("inCorreo").value = u.correo;
    document.getElementById("inIdentificacion").value = u.identificacion;
    document.getElementById("inPassword").value = "placeholder123";
    document.getElementById("inEstado").value = u.estado;
    document.getElementById("inRol").value = u.rol_id;
    document.getElementById("modalUsuario").classList.add("open");
  };

  window.guardarUsuario = async () => {
    const id = document.getElementById("editId").value;
    const data = {
      nombre:         document.getElementById("inNombre").value,
      correo:         document.getElementById("inCorreo").value,
      identificacion: document.getElementById("inIdentificacion").value,
      password:       document.getElementById("inPassword").value,
      estado:         document.getElementById("inEstado").value,
      rol_id:         parseInt(document.getElementById("inRol").value),
    };
    try {
      if (id) {
        await api("PUT", `/usuarios/${id}`, data);
        toast("Usuario actualizado correctamente");
      } else {
        await api("POST", "/usuarios", data);
        toast("Usuario creado correctamente");
      }
      cerrarModal();
      cargarUsuarios();
    } catch (e) {
      toast(e.message, "error");
    }
  };

  window.eliminarUsuario = async (id) => {
    if (!confirm("¿Eliminar este usuario?")) return;
    try {
      await api("DELETE", `/usuarios/${id}`);
      toast("Usuario eliminado");
      cargarUsuarios();
    } catch (e) {
      toast(e.message, "error");
    }
  };

  // ── Inicio ─────────────────────────────────────────────────────────────────
  cargarUsuarios();
</script>
</body>
</html>
