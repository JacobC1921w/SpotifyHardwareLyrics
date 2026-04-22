# SpotifyHardwareLyrics
Display currently playing spotify lyrics on external hardware!

Uses Spicetify to hook into spotify to retreive track data, gets lyrics from lrclib.net, and sends data via API to server file.

Server file currently just displays all received information, however will update to communicate with COM port to display information externally.

Displays the following information:
Artist
Album
Track Name
Progress bar (with timestamps)
Previous lyric
Current lyric
Next lyric


Originally I was going to try to find a static pointer to do this without using Spicetify, however CEF is too hard and I CBF to make it work :p

Currently platform independant (I think), and will hopefully stay so, but I know for a fact serial is gonna be funky...
