SELECT s.fullname, gr.name, sb.name, g.grade, g.grade_date
FROM subjects sb
JOIN grades g ON g.subject_id = sb.id
JOIN students s ON g.student_id = s.id
JOIN groups gr ON s.group_id = gr.id
WHERE g.subject_id = 1 AND gr.id = 2
AND g.grade_date = (SELECT MAX(grade_date) FROM grades
                    WHERE student_id = s.id)
