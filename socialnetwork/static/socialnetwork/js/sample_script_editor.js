// Formatting the editor
$(document).ready(function() {
    var code_editor = ace.edit("code-editor");
    code_editor.setReadOnly(true);
    
    code_editor.setTheme("ace/theme/chrome");
    code_editor.getSession().setMode("ace/mode/javascript");

    $('#code-field').val(code_editor.getValue());


    var json_editor = ace.edit("json-editor");
    json_editor.setReadOnly(true);

    json_editor.setTheme("ace/theme/chrome");
    json_editor.getSession().setMode("ace/mode/json");
    $('#json-field').val(json_editor.getValue());


});
