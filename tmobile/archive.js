// casper
// Mendez 2014
var casper = require('casper').create();
casper.options.viewportSize = {width: 600, height: 600};
casper.pageSettings = {javascriptEnabled: true, loadImages:  true, loadPlugins: true};
phantom.cookiesEnabled = true;


casper.echo("Casper CLI passed args:");
require("utils").dump(casper.cli.args);

casper.echo("Casper CLI passed options:");
require("utils").dump(casper.cli.options);

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
// casper.userAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36');

casper.userAgent('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)');

// casper.on('resource.requested', function(resource) {
//     casper.echo(resource.url);
// });
casper.on('resource.received', function(resource) {
    casper.echo(' Loaded: '+ resource.url);
});

// casper.on('page.resource.requested', function(requestData, request) {
//     if (requestData.url.indexOf('https://www.t-mobile.com/foresee/') === 0) {
//         request.abort();
//     }
//     if (requestData.url.indexOf('https://nexus.ensighten.com/') === 0) {
//         request.abort();
//     }
//     if (requestData.url.indexOf('https://www.googleadservices.com/') === 0) {
//         request.abort();
//     }
//     if (requestData.url.indexOf('https://googleads.g.doubleclick.net') === 0) {
//         request.abort();
//     }
//     if (requestData.url.indexOf('https://fls.doubleclick.net') === 0) {
//         request.abort();
//     }
//     if (requestData.url.indexOf('https://*.fls.doubleclick.net') === 0) {
//         request.abort();
//     }
//     if (requestData.url.indexOf('https://fls.doubleclick.net') === 0) {
//         request.abort();
//     }
//     if (requestData.url.indexOf('https://fls.doubleclick.net') === 0) {
//         request.abort();
//     }
//     if (requestData.url.indexOf('https://fls.doubleclick.net') === 0) {
//         request.abort();
//     }
// });



casper.options.verbose=true;
casper.options.logLevel='debug';

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
var address = 'https://my.t-mobile.com/Default.aspx';
var address = 'https://my.t-mobile.com/Plan/Prepaid/Default.aspx'
var linkSelector = 'a#lnkBtnLogin';


casper.start(address, function() {
    this.wait(2000, function(){
        this.echo('Waited');
    });
});

casper.then( function() {
    this.sendKeys('input#Login1_txtMSISDN', user, {keepFocus: true});
    this.sendKeys('input#Login1_txtPassword', pw, {keepFocus: true});
    this.sendKeys('input#Login1_txtPassword', casper.page.event.key.Enter, {keepFocus: true});
    
    
    // this.fill('form[name="Form1"]', {
    this.fill('form#Form1', {
           'Login1:txtMSISDN': user,
           'Login1:txtPassword':pw,
            }, true);

    this.evaluate(function() {
        document.querySelector('form#Form1').submit();
    });
    
    // //
    // // this.evaluate(function() {
    // //     document.querySelector('a#lnkBtnLogin').classContent = 'primaryStandardBtn';
    // // });
    // this.evaluate(function(linkSelector) {
    //         __utils__.findOne(linkSelector).setAttribute("class", "primaryStandardBtn");
    //     }, linkSelector);
    // // this.echo('Title is now: ' + this.evaluate(function() {
    // //     return document.querySelector('div.div-login-button');
    // // }));
    // this.echo(this.getHTML('div.div-login-button'));
    // // this.echo('Title is now: ' + this.evaluate(function() {
    // //     return document.querySelector('h1').textContent;
    // // }));
    //
    this.wait(10000, function(){
        this.mouseEvent('click', '#lnkBtnLogin');
    });
    this.capture(dir+'/data/bandwidth/tmobile_login.png');
    
});



// casper.then(function() {
//     this.wait(10000, function(){
//         this.capture(dir+'/data/bandwidth/tmobile_login.png');
//     })
// });

//
// casper.then(function() {
//     try {
//         this.wait(2000, function() {
//             this.capture(dir+'/data/bandwidth/tmobile_page.png');
//             fs.write(bwlog, Date.now()+' : '+this.getHTML('div[class="topPanel"]')+'\n', 'a');
//         });
//     } catch(error) {
//         console.log(error);
//     }
// });

casper.run(function () {
    this.echo('Done!').exit();
});
