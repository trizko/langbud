import { conversationState } from "../state/conversation-state.js";

export class SidebarComponent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.addEventListeners();
        this.render();
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

    updateConversationList() {
        const ul = this.shadowRoot.getElementById('conversationList');
        ul.innerHTML = conversationState.conversations.map(conv => `
            <li>${conv.conversation_language}</li>
        `).join('');
    }

    addEventListeners() {
        conversationState.subscribe(this.updateConversationList.bind(this));
    }
}
