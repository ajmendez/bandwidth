// casper
// Mendez 2014
var casper = require('casper').create();
// casper.on('resource.requested', function(resource) {
//
//     for (var obj in resource.headers) {
//         var name = resource.headers[obj].name;
//         var value = resource.headers[obj].value;
//         // if (name == "User-Agent"){
//         //     this.echo(value);
//         // }
//     }
//
// });
casper.userAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36');
// casper.options.verbose=true;
// casper.options.logLevel='debug';
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



casper.start(address, function() {
    this.fill('form[name="Form1"]', {
           'Login1:txtMSISDN': user,
           'Login1:txtPassword':pw,
       }, true);
       this.mouseEvent('click', '#lnkBtnLogin');
});


casper.then(function() {
    this.wait(10000, function(){
        this.capture(dir+'/data/bandwidth/tmobile_login.png');
    })
});


casper.then(function() {
    try {
        this.wait(2000, function() {
            this.capture(dir+'/data/bandwidth/tmobile_page.png');
            fs.write(bwlog, Date.now()+' : '+this.getHTML('div[class="topPanel"]')+'\n', 'a');
        });
    } catch(error) {
        console.log(error);
    }
});

casper.run(function () {
    this.echo('Done!').exit();
});
