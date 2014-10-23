// casper
// Mendez 2014
var casper = require('casper').create();
var fs = require('fs')

var getDir = function() {
    path1 = '/home/ajmendez';
    path2 = '/Users/ajmendez';
    if (fs.exists(path1)) {
        return path1;
    } else {
        return path2;
    };
};

var dir = getDir()
var pw = fs.read(dir+"/.limited/comcast.pw");
var user = fs.read(dir+"/.limited/comcast.user");
var bwlog = dir+"/data/bandwidth/archive.txt";
var address = 'https://customer.comcast.com/MyServices/Internet/?ajax=1';

casper.start(address, function() {
    this.fill('form[name="signin"]', {
        'user': user,
        'passwd':pw,
    }, true);
});

casper.then(function() {
    try {
        // Sometimes catches preload -- so wait?!
        this.wait(2000, function() {
            fs.write(bwlog, Date.now()+' : '+this.getHTML('span[class="cui-meter-details-info"]')+'\n', 'a');
        });
    } catch(error) {
        console.log(error);
        console.log(this.getHTML());
    }
});

casper.run(function () {
    this.echo('Done!').exit();
});
