/*
on_post is called when a user you are following makes a post.

Pro Tip: You can follow yourself for easier testing
*/
function on_post(input) {
	var post_id = input.post.id;
	var content = input.post.content;
	var poster = input.post.user;
	var date = input.post.date;
	
	/*
	This is your persistent data storage. You can edit it
	directly using the editor next to the code editor.
	To update it here, you must pass it back as output.data
	*/
	var data = input.data;

	var output = {};
	output.posts = [];
	output.comments = [];
	output.follow = [];
	output.unfollow = [];
	output.log = [];
	output.data = data


	/*
	// Write a new post like this:

	new_post = {"content": "Hello World! #justprogrammerthings"};
	output.posts.push(new_post);
	

	// Write a comment like this:
	
	response = "Well said, @"+poster;
	new_comment = {"content": response, "post_id": post_id};
	output.comments.push(new_comment);
	
	
	// Follow someone like this:
	
	output.follow.push("my_bff");


	// Unfollow someone like this:

	output.unfollow.push("gary_oak");


	// Log something like this:

	output.log.push("Dear Diary, Today is a good day.");


	// Access and update your data like this:

	var num = data.example_num;
	num += 1;
	data.example_num = num;
	var new_num = 42;
	data.new_num = new_num;
	// save the changes by passing it back as output.data
	output.data = data;

	// Check out some examples by clicking Help or Docs for more info!

	*/


	return output;
}

/*
on_comment is called when someone comments on a post you made
*/
function on_comment(input) {
	var content = input.comment.content;
	var commenter = input.comment.user;
	var date = input.comment.date;
	var parent_post = input.comment.parent_post;
	var parent_post_content = parent_post.content;
	var parent_post_poster = parent_post.user;

	var data = input.data;

	var output = {};
	output.posts = [];
	output.comments = [];
	output.follow = [];
	output.unfollow = [];
	output.log = [];
	output.data = data


	/*
	See on_post for the schema for output
	*/

	return output;
}

/*
on_mention is called when someone mentions you in their post.

The input for on_mention is exactly the same as the input for on_post.
If an event satisfies the conditions for both on_post and on_mention,
only on_post will be called.
*/
function on_mention(input) {
	var post_id = input.post.id;
	var content = input.post.content;
	var poster = input.post.user;
	var date = input.post.date;

	var data = input.data;

	var output = {};
	output.posts = [];
	output.comments = [];
	output.follow = [];
	output.unfollow = [];
	output.log = [];
	output.data = data


	/*
	See on_post for the schema for output
	*/

	return output;
}


/*
on_follow is called when someone starts following you
*/
function on_follow(input) {
	var follower_username = input.follower;

	var data = input.data;

	var output = {};
	output.posts = [];
	output.comments = [];
	output.follow = [];
	output.unfollow = [];
	output.log = [];
	output.data = data


	/*
	See on_post for the schema for output
	*/

	return output;
}
