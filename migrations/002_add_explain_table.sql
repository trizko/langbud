CREATE TABLE explanations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL,
    explanation_text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (message_id) REFERENCES messages (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE INDEX idx_explanations_user_id ON explanations USING HASH (user_id);
CREATE INDEX idx_explanations_message_id ON explanations USING HASH (message_id);