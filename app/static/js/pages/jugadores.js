class PlayersPage {

    constructor() {

        this.container = document.getElementById("players-table-container");
        this.toolbar = document.getElementById("players-toolbar");

        if (!this.container || !this.toolbar) {
            return;
        }

        this.searchInput = document.getElementById("search-player");
        this.positionFilter = document.getElementById("filter-position");
        this.statusFilter = document.getElementById("filter-status");
        this.sortSelect = document.getElementById("sort-players");

        this.abortController = null;
        this.debounceTimer = null;

        this.init();

    }

    init() {

        console.log("✅ PlayersPage inicializado");

        this.bindEvents();

    }

    bindEvents() {

        this.bindSearch();

    }

    bindSearch() {

        this.searchInput.addEventListener("input", () => {

            clearTimeout(this.debounceTimer);

            this.debounceTimer = setTimeout(() => {

                this.fetchPlayers();

            }, 300);

        });

    }

    async fetchPlayers() {

        if (this.abortController) {
            this.abortController.abort();
        }

        this.abortController = new AbortController();

        const params = new URLSearchParams();

        params.set("buscar", this.searchInput.value);
        params.set("partial", "1");

        try {

            const response = await fetch(
                `${window.location.pathname}?${params.toString()}`,
                {
                    signal: this.abortController.signal
                }
            );

            if (!response.ok) {
                throw new Error("No se pudo cargar la tabla.");
            }

            const html = await response.text();

            this.updateTable(html);

        } catch (error) {

            if (error.name !== "AbortError") {
                console.error(error);
            }

        }

    }

    updateTable(html) {

        this.container.outerHTML = html;

        this.container = document.getElementById("players-table-container");

    }

}

window.PlayersPage = PlayersPage;