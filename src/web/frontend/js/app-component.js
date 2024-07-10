export class AppComponent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.render();
        this.addEventListeners();
    }

    render() {
        this.shadowRoot.innerHTML = `
            <style>
            /* Styles for the app */
            </style>
            <header-component></header-component>
            <main>
                <sidebar-component></sidebarcomponent>
                <chat-component></chat>
            </main>
        `;
    }

    addEventListeners() {
        // Add event listeners here
    }
}