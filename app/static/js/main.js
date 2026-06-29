/**
 * Sistema de validación de formularios en tiempo real
 */
const FormValidator = {
  validarEmail: (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email),
  
  validarContraseña: (contraseña) => contraseña.length >= 6,
  
  validarRequerido: (valor) => valor.trim().length > 0,
  
  agregarError: (input, mensaje) => {
    input.classList.add('error');
    let errorDiv = input.nextElementSibling;
    if (!errorDiv || !errorDiv.classList.contains('error-msg')) {
      errorDiv = document.createElement('div');
      errorDiv.className = 'error-msg';
      input.parentNode.insertBefore(errorDiv, input.nextSibling);
    }
    errorDiv.textContent = mensaje;
  },
  
  limpiarError: (input) => {
    input.classList.remove('error');
    const errorDiv = input.nextElementSibling;
    if (errorDiv && errorDiv.classList.contains('error-msg')) {
      errorDiv.remove();
    }
  },
  
  validarFormulario: (formulario) => {
    let esValido = true;
    const inputs = formulario.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
      if (input.hasAttribute('required') && !FormValidator.validarRequerido(input.value)) {
        FormValidator.agregarError(input, 'Este campo es requerido');
        esValido = false;
      } else if (input.type === 'email' && input.value && !FormValidator.validarEmail(input.value)) {
        FormValidator.agregarError(input, 'Email inválido');
        esValido = false;
      } else if (input.type === 'password' && input.value && !FormValidator.validarContraseña(input.value)) {
        FormValidator.agregarError(input, 'La contraseña debe tener al menos 6 caracteres');
        esValido = false;
      } else if (input.value) {
        FormValidator.limpiarError(input);
      }
    });
    
    return esValido;
  }
};

function mostrarToast(mensaje, esError = false) {
  const toast = document.getElementById("toast");
  if (!toast) return;
  toast.textContent = mensaje;
  toast.style.borderColor = esError ? "#FF5468" : "#6BFF8E";
  toast.classList.remove("hidden");
  setTimeout(() => toast.classList.add("hidden"), 4000);
}

document.addEventListener("DOMContentLoaded", () => {
  // Botón de sincronización
  const btnSync = document.getElementById("btn-sync");
  if (btnSync) {
    btnSync.addEventListener("click", async () => {
      btnSync.disabled = true;
      const textoOriginal = btnSync.textContent;
      btnSync.textContent = "⟳ Recolectando...";
      try {
        const resp = await fetch("/api/sync/cheapshark?paginas=2", { method: "POST" });
        const data = await resp.json();
        if (resp.ok) {
          NotificationSystem.success(
            `${data.ofertas_nuevas} ofertas nuevas, ${data.ofertas_actualizadas} actualizadas`,
            'Sincronización completada'
          );
          setTimeout(() => location.reload(), 1500);
        } else {
          NotificationSystem.error(data.detail || "Error al sincronizar");
        }
      } catch (err) {
        NotificationSystem.error("No se pudo conectar con el servidor");
      } finally {
        btnSync.disabled = false;
        btnSync.textContent = textoOriginal;
      }
    });
  }

  // Validación en tiempo real de formularios
  document.querySelectorAll('form').forEach(form => {
    const inputs = form.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
      // Validar al perder el foco
      input.addEventListener('blur', () => {
        if (input.hasAttribute('required') && !FormValidator.validarRequerido(input.value)) {
          FormValidator.agregarError(input, 'Este campo es requerido');
        } else if (input.type === 'email' && input.value && !FormValidator.validarEmail(input.value)) {
          FormValidator.agregarError(input, 'Email inválido');
        } else if (input.type === 'password' && input.value && !FormValidator.validarContraseña(input.value)) {
          FormValidator.agregarError(input, 'Mínimo 6 caracteres');
        } else {
          FormValidator.limpiarError(input);
        }
      });
      
      // Limpiar error mientras se escribe
      input.addEventListener('input', () => {
        if (input.classList.contains('error')) {
          FormValidator.limpiarError(input);
        }
      });
    });
    
    // Validar al enviar el formulario
    form.addEventListener('submit', (e) => {
      if (!FormValidator.validarFormulario(form)) {
        e.preventDefault();
        NotificationSystem.warning('Por favor, completa todos los campos correctamente');
      }
    });
  });

  // Confirmación para formularios de eliminación
  document.querySelectorAll("form.form-eliminar").forEach((form) => {
    form.addEventListener("submit", (e) => {
      if (!confirm("¿Seguro que quieres eliminar este registro?")) {
        e.preventDefault();
      }
    });
  });
});
