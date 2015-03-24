'use strict';
var vm = require('vm');

function safe_run(code, func_name, input) {
	var vm_output = [];
	var sandbox = {	vm_input : input,
					vm_output: vm_output,
					require : function() {throw Error('require not allowed');}}
	vm.createContext(sandbox);
	vm.runInContext('"use strict";\n'+code,sandbox,{'timeout':200});
	vm.runInContext('vm_output.push('+func_name+'(vm_input))',sandbox,{'timeout':200});


	return vm_output[0];
}
