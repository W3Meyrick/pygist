# PYGIST

pygist queries public gists, one user at a time :)

## Syntax

`pygist <username>`

Where `<username>` is the Github user's username.

The first time you query a user the script will display all gists
for that user. A user file will be created in the same working directory
named "./pygist.<username>". Subsequent executions for the same username 
will only show gists published since the last run. 

To reset an individual query delete the file `./pygist.<username>`.
To reset all queries delete all files `./pygist.*`

## Requirements

* Python 2.7 or higher
* Apply requirements.txt with pip

## Exit codes

* User not found: 255
* User has not published any gists: 1
* Success (first or subsequent queries): 0

## Notes

This solution opts not to use the GitHub API 'since' query parameter 
due to it including updated gists. The intention of this script is to 
show only new gists on subsequent executions.