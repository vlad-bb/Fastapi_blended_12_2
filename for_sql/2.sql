SELECT s.id, s.fullname, ROUND(AVG(g.grade), 2) AS average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
where g.subject_id = 3
GROUP BY s.id
ORDER BY average_grade DESC
LIMIT 1;