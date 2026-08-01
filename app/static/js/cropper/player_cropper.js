document.addEventListener("DOMContentLoaded", () => {

    new BaseCropper({

        inputId: "inputImage",

        imageId: "cropperImage",

        previewId: "cropPreview",

        avatarId: "playerAvatar",

        toolbarId: "toolbar",

        applyId: "applyCrop",

        zoomInId: "zoomIn",

        zoomOutId: "zoomOut",

        rotateId: "rotate",

        resetId: "reset",

        width: 300,

        height: 300,

        fileName: "jugador.png"

    });

});