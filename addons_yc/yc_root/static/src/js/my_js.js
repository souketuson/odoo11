// odoo.define(moduleNmae, dependencies, function)
odoo.define('yc_root.my_JS', function (require) {"use strict";
    var core = require('web.core');
    var FormRenderer = require('web.FormRenderer');
    var Widget = require('web.Widget');

    var bgdrawer = Widget.extend({
        // construct
        init: function() {
            var self = this;
            self._super.apply(this, arguments);
             //self.bgChanger();
             /*  this is used to register a listener on an event.
                 form: .on(ev, node.callback, node.context);
                 ev:
                    'resize': implement when browser resize
                    'DOM_updated': implement when DOM updated
                    ...etc.
             */
             core.bus.on('click', "div[name='in_out'] div input:checked", self.bgChanger);
        },
        bgChanger: function() {
            var v = $("div[name='in_out'] div input:checked").attr('data-value');
            if (v =='O') { $('.o_form_sheet').css("background-color","aquamarine");}
            else if(v =='I') { $('.o_form_sheet').css("background-color","hotpink");}
        },
        post_bgChanger: function() {
            var _str = $("span[name='in_out']")[0].innerText;
            if (_str=="出貨") { $('.o_form_sheet').css("background-color","aquamarine");}
            else if(_str=="進貨") { $('.o_form_sheet').css("background-color","hotpink");}
        },
        FormRenderer.include({
            /*
            private method:
                _renderTagSheet : $sheet = $('<div>').addClass('o_form_sheet');
                _renderView:


            */
        },
    });
    });
    // Init a new bgdrawer when the web client is ready
    core.bus.on('web_client_ready', null, function () {
        new bgdrawer();
    });
    return {
        'bgdrawer': bgdrawer,
    };
});




