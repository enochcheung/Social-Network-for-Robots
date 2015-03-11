var Sandbox = require('sandbox');
var s = new Sandbox();

var code = "function add(a,b) {return a+b;}\
			add(2,3)";

s.run(code, function(output) {console.log(output);});