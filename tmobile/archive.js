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
var tmp = fs.read(dir+'/.limited/tmobile.auth');
var user = tmp.split(' ')[0];
var pw = tmp.split(' ')[1];
var bwlog = dir+"/data/bandwidth/tmobile.txt";
var address = 'https://my.t-mobile.com/login/Default.aspx';

// 
casper.start(address, function() {
    this.fill('form[name="Form1"]', {
        'Login1:txtMSISDN': user,
        'Login1:txtPassword':pw,
    }, true);
    this.capture('login.png');
    this.click('a[id=lnkBtnLogin]');
    // this.clickLabel('Log in');
    // var nextLink = 'a[id="lnkBtnLogin""]';
    // console.log(this.getHTML());
    // if (casper.visible(nextLink)) {
    //     casper.thenClick(nextLink);
    // } else {
    //     casper.echo("END")
    // }
});



casper.then(function() {
    // console.log(this.getHTML());
    
    try {
        // Sometimes catches preload -- so wait?!
        this.capture('test.png');
        this.wait(20, function() {
            fs.write(bwlog, Date.now()+' : '+this.getHTML('div[class="topPanel"]')+'\n', 'a');
            // fs.write(bwlog, Date.now()+' : '+this.getHTML('div[class="datausage-mod-div"]')+'\n', 'a');
        });
    } catch(error) {
        console.log(error);
        console.log(this.getHTML());
    }
});

casper.run(function () {
    this.echo('Done!').exit();
});
