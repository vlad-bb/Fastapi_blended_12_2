SELECT s.fullname, sb.name, t.fullname
FROM teachers t
JOIN subjects sb ON sb.teacher_id = t.id
JOIN grades g ON sb.id = g.subject_id
JOIN students s ON g.student_id = s.id
WHERE s.id = 1 AND t.id = 1
GROUP BY sb.name