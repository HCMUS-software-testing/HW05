-- Chạy trên database test local sau khi thay placeholder bằng email thật.
UPDATE users
SET login_attempts = 0, locked_until = NULL
WHERE email = '<lockout-test-email>';

SELECT email, login_attempts, locked_until
FROM users
WHERE email = '<lockout-test-email>';
