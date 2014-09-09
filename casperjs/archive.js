

var page = require('webpage').create(),
    system = require('system'),
    t, address;

var casper = require('casper').create();
var fs = require('fs')
var pw = fs.read('/Users/ajmendez/.limited/comcast.pw');
var bwlog = '/Users/ajmendez/data/bandwidth/archive.txt';


address = 'https://customer.comcast.com/MyServices/Internet/?ajax=1';
t = Date.now();

casper.start(address, function() {
    // console.log('title: ' + this.getTitle());
    this.fill('form[name="signin"]', {
        'user': 'blue.space2014',
        'passwd':pw,
    }, true);
    // this.click('form[name="signin"]').submit();
     // this.capture('login.png');
});

casper.then(function() {
    // this.capture('then.png');
    // this.echo(this.getTitle());
    fs.write(bwlog, Date.now()+' : '+this.getHTML('span[class="cui-meter-details-info"]'), 'a');
    // this.evaluateOrDie(function() {
    //     console.log(this.getTitle());
    //     return /'t'/.test(document.body.innerText);
    // }, 'Failed to login');
});

casper.run(function () {
    this.echo('message sent').exit();
});


// page.open(address, function(status) {
//     console.log(t + ': '+ status);
//     // page.render('comcast.png');
//     var title = page.evaluate(function() {
//         return document.title;
//     })
//     console.log('title: '+title);
//     phantom.exit();
// });