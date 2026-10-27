document.addEventListener("DOMContentLoaded", () => {

    // 1. Registro de Usuario
    const formRegistro = document.getElementById("formRegistro");
    if (formRegistro) {
        formRegistro.addEventListener("submit", async (e) => {
            e.preventDefault();
            const payload = {
                cedula: document.getElementById("cedula").value,
                nombre: document.getElementById("nombre").value,
                username: document.getElementById("username").value,
                email: document.getElementById("email").value,
                password: document.getElementById("password").value
            };

            try {
                const res = await fetch("/api/usuarios", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                alert(data.message);
                if (res.ok) {
                    window.location.href = "/";
                }
            } catch (err) {
                console.error("Error:", err);
            }
        });
    }

    // 2. Crear Grupo
    const formGrupo = document.getElementById("formCrearGrupo");
    if (formGrupo) {
        formGrupo.addEventListener("submit", async (e) => {
            e.preventDefault();
            const payload = {
                nombre_grupo: document.getElementById("nombre_grupo").value.trim(),
                codigo_invitacion: document.getElementById("codigo_crear").value.trim(),
                creador_cedula: document.getElementById("cedula_creador").value.trim()
            };

            try {
                const res = await fetch("/api/grupos", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                
                if (data.status === "success") {
                    alert(data.message);
                    location.reload();
                } else if (data.status === "not_registered") {
                    alert("⚠️ " + data.message);
                    window.location.href = data.redirect_url; // Te redirige a /registros
                } else {
                    alert("Aviso: " + data.message);
                }
            } catch (err) {
                console.error("Error:", err);
                alert("Ocurrió un error al conectar con el servidor.");
            }
        });
    }

    // 3. Unirse a Grupo existente con validación de usuario registrado
    const formUnirseGrupo = document.getElementById("formUnirseGrupo");
    if (formUnirseGrupo) {
        formUnirseGrupo.addEventListener("submit", async (e) => {
            e.preventDefault();
            const payload = {
                codigo_invitacion: document.getElementById("codigo_unirse").value.trim(),
                cedula: document.getElementById("cedula_unirse").value.trim()
            };

            try {
                const res = await fetch("/api/grupos/unirse", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                
                if (data.status === "success") {
                    alert(data.message);
                    location.reload();
                } else if (data.status === "not_registered") {
                    alert("⚠️ " + data.message);
                    window.location.href = data.redirect_url;
                } else {
                    alert("Error: " + data.message);
                }
            } catch (err) {
                console.error("Error:", err);
            }
        });
    }

});

// 4. Guardar Pronóstico (Función global)
async function guardarPronostico(partidoId) {
    const cedulaInput = document.getElementById(`cedula_${partidoId}`);
    const localInput = document.getElementById(`local_${partidoId}`);
    const visitanteInput = document.getElementById(`visitante_${partidoId}`);

    if (!cedulaInput || !cedulaInput.value.trim()) {
        alert("Por favor, ingresa tu número de cédula.");
        return;
    }

    if (!localInput || !visitanteInput || localInput.value === "" || visitanteInput.value === "") {
        alert("Debes ingresar los goles para ambos equipos.");
        return;
    }

    const payload = {
        cedula_usuario: cedulaInput.value.trim(),
        partido_id: partidoId,
        goles_local: parseInt(localInput.value),
        goles_visitante: parseInt(visitanteInput.value)
    };

    try {
        const res = await fetch("/api/pronosticos", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        
        if (data.status === "success") {
            alert(data.message);
            location.reload();
        } else if (data.status === "not_registered") {
            alert("⚠️ " + data.message);
            window.location.href = data.redirect_url;
        } else {
            alert("Aviso: " + data.message);
        }
    } catch (err) {
        console.error("Error:", err);
        alert("Ocurrió un error al conectar con el servidor.");
    }
}

// Cargar los mensajes del chat de un grupo
async function cargarMensajes(codigoGrupo) {
    const chatBox = document.getElementById(`chat_box_${codigoGrupo}`);
    try {
        const res = await fetch(`/api/grupos/mensajes/${codigoGrupo}`);
        const data = await res.json();

        if (data.status === "success" && data.mensajes.length > 0) {
            chatBox.innerHTML = data.mensajes.map(m => `
                <div style="background: rgba(255, 255, 255, 0.03); padding: 6px 10px; border-radius: 6px; border-left: 3px solid var(--purple-glow);">
                    <div style="display: flex; justify-content: space-between; font-size: 0.72rem;">
                        <strong style="color: #ffffff;">${m.nombre_usuario} <span style="color: var(--purple-glow);">@${m.username}</span></strong>
                    </div>
                    <p style="font-size: 0.8rem; color: #e2e8f0; margin-top: 2px;">${m.mensaje}</p>
                </div>
            `).join('');
            chatBox.scrollTop = chatBox.scrollHeight;
        } else {
            chatBox.innerHTML = `<p style="font-size: 0.75rem; color: var(--text-muted); text-align: center;">Aún no hay mensajes. ¡Sé el primero en comentar!</p>`;
        }
    } catch (err) {
        console.error("Error al cargar chat:", err);
    }
}

// Enviar un mensaje al chat del grupo
async function enviarMensajeChat(codigoGrupo) {
    const cedulaInput = document.getElementById(`cedula_chat_${codigoGrupo}`);
    const msgInput = document.getElementById(`msg_chat_${codigoGrupo}`);

    if (!cedulaInput || !cedulaInput.value.trim()) {
        alert("Ingresa tu cédula para comentar.");
        return;
    }

    if (!msgInput || !msgInput.value.trim()) {
        alert("Escribe un mensaje antes de enviar.");
        return;
    }

    const payload = {
        codigo_invitacion: codigoGrupo,
        cedula: cedulaInput.value.trim(),
        mensaje: msgInput.value.trim()
    };

    try {
        const res = await fetch("/api/grupos/mensaje", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (data.status === "success") {
            msgInput.value = "";
            cargarMensajes(codigoGrupo);
        } else if (data.status === "not_registered") {
            alert("⚠️ " + data.message);
            window.location.href = data.redirect_url;
        } else {
            alert("Error: " + data.message);
        }
    } catch (err) {
        console.error("Error al enviar mensaje:", err);
    }
}