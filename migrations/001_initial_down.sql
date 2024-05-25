DROP TABLE IF EXISTS messages;
DROP TRIGGER IF EXISTS update_modified_at_before_update ON users;
DROP FUNCTION IF EXISTS update_modified_at;
DROP INDEX IF EXISTS idx_users_username;
DROP TABLE IF EXISTS users;
