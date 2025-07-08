INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    'admin-0001', 'Admin', 'User', 'admin@example.com', 'hashedpassword', 1,
    datetime('now'), datetime('now')
);

INSERT INTO amenities (id, name, created_at, updated_at)
VALUES 
    ('amenity-0001', 'Wi-Fi', datetime('now'), datetime('now')),
    ('amenity-0002', 'Air Conditioning', datetime('now'), datetime('now')),
    ('amenity-0003', 'Swimming Pool', datetime('now'), datetime('now'));
