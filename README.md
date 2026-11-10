# Paprintco

Paprintco is a basic printing service queue system designed for students who need to request document printing and for the staff who processes those print requests. Students upload one PDF file and choose the printing options they want (color mode, number of copies, paper type, paper size and additional instructions), then track their place in the queue. The staff manage the queue first come, first served, update the status of each print request, and manage the services. All data is saved in PostgreSQL, so nothing is lost when the app restarts.

Requirements: [docs/requirements.md](docs/requirements.md)

Week 4 documents: [schema and ERD](docs/week4/schema.md), [schema review](docs/week4/schema-review.md)

## How to run it

You need Python and Docker Desktop.

1. Create and activate a virtual environment, then install the packages:

   ```
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env`, then change the password in it. Use the same password in `POSTGRES_PASSWORD` and inside `DATABASE_URL`.

3. Start PostgreSQL and wait until `docker compose ps` says **healthy**:

   ```
   docker compose up -d
   ```

4. Create the tables and add the starting service:

   ```
   flask --app app db upgrade
   flask --app app seed
   ```

5. Run the app and open `http://127.0.0.1:5000` in your browser:

   ```
   flask --app app run --debug
   ```

Use `docker compose down` to stop the database. Your data stays. Do not use `docker compose down -v`, because it deletes the data.

## Note

The staff pages (`/staff` and `/staff/services`) have no login yet. Thus, anyone who knows the address can open them. Staff login comes in a later week.

★ Staff feature: the staff dashboard lets staff monitor the printing queue, view waiting requests, and update the status of each print request.