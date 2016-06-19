# JSON diff API
The goal of this project is to provide a generic way of storing and comparing multiple versions of data source stored as JSON documents in git repositories. The application is designed to be generic and special treatment of specific data sources should be kept at a minimum.


## Endpoints
### GET /
Lists all available repositories

### GET /repository_name
 Lists added, changed and deleted files in the latest version of the repository
 
### GET /repository_name/files
Lists all files available in the given repository 
#### Arguments
*	search_term – only returns files that match the given search term based on a git grep

### GET /repository_name/files/<file_name>
View a given file in a given repository 
#### Arguments
*	steps – show the file for the given amount of steps from HEAD

### POST /repository_name/update
Takes a zip-file containing the complete latest version of the data source and creates a new commit using the data.
#### Arguments
*	steps – show the diff for the given amount of steps from HEAD

### GET repository_name/files/file_name/diff
Shows a line based diff of the given file in the given repository

### GET /repository_name/commits
Returns a list of commits for the given repository
#### Arguments
*	amount – the amount of commits you want to fetch from the API (default: 10)

## Improvements
### Authentication
The application does not enforce any form of authentication in its current state. This should be resolved if this where ever to be put into production.
### Testing with bigger data sources
As of now the app has only been tested using [NSL](http://nsl.mpa.se/) which is a fairly small data source. Because of this the app should be tested with more and bigger data sets to make sure the API remains stable and can respond in a timely fassion. 

## Related projects
* [JSON diff frontend](https://github.com/c0d3m0nkey/json-diff-frontend)
* [XML to JSON converter](https://github.com/c0d3m0nkey/xml-to-json-converter)
