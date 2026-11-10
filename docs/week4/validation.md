# Validation

| Rule | Layer | How I tested it | What happened |
| --- | --- | --- | --- |
| First name and last name must not be empty | Flask | `curl` POST to `/join` with `first_name=` and `last_name=` | HTTP/1.1 400 BAD REQUEST |
| A name is at most 60 characters | Flask | `curl` with a `first_name` of 70 letters | HTTP/1.1 400 BAD REQUEST |
| The service must exist | Flask | `curl` with `service_id=999` | HTTP/1.1 400 BAD REQUEST |
| A switched-off service cannot be chosen | Flask | Switched a service off in Manage services, then `curl` with its `service_id` | HTTP/1.1 400 BAD REQUEST |
| Number of copies must be from 1 to 100 | Flask | `curl` with `copies=0`, then `101`, then `abc` | HTTP/1.1 400 BAD REQUEST |
| Color mode must be Grayscale or Colored | Flask | `curl` with `color_mode=Rainbow` | HTTP/1.1 400 BAD REQUEST |
| Notes are at most 300 characters | Flask | `curl` with `notes` of 301 letters | HTTP/1.1 400 BAD REQUEST |
| The file must be a real PDF | Flask | `curl` with a text file sent as `fake.pdf` | HTTP/1.1 400 BAD REQUEST |
| A file name is at most 255 characters | Flask | `curl` with a valid PDF sent with a 300-letter file name | HTTP/1.1 400 BAD REQUEST |
| FOREIGN KEY: a ticket needs a real service | Database | `INSERT INTO tickets (user_id, service_id, file_name, color_mode, copies, paper_type, paper_size) VALUES (2, 999, 'a.pdf', 'Colored', 1, 'Bond Paper', 'A4');` in psql | `ERROR: insert or update on table "tickets" violates foreign key constraint "tickets_service_id_fkey"` |
| FOREIGN KEY: a ticket needs a real user | Database | Same insert with `user_id` 999 | `ERROR: insert or update on table "tickets" violates foreign key constraint "tickets_user_id_fkey"` |
| CHECK: status must be one of five values | Database | `UPDATE tickets SET status = 'lost' WHERE id = 1;` | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_status"` |
| CHECK: copies are from 1 to 100 | Database | `UPDATE tickets SET copies = 0 WHERE id = 1;` | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_copies"` |
| CHECK: color mode is Grayscale or Colored | Database | `UPDATE tickets SET color_mode = 'Rainbow' WHERE id = 1;` | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_color_mode"` |
| CHECK: notes are at most 300 characters | Database | `UPDATE tickets SET notes = repeat('x', 301) WHERE id = 1;` | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_notes"` |
| CHECK: stored PDF name is 32 hex letters and `.pdf` | Database | `UPDATE tickets SET stored_name = 'evil.exe' WHERE id = 1;` | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_stored_name"` |
| CHECK: printing_at is not before created_at | Database | `UPDATE tickets SET printing_at = created_at - interval '1 day' WHERE id = 1;` | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_printing_at_after_created"` |
| CHECK: a first name is not blank | Database | `INSERT INTO users (first_name, last_name) VALUES ('   ', 'Copy');` | `ERROR: new row for relation "users" violates check constraint "ck_users_first_name"` |
| CHECK: role is requester or staff | Database | `UPDATE users SET role = 'boss' WHERE id = 2;` | `ERROR: new row for relation "users" violates check constraint "ck_users_role"` |
| CHECK: a service name is not blank | Database | `INSERT INTO services (name) VALUES ('  ');` | `ERROR: new row for relation "services" violates check constraint "ck_services_name"` |
| UNIQUE: a first and last name appears once | Database | `INSERT INTO users (first_name, last_name) VALUES ('Ana', 'Lee');` (already exists) | `ERROR: duplicate key value violates unique constraint "uq_users_first_name_last_name"` |
| UNIQUE: a service name appears once | Database | `INSERT INTO services (name) VALUES ('Printing');` | `ERROR: duplicate key value violates unique constraint "services_name_key"` |
| UNIQUE: a stored PDF belongs to one ticket | Database | `UPDATE tickets SET stored_name = (SELECT stored_name FROM tickets WHERE id = 1) WHERE id = 2;` | `ERROR: duplicate key value violates unique constraint "tickets_stored_name_key"` |
| UNIQUE (partial): one printing ticket per service | Database | Inserted two tickets with `status = 'printing'` for service 1 | The first worked. The second: `ERROR: duplicate key value violates unique constraint "uq_tickets_one_printing"` |
| NOT NULL: a ticket needs a file name | Database | `INSERT INTO tickets (user_id, service_id, color_mode, copies, paper_type, paper_size) VALUES (2, 1, 'Colored', 1, 'Bond Paper', 'A4');` | `ERROR: null value in column "file_name" of relation "tickets" violates not-null constraint` |
| NOT NULL: a user needs a last name | Database | `INSERT INTO users (first_name) VALUES ('Solo');` | `ERROR: null value in column "last_name" of relation "users" violates not-null constraint` |
| RESTRICT: a service with tickets cannot be deleted | Database | `DELETE FROM services WHERE id = 1;` | `ERROR: update or delete on table "services" violates foreign key constraint "tickets_service_id_fkey" on table "tickets"` |
| RESTRICT: a user with tickets cannot be deleted | Database | `DELETE FROM users WHERE id = 2;` | `ERROR: update or delete on table "users" violates foreign key constraint "tickets_user_id_fkey" on table "tickets"` |