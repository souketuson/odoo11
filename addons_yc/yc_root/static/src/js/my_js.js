// odoo.define(moduleNmae, dependencies, function)
odoo.define('yc_root.my_JS', function (require) {"use strict";
    var core = require('web.core');
    var FormRenderer = require('web.FormRenderer');
    var Widget = require('web.Widget');

    var bgdrawer = Widget.extend({
        /* <init: construct before loading full DOM>*/
        init: function() {
            var self = this;
            self._super.apply(this, arguments);
             //self.bgChanger();
             /*  this is used to register a listener on an event.
                  form: .on(ev, node.callback, node.context);
                   ev:
                      'resize': implement when browser resize
                      'DOM_updated': implement when DOM updated
                      ...etc.                                      */
             core.bus.on('click', "div[name='in_out'] div input:checked", self.bgChanger);
             core.bus.on('DOM_updated', "span[name='in_out']", self.post_bgChanger);
             core.bus.on('click', "button .o_pager_next", self.post_bgChanger);
        },
        bgChanger: function() {
            var v = $("div[name='in_out'] div input:checked").attr('data-value');
            if (v =='O') { $('.o_form_sheet').css("background-color","#adff2f");}
            else if(v =='I') { $('.o_form_sheet').css("background-color","#ffc0cb");}
        },
        post_bgChanger: function() {
            if ($("span[name='in_out']")[0]){
                var _str = $("span[name='in_out']")[0].innerHTML;
                if (_str=="出貨") { $('.o_form_sheet').css("background-color","#adff2f");}
                else if(_str=="進貨") { $('.o_form_sheet').css("background-color","#ffc0cb");}
            }
        },
    });

    // Init a new bgdrawer when the web client is ready
    /*core.bus.on('web_client_ready', null, function () {new bgdrawer();});
    return {'bgdrawer': bgdrawer,};*/

    var my_widget = new bgdrawer(this);
    my_widget.appendTo($(".o_form_sheet"));

});




