SELECT g.id, g.name, sb.name, round(AVG(gr.grade), 2) AS avg_grade
FROM groups g
JOIN students s ON g.id = s.group_id
JOIN grades gr ON s.id = gr.student_id
JOIN subjects sb ON sb.id = gr.subject_id
WHERE sb.id = 3
GROUP BY g.id