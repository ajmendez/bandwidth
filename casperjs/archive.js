// casper
// Mendez 2014
var casper = require('casper').create();
var fs = require('fs')
var pw = fs.read("/home/ajmendez/.limited/comcast.pw");
var user = fs.read("/home/ajmendez/.limited/comcast.user");
var bwlog = "/home/ajmendez/data/bandwidth/archive.txt";
var address = 'https://customer.comcast.com/MyServices/Internet/?ajax=1';

casper.start(address, function() {
    this.fill('form[name="signin"]', {
        'user': user,
        'passwd':pw,
    }, true);
});

casper.then(function() {
    fs.write(bwlog, Date.now()+' : '+this.getHTML('span[class="cui-meter-details-info"]')+'\n', 'a');
});

casper.run(function () {
    this.echo('message sent').exit();
});
