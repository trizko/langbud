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
            main {
                display: flex;
            }
            sidebar-component {
                display: block;
                border: 1px solid black;
                width: 20%;
                height: 100vh;
            }
            chat-component {
                display: block;
                border: 1px solid black;
                width: 80%;
            }
            </style>

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