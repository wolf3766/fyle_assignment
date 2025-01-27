-- Write query to get count of assignments in each grade
select a.grade, count(*) as count from assignments as a where a.grade is not NULL group by a.grade 