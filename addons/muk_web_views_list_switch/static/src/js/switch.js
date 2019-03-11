/**********************************************************************************
* 
* 	Copyright (C) 2018 MuK IT GmbH
*	
*	Odoo Proprietary License v1.0
*	This software and associated files (the "Software") may only be used 
*	(executed, modified, executed after modifications) if you have
*	purchased a valid license from the authors, typically via Odoo Apps,
*	or if you have received a written agreement from the authors of the
*	Software (see the COPYRIGHT file).
*	
*	You may develop Odoo modules that use the Software as a library 
*	(typically by depending on it, importing it and using its resources),
*	but without copying any source code or material from the Software.
*	You may distribute those modules under the license of your choice,
*	provided that this license is compatible with the terms of the Odoo
*	Proprietary License (For example: LGPL, MIT, or proprietary licenses
*	similar to this one).
*	
*	It is forbidden to publish, distribute, sublicense, or sell copies of
*	the Software or modified copies of the Software.
*	
*	The above copyright notice and this permission notice must be included
*	in all copies or substantial portions of the Software.
*	
*	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
*	OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
*	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
*	THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
*	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
*	FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
*	DEALINGS IN THE SOFTWARE.
*
**********************************************************************************/

odoo.define('muk_web_views_list_switch.listview', function(require) {
"use strict";

var ajax = require('web.ajax');
var core = require('web.core');
var utils = require('web.utils');
var config = require('web.config');
var session = require('web.session');
var framework = require('web.framework');

var ListView = require('web.ListView');
var ListController = require('web.ListController');

var QWeb = core.qweb;
var _t = core._t;

ListController.include({
    renderButtons: function () {
    	var self = this;
        var context = this.model.get(this.handle, {raw: true}).getContext();
        this._super.apply(this, arguments);
        if (context.disable_switch) {
        	this._renderSwitchButtons(false);
        } else if (context.switch_group) {
        	session.user_has_group(context.switch_group).then(function(check) {
        		self._renderSwitchButtons(check);
    	    });
        } else {
        	this._renderSwitchButtons(true);
        }
    },
    _renderSwitchButtons: function (visable) {
    	if(this.$buttons) {
        	var $switch = this.$buttons.find('.muk_list_button_switch');
        	if(visable) {
        		$switch.prop('checked', !!this.editable);
            	$switch.data('editable', this.editable || "top");
                $switch.bootstrapSwitch({
            		size: 'small',
            		labelText: _t("Mode"),
            		offText: _t("Read"),
            		onText: _t("Edit"),
            		wrapperClass: "muk_list"
            	});
        	} else {
        		$switch.hide();
        	}
        	if(!this.$switch) {
        		$switch.on('switchChange.bootstrapSwitch',
        				_.bind(this._switch_editable_mode, this));
        		this.$switch = $switch;
        	}
        }
    },
    _switch_editable_mode: function(event, state) {
    	var self = this;
    	if(state) {
    		this.editable = this.$switch.data('editable');
    		this.renderer.editable = this.$switch.data('editable');
    	} else {
    		this.editable = false;
    		this.renderer.editable = false;
    	}
    	this.reload().then(function() {
    		self._updateButtons('readonly');
    	});
    },
});

});