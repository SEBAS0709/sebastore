function mostrarToast(mensaje, esError = false) {
  const toast = document.getElementById("toast");
  if (!toast) return;
  toast.textContent = mensaje;
  toast.style.borderColor = esError ? "#FF5468" : "#6BFF8E";
  toast.classList.remove("hidden");
  setTimeout(() => toast.classList.add("hidden"), 4000);
}

document.addEventListener("DOMContentLoaded", () => {
  const btnSync = document.getElementById("btn-sync");
  if (btnSync) {
    btnSync.addEventListener("click", async () => {
      btnSync.disabled = true;
      const textoOriginal = btnSync.textContent;
      btnSync.textContent = "Recolectando...";
      try {
        const resp = await fetch("/api/sync/cheapshark?paginas=2", { method: "POST" });
        const data = await resp.json();
        if (resp.ok) {
          mostrarToast(
            `Listo: ${data.ofertas_nuevas} ofertas nuevas, ${data.ofertas_actualizadas} actualizadas.`
          );
          setTimeout(() => location.reload(), 1200);
        } else {
          mostrarToast(data.detail || "Error al sincronizar", true);
        }
      } catch (err) {
        mostrarToast("No se pudo conectar con el servidor", true);
      } finally {
        btnSync.disabled = false;
        btnSync.textContent = textoOriginal;
      }
    });
  }

  // Confirmación para formularios de eliminación
  document.querySelectorAll("form.form-eliminar").forEach((form) => {
    form.addEventListener("submit", (e) => {
      if (!confirm("¿Seguro que quieres eliminar este registro?")) {
        e.preventDefault();
      }
    });
  });
});
