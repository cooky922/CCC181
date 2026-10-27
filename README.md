# Paprintco

Paprintco is a basic printing service queue system designed for students who need to request document printing and for the staff who processes those print requests. It offers one service, Print: students upload one PDF file and choose the printing options they want (color mode, number of copies, paper type, paper size and additional instructions), then track their place in the queue, while the staff manage the queue first come, first served and update the status of each print request. In order to run Paprintco, create a virtual environment first, run `pip install -r requirements.txt`, and then run `flask --app app run --debug` and open `http://127.0.0.1:5000` in your browser.

Note: the staff dashboard (`/staff`) has no login yet. Thus, anyone who knows the address can open it. Staff login comes in a later week.

★ Staff feature: the staff dashboard lets staff monitor the printing queue, view waiting requests, and update the status of each print request.