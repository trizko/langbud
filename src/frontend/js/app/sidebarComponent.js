import { LANGUAGE_MAPPING } from "../state/constants.js";
import { fetchConversationsSuccess, setActiveConversationAndMessages } from "../state/actions.js";
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
        this.addEventListeners();
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
        const state = store.getState();
        const ul = this.shadowRoot.getElementById('conversationList');
        ul.innerHTML = state.conversations.map(conv => `
            <li>
                <button class="conversation-item ${conv.conversation_id === state.activeConversationId ? 'selected' : ''}" data-id="${conv.conversation_id}">
                    ${LANGUAGE_MAPPING[conv.conversation_language]}
                </button>
            </li>
        `).join('');

        ul.querySelectorAll('.conversation-item').forEach(item => {
            item.addEventListener('click', async (e) => {
                let userResponse = await fetch('/api/user/', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        active_conversation_id: Number(e.target.dataset.id),
                    }),
                });
                let user = await userResponse.json();
                let messagesResponse = await fetch('/api/messages');
                let messages = await messagesResponse.json();
                store.dispatch(setActiveConversationAndMessages(user.active_conversation_id, messages));
            });
        });
    }

    addEventListeners() {
        const addButton = this.shadowRoot.getElementById('addConversationBtn');
        addButton.addEventListener('click', () => {});
    }
}
