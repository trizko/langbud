import { LANGUAGE_MAPPING } from "../state/constants.js";
import { fetchConversationsSuccess } from "../state/actions.js";
import { store } from "../state/store.js";

export class SidebarComponent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
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

    connectedCallback() {
        this.unsubscribe = store.subscribe(() => this.render());
        this.fetchConversations();
    }

    disconnectedCallback() {
        this.unsubscribe();
    }

    async fetchConversations() {
        let response = await fetch('/api/conversations');
        let data = await response.json();
        store.dispatch(fetchConversationsSuccess(data));
    }

    render() {
        const conversations = store.getState().conversations;
        const ul = this.shadowRoot.getElementById('conversationList');
        ul.innerHTML = conversations.map(conv => `
            <li>
                <button class="conversation-item ${conv.conversation_id === conversations.activeConversationId ? 'selected' : ''}" data-id="${conv.conversation_id}">
                    ${LANGUAGE_MAPPING[conv.conversation_language]}
                </button>
            </li>
        `).join('');

        ul.querySelectorAll('.conversation-item').forEach(item => {
            item.addEventListener('click', (e) => store.dispatch(setActiveConversation(Number(e.target.dataset.id))));
        });

        this.addEventListeners();
    }

    addEventListeners() {
        const addButton = this.shadowRoot.getElementById('addConversationBtn');
        addButton.addEventListener('click', () => {});
    }
}
