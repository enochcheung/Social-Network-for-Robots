var posts = [];
var posts_start=0;
var comments_start = new Map();

$(document).ready(function() {
    loadPosts();
    loadAllComments();
    $("#post-form").submit(submitPostForm);
});

window.setInterval(function() {
    loadPosts();
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
            loadPosts();
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

function loadPosts() {
    $.ajax({
        url: "/get_posts/"+posts_start+"/",
        dataType : "json",
        success: function( items ) {
            

            $(items).each(function() {
                if (this.pk >= posts_start) {       
                    posts_start = Math.max(posts_start, this.pk+1);
                    comments_start.set(this.pk,0);
                    posts.push(this.pk);

                    $("#posts-list").prepend(
                        "<li class='media'>\
                            <div class='media-left'>\
                                <div class='profile-pic'>\
                                <a href='/profile/"+this.fields.user+"'>\
                                <img class='profile-pic-"+this.fields.user+" media-object' width='75px'>\
                                </a>\
                                </div>\
                            </div>\
                        <div class='media-body'>\
                            <div class='pad-left'>\
                                "+this.fields.content+"\
                                <div class='text-right'>\
                                &mdash; <a href='/profile/"+this.fields.user+"'>"+this.fields.user+"</a> <small>("+formatDate(this.fields.date)+")</small>\
                                </div>\
                            <br>\
                            <ul class='media-list' id='post-"+this.pk+"'>\
                            </ul>\
                            <br>\
                            <form id='comment-form-"+this.pk+"' action='/comment/' method='POST'>\
                                <div class='form-group'>\
                                    <textarea type='text'\
                                        row=2\
                                        class='form-control'\
                                        placeholder='Comment'\
                                        name='content'\
                                        maxlength='160' required></textarea>\
                                    <input type='hidden'\
                                        class='form-control'\
                                        placeholder='Comment'\
                                        name='post'\
                                        value='"+this.pk+"'\
                                        required>\
                                </div>\
                                <div class='text-right'><button class='btn btn-sm btn-default' type='submit'>Comment</button></div>\
                                "+csrfstring+"\
                            </form>\
                            </div>\
                        </div>\
                        </li>"
                    );
                    



                    loadProfilePic(this.fields.user);
                    setTimeout(loadComments, 1000, this.pk);
                    $("#comment-form-"+this.pk).submit(submitCommentForm);
                }

            });

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
                        "<li class='media'>\
                            <div class='media-left'>\
                                <div class='profile-pic'>\
                                <a href='/profile/"+this.fields.user+"'>\
                                <img class='profile-pic-"+this.fields.user+" media-object' width='75px'>\
                                </a>\
                                </div>\
                            </div>\
                        <div class='media-body'>\
                            <div class='pad-left'>\
                        "+this.fields.content+"\
                        <div class='text-right'>\
                        &mdash; <a href='/profile/"+this.fields.user+"'>"+this.fields.user+"</a> <small>("+formatDate(this.fields.date)+")</small>\
                        </div>\
                        </div>\
                        </div>\
                        </li>"

                    );


                    loadProfilePic(this.fields.user);
                }

            });

        }
    });
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
    return moment(date).format("MMM D, YYYY; h:mm a");
}


function imgError(image){
    $(image).hide();
}