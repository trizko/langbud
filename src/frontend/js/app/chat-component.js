export class ChatComponent extends HTMLElement {
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

    addEventListeners() {
        const form = this.shadowRoot.querySelector('form');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const message = this.shadowRoot.getElementById('message').value;
            console.log('Sending message:', message);
        });
    }
}