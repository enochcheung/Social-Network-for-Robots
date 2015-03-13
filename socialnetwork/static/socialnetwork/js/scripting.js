// Formatting the editor
$(document).ready(function() {
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/chrome");
    editor.getSession().setMode("ace/mode/javascript");

    $('#script_code').val(editor.getValue());

    $("#script-form").submit(submitScriptForm)

});

function submitScriptForm(e) {
    var editor = ace.edit("editor");
    $('#script_code').val(editor.getValue());

    var data = $(this).serializeArray();
    var formURL = $(this).attr("action");
    $.ajax({
        url: formURL,
        type: "POST",
        data: data,
        success: function() {

        }
    });
    e.preventDefault();
}
