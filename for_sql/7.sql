SELECT s.id, s.fullname, sb.name, g.grade
FROM students s
JOIN grades g ON s.id = g.student_id
JOIN subjects sb ON g.subject_id = sb.id
WHERE s.group_id = 2 AND sb.id = 3