class LoginForm extends HTMLElement {
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
                form {
                    display: flex;
                    flex-direction: column;
                }
                input, button {
                    margin-bottom: 10px;
                    padding: 5px;
                }
            </style>
            <form>
                <input type="text" id="username" placeholder="Username" required>
                <input type="password" id="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
            <a href="/login-with-discord">
                <button>Login with Discord</button>
            </a>
        `;
    }

    addEventListeners() {
        const form = this.shadowRoot.querySelector('form');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const username = this.shadowRoot.getElementById('username').value;
            const password = this.shadowRoot.getElementById('password').value;
            console.log('Login attempt:', { username, password });
        });
    }
}

customElements.define('login-form', LoginForm);
