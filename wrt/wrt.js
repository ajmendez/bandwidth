// casper : wrt
// Mendez 2014
var address = 'http://10.97.42.1/Status_Internet.asp';
var x = require('casper').selectXPath;
var casper = require('casper').create({
    verbose: false,
    logLevel: 'debug'
});
casper.options.viewportSize = {width: 1366, height: 667};

casper.start();
casper.setHttpAuth('username', 'password');

casper.thenOpen(address, function() {
    // this.test.assertUrlMatch(/^https:\/\/mysite.com\/a\/dashboard$/);
});

casper.run(function() {
    // this.test.renderResults(true);
    casper.capture('test.png');
    this.exit();
});


// var page = require('webpage').create();
// var address = 'http://10.97.42.1/Status_Internet.asp';
// page.open(address, function() {
//   page.render('wrt.png');
//   phantom.exit();
// });

// var casper = require('casper').create();
// var address = 'http://10.97.42.1/Status_Internet.asp';
//
// casper.start(address, function() {
//     // casper.render('test.png');
//     this.echo('start');
// });
//
// casper.then(function() {
//     this.echo('then');
// });
//
// casper.run(function () {
//     this.echo('Done!').exit();
// });