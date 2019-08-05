// odoo.define(moduleNmae, dependencies, function)
odoo.define('yc_root.my_JS', function (require) {"use strict";
    var ajax = require('web.ajax');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var Widget = require('web.Widget');
    var bgdrawer = Widget.extend({
        /* <init: construct before loading DOM completely.>*/
        init: function(parent, options, event) {
            this._super.apply(this, arguments);
             /*  this is used to register a listener on an event.
                  form: .on(ev, node.callback, node.context);
                  ev:
                     'resize': implement when browser resize
                     'DOM_updated': implement when DOM updated
                     ...etc.
             */
            core.bus.on('click', this, this.return_Click); //版面1退回
            core.bus.on('DOM_updated', this, this.note_auto_complete); // 備註autocomplete

        },
        return_Click: function() {
            if ($('div .purchase1_for_js').length ==1){
                var div = $('div #toggle_return');
                var btn = $("div[name='return_btn'] input");
                var wizard = $('.mummy_return');
                if (btn.prop('checked')==true){
                    div.css('display','unset');
                    // comfirm.css({'display':'unset','color':'white','background-color':'#7c7bad'});
                    wizard[0].innerText = "關閉退回";
                    wizard.css("background-color","#568e8f");
                    wizard.hover(function(e) {
                          $(this).css("background-color",e.type === "mouseenter"?"#568e8f":"#80b1b3")
                    });
                }
                else if (btn.prop('checked')==false){
                    div.css('display','none');
                    //comfirm.css('display','none');
                    wizard[0].innerText = "搜尋退回";
                    wizard.css("background-color","#5f5e97");
                    wizard.hover(function(e) {
                          $(this).css("background-color",e.type === "mouseenter"?"#5f5e97":"#7c7bad")
                    });
                }
            }
        },
        // this work while dom loaded
        note_auto_complete: function(){
            var note1 = $("input[name='notices1']");
            var note2 = $("input[name='notices2']");
            var note3 = $("input[name='notices3']");
            var qc1 = $("input[name='qcnote1']");
            var qc2 = $("input[name='qcnote2']");
            var qc3 = $("input[name='qcnote3']");
            var pn1 = $("input[name='prodnote1']");
            var pn2 = $("input[name='prodnote2']");
            var pn3 = $("input[name='prodnote3']");

            note1.autocomplete({
                position: { my: "left bottom", at: "left top", collision: "flip" },
                minLength: 1,
                source: function (request, response) {
                    ajax.jsonRpc("/serial_search", "call", {"serial": note1.val()})
                        .then(function (data) {
                            response(data);
                        });
                },
                response: function (event, ui) {
                    if (ui.content.length === 1) {
                        ui.item = ui.content[0];
                    }
                },
            });
            note2.autocomplete({
                position: { my: "left bottom", at: "left top", collision: "flip" },
                minLength: 1,
                source: function (request, response) {
                    ajax.jsonRpc("/serial_search", "call", {"serial": note2.val()})
                        .then(function (data) {
                            response(data);
                        });
                },
                response: function (event, ui) {
                    if (ui.content.length === 1) {
                        ui.item = ui.content[0];
                    }
                },
            });
            note3.autocomplete({
                position: { my: "left bottom", at: "left top", collision: "flip" },
                minLength: 1,
                source: function (request, response) {
                    ajax.jsonRpc("/serial_search", "call", {"serial": note3.val()})
                        .then(function (data) {
                            response(data);
                        });
                },
                response: function (event, ui) {
                    if (ui.content.length === 1) {
                        ui.item = ui.content[0];
                    }
                },
            });
            qc1.autocomplete({
                position: { my: "left bottom", at: "left top", collision: "flip" },
                minLength: 1,
                source: function (request, response) {
                    ajax.jsonRpc("/serial_search", "call", {"serial": qc1.val()})
                        .then(function (data) {
                            response(data);
                        });
                },
                response: function (event, ui) {
                    if (ui.content.length === 1) {
                        ui.item = ui.content[0];
                    }
                },
            });
            qc2.autocomplete({
                position: { my: "left bottom", at: "left top", collision: "flip" },
                minLength: 1,
                source: function (request, response) {
                    ajax.jsonRpc("/serial_search", "call", {"serial": qc2.val()})
                        .then(function (data) {
                            response(data);
                        });
                },
                response: function (event, ui) {
                    if (ui.content.length === 1) {
                        ui.item = ui.content[0];
                    }
                },
            });
            qc3.autocomplete({
                position: { my: "left bottom", at: "left top", collision: "flip" },
                minLength: 1,
                source: function (request, response) {
                    ajax.jsonRpc("/serial_search", "call", {"serial": qc3.val()})
                        .then(function (data) {
                            response(data);
                        });
                },
                response: function (event, ui) {
                    if (ui.content.length === 1) {
                        ui.item = ui.content[0];
                    }
                },
            });
            pn1.autocomplete({
                position: { my: "left bottom", at: "left top", collision: "flip" },
                minLength: 1,
                source: function (request, response) {
                    ajax.jsonRpc("/serial_search", "call", {"serial": pn1.val()})
                        .then(function (data) {
                            response(data);
                        });
                },
                response: function (event, ui) {
                    if (ui.content.length === 1) {
                        ui.item = ui.content[0];
                    }
                },
            });
            pn2.autocomplete({
                position: { my: "left bottom", at: "left top", collision: "flip" },
                minLength: 1,
                source: function (request, response) {
                    ajax.jsonRpc("/serial_search", "call", {"serial": pn2.val()})
                        .then(function (data) {
                            response(data);
                        });
                },
                response: function (event, ui) {
                    if (ui.content.length === 1) {
                        ui.item = ui.content[0];
                    }
                },
            });
            pn3.autocomplete({
                position: { my: "left bottom", at: "left top", collision: "flip" },
                minLength: 1,
                source: function (request, response) {
                    ajax.jsonRpc("/serial_search", "call", {"serial": pn3.val()})
                        .then(function (data) {
                            response(data);
                        });
                },
                response: function (event, ui) {
                    if (ui.content.length === 1) {
                        ui.item = ui.content[0];
                    }
                },
            });
        },

    });

    // Init a new bgdrawer when the web client is ready
    /*core.bus.on('web_client_ready', null, function () {new bgdrawer();});
    return {'bgdrawer': bgdrawer,};*/

    var my_widget = new bgdrawer(this);
    my_widget.appendTo($(".o_form_sheet"));
});





