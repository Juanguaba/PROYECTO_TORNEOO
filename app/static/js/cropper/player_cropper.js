let cropper = null;

const inputImage = document.getElementById("inputImage");
const avatar = document.getElementById("playerAvatar");
const cropperImage = document.getElementById("cropperImage");
const toolbar = document.getElementById("toolbar");
const applyButton = document.getElementById("applyCrop");

if (inputImage && avatar && cropperImage) {

    inputImage.addEventListener("change", function (e) {

        const file = e.target.files[0];

        if (!file) return;

        const reader = new FileReader();

        reader.onload = function (event) {

            cropperImage.src = event.target.result;

            cropperImage.style.display = "block";

            document.getElementById("cropPreview").style.display = "block";

            avatar.style.display = "none";

            if (cropper) {

                cropper.destroy();

            }

            cropper = new Cropper(cropperImage, {

                aspectRatio: 1,

                viewMode: 1,

                preview: ".preview",

                autoCropArea: 1,

                movable: true,

                zoomable: true,

                scalable: true,

                rotatable: true,

                responsive: true

            });

            toolbar.classList.add("active");

        };

        reader.readAsDataURL(file);

    });

}


document.getElementById("zoomIn").addEventListener("click", function () {

    if (cropper) {

        cropper.zoom(0.1);

    }

});


document.getElementById("zoomOut").addEventListener("click", function () {

    if (cropper) {

        cropper.zoom(-0.1);

    }

});


document.getElementById("rotate").addEventListener("click", function () {

    if (cropper) {

        cropper.rotate(90);

    }

});


document.getElementById("reset").addEventListener("click", function () {

    if (cropper) {

        cropper.reset();

    }

});


applyButton.addEventListener("click", function () {

    if (!cropper) return;

    const canvas = cropper.getCroppedCanvas({

        width: 300,

        height: 300,

        imageSmoothingQuality: "high"

    });

    avatar.src = canvas.toDataURL("image/png");

    avatar.style.display = "block";

    cropperImage.style.display = "none";

    document.getElementById("cropPreview").style.display = "none";

    document.querySelector(".preview").style.display = "none";

    avatar.style.display = "block";

    cropperImage.style.display = "none";

    canvas.toBlob(function (blob) {

        const archivo = new File(

            [blob],

            "jugador.png",

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

    toolbar.classList.remove("active");

});