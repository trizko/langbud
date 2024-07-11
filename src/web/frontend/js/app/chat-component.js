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
            /* Styles for the chat component */
            </style>
            <div>
                <h2>Chat</h2>
                <div id="chat"></div>
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