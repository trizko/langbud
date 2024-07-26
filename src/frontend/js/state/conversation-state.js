export const conversationState = {
    conversations: [],
    subscribers: [],
  
    get() {
      return fetch('/api/conversations')
        .then(response => response.json())
        .then(data => {
          this.conversations = data;
          this.notify();
        });
    },
  
    add(conversation) {
      this.conversations.push(conversation);
      this.notify();
    },
  
    subscribe(callback) {
      this.subscribers.push(callback);
    },
  
    notify() {
      this.subscribers.forEach(callback => callback());
    }
  };
  
  conversationState.get();
  