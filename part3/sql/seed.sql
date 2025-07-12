INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    'u-001',
    'Admin',
    'User',
    'admin@hbnb.com',
    'hashed_password_placeholder',
    TRUE,
    datetime('now'),
    datetime('now')
);

INSERT INTO amenities (id, name, created_at, updated_at)
VALUES 
    ('a-001', 'WiFi', datetime('now'), datetime('now')),
    ('a-002', 'TV', datetime('now'), datetime('now')),
    ('a-003', 'Pool', datetime('now'), datetime('now'));
