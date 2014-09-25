// casper
// Mendez 2014
var casper = require('casper').create();
// casper.options.pageSettings={javascriptEnabled:false};
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
// var address = 'https://my.t-mobile.com/Default.aspx?rp.Logon=true'

// 
casper.start(address, function() {
    // try {
    //     this.mouseEvent('click','.fsrCloseBtn');
    // } catch(error) {
    //     this.echo('asd');
    // };
    // this.sendKeys('input[name="Login1:txtPassword"]', pw);
    // this.sendKeys('input[name="Login1:txtPassword"]', casper.page.event.key.CapsLock);
    
    this.fill('form[name="Form1"]', {
           'Login1:txtMSISDN': user,
           'Login1:txtPassword':pw,
       }, false);
       this.mouseEvent('click', '#lnkBtnLogin');
    // this.sendKeys('input[name="Login1:txtPassword"]', casper.page.event.key.Tab);
    // this.capture('before.png');
    // console.log(this.getHTML());
    //
    //
    // // this.mouseEvent('mouseover', 'input[name="Login1:txtMSISDN"]');
    // this.wait(1, function() {
    //     // this.mouseEvent('click', 'input[name="Login1:txtMSISDN"]');
    //     this.sendKeys('input[name="Login1:txtMSISDN"]', user);
    //     this.sendKeys('input[name="Login1:txtMSISDN"]', casper.page.event.key.Tab);
    //     // this.sendKeys('input[name="Login1:txtMSISDN"]', casper.page.event.key.Enter , {keepFocus: true});
    //
    // });
    // // this.mouseEvent('mouseout', 'input[name="Login1:txtMSISDN"]');
    //
    // // this.mouseEvent('mouseover', 'input[name="Login1:txtPassword"]');
    // this.wait(1, function() {
    //     this.mouseEvent('click', 'input[name="Login1:txtPassword"]');
    //     this.sendKeys('input[name="Login1:txtPassword"]', pw);
    //     this.sendKeys('input[name="Login1:txtPassword"]', casper.page.event.key.CapsLock);
    //     this.sendKeys('input[name="Login1:txtPassword"]', casper.page.event.key.Tab);
    //
    //     // this.sendKeys('input[name="Login1:txtPassword"]', pw, {keepFocus: true});
    //     this.sendKeys('input[name="Login1:txtPassword"]', casper.page.event.key.Enter);
    // });
    // // this.mouseEvent('click','div[id="CapsKeyMsg"]')
    //
    // this.wait(1, function() {
    //     this.fill('form[name="Form1"]', {
    //         'Login1:txtMSISDN': user,
    //         'Login1:txtPassword':pw,
    //     }, false);
    //     this.mouseEvent('click','#Login1_chkRemember');
    //
    //     // this.mouseEvent('mouseover', 'a[id="lnkBtnLogin"]');
    //     // this.mouseEvent('click', '#lnkBtnLogin');
    //     // this.mouseEvent('mouseout', 'input[name="Login1:txtPassword"]');
    //     // this.echo(this.getFormValues('form'));
    // });
    //
    //
    // // this.click('#lnkBtnLogin');
    // // this.mouseEvent('click', 'a[id="lnkBtnLogin"]');
    //
    // // this.echo(this.status(true));
    //
    //
    //
    // // this.capture('login.png');
    // // this.click('a[id=lnkBtnLogin]');
    // // this.clickLabel('Log in');
    // // var nextLink = '#lnkBtnLogin';
    // // // console.log(this.getHTML());
    // // if (casper.visible(nextLink)) {
    // //     casper.thenClick(nextLink);
    // // } else {
    // //     casper.echo("END");
    // // }
});


casper.then(function() {
    this.wait(5000, function(){
        this.capture('login.png');
    })
    
    // this.evaluateOrDie(function() {
    //     // this.capture('login.png');
    //     return this.click('#lnkBtnLogin');
    //     // return /message sent/.test(document.body.innerText);
    // }, 'Clicking failed');
});


// casper.thenClick('#lnkBtnLogin', function() {
//     console.log("Woop!");
//     // this.capture('login.png');
// });

// casper.then(function() {
//     console.log(this.getTitle());
// });



casper.then(function() {
    // console.log(this.getHTML());

    try {
        // Sometimes catches preload -- so wait?!
        // this.capture('test.png');
        this.wait(2000, function() {
            fs.write(bwlog, Date.now()+' : '+this.getHTML('div[class="topPanel"]')+'\n', 'a');
            // fs.write(bwlog, Date.now()+' : '+this.getHTML('div[class="datausage-mod-div"]')+'\n', 'a');
        });
    } catch(error) {
        console.log(error);
        // console.log(this.getHTML());
    }
});

casper.run(function () {
    // this.capture('login.png');
    // this.echo(Date.now()+' : '+this.getHTML('div[class="topPanel"]')+'\n');
    // this.echo('xxx: '+Date.now()+' : '+this.getHTML('span[class="home-txt20"]')+'\n');
    // this.echo(this.getHTML('div[class="datausage-mod-desc"]')+'\n');
    this.echo('Done!').exit();
});
