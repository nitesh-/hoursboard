HoursBoard
==========
HoursBoard is a tool to generate details about how much time your screen was locked.

It gives the following details:

 - Screen lock time.
 - Screen unlock time.
 - Total time computer was switched ON.
 - Keep track of each logout by adding a Logout Tag.
 - If you don't wish to count a particular logout, provide 'space' as a logout tag.

Installation:
-------------

 1. Edit the `conf` file to specify directory to save logs.
 2. Grant `hoursboard.py` and `hoursboard-monit` execute permissions.
 3. Put `hoursboard-monit` in your startup script or run it once. This script will run in background and log your login/logout activity.
 4. To check screen lock summary, run `python hoursboard.py $(date +%F)`.
