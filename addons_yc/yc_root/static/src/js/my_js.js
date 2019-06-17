// odoo.define(moduleNmae, dependencies, function)
odoo.define('yc_root.my_JS', function (require) {"use strict";
    var core = require('web.core');
    var Widget = require('web.Widget');
    var bgdrawer = Widget.extend({
        // construct
        init: function() {
            var self = this;
            self._super.apply(this, arguments);
            self.bgChanger();
             /*  this is used to register a listener on an event.
                 'resize': implement when browser resize
                 'DOM_updated': implement when DOM updated
                 ...etc.
             */
             core.bus.on('resize', self, self.bgChanger);
        },
        bgChanger: function() {
            var v = $("div[name='in_out'] div input:checked").attr('data-value');
            if (v =='O') { $('.o_form_sheet').css("background-color","aquamarine");}
            else if(v =='I') { $('.o_form_sheet').css("background-color","hotpink");}
        },
    });
    // Init a new bgdrawer when the web client is ready
    core.bus.on('web_client_ready', null, function () {
        new bgdrawer();
    });
    return {
        'bgdrawer': bgdrawer,
    };
});

    /*
    init: function(){
        var v = $("div[name='in_out'] div input:checked").attr('data-value');
        if (v =='O') {
            $('.o_form_sheet').css("background-color","blue");
            }
        else {
            $('.o_form_sheet').css("background-color","yellow");
            }
        }
    })

    window.onload = function(){
        var v = $("div[name='in_out'] div input:checked").attr('data-value');
        if (v =='O') {
            $('.o_form_sheet').css("background-color","blue");
            }
        else {
            $('.o_form_sheet').css("background-color","yellow");
            }
    }

    $(window).load(function(){
        var v = $("div[name='in_out'] div input:checked").attr('data-value');
        if (v =='O') {
            $('.o_form_sheet').css("background-color","blue");
            }
        else {
            $('.o_form_sheet').css("background-color","yellow");
            }
        console.log('hi');
        console.log(v);
    });
    */




