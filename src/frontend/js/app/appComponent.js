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
                height: 100%;
            }

            sidebar-component {
                width: 20%;
                display: block;
                background-color: #f4f4f4;
                overflow-y: auto;
                overflow-x: hidden;
                padding: 10px;
                box-sizing: border-box;
            }

            chat-component {
                flex: 1;
                background-color: #fff;
                box-sizing: border-box;
            }
            </style>

            <main>
                <sidebar-component></sidebar-component>
                <chat-component></chat-component>
            </main>
        `;
    }

    addEventListeners() {
        // Add event listeners here
    }
}