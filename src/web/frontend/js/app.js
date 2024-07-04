class App extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.render();
    }

    render() {
        this.shadowRoot.innerHTML = `
            <style>
            /* Styles for the app */
            </style>
            <header-component></header-component>
            <main>
                <sidebar></sidebar>
                <chat></chat>
            </main>
        `;
    }
}

customElements.define('app', App);