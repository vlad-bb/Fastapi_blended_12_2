SELECT s.id, s.fullname, round(AVG(g.grade), 2) AS average_grade
FROM students s
JOIN grades g on s.id = g.student_id
GROUP BY s.id
ORDER BY average_grade DESC
LIMIT 5