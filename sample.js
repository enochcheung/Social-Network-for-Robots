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


function on_mention(input) {
    var post_content = input.post.content;
    var post_id = input.post.id;
    var data = input.data;
    data.num = data.num+1;
    
    var output = {comments:[{post_id:post_id, content:"response to mention: "+post_content+" ("+data.num+")"}], data:data};
    return output;
}



function on_follow(input) {
    var follower = input.follower;
    
    var new_post = {"content":"@"+follower+" welcome!"};

    var output = {"posts":[new_post]};
    
    return output;
}



// Jules

function on_post(input) {
    var post = input.post;
    
     if (post.content.indexOf("what")!= -1 || post.content.indexOf("What")!= -1 ) {
        var post_id = input.post.id;
        var author = post.user;
        var data = input.data;
        
        if (!(data.watching.hasOwnProperty(author))) {
            data.watching[author]=0;
        }
        
        var content = "";
        
        times = data.watching[author];
        if (times === 0) {
            content = "What country are you from?";
        } else if (times===1) {
            content = "\"What\" ain't no country I ever heard of! They speak English in \"What\"?";
            
        } else if (times===2) {
            content = "English, motherf**ker! Do you speak it!?";
        } else if (times===3) {
            content = "Say \"what\" again! SAY \"what\" again! I dare you! I double-dare you, motherf**ker! Say \"what\" one more goddamn time!";
            
        } else if (times===4) {
            content = "*BOOM*";
            data.watching[author]=-1;
        }
        
        data.watching[author]++;
    
        var comment = {"post_id":post_id, "content":content};
        var output = {"comments":[comment]};
        output.data = data;
    
        return output;
    }
    
    return {};
}

function on_mention(input) {
    var post = input.post;
    
    if (post.content.indexOf("follow")!= -1) {
        var post_id = input.post.id;
        var author = post.user;
        var data = input.data;
        
        if (!(data.watching.hasOwnProperty(author))) {
            data.watching[author]=0;
        }
    
        var comment = {"post_id":post_id, "content":"What does Marsellus Wallace look like?"};
        var output = {"comments":[comment]};
        output.follow = [author];
        output.data = data;
    
        return output;
    }
    
    return {};
    

}


{
  "watching":{}
}




// todo
function on_mention(input) {
    var post_id = input.post.id;
    var content = input.post.content;
    var poster = input.post.user;

    var data = input.data;

    var output = {};
    output.comments = [];

    var lists = data.lists;
    if (!lists.hasOwnProperty(poster)) {
        lists[poster] = [];
    }
    var list = lists[poster];
    
    var regex = /^@todo (\w+) (.*)/;
    var match = regex.exec(content);
    
    var response = "";
    if (!match) {
        response = "Commands:\n@todo add item\n@todo remove index\n.\n";
    } else if (match[1]=="add") {
        list.push(match[2]);
    } else if (match[1]=="remove") {
        var index = parseInt(match[2]);
        if (!((index<=list.length)&&(1<= index))) {
            response = "Invalid index for removal\n";
        } else {
            list.splice(index-1,1);
        }
    }
    
    for (i=0;i<list.length;i++) {
        response += String(i+1)+". "+list[i]+"\n";
    }
    new_comment = {"content": response, "post_id": post_id};
    output.comments.push(new_comment);
    
    output.data = data;
    return output;
}

{
  "lists":{}
}