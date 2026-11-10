# Paprintco Requirements

## Setting
 
| | |
| --- | --- |
| **Setting** | A free student-organization printing service (Student Scholars Organization office) with a first come, first served print queue |
| **People who wait** | Students who need documents printed but do not own a printer (persona: Pia) |
| **People who serve** | Student officers in charge of the printing station (persona: Renebel) |
 
**Problem statement:** A student who owns no printer needs a way to send a PDF with its print settings and see their place in line, because waiting at the printing station without knowing when the copies will be ready wastes time close to deadlines. The officer at the station needs a way to see requests in the order they arrived and print the next one, because tracking requests in chat messages makes it easy to skip someone.
 
## Functional requirements
 
A ★ marks a requirement that is specific to printing.
 
| ID | Requirement | Priority | Stores data? | Status |
| --- | --- | --- | --- | --- |
| FR-01 | A requester can submit their first name, last name, a service, one PDF file and its print specifications (color mode, copies, paper type, paper size and instructions). | Must | Yes | Built (Week 3) |
| FR-02 | A requester can receive a ticket number after submitting their print request. | Must | Yes | Built (Week 3) |
| FR-03 | A requester can see how many requests are ahead of theirs and the current status of their print request. | Must | Yes | Built (Week 3) |
| FR-04 | A requester can see their queue position and status being updated automatically on their ticket page. | Should | No | Built (Week 3) |
| FR-05 | A requester can cancel their request while it is still waiting. | Must | Yes | Built (Week 3) |
| FR-06 | A staff member can see all waiting requests in queue order, with each request's print specifications. | Must | Yes | Built (Week 3) |
| FR-07 | A staff member can print the next request in the queue. | Must | Yes | Built (Week 3) |
| FR-08 | A staff member can filter all print requests by status. | Should | No | Built (Week 3) |
| FR-09 | A staff member can click "Mark as ready" on the request that is printing. | Must | Yes | Built (Week 3) |
| FR-10 | A staff member can click "Mark as done" on requests that are ready to be picked up. | Must | Yes | Built (Week 3) |
| FR-11 ★ | A staff member can open a request's PDF to check it before printing. | Must | Yes | Built (Week 3) |
| FR-12 ★ | A requester's PDF is deleted from the server when their request is done or cancelled. | Should | Yes | This week |
| FR-13 | A staff member can permanently delete a request. | Should | Yes | This week |
| FR-14 | A staff member can add, rename, deactivate and delete services. | Should | Yes | This week |
| FR-15 ★ | A requester can choose which pages of the PDF to print, or print all pages. | Could | Yes | Later |
| FR-16 ★ | A requester can choose different print specifications for each page. | Won't (this semester) | Yes | Later |
| FR-17 ★ | A staff member can print only one request at a time on each printer. | Must | Yes | Built (Week 3) |
| FR-18 ★ | A staff member can mark printing as unavailable with a reason (out of ink or out of paper), and a requester sees the notice and cannot submit a request until printing is available again. | Should | Yes | Later |
| FR-19 ★ | A requester can print up to 20 pages per week, and further requests are refused once that limit is reached. | Could | Yes | Later |
| FR-20 ★ | A staff member can place a request in the short-document queue or the long-document queue when there are two printers. | Could | Yes | Later |
| FR-21 | A requester can request other services besides printing, such as photocopying a physical document or getting blank paper. | Could | Yes | Later |
 
## Non-functional requirements

| ID | Requirement | Category | Priority |
| --- | --- | --- | --- |
| NFR-01 | The My place page shows the latest position and status within 10 seconds of a change, without a page reload. | Performance | Must |
| NFR-02 | The My place page loads in under 2 seconds on mobile data. | Performance | Should |
| NFR-03 | No ticket, user or service is lost when the Flask server or the database container restarts, and every ticket keeps the same status it had before the restart. | Reliability | Must |
| NFR-04 | The database generates every ticket number, so two people never get the same ticket, even if they join at the same moment. | Data integrity | Must |
| NFR-05 | The database rejects a ticket that points to a missing service or user, a status outside the allowed list, and a request for fewer than 1 copy. | Data integrity | Must |
| NFR-06 | Every screen works at a phone width of 375 px with no sideways page scroll. | Usability | Must |
| NFR-07 | Buttons and inputs are at least 44 px tall on a phone. | Usability | Must |
| NFR-08 | A first-time requester can submit a print request and find their ticket number in under 3 minutes. | Usability | Should |
| NFR-09 | Every screen scores 90 or higher on the Lighthouse accessibility audit. | Accessibility | Must |
| NFR-10 | Uploads are accepted only as PDF files up to 16 MB. | Security | Must |
| NFR-11 | Uploaded files are stored outside the project folder under random names. | Security | Must |
| NFR-12 | No SQL is built with string formatting. | Security | Must |
| NFR-13 | No password or secret key is stored in the repository. | Security | Must |
 
## MVP and out of scope

**MVP:** FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-07, FR-08, FR-09, FR-10, FR-11, FR-17, NFR-03, NFR-04, NFR-05, NFR-10, NFR-11, NFR-12.
 
This is the smallest useful version because a request can go all the way from submission to pickup, in first-come first-served order, with one request printing at a time and nothing lost on a restart. Everything else makes the app easier to use or cleaner to run, but the queue works without it.
 
**Out of scope:**
 
| Feature | Reason |
| --- | --- |
| Pricing and payment | The service is free, so nothing is charged. |
| Sending jobs straight to the printer from the app | It needs printer drivers and hardware access. Staff open the PDF and print it themselves. |
| Detecting ink and paper levels automatically | It needs printer-specific software. Staff mark printing unavailable by hand (FR-18). |
| Email or text notifications | They need outside services that are not part of this course. The My place page updates by itself instead. |
| Accepting Word files or images and converting them | Conversion adds a security and reliability risk. PDF only keeps uploads simple and checkable. |
 
## Feedback from a real person

| Role | What they said | What I changed |
| --- | --- | --- |
| Undergraduate student who requests prints | "Oo, makatabang gyud kaayo kung makapili ra ko ug unsa nga mga page akong i-print, kay most of the time usa ra ka page akong kinahanglan." | I kept FR-15 (choosing which pages to print) because the person wanted it. It stays as *Later* for now. |
| Same person | "Ug dapat makita dayon sa app kung wala nay ink or paper, para dili na ko mag-submit ug maghulat sa wala." | I kept FR-18 (printing marked unavailable with a reason) because the person wanted it. It stays as *Later* for now. |
| Same person | "Okay ra man sa akoa ang printout limit since libre ra gyud ang printing, so ang 20 ka pages per week kay okay na dayon." | I changed FR-19 to name the limit they suggested, 20 pages per week. |
| Same person | "Hasol kaayo kung maghulat pa ka nga usa ra diay ka page imong i-print, pero daghan kaayog pages ang nauna nimo." | I kept FR-20 (separate short-document and long-document queues) because the person wanted it. It stays as *Later* for now. |
| Same person | "Importante sab kaayo if makapangayo ka ug blank paper ug photocopy na service. For example, nagpa-print ko sa akong COR para naa koy mapasa for the scholarship requirement." | I added FR-21, because they need a service that is not only printing. |