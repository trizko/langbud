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
                #languageDropdown {
                    display: none;
                    width: 100%;
                    padding: 5px;
                    margin-top: 5px;
                }
            </style>
            <div>
                <h2>Conversations</h2>
                <ul id="conversationList"></ul>
                <button id="addConversationBtn">+ New Conversation</button>
                <select id="languageDropdown"></select>
            </div>
        `;
    }

    connectedCallback() {
        this.unsubscribe = store.subscribe(() => this.render());
        this.fetchConversations();
        this.addEventListeners();
        this.populateLanguageDropdown();
    }

    disconnectedCallback() {
        this.unsubscribe();
    }

    async fetchConversations() {
        let response = await fetch('/api/conversations');
        let data = await response.json();
        store.dispatch(fetchConversationsSuccess(data.active_conversation_id, data.conversations));
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

    populateLanguageDropdown() {
        const dropdown = this.shadowRoot.getElementById('languageDropdown');
        dropdown.innerHTML = `
            <option value="">Select a language</option>
            ${Object.entries(LANGUAGE_MAPPING).map(([key, value]) => `
                <option value="${key}">${value}</option>
            `).join('')}
        `;
    }

    async createNewConversation(language) {
        const response = await fetch('/api/conversations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ language }),
        });
        const newConversation = await response.json();
        await this.fetchConversations();
        store.dispatch(setActiveConversationAndMessages(newConversation.conversation_id, []));
    }

    addEventListeners() {
        const addButton = this.shadowRoot.getElementById('addConversationBtn');
        const dropdown = this.shadowRoot.getElementById('languageDropdown');

        addButton.addEventListener('click', () => {
            console.log(dropdown.style);
            dropdown.style.display = 'block';
            addButton.style.display = 'none';
        });

        dropdown.addEventListener('change', async (e) => {
            const selectedLanguage = e.target.value;
            if (selectedLanguage) {
                await this.createNewConversation(selectedLanguage);
                addButton.style.display = 'block';
                dropdown.style.display = 'none';
                dropdown.value = '';
            }
        });
    }
}
