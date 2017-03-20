var PythonShell = require('python-shell');
// 1440 represents the hours in a day
var minutes = 1, the_interval = minutes * 60 * 1000;
setInterval(function() {
  	PythonShell.run('wordaday.py', function (err) {
	  if (err) throw err;
	  console.log('finished');
	});
}, the_interval);

//forever start runscript.js
//forever stop runscript.js
