import { fetchMessagesSuccess } from '../state/actions.js';
import { store } from '../state/store.js';

export class ChatComponent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.innerHTML = `
        <style>
            .chat-container {
                width: 50%;
                margin: 0 auto;
                font-family: Arial, sans-serif;
            }
            .chat {
                display: flex;
                flex-direction: column;
                background-color: #f0f0f0;
                border-radius: 10px;
                padding: 10px;
                max-height: 400px;
                overflow-y: auto;
            }
            .message {
                display: inline-block;
                margin-bottom: 10px;
                padding: 8px 12px;
                border-radius: 18px;
                max-width: 80%;
                word-wrap: break-word;
            }
            .sent {
                background-color: #DCF8C6;
                align-self: flex-end;
                margin-left: auto;
                text-align: right;
            }
            .received {
                background-color: #FFFFFF;
                align-self: flex-start;
                text-align: left;
            }
            form {
                display: flex;
                margin-top: 10px;
            }
            input {
                flex-grow: 1;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 20px;
                margin-right: 5px;
            }
            button {
                padding: 8px 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 20px;
                cursor: pointer;
            }
        </style>
        <div class="chat-container">
            <div class="chat" id="chat"></div>
            <form>
                <input type="text" id="message" placeholder="Message" required>
                <button type="submit">Send</button>
            </form>
        </div>
        `;
    }

    connectedCallback() {
        this.unsubscribe = store.subscribe(() => this.render());
        this.fetchMessages();
    }

    fetchMessages() {
        fetch('/api/messages')
            .then(response => response.json())
            .then(data => store.dispatch(fetchMessagesSuccess(data)));
    }

    render() {
        const messages = store.getState().messages;
        const chat = this.shadowRoot.getElementById('chat');
        chat.innerHTML = messages.map(msg => {
            const msg_type = msg.is_from_user ? 'sent' : 'received';
            return `<div class="message ${msg_type}">
                ${msg.message_text}
            </div>`;
        }).join('');
        chat.scrollTop = chat.scrollHeight;

        this.addEventListeners();
    }

    addEventListeners() {
        const form = this.shadowRoot.querySelector('form');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const messageInput = this.shadowRoot.getElementById('message');
            const message = messageInput.value.trim();
            console.log("Sending message:", message);
        });
    }
}
