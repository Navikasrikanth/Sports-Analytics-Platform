USE sports_analytics;

-- USE sports_analytics;

-- ===========================
-- USERS (for login)
-- Passwords should be hashed in real app
-- ===========================
-- INSERT INTO Users (username, email, password_hash, role)
-- VALUES
-- ('admin', 'admin@clubanalytics.com', '$2y$10$FAKEHASHEDPASSWORD', 'admin'),
-- ('coach_view', 'coach@clubanalytics.com', '$2y$10$FAKEHASHEDPASSWORD', 'viewer');

-- ===========================
-- TEAMS
-- ===========================
INSERT INTO Teams (team_name, coach_name, founded_year, home_city)
VALUES
('Manchester United', 'Erik ten Hag', 1878, 'Manchester'),
('FC Barcelona', 'Xavi Hernandez', 1899, 'Barcelona'),
('Bayern Munich', 'Thomas Tuchel', 1900, 'Munich'),
('Paris Saint-Germain', 'Luis Enrique', 1970, 'Paris');

-- ===========================
-- PLAYERS
-- ===========================
INSERT INTO Players (name, dob, position, nationality, team_id)
VALUES
('Marcus Rashford', '1997-10-31', 'Forward', 'England', 1),
('Bruno Fernandes', '1994-09-08', 'Midfielder', 'Portugal', 1),
('Pedri Gonzalez', '2002-11-25', 'Midfielder', 'Spain', 2),
('Robert Lewandowski', '1988-08-21', 'Forward', 'Poland', 2),
('Joshua Kimmich', '1995-02-08', 'Midfielder', 'Germany', 3),
('Thomas Müller', '1989-09-13', 'Forward', 'Germany', 3),
('Kylian Mbappé', '1998-12-20', 'Forward', 'France', 4),
('Marco Verratti', '1992-11-05', 'Midfielder', 'Italy', 4);

-- ===========================
-- MATCHES
-- ===========================
INSERT INTO Matches (date, home_team_id, away_team_id, stadium, status)
VALUES
('2024-12-01', 1, 2, 'Old Trafford', 'Completed'),
('2024-12-05', 3, 4, 'Allianz Arena', 'Completed'),
('2024-12-10', 2, 4, 'Camp Nou', 'Completed');

-- ===========================
-- TEAM_MATCH
-- ===========================
INSERT INTO Team_Match (team_id, match_id) VALUES
(1,1),(2,1),
(3,2),(4,2),
(2,3),(4,3);

-- ===========================
-- SCORES (play-by-play)
-- Manchester United vs Barcelona
INSERT INTO Scores (match_id, team_id, player_id, points, minute_scored)
VALUES
(1, 1, 1, 1, 12),   -- Rashford
(1, 2, 3, 1, 33),   -- Pedri
(1, 2, 4, 1, 77);   -- Lewandowski

-- Bayern vs PSG
INSERT INTO Scores (match_id, team_id, player_id, points, minute_scored)
VALUES
(2, 3, 5, 1, 26),   -- Kimmich
(2, 4, 7, 1, 54),   -- Mbappe
(2, 3, 6, 1, 80);   -- Müller

-- Barcelona vs PSG
INSERT INTO Scores (match_id, team_id, player_id, points, minute_scored)
VALUES
(3, 2, 3, 1, 14),   -- Pedri
(3, 4, 8, 1, 61),   -- Verratti
(3, 4, 7, 1, 89);   -- Mbappe

-- ===========================
-- INJURIES
-- ===========================
INSERT INTO Injuries (player_id, injury_type, injury_date, expected_return, status)
VALUES
(1, 'Hamstring Strain', '2024-12-02', '2025-01-05', 'Recovering'),
(4, 'Foot Fracture', '2024-11-28', '2025-03-15', 'Injured'),
(7, 'Groin Injury', '2024-12-10', NULL, 'Injured');
