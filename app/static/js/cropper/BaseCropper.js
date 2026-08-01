class BaseCropper {

    constructor(config) {

        this.input = document.getElementById(config.inputId);
        this.image = document.getElementById(config.imageId);
        this.preview = document.getElementById(config.previewId);
        this.avatar = document.getElementById(config.avatarId);

        this.toolbar = document.getElementById(config.toolbarId);

        this.zoomIn = document.getElementById(config.zoomInId);
        this.zoomOut = document.getElementById(config.zoomOutId);
        this.rotate = document.getElementById(config.rotateId);
        this.reset = document.getElementById(config.resetId);
        this.apply = document.getElementById(config.applyId);

        this.width = config.width || 300;
        this.height = config.height || 300;
        this.fileName = config.fileName || "image.png";

        this.cropper = null;

        if (!this.input || !this.image) {
            return;
        }

        this.init();
    }

    init() {

        this.registerInput();

        this.registerToolbar();

    }

    registerInput() {

        this.input.addEventListener("change", (e) => {

            const file = e.target.files[0];

            if (!file) return;

            const reader = new FileReader();

            reader.onload = (event) => {

                this.image.src = event.target.result;

                this.image.style.display = "block";

                if (this.avatar) {
                    this.avatar.style.display = "none";
                }

                if (this.cropper) {
                    this.cropper.destroy();
                }

                this.cropper = new Cropper(this.image, {

                    aspectRatio: 1,

                    viewMode: 1,

                    preview: this.preview,

                    autoCropArea: 1,

                    movable: true,

                    zoomable: true,

                    scalable: true,

                    rotatable: true,

                    responsive: true

                });

                if (this.toolbar) {
                    this.toolbar.classList.add("active");
                }

                if (this.preview) {
                    this.preview.style.display = "block";
                }

            };

            reader.readAsDataURL(file);

        });

    }

    registerToolbar() {

        if (this.zoomIn) {

            this.zoomIn.onclick = () => {

                if (this.cropper) {
                    this.cropper.zoom(0.1);
                };

            };

        }

        if (this.zoomOut) {

            this.zoomOut.onclick = () => {

                if (this.cropper) {
                    this.cropper.zoom(-0.1);
                };

            };

        }

        if (this.rotate) {

            this.rotate.onclick = () => {

                if (this.cropper) {
                    this.cropper.rotate(90);
                };

            };

        }

        if (this.reset) {

            this.reset.onclick = () => {

                if (this.cropper) {
                    this.cropper.reset();
                };

            };

        }

        if (this.apply) {

            this.apply.onclick = () => {

                if (!this.cropper) return;

                const canvas = this.cropper.getCroppedCanvas({

                    width: this.width,

                    height: this.height,

                    imageSmoothingQuality: "high"

                });

                const dataUrl = canvas.toDataURL("image/png");

                this.image.src = dataUrl;

                this.image.style.display = "none";

                if (this.avatar) {

                    this.avatar.src = dataUrl;

                    this.avatar.style.display = "block";

                }

                canvas.toBlob((blob) => {

                    const archivo = new File(
                        [blob],
                        this.fileName,
                        {
                            type: "image/png"
                        }
                    );

                    const dataTransfer = new DataTransfer();

                    dataTransfer.items.add(archivo);

                    this.input.files = dataTransfer.files;

                }, "image/png");

                this.cropper.destroy();

                this.cropper = null;

                if (this.toolbar) {
                    this.toolbar.classList.remove("active");
                }

            };

        }

    }

}