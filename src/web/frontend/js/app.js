class App extends HTMLElement {
    constructor() {
      super();
      const shadow = this.attachShadow({ mode: 'open' });
      shadow.innerHTML = `
        <style>
          /* Styles for the app */
        </style>
        <header-component></header-component>
        <main>
          <sidebar></sidebar>
          <chat></chat>
        </main>
      `;
    }
  }

  customElements.define('app', App);