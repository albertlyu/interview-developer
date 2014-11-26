var connect = require('connect');
var serveStatic = require('serve-static');

connect().use(serveStatic(__dirname)).listen(8000);

console.log('Server running at http://localhost:8000/');