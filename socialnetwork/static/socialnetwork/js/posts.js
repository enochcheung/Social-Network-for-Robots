var posts = [];
var posts_start=0;
var posts_end= Number.MAX_VALUE;
var posts_end_reached = false;
var comments_start = new Map();
// variables from html document: csrfstring, posts_url

$(document).ready(function() {
    loadPosts(false);
    loadAllComments();
    $("#post-form").submit(submitPostForm);
});

$(window).scroll(function()
{
    if($(window).scrollTop() == $(document).height() - $(window).height())
    {
        if (!posts_end_reached) {
            $('div#loadericon').show();
        
            loadPostsPrev();

        }
    }
});

window.setInterval(function() {
    loadPosts(false);
    loadAllComments();
}, 60000);

function submitPostForm(e) {
    var postData = $(this).serializeArray();
    var formURL = $(this).attr("action");
    $.ajax({
        url: formURL,
        type: "POST",
        data: postData,
        success: function() {
            loadPosts(true);
        }
    });
    e.preventDefault();
    $(this)[0].reset();
}

function submitCommentForm(e) {
    var commentData = $(this).serializeArray();
    var formURL = $(this).attr("action");
    $.ajax({
        url: formURL,
        type: "POST",
        data: commentData,
        success: function() {
            post_id = postIdFromCommentForm(commentData);
            loadComments(post_id);
        }
    });
    e.preventDefault();
    $(this)[0].reset();
}

function postIdFromCommentForm(commentData) {
    for (i=0; i<commentData.length; i++) {
        if (commentData[i].name === 'post') {
            return parseInt(commentData[i].value);
        }
    }
}

function loadAllComments() {
    posts.forEach(loadComments);
}

function loadPosts(delayComments) {
    $.ajax({
        url: posts_url.replace("0000",posts_start),
        dataType : "json",
        success: function( items ) {
            

            $(items).each(function() {
                if (this.pk >= posts_start) {       
                    posts_start = Math.max(posts_start, this.pk+1);
                    posts_end = Math.min(posts_end, this.pk);

                    comments_start.set(this.pk,0);
                    posts.push(this.pk);

                    $("#posts-list").prepend(
                        postHtml(this.pk,this.fields.user,this.fields.content, this.fields.date)
                    );
                    



                    loadProfilePic(this.fields.user);
                    if (delayComments) {
                        setTimeout(loadComments, 1000, this.pk);
                    }
                    else {
                        loadComments(this.pk);
                    }
                    $("#comment-form-"+this.pk).submit(submitCommentForm);
                }

            });

        }
    });
}

function morePosts() {
    loadPostsPrev();
}

function loadPostsPrev() {
    $.ajax({
        url: posts_prev_url.replace("0000",posts_end-1),
        dataType : "json",
        success: function( items ) {
            
            if (items.length == 0) {
                posts_end_reached = true;
            }

            $(items).each(function() {
                if (this.pk < posts_end) {       
                    posts_end = Math.min(posts_end, this.pk);
                    comments_start.set(this.pk,0);
                    posts.push(this.pk);

                    $("#posts-list").append(
                        postHtml(this.pk,this.fields.user,this.fields.content, this.fields.date)
                    );
                    



                    loadProfilePic(this.fields.user);
                    loadComments(this.pk);
                    $("#comment-form-"+this.pk).submit(submitCommentForm);
                }

            });

            $('div#loadericon').hide();

        }
    });
}


function loadComments(post_id) {
    var comment_start_id = comments_start.get(post_id);

    $.ajax({
        url: "/get_comments/"+post_id+"/"+comment_start_id+"/",
        dataType : "json",
        success: function( items ) {
            

            $(items).each(function() {
                if (this.pk >= comments_start.get(post_id)) {
                    comments_start.set(post_id, Math.max(this.pk+1, comments_start.get(post_id)));

                    $("#post-"+post_id).append(
                        commentHtml(this.fields.pk,this.fields.user,this.fields.content,this.fields.date));


                    loadProfilePic(this.fields.user);
                }

            });

        }
    });
}

function postHtml(key, username, content, date) {
    return "<li class='media'>\
                            <div class='media-left'>\
                                <a href='/profile/"+username+"'>\
                                <img class='profile-pic-"+username+" media-object'>\
                                </a>\
                            </div>\
                        <div class='media-body'>\
                                <strong><a href='/profile/"+username+"'>"+username+"</a></strong>\
                                <p>"+content+"</p> <span class='date sub-text'>"+formatDate(date)+"</span>\
                            <br>\
                            <ul class='comments-list media-list' id='post-"+key+"'>\
                            </ul>\
                            <br>\
                            <form id='comment-form-"+key+"' action='/comment/' method='POST'>\
                                <div class='input-group'>\
                                    <input type='text'\
                                        row=2\
                                        class='form-control'\
                                        placeholder='Comment'\
                                        name='content'\
                                        maxlength='160' required></textarea>\
                                <div class='input-group-btn'><button class='btn btn-md btn-default' type='submit'>Comment</button></div>\
                                </div>\
                                <input type='hidden'\
                                        class='form-control'\
                                        placeholder='Comment'\
                                        name='post'\
                                        value='"+key+"'\
                                        required>\
                                "+csrfstring+"\
                            </form>\
                        </div>\
                        </li>";

}

function commentHtml(key, username, content, date) {
    return "<li>\
                            <div>\
                                <a href='/profile/"+username+"'>\
                                <img class='profile-pic-"+username+"'>\
                                </a>\
                            </div>\
                        <div>\
                                <strong><a href='/profile/"+username+"'>"+username+"</a></strong>\
                                <p>"+content+" </p>\
                                 <span class='date sub-text'>"+ formatDate(date)+"</span>\
                        </div>\
                        </li>";

}

function loadProfilePic(username) {
    $.ajax({
        url: "/profile_pic_url/"+username+"/",
        dataType : "text",
        success: function( txt ) {
            $(".profile-pic-"+username).attr('src', txt);
            
            }

        
    });

}

function formatDate(date) {
    dateObj = moment(date);
    if (dateObj.diff(moment()) < 43200000) {
        return dateObj.fromNow();
    }

    return dateObj.calendar();
    //return moment(date).format("MMM D, YYYY; h:mm a");
}


function imgError(image){
    $(image).hide();
}