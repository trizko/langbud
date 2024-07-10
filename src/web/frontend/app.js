import { AppComponent } from './js/app-component.js';
import { HeaderComponent } from './js/header-component.js';
import { SidebarComponent } from './js/sidebar-component.js';
import { Chat } from './js/chat.js';

customElements.define('app-component', AppComponent);
customElements.define('header-component', HeaderComponent);
customElements.define('sidebar-component', SidebarComponent);
customElements.define('chat', Chat);