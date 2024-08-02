export const messageState = {
    messages: [],
    subscribers: [],
    activemessageId: 0,

    get() {
      return fetch('/api/messages')
        .then(response => response.json())
        .then(data => {
          this.messages = data;
          this.notify();
        });
    },
  
    add(message) {
      this.messages.push(message);
      this.notify();
    },

    subscribe(callback) {
      this.subscribers.push(callback);
    },
  
    notify() {
      this.subscribers.forEach(callback => callback());
    }
  };
  
  messageState.get();
  