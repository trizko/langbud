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
                .conversation-item {
                    display: block;
                    width: 100%;
                    padding: 10px;
                    text-align: left;
                    background-color: white;
                    border: none;
                    border-bottom: 1px solid #ccc;
                    cursor: pointer;
                }
                .conversation-item:hover {
                    background-color: #f0f0f0;
                }
                .conversation-item.selected {
                    background-color: #e0e0e0;
                    font-weight: bold;
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
            <li>
                <button class="conversation-item ${conv.conversation_id === conversationState.activeConversationId ? 'selected' : ''}" data-id="${conv.conversation_id}">
                    ${conv.conversation_language}
                </button>
            </li>
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
