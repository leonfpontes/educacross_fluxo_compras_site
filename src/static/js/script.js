console.log("script.js carregado."); // Log de carregamento do script

document.addEventListener("DOMContentLoaded", function() {
    console.log("DOMContentLoaded disparado."); // Log do DOM pronto

    const modal = document.getElementById("uploadModal");
    const closeButton = modal ? modal.querySelector(".close-button") : null;
    const editIcons = document.querySelectorAll(".edit-icon");
    const uploadForm = document.getElementById("uploadForm");
    const fileNameToReplaceSpan = document.getElementById("fileNameToReplace");
    const targetFileInput = document.getElementById("targetFile");
    const fileTypeInput = document.getElementById("fileType");
    const uploadMessageDiv = document.getElementById("uploadMessage");
    const fileUploadInput = document.getElementById("fileUpload");

    if (!modal || !closeButton || !uploadForm || !fileNameToReplaceSpan || !targetFileInput || !fileTypeInput || !uploadMessageDiv || !fileUploadInput) {
        console.warn("Um ou mais elementos do modal de upload não foram encontrados. A funcionalidade de edição pode não funcionar.");
    } else {
        console.log("Todos os elementos do modal encontrados.");
    }

    console.log(`Encontrados ${editIcons.length} ícones de edição.`); 

    editIcons.forEach((icon, index) => {
        console.log(`Adicionando listener ao ícone ${index + 1}:`, icon); 
        icon.addEventListener("click", function(event) {
            event.preventDefault();
            // alert("Ícone de edição clicado! Target: " + this.dataset.targetFile); // Removido alerta original
            console.log("Ícone de edição clicado:", this);
            console.log("Dataset targetFile:", this.dataset.targetFile);
            console.log("Dataset fileType:", this.dataset.fileType);
            console.log("Modal:", modal);
            
            const targetFile = this.dataset.targetFile;
            const fileType = this.dataset.fileType;
            
            if (modal && fileNameToReplaceSpan && targetFileInput && fileTypeInput && uploadMessageDiv && uploadForm) {
                console.log("Abrindo modal para:", targetFile);
                fileNameToReplaceSpan.textContent = targetFile;
                targetFileInput.value = targetFile;
                fileTypeInput.value = fileType;
                uploadMessageDiv.innerHTML = ""; 
                uploadForm.reset(); 
                modal.style.display = "block";
            } else {
                console.error("Erro: Elementos do modal não estão disponíveis ao tentar abrir.");
                // alert("Erro ao tentar abrir o formulário de upload. Elementos faltando. Verifique o console."); // Removido alerta original
            }
        });
    });

    if (closeButton) {
        closeButton.onclick = function() {
            if (modal) modal.style.display = "none";
        }
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            if (modal) modal.style.display = "none";
        }
    }

    if (uploadForm) {
        uploadForm.addEventListener("submit", function(event) {
            event.preventDefault();
            uploadMessageDiv.innerHTML = "Enviando...";
            const formData = new FormData(this);

            fetch(UPLOAD_URL, {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    uploadMessageDiv.innerHTML = `<p style=\"color:green;\">${data.message}</p>`;
                    if (data.new_src && targetFileInput.value === "fluxo_compras_visual.png") {
                        const imgElement = document.getElementById("fluxogramaVisual");
                        if (imgElement) {
                            imgElement.src = data.new_src + "?v=" + new Date().getTime(); // Cache busting para a imagem
                        }
                    }
                    setTimeout(() => {
                        if (modal) modal.style.display = "none";
                    }, 2000);
                } else {
                    uploadMessageDiv.innerHTML = `<p style=\"color:red;\">Erro: ${data.message}</p>`;
                }
            })
            .catch(error => {
                console.error("Erro no upload:", error);
                uploadMessageDiv.innerHTML = `<p style=\"color:red;\">Erro de conexão ao tentar enviar o arquivo.</p>`;
            });
        });
    }
});

