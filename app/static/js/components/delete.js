document.querySelectorAll(".form-eliminar").forEach(form => {

    form.addEventListener("submit", function (e) {

        e.preventDefault();

        Swal.fire({
            title: "¿Eliminar jugador?",
            text: "Esta acción no se puede deshacer.",
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Sí, eliminar",
            cancelButtonText: "Cancelar",
            confirmButtonColor: "#dc3545"
        }).then((result) => {
            if (result.isConfirmed) {
                form.submit();
            }
        });

    });

});