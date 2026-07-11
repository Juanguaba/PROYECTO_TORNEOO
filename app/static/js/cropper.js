let cropper;

const inputImage = document.getElementById("inputImage");
const previewImage = document.getElementById("previewImage");

inputImage.addEventListener("change", function (e) {

    const file = e.target.files[0];

    if (!file) return;

    const reader = new FileReader();

    reader.onload = function (event) {

        previewImage.src = event.target.result;

        previewImage.style.display = "block";

        if (cropper) {
            cropper.destroy();
        }

        cropper = new Cropper(previewImage, {

            aspectRatio: 1,

            viewMode: 1,

            preview: ".preview",

            autoCropArea: 1,

            movable: true,

            zoomable: true,

            scalable: true,

            rotatable: true

        });

        document.getElementById("toolbar").classList.add("active");

    };

    reader.readAsDataURL(file);

});


document.getElementById("zoomIn").onclick = function () {

    if (cropper) {

        cropper.zoom(0.1);

    }

};


document.getElementById("zoomOut").onclick = function () {

    if (cropper) {

        cropper.zoom(-0.1);

    }

};


document.getElementById("rotate").onclick = function () {

    if (cropper) {

        cropper.rotate(90);

    }

};


document.getElementById("reset").onclick = function () {

    if (cropper) {

        cropper.reset();

    }

};

document
.getElementById("toolbar")
.classList.add("active");

document
.getElementById("toolbar")
.classList.remove("active");

const applyButton = document.getElementById("applyCrop");

applyButton.addEventListener("click", function () {

    if (!cropper) return;

    const canvas = cropper.getCroppedCanvas({

        width: 300,
        height: 300,
        imageSmoothingQuality: "high"

    });

    previewImage.src = canvas.toDataURL("image/png");

    canvas.toBlob(function (blob) {

        const archivo = new File(
            [blob],
            "escudo.png",
            {
                type: "image/png"
            }
        );

        const dataTransfer = new DataTransfer();

        dataTransfer.items.add(archivo);

        inputImage.files = dataTransfer.files;

    }, "image/png");

    cropper.destroy();

    cropper = null;

    document
        .getElementById("toolbar")
        .classList.remove("active");

});