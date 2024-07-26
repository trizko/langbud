import { conversationState } from "../state/conversation-state.js";

export class SidebarComponent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        conversationState.subscribe(this.updateConversationList.bind(this));
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
                #addConversationBtn {
                    display: block;
                    width: 100%;
                    padding: 10px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    cursor: pointer;
                    margin-top: 10px;
                }
                #addConversationBtn:hover {
                    background-color: #45a049;
                }
            </style>
            <div>
                <h2>Conversations</h2>
                <ul id="conversationList"></ul>
                <button id="addConversationBtn">+ New Conversation</button>
            </div>
        `;
    }

    addEventListeners() {
        const addButton = this.shadowRoot.getElementById('addConversationBtn');
        addButton.addEventListener('click', () => this.addConversation());
    }

    updateConversationList() {
        const ul = this.shadowRoot.getElementById('conversationList');
        ul.innerHTML = conversationState.conversations.map(conv => `
            <li>${conv.conversation_language}</li>
        `).join('');
    }

    addConversation() {
        conversationState.add({
            conversation_id: 99,
            user_id: 1,
            conversation_language: 'new',
        });
    }
}
