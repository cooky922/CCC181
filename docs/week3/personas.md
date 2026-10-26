## Pia, the person waiting
 
> "Daghan kaayo kog i-print, pero dili pud ko ganahan magtambay ug pila ka minuto sa printing station nga wa ko kabalo kung kanus-a nako ma claim. If possible, gusto nako i-submit akong file and get notified kung ready na i-claim." *(interview)*

| | |
| --- | --- |
| **Photo or sketch** | <p align="center"><img src="screenshots/persona-1.png" width="25%" /></p> |
| **Age, role and background** | 22, 4th-year BS Biology (Microbiology) student. In her thesis semester, she prints drafts, revisions, tables and figures often. Does not own a printer. |
| **Goals** | 1. Send her thesis files for printing without queuing in person.<br>2. Know how many requests are ahead of hers, and when hers is ready for pickup.<br>3. Get the right print settings (color for figures, grayscale for text, the right paper) the first time. |
| **Frustrations** | 1. Has a lot to print but no printer of her own.<br>2. Waiting around with no idea of her turn.<br>3. Reprints when configurations are wrong, which costs time and money close to deadlines. |
| **Devices and context** | Phone between lab sessions and library time, laptop when she is writing. Often using campus Wi-Fi that is slow at peak hours. Usually carrying lab notes or a backpack, so she uses one hand. |
| **Tech comfort** | Medium. Comfortable with forms, file uploads and messaging apps, but does not want to learn a complicated system. |
| **Accessibility needs** | Tired eyes late in the day, so large text and strong contrast. Phone-first, one-handed use with large tap targets. Slow data, so pages must be light. |
 
### Scenario
 
It is the week before the thesis draft is due. Pia finishes revising her Chapter 3 in the CSM library and realizes she needs three copies of her full draft plus colored figures. She opens Paprintco on her phone, attaches the PDF, select appropriate printing specifications such as choosing A4 paper size. She gets ticket #14 and sees "3 requests ahead of you". She then walks to her lab while Paprintco automatically updates her queue position and status. When the status changes to "Ready", she walks to the printing station and gets her copies without waiting in line.
 
### Top tasks in the app
 
| Task | Screen | Requirement ID |
| --- | --- | --- |
| Submit their name, PDF attachment, and its printing specifications | Request print | FR-01 |
| Receive their ticket number for their print request | My ticket | FR-02 |
| Check how many requests are ahead and the current status | My ticket | FR-03 |
| See how close the line is to finishing | Queue line | FR-04 |
| Cancel a request that is still waiting | My ticket | FR-05 |
 
### What this means for my interface
 
1. Because Pia checks her phone between lab sessions, her ticket number, status and "requests ahead" message must be the biggest things on My ticket.
2. Because her campus Wi-Fi is slow, pages must stay light, and the status must update by itself every few seconds without a reload.
3. Because wrong print settings mean costly reprints, the request form must show every choice (e.g. color mode, pages, copies, paper type) with plain labels, and show clear error messages that keep what she typed.
4. Because she is often carrying things, buttons and inputs must be large enough to tap with one hand.
---
 
## Renebel, the staff member
 
> "Usahay kapoy na gyud kay sige'g send ug files ang mga tao sa Messenger tibuok adlaw. Mag-scroll pa ko pataas ug paubos para ma-check pa kung kinsay unang nag-send, unya kung naay malaktawan, murag ako dayon ang basulon. Lisod kaayo i-track ang tanan kung daghan na kaayo ang requests." *(interview)*
 
| | |
| --- | --- |
| **Photo or sketch** | <p align="center"><img src="screenshots/persona-2.png" width="25%" /></p> |
| **Age, role and background** | 20, 3rd-year BS Electronics Engineering student and officer in charge of free printing services at the Student Scholars Organization office. Responsible for organizing print requests, facilitating printing, and helping students receive their documents. |
| **Goals** | 1. See all print requests in one place, in the order they came in.<br>2. Decide quickly whose request to print next, and be able to show that it was fair.<br>3. Get each file and its print settings without asking the requester again. |
| **Frustrations** | 1. Requests and attachments arrive through Messenger, mixed in with other chats.<br>2. The volume of requests is high, and he is unsure which one to entertain first.<br>3. Requesters keep messaging "is mine done yet?", which interrupts the printing itself. |
| **Devices and context** | A shared organization laptop at the printing station. Sometimes his own phone. Busy office, interruptions from walk-ins, printing and handing out copies at the same time. |
| **Tech comfort** | High. Knowledgeable about technology and comfortable with dashboards, but has little time to learn or set anything up. |
| **Accessibility needs** | Needs to scan the queue at a glance in a noisy, busy setting. The most common action must be easy to reach, and a status must never be shown by color alone. |
 
### Scenario
 
It is 2 PM and the office is crowded. Renebel opens the Paprintco staff dashboard on the shared laptop and sees print requests arranged in queue order. He clicks "Print next", and the system selects the earliest waiting request, ticket #11. The attached PDF and its specifications are available for inspection, including paper size, paper type, color mode, and number of copies. After processing the print request, he updates its status to "Ready". Paprintco updates the requester's ticket. Once the documents are collected, he then marks the request as "Done".

### Top tasks in the app
 
| Task | Screen | Requirement ID |
| --- | --- | --- |
| See all waiting requests and their printing specifications in queue order | Staff dashboard | FR-06 |
| Print the next request and update its status | Staff dashboard | FR-07 |
 
### What this means for my interface

1. Because Renebel is unsure which request to entertain first, the dashboard must arrange print requests by submission time and provide a clear "Print next" button to help process requests fairly.
2. Because he needs to process requests efficiently, each request must clearly display the uploaded PDF, paper size, paper type, color mode for the entire document, and number of copies.
3. Because the office is busy and he prints in between, status buttons must be one click, and a status must be shown in words, not only color.
4. Because many requesters ask "is mine done?", status changes must show on the requester's ticket automatically, so he does not have to answer in chat.