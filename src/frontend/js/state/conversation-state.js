export const conversationState = {
    conversations: [],
    subscribers: [],
    activeConversationId: 0,

    get() {
      return fetch('/api/user')
        .then(response => response.json())
        .then(data => {
          this.activeConversationId = data.active_conversation_id;
          return fetch('/api/conversations');
        })
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

    setActiveConversation(conversationId) {
      return fetch('/api/user', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          active_conversation_id: conversationId
        })
      })
      .then(response => response.json())
      .then(data => {
        this.activeConversationId = data.active_conversation_id;
        this.notify();
      });
    },
  
    subscribe(callback) {
      this.subscribers.push(callback);
    },
  
    notify() {
      this.subscribers.forEach(callback => callback());
    }
  };
  
  conversationState.get();
  