function togglePassword(id) {
  const input = document.getElementById(id);
  const icon = input.nextElementSibling;

  if (input.type === "password") {
    input.type = "text";
    icon.textContent = "visibility"; // ojo abierto
  } else {
    input.type = "password";
    icon.textContent = "visibility_off"; // ojo bloqueado
  }
}

function validarRegistro() {
  const pass = document.getElementById("password").value;
  const confirm = document.getElementById("confirmPassword").value;
  const errorMsg = document.getElementById("errorMsg");

  if (pass !== confirm) {
    errorMsg.textContent = "❌ Las contraseñas no coinciden";
    errorMsg.style.color = "red";
    return false; // evita que se envíe el formulario
  }

  errorMsg.textContent = ""; // limpia el mensaje si coinciden
  return true; // permite enviar el formulario
}
