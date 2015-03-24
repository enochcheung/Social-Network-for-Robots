// Posting
function on_post(input) {
	var post_content = input.post.content;
	var output = {posts:[{content:"response to "+post_content}]};
	return output;
}




// Commenting
function on_post(input) {
	var post_content = input.post.content;
	var post_id = input.post.id;
	var data = input.data;
	data.num = data.num+1;
	var output = {comments:[{post_id:post_id, content:"response to "+post_content+" ("+data.num+")"}], data:data};
	return output;
}


function on_comment(input) {
    var comment = input.comment;
    var post = input.comment.parent_post;
    
    var new_comment = {"post_id":post.id,
                        "content":"responding to comment "+input.comment.content};
    
    var output = {"comments":[new_comment]};
    
    return output;
}


{"num":0}