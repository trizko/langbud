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
} from './actionTypes.js';

const initialState = {
    conversations: [],
    messages: [],
    activeConversationId: -1,
    error: null,
};

const reducer = (state = initialState, action) => {
    switch (action.type) {
        case SET_ACTIVE_CONVERSATION:
            return {
                ...state,
                activeConversationId: action.conversationId,
            };
        case FETCH_CONVERSATIONS_SUCCESS:
            return {
                ...state,
                conversations: action.conversations,
            };
        case FETCH_CONVERSATIONS_FAILURE:
            return {
                ...state,
                error: action.error,
            };
        case ADD_CONVERSATION_REQUEST:
            return state;
        case ADD_CONVERSATION_SUCCESS:
            return {
                ...state,
                conversations: state.conversations.concat(action.conversation),
            };
        case ADD_CONVERSATION_FAILURE:
            return {
                ...state,
                error: action.error,
            };
        case ADD_MESSAGE_REQUEST:
            return state;
        case ADD_MESSAGE_SUCCESS:
            return {
                ...state,
                messages: state.messages.concat(action.message),
            };
        case ADD_MESSAGE_FAILURE:
            return {
                ...state,
                error: action.error,
            };
        default:
            return state;
    }
};

export default reducer;
