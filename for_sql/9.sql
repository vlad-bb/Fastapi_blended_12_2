SELECT s.id, s.fullname, sb.name
FROM students s
JOIN grades g ON s.id = g.subject_id
JOIN subjects sb ON g.student_id = sb.id
WHERE s.id = 3
GROUP BY sb.name