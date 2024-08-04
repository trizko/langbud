import {
    SET_ACTIVE_CONVERSATION,
    FETCH_CONVERSATIONS_SUCCESS,
    FETCH_CONVERSATIONS_FAILURE,
    ADD_CONVERSATION_REQUEST,
    ADD_CONVERSATION_SUCCESS,
    ADD_CONVERSATION_FAILURE,
    ADD_MESSAGE_REQUEST,
    ADD_MESSAGE_SUCCESS,
    ADD_MESSAGE_FAILURE,
} from './actionTypes';

export const setActiveConversation = (conversationId) => ({
    type: SET_ACTIVE_CONVERSATION,
    conversationId
});

export const fetchConversationsSuccess = (conversations) => ({
    type: FETCH_CONVERSATIONS_SUCCESS,
    conversations
});

export const fetchConversationsFailure = (error) => ({
    type: FETCH_CONVERSATIONS_FAILURE,
    error
});

export const addConversationRequest = () => ({
    type: ADD_CONVERSATION_REQUEST,
    conversation
});

export const addConversationSuccess = (conversation) => ({
    type: ADD_CONVERSATION_SUCCESS,
    conversation
});

export const addConversationFailure = (error) => ({
    type: ADD_CONVERSATION_FAILURE,
    error
});

export const addMessageRequest = () => ({
    type: ADD_MESSAGE_REQUEST,
    message
});

export const addMessageSuccess = (message) => ({
    type: ADD_MESSAGE_SUCCESS,
    message
});

export const addMessageFailure = (error) => ({
    type: ADD_MESSAGE_FAILURE,
    error
});