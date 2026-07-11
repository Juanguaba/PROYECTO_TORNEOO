document.addEventListener("DOMContentLoaded", function () {

    const formularios = document.querySelectorAll(".delete-form");

    formularios.forEach(formulario => {

        formulario.addEventListener("submit", function (e) {

            e.preventDefault();

            const nombre = formulario.dataset.equipo;

            Swal.fire({

                title: "¿Eliminar equipo?",

                html: `
                    <p>Se eliminará el equipo:</p>
                    <h4><strong>${nombre}</strong></h4>
                    <br>
                    <p class="text-danger">
                        Esta acción no se puede deshacer.
                    </p>
                `,

                icon: "warning",

                showCancelButton: true,

                confirmButtonColor: "#dc3545",

                cancelButtonColor: "#6c757d",

                confirmButtonText: "🗑 Eliminar",

                cancelButtonText: "Cancelar",

                reverseButtons: true

            }).then((result) => {

                if (result.isConfirmed) {

                    formulario.submit();

                }

            });

        });

    });

});