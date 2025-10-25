-- Insert Term 1 subjects
INSERT INTO subjects (subject_code, name, term_number, skill_type) VALUES
('BCU101', 'BCU', 1, 'hard_skill'),
('ENG101', 'English for IT', 1, 'both'),
('GEN101', 'General English', 1, 'soft_skill'),
('PL101', 'PL (Programming Language)', 1, 'hard_skill'),
('LOG101', 'Logic', 1, 'hard_skill'),
('DES101', 'Design', 1, 'both');

-- Insert Term 2 subjects
INSERT INTO subjects (subject_code, name, term_number, skill_type) VALUES
('WEB201', 'Web Design', 2, 'hard_skill'),
('ALG201', 'Algorithm', 2, 'hard_skill'),
('PL201', 'PL (Programming Language)', 2, 'hard_skill'),
('GEN201', 'General English', 2, 'soft_skill'),
('ENG201', 'English for IT', 2, 'both');

-- Insert sample terms
INSERT INTO terms (term_number, term_name, start_date, end_date, academic_year) VALUES
(1, 'Term 1', '2024-09-01', '2024-11-30', '2024-2025'),
(2, 'Term 2', '2024-12-01', '2025-02-28', '2024-2025');

-- Insert sample students
INSERT INTO students (student_id, name, email, program, enrollment_date) VALUES
('S2024001', 'John Doe', 'john.doe@example.com', 'Information Technology', '2024-09-01'),
('S2024002', 'Jane Smith', 'jane.smith@example.com', 'Information Technology', '2024-09-01'),
('S2024003', 'Mike Johnson', 'mike.johnson@example.com', 'Information Technology', '2024-09-01');

-- Insert sample skills
INSERT INTO skills (skill_name, skill_type, description) VALUES
('Programming', 'hard_skill', 'Ability to write and understand code'),
('Web Development', 'hard_skill', 'Creating websites and web applications'),
('Problem Solving', 'hard_skill', 'Analytical and logical thinking'),
('Communication', 'soft_skill', 'Effective verbal and written communication'),
('Teamwork', 'soft_skill', 'Collaboration and group work'),
('Critical Thinking', 'soft_skill', 'Analysis and evaluation of information');
