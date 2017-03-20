var walk    = require('walk');
var files   = [];
const readline = require('readline');

path_file = os.path.abspath("")
// Walker options
var walker  = walk.walk(path_file+'/Dates', { followLinks: false });

walker.on('file', function(root, stat, next) {
    // Add this file to the list of files
    files.push(stat.name);
    next();
});

walker.on('end', function() {
  files.forEach(function(value){
  value = value.replace('.json','')
  console.log(value);

});
  console.log('TodaysWord');
  console.log('YesterdaysWord');
});


const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});
console.log(' ')
rl.question('file to Open', (answer) => {
  // TODO: Log the answer in a database
  var fs = require('fs');
  var obj;
  var util = require("util")
  fileName= ''

if (answer =='TodaysWord')
  {
    fileName = path_file+answer+'.json'
  }
  else if (answer == 'YesterdaysWord'){
    fileName = path_file+answer+'.json'
  }
  else{
    fileName = path_file+answer+'.json'
  }
  console.log(fileName)
  console.log(' ')

  fs.readFile(fileName, 'utf8', function (err, data) {
    if (err) throw err;
      obj = JSON.parse(data);
     var keys = Object.keys( obj );
  for( var i = 0,length = keys.length; i < length; i++ ) {
      
      console.log(keys[i] + ':' + obj[ keys[ i ] ]);
      console.log(' ')
  }
  });
rl.close();
});
