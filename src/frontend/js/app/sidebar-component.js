export class SidebarComponent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.conversations = [];
    }

    connectedCallback() {
        this.fetchConversations();
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

    async fetchConversations() {
        try {
            const response = await fetch('/api/conversations');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            this.conversations = await response.json();
            this.updateConversationList();
        } catch (error) {
            console.error('Error fetching conversations:', error);
        }
    }

    updateConversationList() {
        const ul = this.shadowRoot.getElementById('conversationList');
        ul.innerHTML = this.conversations.map(conv => `
            <li>${conv.conversation_language}</li>
        `).join('');
    }

    addEventListeners() {
        // Add event listeners here
    }
}
