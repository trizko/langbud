DROP INDEX IF EXISTS idx_explanations_message_id;
DROP INDEX IF EXISTS idx_explanations_user_id;
DROP TABLE IF EXISTS explanations;

DROP TABLE IF EXISTS messages;

DROP TRIGGER IF EXISTS update_modified_at_before_update ON users;
DROP FUNCTION IF EXISTS update_modified_at;
DROP INDEX IF EXISTS idx_users_username;
DROP TABLE IF EXISTS users;
