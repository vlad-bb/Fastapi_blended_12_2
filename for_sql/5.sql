SELECT t.id, t.fullname, s.name
FROM teachers t
JOIN subjects s ON t.id = s.teacher_id
WHERE t.id = 3