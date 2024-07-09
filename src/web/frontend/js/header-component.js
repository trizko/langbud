export class Header extends HTMLElement {
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
            /* Styles for the Header */
            </style>
            <header>
                <h1>Langbud</h1>
                <nav>
                    <a href="/profile">Profile</a>
                    <a href="/settings">Settings</a>
                </nav>
            </header>
        `;
    }

    addEventListeners() {
        // Add event listeners here
    }
}