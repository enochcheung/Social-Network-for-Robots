function on_post(input) {
	var post_content = input.post.content;
	var output = {posts:[{content:"response to "+post_content}]};
	return output;
}