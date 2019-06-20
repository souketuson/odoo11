// odoo.define(moduleNmae, dependencies, function)
odoo.define('yc_root.my_JS', function (require) {"use strict";
    var core = require('web.core');
    var FormRenderer = require('web.FormRenderer');
    var Widget = require('web.Widget');

    var bgdrawer = Widget.extend({
        /* <init: construct before loading full DOM>
           I'm not sure how click radio implement works.
           If you set breakpoint on core.bus.on click event, you'll find DOM don't set completely.
           So there're must some mysterious ways to get DOM node attributions.
           However, it's wired that I can get variable v in bgChanger, but can't get _str in
           post_bgChanger from the beginning.
        */
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
             //core.bus.on('load', "span[name='in_out']", self.post_bgChanger);
        },
        start: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                core.bus.on('click', "span[name='in_out']", self.post_bgChanger);
            });

        },
        bgChanger: function() {
            var v = $("div[name='in_out'] div input:checked").attr('data-value');
            if (v =='O') { $('.o_form_sheet').css("background-color","#adff2f");}
            else if(v =='I') { $('.o_form_sheet').css("background-color","#ffc0cb");}
        },
        post_bgChanger: function() {
            var _str = $("span[name='in_out']")[0].innerHTML;
            if (_str=="出貨") { $('.o_form_sheet').css("background-color","aquamarine");}
            else if(_str=="進貨") { $('.o_form_sheet').css("background-color","hotpink");}
        },

    });
    // Init a new bgdrawer when the web client is ready
    core.bus.on('web_client_ready', null, function () {
        new bgdrawer();
    });

    FormRenderer.extend({
        /*
        overwrite FormRenderer's method may feasible for post-rendering
        private method:
            _renderTagSheet: $sheet = $('<div>').addClass('o_form_sheet');
            _renderView:
            _updateView:
        */
    });
    return {
        'bgdrawer': bgdrawer,
    };
});




