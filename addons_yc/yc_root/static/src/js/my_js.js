// odoo.define(moduleNmae, dependencies, function)
odoo.define('yc_root.my_JS', function (require) {"use strict";
    var core = require('web.core');

    var Widget = require('web.Widget');
    var bgdrawer = Widget.extend({
        /* <init: construct before loading DOM completely.>*/
        init: function(parent, options) {
            this._super.apply(this, arguments);
             /*  this is used to register a listener on an event.
                  form: .on(ev, node.callback, node.context);
                  ev:
                     'resize': implement when browser resize
                     'DOM_updated': implement when DOM updated
                     ...etc.
             */
            core.bus.on('click', "div[name='in_out'] div input:checked", this.bgChanger);
            core.bus.on('DOM_updated', "span[name='in_out']", this.post_bgChanger);
            core.bus.on('click', "button .o_pager_next", this.post_bgChanger);
            core.bus.on('click', this, this._onCellClick);
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
                var wizard = $('.open_the_door')
                var comfirm = $("button[name='itself_update']");
                if (btn.prop('checked')==true){
                    div.css('display','unset');
                    comfirm.css({'display':'unset','color':'white','background-color':'#7c7bad'});
                    wizard[0].innerText = "關閉舊檔搜尋";
                    wizard.css("background-color","#568e8f");
                    wizard.hover(function(e) {
                          $(this).css("background-color",e.type === "mouseenter"?"#568e8f":"#80b1b3")
                    });
                    comfirm.hover(function(e) {
                        $(this).css("background-color",e.type === "mouseenter"?"#5f5e97":"#7c7bad");
                    });
                }
                else if (btn.prop('checked')==false){
                    div.css('display','none');
                    comfirm.css('display','none');
                    wizard[0].innerText = "開啟舊檔搜尋";
                    wizard.css("background-color","#7c7bad");
                    wizard.hover(function(e) {
                          $(this).css("background-color",e.type === "mouseenter"?"#5f5e97":"#7c7bad")
                    });
                }

        },
    });

    // Init a new bgdrawer when the web client is ready
    /*core.bus.on('web_client_ready', null, function () {new bgdrawer();});
    return {'bgdrawer': bgdrawer,};*/

    var my_widget = new bgdrawer(this);
    my_widget.appendTo($(".o_form_sheet"));
});





