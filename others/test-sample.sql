SELECT *
FROM Users as u
WHERE EXISTS (SELECT * From Users
				WHERE name = 'Sheila Williams'
				AND sleeping <= u.sleeping + interval '1 hour'
				AND sleeping >= u.sleeping - interval '1 hour')
AND name <> 'Sheila Williams';


SELECT *
FROM Users as u
WHERE EXISTS (SELECT * From Users
				WHERE name = 'Sheila Williams'
				AND waking <= u.waking + interval '1 hour'
				AND waking >= u.waking - interval '1 hour')
AND name <> 'Sheila Williams';


SELECT *
FROM Users as u
WHERE EXISTS (SELECT * From Users
				WHERE name = 'Sheila Williams'
				AND smoking = u.smoking)
AND name <> 'Sheila Williams';


SELECT *
FROM Users as u
WHERE EXISTS (SELECT * From Users
				WHERE name = 'Sheila Williams'
				AND room_utility = u.room_utility)
AND name <> 'Sheila Williams';