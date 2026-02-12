async function loadInvoices() {
    const res = await fetch("/invoices/");
    const data = await res.json();

    const tbody = document.querySelector("#invoiceTable tbody");
    tbody.innerHTML = "";

    data.forEach(inv => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${inv.id}</td>
            <td>${inv.supplier}</td>
            <td>${inv.date}</td>
            <td>${inv.total}</td>
            <td>
                <button onclick="deleteInvoice(${inv.id})">Eliminar</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function deleteInvoice(id) {
    await fetch(`/invoices/${id}`, { method: "DELETE" });
    loadInvoices();
}

async function exportAll() {
    window.location.href = "/export/";
}

document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const file = document.getElementById("fileInput").files[0];
    if (!file) return alert("Seleccioná un archivo");

    const formData = new FormData();
    formData.append("file", file);

    document.getElementById("status").innerText = "Procesando...";

    const res = await fetch("/upload/", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    document.getElementById("status").innerText =
        "Factura guardada con ID " + data.id;

    loadInvoices();
});

window.onload = loadInvoices;
