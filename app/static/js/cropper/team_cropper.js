
document.addEventListener("DOMContentLoaded", function () {

    let cropper = null;

    const inputImage = document.getElementById("inputImage");
    const previewImage = document.getElementById("previewImage");
    const previewContainer = document.querySelector(".preview");
    const toolbar = document.getElementById("toolbar");

    const zoomIn = document.getElementById("zoomIn");
    const zoomOut = document.getElementById("zoomOut");
    const rotate = document.getElementById("rotate");
    const reset = document.getElementById("reset");
    const applyButton = document.getElementById("applyCrop");

    // Comprobar que los elementos existen
    if (
        !inputImage ||
        !previewImage ||
        !previewContainer ||
        !toolbar
    ) {
        console.error("No se encontraron los elementos del editor de escudos.");
        return;
    }

    // Seleccionar imagen
    inputImage.addEventListener("change", function (event) {

        const file = event.target.files[0];

        if (!file) return;

        if (!file.type.startsWith("image/")) {
            alert("Selecciona un archivo de imagen válido.");
            inputImage.value = "";
            return;
        }

        const reader = new FileReader();

        reader.onload = function (e) {

            // Destruir instancia anterior
            if (cropper) {
                cropper.destroy();
                cropper = null;
            }

            // Mostrar imagen seleccionada
            previewImage.style.display = "block";
            previewImage.src = e.target.result;

            previewImage.onload = function () {

                // Inicializar Cropper cuando la imagen ya cargó
                cropper = new Cropper(previewImage, {

                    aspectRatio: 1,
                    viewMode: 1,
                    preview: ".preview",
                    autoCropArea: 1,

                    movable: true,
                    zoomable: true,
                    scalable: true,
                    rotatable: true,

                    responsive: true,
                    background: false,

                    ready: function () {
                        toolbar.classList.add("active");
                    }

                });

            };

        };

        reader.readAsDataURL(file);

    });

    // Acercar
    zoomIn?.addEventListener("click", function () {
        if (cropper) cropper.zoom(0.1);
    });

    // Alejar
    zoomOut?.addEventListener("click", function () {
        if (cropper) cropper.zoom(-0.1);
    });

    // Rotar
    rotate?.addEventListener("click", function () {
        if (cropper) cropper.rotate(90);
    });

    // Restablecer
    reset?.addEventListener("click", function () {
        if (cropper) cropper.reset();
    });

    // Aplicar recorte
    applyButton?.addEventListener("click", function () {

        if (!cropper) return;

        const canvas = cropper.getCroppedCanvas({
            width: 300,
            height: 300,
            imageSmoothingEnabled: true,
            imageSmoothingQuality: "high"
        });

        if (!canvas) return;

        // Mostrar imagen recortada en la vista previa
        const croppedImage = canvas.toDataURL("image/png");

        previewContainer.innerHTML = "";

        const img = document.createElement("img");
        img.src = croppedImage;
        img.alt = "Escudo recortado";

        img.style.width = "100%";
        img.style.height = "100%";
        img.style.objectFit = "contain";

        previewContainer.appendChild(img);

        // Convertir el recorte a archivo para enviarlo al servidor
        canvas.toBlob(function (blob) {

            if (!blob) {
                alert("No se pudo procesar el recorte.");
                return;
            }

            const archivo = new File(
                [blob],
                "escudo.png",
                { type: "image/png" }
            );

            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(archivo);

            inputImage.files = dataTransfer.files;

        }, "image/png");

        // Destruir Cropper
        cropper.destroy();
        cropper = null;

        // Ocultar herramientas
        toolbar.classList.remove("active");

        // Ocultar imagen de edición
        previewImage.style.display = "none";

    });

});
