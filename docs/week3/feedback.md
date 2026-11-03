## Self-review of Personas and Wireframes
Screen 1 | Frames: request-phone, request-laptop
 
**Works well:** The form has one heading, a label above every field and one big full-width "Submit request" button, so Pia can tell what to do within 5 seconds, even with one hand on a phone. This follows Pia rule 3 (every choice shown with plain labels) and rule 4 (large tap targets). On the laptop, related fields sit side by side (color mode with number of copies, paper type with paper size), which keeps the form short.
 
**Problem:** Error prevention. The "[Upload File (.pdf)]" bar is a single full-width box with no room for the chosen file name or the file limits, and no layout space is shown for what happens when a field is blank or the file is not a PDF. Pia is on slow campus Wi-Fi, so she cannot tell whether the upload worked or why the form failed (rule 3 asks for clear error messages that keep what she typed). The input boxes on the phone also look short for a one-handed tap (rule 4).
 
**Change (kept):** I am keeping the layout. One column on the phone and two columns on the laptop is already the simplest form that meets FR-01 and FR-02, and extra elements would only slow Pia down. The problems are not layout decisions, so I will fix them in the HTML. Each field gets a message under it (for example "Enter your name.") that appears after submitting, and the form keeps what Pia typed. I will make inputs and buttons at least 44 px tall in Part 4. I am keeping paper type and paper size as two fields because Pia already thinks of them separately (for example "Bond paper, A4").
 
---
 
Screen 2 | Frames: my-place-phone, my-place-laptop
 
**Works well:** The ticket number (#11) is the largest thing on screen, followed by "5 requests ahead of you", so Pia sees what she needs first while walking between classes. "Updated just now" shows that the page refreshes by itself. This follows Pia rule 1 (ticket number, status and requests ahead are the biggest things) and rule 2 (the status updates by itself). "Cancel request" sits at the bottom, away from the information, so it is hard to tap by accident.
 
**Problem:** Visibility of system status and consistency. The "WAITING" badge is very small compared with the ticket number, which is hard to read for Pia, who has tired eyes late in the day (accessibility need). Nothing shows how close the request is to being done, so FR-04 is only covered by a number. On the laptop frame, the "Updated just now" text overlaps the "Your Request" box.
 
**Change (updated):** I am keeping the order (ticket number, status, position, request details, cancel) because it already matches what Pia needs first. I am making three changes to the wireframes. The status becomes a larger label that says "WAITING", with the same five words used on the staff dashboard screen (Waiting, Printing, Ready, Done, Cancelled). I am also fixing the overlapping text on the laptop frame. In the HTML, "Cancel request" will only show while the request is pending and will ask "Cancel this request?" before it goes through. I am not adding a refresh button because the page already updates by itself.
 
---
 
Screen 3 | Frames: dashboard-phone, dashboard-laptop
 
**Works well:** "Now Printing" is at the top, with "Print next" right under it and the counts below. The action Renebel uses most is the easiest to reach, which follows Renebel rule 1 (submission order and a clear "Print next" button) and rule 3 (one-click statuses). The list is titled "in ticket order", so he can show that requests are handled fairly. Each request shows its details through "View Details" (rule 2). On the laptop the two columns keep the current work on the left and the waiting list on the right, and the phone stacks the same blocks.
 
**Problem:** Error prevention and recognition rather than recall. "Print next" is drawn as available while a request is already printing, but my rule is one printing request at a time, so the screen invites a mistake. The phone and laptop frames also disagree (the phone has three tiles, the laptop five).

**Change (updated):** I am making the "Print next" button and the "Print" button on each waiting row look disabled while a request is already printing. On the phone, the three count cards (waiting, ready, done) become a row that scrolls sideways, which gives four cards (waiting, ready, cancelled, done), and the "total requests" card sits above them. This matches the laptop frame, so both frames now show the same five counts. The file and its print specifications stay available through "View Details" on each row. I am keeping the two-column laptop layout and the single "Mark as ready for pickup" button because they keep the most frequent actions close together for one hand on a busy counter.