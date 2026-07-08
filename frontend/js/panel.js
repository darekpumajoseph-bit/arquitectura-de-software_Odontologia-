// ============================================
// PANEL.JS - Dashboard Administrador (VERSIÓN FINAL PULIDA)
// ============================================

// ── Variables para el modal de confirmación ──────────────────────────────────
let usuarioAEliminar = null;
let pacienteEditandoId = null;

// ── API ──────────────────────────────────────────────────────────────────────
const API = "http://127.0.0.1:8000";

// ── Mostrar/ocultar contraseña ──────────────────────────────────────────────
function togglePassword(id) {
    const input = document.getElementById(id);
    const icon = input.nextElementSibling;
    if (input.type === "password") {
        input.type = "text";
        icon.textContent = "visibility";
    } else {
        input.type = "password";
        icon.textContent = "visibility_off";
    }
}
window.togglePassword = togglePassword;

// ── Mostrar/ocultar campos según el rol ────────────────────────────────────
function toggleCamposPaciente() {
    const rol = document.getElementById("inRol").value;
    const camposComunes = document.getElementById("camposComunes");
    const camposPaciente = document.getElementById("camposPaciente");
    const camposOdontologo = document.getElementById("camposOdontologo");

    camposComunes?.classList.remove("show");
    camposPaciente?.classList.remove("show");
    camposOdontologo?.classList.remove("show");

    if (rol === "Administrador") {
        camposComunes?.classList.add("show");
    } else if (rol === "Paciente") {
        camposComunes?.classList.add("show");
        camposPaciente?.classList.add("show");
    } else if (rol === "Odontologo") {
        camposComunes?.classList.add("show");
        camposOdontologo?.classList.add("show");
    }
}
window.toggleCamposPaciente = toggleCamposPaciente;

// ── Validar correo ───────────────────────────────────────────────────────────
function validarCorreo(correo) {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(correo);
}

// ── Validar teléfono ──────────────────────────────────────────────────────
function validarTelefono(telefono) {
    const regex = /^[0-9+\-\s]{7,15}$/;
    return regex.test(telefono);
}

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

// ── Renderizar tabla ───────────────────────────────────────────────────────
function renderTabla(usuarios) {
    const colores = { "Administrador": "red", "Odontologo": "blue", "Paciente": "yellow" };
    const tbody = document.getElementById("tablaUsuarios");

    if (!usuarios || !usuarios.length) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;padding:30px;color:var(--text-muted)">Sin usuarios registrados</td></tr>`;
        return;
    }

    usuarios.sort((a, b) => a.id_usuario - b.id_usuario);

    tbody.innerHTML = usuarios.map((u, index) => `
        <tr>
            <td><strong>${index + 1}</strong></td>
            <td>${u.correo}</td>
            <td><span class="badge ${colores[u.rol] || 'blue'}">${u.rol || '—'}</span></td>
            <td><span class="badge ${u.estado === 'Activo' ? 'green' : 'yellow'}">${u.estado || '—'}</span></td>
            <td>
                <button class="btn-icon" title="Editar" onclick="editarUsuario(${u.id_usuario})">
                    <span class="material-symbols-outlined">edit</span>
                </button>
                <button class="btn-danger" title="Eliminar" onclick="abrirConfirmModal(${u.id_usuario}, '${u.correo}', '${u.rol}')">
                    <span class="material-symbols-outlined">delete</span>
                </button>
            </td>
        </tr>
    `).join("");

    document.getElementById("cntOdontologos").textContent = usuarios.filter(u => u.rol === "Odontologo").length;
    document.getElementById("cntPacientes").textContent = usuarios.filter(u => u.rol === "Paciente").length;
}

// ── Cargar usuarios ────────────────────────────────────────────────────────
async function cargarUsuarios() {
    try {
        console.log("🔄 Cargando usuarios...");
        const usuarios = await api("GET", "/usuarios");
        console.log("✅ Usuarios cargados:", usuarios.length);
        renderTabla(usuarios);
    } catch (e) {
        console.error("❌ Error al cargar usuarios:", e);
        toast("❌ No se pudo conectar con el servidor", "error");
        document.getElementById("tablaUsuarios").innerHTML = `
            <tr>
                <td colspan="5" style="text-align:center;padding:30px;color:var(--text-muted)">
                    ❌ Error de conexión: ${e.message}
                </td>
            </tr>
        `;
    }
}

// ── Validación en tiempo real ────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
    const usuarioActual = JSON.parse(localStorage.getItem('usuario_actual') || 'null');
    if (!usuarioActual) {
        window.location.href = "login.html";
        return;
    }

    cargarUsuarios();

    const correoInput = document.getElementById('inCorreo');
    const correoError = document.getElementById('correoError');
    correoInput?.addEventListener('input', function() {
        const correo = this.value.trim();
        if (correo.length === 0) {
            this.classList.remove('input-error');
            correoError.classList.remove('show');
            return;
        }
        if (validarCorreo(correo)) {
            this.classList.remove('input-error');
            correoError.classList.remove('show');
        } else {
            this.classList.add('input-error');
            correoError.classList.add('show');
        }
    });

    const passwordInput = document.getElementById('inPassword');
    const passwordError = document.getElementById('passwordError');
    passwordInput?.addEventListener('input', function() {
        const pwd = this.value;
        if (pwd === "********" || pwd === "") {
            this.classList.remove('input-error');
            passwordError.classList.remove('show');
            return;
        }
        if (pwd.length > 0 && pwd.length < 6) {
            this.classList.add('input-error');
            passwordError.classList.add('show');
        } else {
            this.classList.remove('input-error');
            passwordError.classList.remove('show');
        }
    });

    const telefonoInput = document.getElementById('inTelefono');
    const telefonoError = document.getElementById('telefonoError');
    telefonoInput?.addEventListener('input', function() {
        const telefono = this.value.trim();
        if (telefono.length === 0) {
            this.classList.remove('input-error');
            telefonoError.classList.remove('show');
            return;
        }
        if (validarTelefono(telefono)) {
            this.classList.remove('input-error');
            telefonoError.classList.remove('show');
        } else {
            this.classList.add('input-error');
            telefonoError.classList.add('show');
        }
    });

    document.getElementById('btnGuardarUsuario')?.addEventListener('click', guardarUsuario);
});

// ── Modal Usuario ──────────────────────────────────────────────────────────
function abrirModal() {
    pacienteEditandoId = null;
    document.getElementById("editId").value = "";
    document.getElementById("modalTitulo").textContent = "Nuevo Usuario";
    
    document.getElementById("inCorreo").value = "";
    document.getElementById("inCorreo").classList.remove('input-error');
    document.getElementById("correoError").classList.remove('show');
    
    document.getElementById("inPassword").value = "";
    document.getElementById("inPassword").placeholder = "•••••••• (mínimo 6 caracteres)";
    document.getElementById("inPassword").classList.remove('input-error');
    document.getElementById("passwordError").classList.remove('show');
    
    document.getElementById("inNombre").value = "";
    document.getElementById("inApellido").value = "";
    document.getElementById("inTelefono").value = "";
    document.getElementById("inTelefono").classList.remove('input-error');
    document.getElementById("telefonoError").classList.remove('show');
    
    document.getElementById("inDocumento").value = "";
    document.getElementById("inEspecialidad").value = "";
    document.getElementById("inConsultorio").value = ""; 
    document.getElementById("inFechaNacimiento").value = "";
    document.getElementById("inGenero").value = "";
    document.getElementById("inDireccion").value = "";
    document.getElementById("inEps").value = "";
    document.getElementById("inAlergias").value = "";
    
    document.getElementById("inRol").value = "Paciente";
    document.getElementById("inEstado").value = "Activo";
    
    toggleCamposPaciente();
    
    document.getElementById("btnGuardarUsuario").disabled = false;
    document.getElementById("btnGuardarUsuario").innerHTML = '<span class="material-symbols-outlined">save</span> Guardar';
    document.getElementById("modalUsuario").classList.add("open");
}
window.abrirModal = abrirModal;

function cerrarModal() {
    document.getElementById("modalUsuario").classList.remove("open");
    
    document.getElementById("editId").value = "";
    document.getElementById("inCorreo").value = "";
    document.getElementById("inPassword").value = "";
    document.getElementById("inNombre").value = "";
    document.getElementById("inApellido").value = "";
    document.getElementById("inTelefono").value = "";
    document.getElementById("inDocumento").value = "";
    document.getElementById("inEspecialidad").value = "";
    document.getElementById("inConsultorio").value = "";
    document.getElementById("inFechaNacimiento").value = "";
    document.getElementById("inGenero").value = "";
    document.getElementById("inDireccion").value = "";
    document.getElementById("inEps").value = "";
    document.getElementById("inAlergias").value = "";
    
    pacienteEditandoId = null;
}
window.cerrarModal = cerrarModal;

// ── Editar Usuario ────────────────────────────────────────────────────────
async function editarUsuario(id) {
    try {
        console.log("🔄 Editando usuario ID:", id);
        const u = await api("GET", `/usuarios/${id}`);
        
        pacienteEditandoId = null;
        
        document.getElementById("editId").value = u.id_usuario;
        document.getElementById("modalTitulo").textContent = "Editar Usuario";
        document.getElementById("inCorreo").value = u.correo;
        document.getElementById("inCorreo").classList.remove('input-error');
        document.getElementById("correoError").classList.remove('show');
        
        const contrasenaPlano = u.contrasena_plano || u.contrasena || "********";
        document.getElementById("inPassword").value = contrasenaPlano;
        document.getElementById("inPassword").placeholder = "******** (Dejar así para no cambiar)";
        document.getElementById("inPassword").classList.remove('input-error');
        document.getElementById("passwordError").classList.remove('show');
        
        document.getElementById("inRol").value = u.rol;
        document.getElementById("inEstado").value = u.estado;
        
        document.getElementById("inNombre").value = "";
        document.getElementById("inApellido").value = "";
        document.getElementById("inTelefono").value = "";
        document.getElementById("inDocumento").value = "";
        document.getElementById("inEspecialidad").value = "";
        document.getElementById("inConsultorio").value = "";
        document.getElementById("inFechaNacimiento").value = "";
        document.getElementById("inGenero").value = "";
        document.getElementById("inDireccion").value = "";
        document.getElementById("inEps").value = "";
        document.getElementById("inAlergias").value = "";

        // ── PACIENTE ──
        if (u.rol === "Paciente") {
            try {
                const pacientes = await api("GET", "/pacientes");
                const paciente = pacientes.find(p => p.correo === u.correo);

                if (paciente) {
                    pacienteEditandoId = paciente.id_paciente;
                    document.getElementById("inNombre").value = paciente.nombre || "";
                    document.getElementById("inApellido").value = paciente.apellido || "";
                    document.getElementById("inDocumento").value = paciente.documento || "";
                    document.getElementById("inTelefono").value = paciente.telefono || "";
                    
                    // 🔥 Formatear fecha para input type="date" (YYYY-MM-DD)
                    const fechaRaw = paciente.fecha_nacimiento || "";
                    document.getElementById("inFechaNacimiento").value = fechaRaw.substring(0, 10);
                    
                    document.getElementById("inGenero").value = paciente.genero || "";
                    document.getElementById("inDireccion").value = paciente.direccion || "";
                    document.getElementById("inEps").value = paciente.eps || "";
                    document.getElementById("inAlergias").value = paciente.alergias || "";
                }
            } catch(error) {
                console.error("Error cargando paciente:", error);
            }
        }

        // ── ODONTÓLOGO ──
        if (u.rol === "Odontologo") {
            try {
                const odontologos = await api("GET", "/odontologos");
                const odontologo = odontologos.find(o => o.correo === u.correo);
                if (odontologo) {
                    document.getElementById("inNombre").value = odontologo.nombre || "";
                    document.getElementById("inApellido").value = odontologo.apellido || "";
                    document.getElementById("inDocumento").value = odontologo.documento || "";
                    document.getElementById("inTelefono").value = odontologo.telefono || "";
                    document.getElementById("inEspecialidad").value = odontologo.especialidad || "";
                    document.getElementById("inConsultorio").value = odontologo.id_consultorio || "";
                }
            } catch (error) {
                console.error(error);
            }
        }
        
        toggleCamposPaciente();
        
        document.getElementById("btnGuardarUsuario").disabled = false;
        document.getElementById("btnGuardarUsuario").innerHTML = '<span class="material-symbols-outlined">save</span> Guardar';
        document.getElementById("modalUsuario").classList.add("open");
        
    } catch (e) {
        console.error("❌ Error al editar usuario:", e);
        toast(`❌ ${e.message}`, "error");
    }
}
window.editarUsuario = editarUsuario;

// ── Guardar Usuario ──────────────────────────────────────────────────────────
async function guardarUsuario() {
    const id = document.getElementById("editId").value;
    const correo = document.getElementById("inCorreo").value.trim();
    const contrasena = document.getElementById("inPassword").value.trim();
    const rol = document.getElementById("inRol").value;
    const estado = document.getElementById("inEstado").value;
    const btn = document.getElementById("btnGuardarUsuario");

    // Lectura segura de campos (usando ?. para evitar errores si no existen en el HTML)
    const nombre = document.getElementById("inNombre")?.value.trim() || "";
    const apellido = document.getElementById("inApellido")?.value.trim() || "";
    const telefono = document.getElementById("inTelefono")?.value.trim() || "";
    const documento = document.getElementById("inDocumento")?.value.trim() || "";
    const especialidad = document.getElementById("inEspecialidad")?.value.trim() || "";
    const id_consultorio = parseInt(document.getElementById("inConsultorio")?.value) || 0;

    // ── Validación Básica ──
    if (!correo) { toast("Ingrese el correo.", "warning"); return; }
    if (!validarCorreo(correo)) { toast("Correo inválido.", "error"); return; }

    // ── Validación Contraseña ──
    const PASSWORD_PLACEHOLDER = "********";
    const esPlaceholder = contrasena === PASSWORD_PLACEHOLDER;
    const estaVacia = contrasena === "";

    if (!id) {
        if (estaVacia || esPlaceholder) { toast("Ingrese una contraseña.", "warning"); return; }
        if (contrasena.length < 6) { toast("La contraseña debe tener mínimo 6 caracteres.", "error"); return; }
    }

    let enviarContrasena = null;
    if (id) {
        if (!estaVacia && !esPlaceholder) {
            if (contrasena.length < 6) { toast("La contraseña debe tener mínimo 6 caracteres.", "error"); return; }
            enviarContrasena = contrasena;
        }
    } else {
        enviarContrasena = contrasena;
    }

    // ── Validación por Roles ──
    if (rol === "Paciente") {
        if (!nombre || !apellido || !documento || !telefono) {
            toast("Complete todos los datos del paciente.", "warning"); return;
        }
    }

    if (rol === "Odontologo") {
        if (!nombre || !apellido || !documento || !telefono || !especialidad || !id_consultorio) {
            toast("Complete todos los datos del odontólogo.", "warning"); return;
        }
    }

    btn.disabled = true;
    btn.innerHTML = `<span class="material-symbols-outlined spinner">progress_activity</span> Guardando...`;

    try {
        // ============================================
        // EDITAR USUARIO
        // ============================================
        if (id) {
            const usuarioActual = await api("GET", `/usuarios/${id}`);
            const correoAnterior = usuarioActual.correo;

            const dataUsuario = { correo, rol, estado };
            if (enviarContrasena) dataUsuario.contrasena = enviarContrasena;
            await api("PUT", `/usuarios/${id}`, dataUsuario);

            // ── ACTUALIZAR PACIENTE ──
            if (rol === "Paciente") {
                // Si tenemos el ID guardado, lo usamos directamente para el PUT
                let targetId = pacienteEditandoId;
                
                // Si no lo tenemos (fallback), lo buscamos por correo
                if (!targetId) {
                    const pacientes = await api("GET", "/pacientes");
                    const paciente = pacientes.find(p => p.correo === correoAnterior);
                    if (paciente) targetId = paciente.id_paciente;
                }

                if (targetId) {
                    const dataPaciente = {
                        nombre, apellido, documento, telefono, correo,
                        fecha_nacimiento: document.getElementById("inFechaNacimiento")?.value || null,
                        genero: document.getElementById("inGenero")?.value || null,
                        direccion: document.getElementById("inDireccion")?.value || null,
                        eps: document.getElementById("inEps")?.value || null,
                        alergias: document.getElementById("inAlergias")?.value || null
                    };
                    console.log("📤 Enviando PUT a paciente ID:", targetId, dataPaciente);
                    await api("PUT", `/pacientes/${targetId}`, dataPaciente);
                    toast("✅ Paciente actualizado correctamente");
                } else {
                    console.warn("⚠️ No se encontró el paciente para actualizar.");
                }
            }

            // ── ACTUALIZAR ODONTÓLOGO ──
            if (rol === "Odontologo") {
                const odontologos = await api("GET", "/odontologos");
                const odontologo = odontologos.find(o => o.correo === correoAnterior);
                if (odontologo) {
                    await api("PUT", `/odontologos/${odontologo.id_odontologo}`, {
                        nombre, apellido, documento, telefono, correo, especialidad, id_consultorio
                    });
                    toast("✅ Odontólogo actualizado correctamente");
                }
            }

            if (rol !== "Paciente" && rol !== "Odontologo") {
                toast("✅ Usuario actualizado correctamente");
            }

        } 
        // ============================================
        // CREAR USUARIO
        // ============================================
        else {
            if (rol === "Paciente") {
                await api("POST", "/usuarios/registro", {
                    correo, contrasena: enviarContrasena, nombre, apellido, documento, telefono,
                    fecha_nacimiento: document.getElementById("inFechaNacimiento")?.value || null,
                    genero: document.getElementById("inGenero")?.value || null,
                    direccion: document.getElementById("inDireccion")?.value || null,
                    eps: document.getElementById("inEps")?.value || null,
                    alergias: document.getElementById("inAlergias")?.value || null
                });
                toast("✅ Paciente registrado correctamente");
            }
            else if (rol === "Odontologo") {
                // Crear Usuario
                await api("POST", "/usuarios", {
                    correo, contrasena: enviarContrasena, rol: "Odontologo", estado: "Activo"
                });
                // Crear Odontólogo
                await api("POST", "/odontologos", {
                    nombre, apellido, documento, telefono, correo, especialidad, id_consultorio
                });
                toast("✅ Odontólogo registrado correctamente");
            }
            else {
                await api("POST", "/usuarios", {
                    correo, contrasena: enviarContrasena, rol, estado
                });
                toast("✅ Administrador registrado correctamente");
            }
        }

        cerrarModal();
        cargarUsuarios();

    } catch (error) {
        console.error(error);
        toast(error.message, "error");
        btn.disabled = false;
        btn.innerHTML = `<span class="material-symbols-outlined">save</span> Guardar`;
    }
}
window.guardarUsuario = guardarUsuario;

// ── MODAL DE CONFIRMACIÓN PARA ELIMINAR ────────────────────────────────────
function abrirConfirmModal(id, correo, rol) {
    usuarioAEliminar = id;
    document.getElementById("confirmIcon").textContent = "warning";
    document.getElementById("confirmIcon").className = "material-symbols-outlined confirm-icon warning";
    document.getElementById("confirmTitulo").textContent = "¿Eliminar este usuario?";
    document.getElementById("confirmMensaje").textContent = "Esta acción no se puede deshacer. El usuario será eliminado permanentemente del sistema.";
    document.getElementById("userInfo").style.display = "block";
    document.getElementById("confirmFooter").style.display = "flex";
    document.getElementById("confirmId").textContent = id;
    document.getElementById("confirmCorreo").textContent = correo;
    document.getElementById("confirmRol").textContent = rol;
    
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
    usuarioAEliminar = null;
}
window.cerrarConfirmModal = cerrarConfirmModal;

function mostrarErrorConfirmacion(mensaje) {
    document.getElementById("confirmIcon").textContent = "error";
    document.getElementById("confirmIcon").className = "material-symbols-outlined confirm-icon error";
    document.getElementById("confirmTitulo").textContent = "❌ No se puede eliminar";
    document.getElementById("confirmMensaje").textContent = mensaje || "El usuario no se puede eliminar porque tiene registros asociados en el sistema.";
    document.getElementById("userInfo").style.display = "none";
    document.getElementById("confirmFooter").style.display = "flex";
    
    const btn = document.getElementById("btnConfirmEliminar");
    btn.disabled = false;
    btn.className = "btn-confirm-cancelar";
    btn.innerHTML = '<span class="material-symbols-outlined">close</span> Cerrar';
    btn.onclick = function() { cerrarConfirmModal(); };
}

async function confirmarEliminar() {
    if (!usuarioAEliminar) return;
    const btn = document.getElementById("btnConfirmEliminar");
    btn.disabled = true;
    btn.innerHTML = `<span class="material-symbols-outlined spinner">progress_activity</span> Eliminando...`;

    try {
        await api("DELETE", `/usuarios/${usuarioAEliminar}`);
        toast("✅ Usuario eliminado correctamente", "success");
        cerrarConfirmModal();
        cargarUsuarios();
    } catch (error) {
        console.error("❌ Error al eliminar:", error);
        let mensajeError = error.message || "Error al eliminar el usuario";
        if (mensajeError.includes("pacientes asociados") || mensajeError.includes("registros asociados")) {
            mensajeError = "Este usuario tiene registros asociados. No se puede eliminar directamente.";
        }
        toast(`❌ ${mensajeError}`, "error");
        mostrarErrorConfirmacion(mensajeError);
    }
}
window.confirmarEliminar = confirmarEliminar;