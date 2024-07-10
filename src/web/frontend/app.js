import { AppComponent } from './js/app-component.js';
import { HeaderComponent } from './js/header-component.js';
import { Sidebar } from './js/sidebar.js';
import { Chat } from './js/chat.js';

customElements.define('app-component', AppComponent);
customElements.define('header-component', HeaderComponent);
customElements.define('sidebar', Sidebar);
customElements.define('chat', Chat);