// ============================================
// AUTH.JS - Funciones de autenticación
// ============================================

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

// ── Validar registro (contraseñas coinciden) ────────────────────────────────
function validarRegistro() {
  const pass = document.getElementById("password").value;
  const confirm = document.getElementById("confirmPassword").value;
  const errorMsg = document.getElementById("errorMsg");

  if (pass !== confirm) {
    errorMsg.textContent = "❌ Las contraseñas no coinciden";
    errorMsg.classList.add("show");
    return false;
  }

  errorMsg.textContent = "";
  errorMsg.classList.remove("show");
  return true;
}

// ── Validación de correo ───────────────────────────────────────────────────
function validarCorreo(correo) {
  const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return regex.test(correo);
}

// ── Medidor de fortaleza de contraseña ────────────────────────────────────
function medirFortaleza(pwd) {
  let score = 0;
  if (pwd.length >= 8) score++;
  if (/[a-z]/.test(pwd) && /[A-Z]/.test(pwd)) score++;
  if (/\d/.test(pwd)) score++;
  if (/[^a-zA-Z0-9]/.test(pwd)) score++;
  return score;
}

// ── Mostrar fortaleza de contraseña ────────────────────────────────────────
function mostrarFortaleza(pwd) {
  const strengthDiv = document.getElementById('passwordStrength');
  if (!strengthDiv) return;
  
  if (pwd.length === 0) {
    strengthDiv.textContent = '';
    strengthDiv.className = 'password-strength';
    return;
  }
  
  const score = medirFortaleza(pwd);
  let mensaje = '';
  let clase = '';
  if (score <= 1) { mensaje = 'Débil'; clase = 'weak'; }
  else if (score === 2) { mensaje = 'Media'; clase = 'medium'; }
  else { mensaje = 'Fuerte'; clase = 'strong'; }
  
  strengthDiv.textContent = `Fortaleza: ${mensaje}`;
  strengthDiv.className = `password-strength ${clase}`;
}

// ── Toast ──────────────────────────────────────────────────────────────────
function toast(msg, tipo = "success") {
  const t = document.getElementById("toast");
  if (!t) {
    console.warn("Toast element not found");
    return;
  }
  t.textContent = msg;
  t.className = `toast show ${tipo}`;
  setTimeout(() => t.classList.remove("show"), 3000);
}

// ── Verificar sesión ────────────────────────────────────────────────────────
function verificarSesion() {
  const usuario = localStorage.getItem('usuario_actual');
  if (!usuario) {
    window.location.href = "login.html";
    return null;
  }
  try {
    return JSON.parse(usuario);
  } catch {
    window.location.href = "login.html";
    return null;
  }
}

// ── Cerrar sesión ────────────────────────────────────────────────────────────
function cerrarSesion() {
  localStorage.removeItem('usuario_actual');
  window.location.href = "login.html";
}

// ── Verificar permisos por rol ──────────────────────────────────────────────
function tienePermiso(usuario, rolesPermitidos) {
  if (!usuario) return false;
  return rolesPermitidos.includes(usuario.rol);
}

// ── Obtener usuario actual ──────────────────────────────────────────────────
function getUsuarioActual() {
  const usuario = localStorage.getItem('usuario_actual');
  if (!usuario) return null;
  try {
    return JSON.parse(usuario);
  } catch {
    return null;
  }
}