odoo.define('yc_root', function (require) {
"use strict";
var Model = require('web.Model');
var custom_model = new Model("yc.weight");
custom_model.call("my_function");
});
