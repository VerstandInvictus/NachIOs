# NachIOs
A collection of Hook.io and other scripts for connecting the Nachapp.com API to other services, mainly IFTTT.

ifthentrack.py - IFTTT Maker -> Hook.io script that updates a specified Nach tracker with today's date and an arbitrary value.

ifthenstep.py - IFTTT Maker -> Hook.io script that adds a step to a 
specified Nach tracker. Can set up to 2 notes as well as subject, and is designed for use with IFTTT email (subject -> title, body -> note, attachment URL -> note).

pocketcheck.py - self-hosted (I use AWS Linux) script that checks Pocket on 
a cron timer and makes completed steps for anything that's been archived 
since the last time it was run. Uses MongoDB for storing the timestamp; that's
 overkill, but I had a running MongoDB instance on the AWS box I'm using, so 
 it was easy and convenient. You could just as easily use Redis or Memcached
  or write to an INI file. Private settings are stored in a config.py file.