// ── Configuración base ────────────────────────────────────────────────────────
const API_BASE = "http://127.0.0.1:8000";

async function request(method, path, body = null) {
  const options = {
    method,
    headers: { "Content-Type": "application/json" },
  };
  if (body) options.body = JSON.stringify(body);
  const res = await fetch(`${API_BASE}${path}`, options);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Error ${res.status}`);
  }
  return res.status === 204 ? null : res.json();
}

// ── Usuarios ──────────────────────────────────────────────────────────────────
export const getUsuarios      = ()           => request("GET",    "/usuarios");
export const getUsuario       = (id)         => request("GET",    `/usuarios/${id}`);
export const createUsuario    = (data)       => request("POST",   "/usuarios", data);
export const updateUsuario    = (id, data)   => request("PUT",    `/usuarios/${id}`, data);
export const deleteUsuario    = (id)         => request("DELETE", `/usuarios/${id}`);

// ── Roles ─────────────────────────────────────────────────────────────────────
export const getRoles         = ()           => request("GET",    "/roles");
export const createRol        = (data)       => request("POST",   "/roles", data);
export const updateRol        = (id, data)   => request("PUT",    `/roles/${id}`, data);
export const deleteRol        = (id)         => request("DELETE", `/roles/${id}`);

// ── Tratamientos ──────────────────────────────────────────────────────────────
export const getTratamientos  = ()           => request("GET",    "/tratamientos");
export const createTratamiento= (data)       => request("POST",   "/tratamientos", data);
export const updateTratamiento= (id, data)   => request("PUT",    `/tratamientos/${id}`, data);
export const deleteTratamiento= (id)         => request("DELETE", `/tratamientos/${id}`);

// ── Citas ─────────────────────────────────────────────────────────────────────
export const getCitas         = ()           => request("GET",    "/citas");
export const getCitasPaciente = (pid)        => request("GET",    `/citas/paciente/${pid}`);
export const createCita       = (data)       => request("POST",   "/citas", data);
export const updateCita       = (id, data)   => request("PUT",    `/citas/${id}`, data);
export const patchEstadoCita  = (id, estado) => request("PATCH",  `/citas/${id}/estado?estado=${encodeURIComponent(estado)}`);
export const deleteCita       = (id)         => request("DELETE", `/citas/${id}`);

// ── Servicios ─────────────────────────────────────────────────────────────────
export const getServicios     = ()           => request("GET",    "/servicios");
export const getServiciosPac  = (pid)        => request("GET",    `/servicios/paciente/${pid}`);
export const createServicio   = (data)       => request("POST",   "/servicios", data);
export const deleteServicio   = (id)         => request("DELETE", `/servicios/${id}`);

// ── Proveedores ───────────────────────────────────────────────────────────────
export const getProveedores   = ()           => request("GET",    "/proveedores");
export const createProveedor  = (data)       => request("POST",   "/proveedores", data);
export const updateProveedor  = (id, data)   => request("PUT",    `/proveedores/${id}`, data);
export const deleteProveedor  = (id)         => request("DELETE", `/proveedores/${id}`);
 

