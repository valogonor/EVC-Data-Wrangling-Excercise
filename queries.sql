/*
Since there's no id column in the vendor4_users table, I made the combination of last_first_name and reg_date the id. I chose those columns for the id because
there were no null values for those columns. I used the placement of the comma in last_first_name to split the column into first_name and last_name.
*/
SELECT CONCAT(last_first_name, reg_date) AS id,
  split_part(last_first_name, ',', 2) first_name,
  split_part(last_first_name, ',', 1) last_name,
  phone AS phone_number,
  zip_code,
  EXTRACT(MONTH FROM reg_date) month_registerted
FROM vendor4_users;

--I created common table expressions for each of the counts and created a select statement that joined the three CTEs on the columns in the group by clause.
WITH total_count AS(
  SELECT org, state, COUNT(*) total
  FROM registrations
  GROUP BY org, state
),
completed_registration_count AS(
  SELECT org, state, COUNT(*) completed_registrations
  FROM registrations
  WHERE is_complete_registration = true
  GROUP BY org, state
),
valid_incomplete_registration_count AS(
  SELECT org, state, COUNT(*) valid_incomplete_registrations
  FROM registrations
  WHERE is_complete_registration = false AND is_valid_registration = true
  GROUP BY org, state
)

SELECT tc.org, tc.state, total, completed_registrations, valid_incomplete_registrations
FROM total_count tc
JOIN completed_registration_count crc
ON tc.org = crc.org AND tc.state = crc.state
JOIN valid_incomplete_registration_count virc
ON tc.org = virc.org AND tc.state = virc.state;

-- In order to get all the calls and find out which ones did not have callers, I started with dials and did a left join on callers before joining programs.
SELECT p.name program_name, p.date program_date, COALESCE(c.name, 'autodialer') caller_name, COUNT(*) num_calls
FROM dials d
LEFT JOIN callers c 
ON c.id = d.caller_id
JOIN programs p
ON p.id = d.program_id
GROUP BY 3, 1, 2;