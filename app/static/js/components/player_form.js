const fechaNacimiento = document.getElementById("fechaNacimiento");
const edadJugador = document.getElementById("edadJugador");

if (fechaNacimiento && edadJugador) {

    fechaNacimiento.addEventListener("change", function () {

        if (!this.value) {

            edadJugador.value = "";

            return;

        }

        const nacimiento = new Date(this.value);
        const hoy = new Date();

        let edad = hoy.getFullYear() - nacimiento.getFullYear();

        const mes = hoy.getMonth() - nacimiento.getMonth();

        if (
            mes < 0 ||
            (mes === 0 && hoy.getDate() < nacimiento.getDate())
        ) {

            edad--;

        }

        edadJugador.value = edad + " años";

    });

}