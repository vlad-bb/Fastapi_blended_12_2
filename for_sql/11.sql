SELECT round(AVG(g.grade), 2) AS avg_grade, s.fullname, t.fullname
FROM students s
JOIN grades g ON s.id = g.student_id
JOIN subjects sb ON g.subject_id = sb.id
JOIN teachers t ON sb.teacher_id = t.id
WHERE t.id = 2 AND s.id = 5
