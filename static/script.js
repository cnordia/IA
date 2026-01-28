document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("btn-buscar");
    
    btn.addEventListener("click", async () => {

        const contexto = document.getElementById("contexto").value;
        const pregunta = document.getElementById("pregunta").value;
        const errorMsg = document.getElementById("mensaje-error");
        const resultadoSection = document.getElementById("resultado-section");

        errorMsg.innerText = "";
        if (!contexto || !pregunta) {
            errorMsg.innerText = "⚠️ Por favor, rellena ambos campos.";
            return;
        }

        btn.disabled = true;
        btn.innerText = "Pensando...";

        try {
            const respuesta = await fetch("/consulta/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ pregunta: pregunta, contexto: contexto })
            });

            if (!respuesta.ok) throw new Error("Error en el servidor");

            const data = await respuesta.json();

            mostrarResultado(data);

        } catch (error) {
            errorMsg.innerText = "❌ Hubo un error al conectar con la IA.";
            console.error(error);
        } finally {
            btn.disabled = false;
            btn.innerText = "🔍 Buscar Respuesta";
        }
    });
});

function mostrarResultado(data) {
    const sectionRespuesta = document.getElementById("resultado-section");
    const resultado = document.getElementById("respuesta-texto");

    resultado.innerText = data.respuesta;

    sectionRespuesta.classList.remove("hidden");
}