// odoo.define(moduleNmae, dependencies, function)
odoo.define('yc_root.purchase_rpc', function (require) {"use strict";
    var ajax = require('web.ajax');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var weContext = require('web_editor.context');
    var Widget = require('web.Widget');

    var note_suggestion = Widget.extend({
        init: function(parent, options, event) {
            this._super.apply(this, arguments);
            //core.bus.on('DOM_updated', null, this.note);

        },


    });
    /*$(document).ready(function() {
        var res = rpc.query({
            model: 'yc.setpurchasenote',
            method: 'name_get',
            args: [],
        });
        return res
        tags = ['11111111', '22222222', '33333333'];
        $("input[name='notices1']").autocomplete({
            source: tags
        });
        alert('success');
    });*/
    /*function autocompleteWithPages(self, $input) {
        $input.autocomplete({
            source: function (request, response) {
                return self._rpc({
                    model: 'website',
                    method: 'search_pages',
                    args: [null, request.term],
                    kwargs: {
                        limit: 15,
                        context: weContext.get(),
                    },
                }).then(function (exists) {
                    var rs = _.map(exists, function (r) {
                        return r.loc;
                    });
                    response(rs);
                });
            },
        });
    }*/
});





