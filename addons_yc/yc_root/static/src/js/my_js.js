// odoo.define(moduleNmae, dependencies, function)
odoo.define('yc_root.my_JS', function (require) {"use strict";
    var core = require('web.core');

    var Widget = require('web.Widget');
    var bgdrawer = Widget.extend({
        /* <init: construct before loading DOM completely.>*/
        init: function() {
            var self = this;
            self._super.apply(this, arguments);
             /*  this is used to register a listener on an event.
                  form: .on(ev, node.callback, node.context);
                  ev:
                     'resize': implement when browser resize
                     'DOM_updated': implement when DOM updated
                     ...etc.
             */
             core.bus.on('click', "div[name='in_out'] div input:checked", self.bgChanger);
             core.bus.on('DOM_updated', "span[name='in_out']", self.post_bgChanger);
             core.bus.on('click', "button .o_pager_next", self.post_bgChanger);
             core.bus.on('click', self, self._onCellClick);
             // core.bus.on('rpc_request', null, self.enable_btn);

        },
        test: function() {
            $('.o_form_sheet').css("background-color","#adff2f");
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
        enable_btn: function() {
            var car_no=$('div[name="car_no"] input');
            var btn=$('button[name="154"]');
            if (car_no.val()=="") {
                btn.css({"cursor": "not-allowed","pointer-events": "none","opacity": 0.65});
            }
            else if(car_no.val()!="") {
                btn.css({"cursor": "","pointer-events": "unset","opacity": 1});
            }
        },
        enable_tabindex: function() {
            var radio= $('input[type="checkbox"]');
            radio.attr('tabeindex','-1');
        },
        _onCellClick: function() {
            var div = $('div #toggle_elf');
            var btn = $("div[name='wizard_btn'] input");
            if (btn.prop('checked')==true){
                div.css('display','unset')
                $('.open_the_door')[0].innerText = "關閉舊檔搜尋"
            }
            else{
                div.css('display','none')
                $('.open_the_door')[0].innerText = "開啟舊檔搜尋"
            }
        },
    });

    // Init a new bgdrawer when the web client is ready
    /*core.bus.on('web_client_ready', null, function () {new bgdrawer();});
    return {'bgdrawer': bgdrawer,};*/

    var my_widget = new bgdrawer(this);
    my_widget.appendTo($(".o_form_sheet"));
});





