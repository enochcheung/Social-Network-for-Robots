// Formatting the editor
$(document).ready(function() {
    var code_editor = ace.edit("code-editor");
    
    code_editor.setTheme("ace/theme/chrome");
    code_editor.getSession().setMode("ace/mode/javascript");

    $('#code-field').val(code_editor.getValue());


    var json_editor = ace.edit("json-editor");

    json_editor.setTheme("ace/theme/chrome");
    json_editor.getSession().setMode("ace/mode/json");
    $('#json-field').val(json_editor.getValue());


    $("#script-form").submit(submitScriptForm)

});

function submitScriptForm(e) {
    var code_editor = ace.edit("code-editor");
    var json_editor = ace.edit("json-editor")

    $('#code-field').val(code_editor.getValue());
    $('#json-field').val(json_editor.getValue());

    var data = $(this).serializeArray();
    var formURL = $(this).attr("action");
    $.ajax({
        url: formURL,
        type: "POST",
        data: data,
        success: function() {
            // 
        }
    });
    // e.preventDefault();
}
