export class SidebarComponent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.conversations = [];
    }

    connectedCallback() {
        this.render();
        this.addEventListeners();
    }

    render() {
        this.shadowRoot.innerHTML = `
            <style>
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                li {
                    padding: 10px;
                    border-bottom: 1px solid #ccc;
                }
            </style>
            <div>
                <h2>Conversations</h2>
                <ul id="conversationList"></ul>
            </div>
        `;
    }

    addEventListeners() {
        // Add event listeners here
    }
}
