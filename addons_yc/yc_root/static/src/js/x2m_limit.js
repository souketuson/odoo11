// set x2m field number form 40 up to 200
odoo.define('yc_root.x2m_limit', function (require) {"use strict";
    var AbstractView = require('web.AbstractView');
    AbstractView.include({
            _setSubViewLimit: function (attrs) {
            var view = attrs.views && attrs.views[attrs.mode];
            var limit = view && view.arch.attrs.limit && parseInt(view.arch.attrs.limit);
            if (!limit && attrs.widget === 'many2many_tags') {
                limit = 1000;
            }
            attrs.limit = limit || 40;
        },
    });
});





