##Product Backlog

* User submits JavaScript code which is executed server-side in a sandbox when certain events occurs. The user will be able to edit their code in their browser, with some syntax highlighting. The code that the user writes will be functions that takes as input details about an event, and output a list of actions to be taken.
  * Persistent data storage is available to the user's scripts, allowing the user's functions to be stateful. The data will be in JSON format, which will be given as part of the input, and the user can choose to return an update.
  * When there is an error during execution of the user's JavaScript, or an error in the format of the output, these errors will be logged and timestamped. Additional infomration about the error will be available for the user to view.
  * Available events:
    * Another user starts following you
    * A user you are following makes a post
    * A user you are following makes a comment
    * A user mentions you (using `@` tag) in a post
    * A user comments on your post
  * Available actions:
    * Write a new post
    * Write a new comment, specifying parent post (by id)
    * Start following a user
    * Stop following a user
    * Update persistent storage
    * Make an entry in the log
