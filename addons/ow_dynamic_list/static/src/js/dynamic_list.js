odoo.define('ow_dynamic_list.DynamicList', function(require) {

    "use strict";
    var core = require('web.core');
    var ListView = require('web.ListView');
    var ListController = require('web.ListController');
    var rpc = require('web.rpc');
    var session = require('web.session');
    var QWeb = core.qweb;

    var _t = core._t;

    ListView.include({
		init: function (viewInfo, params) {
            this._super.apply(this, arguments);
			var arch = viewInfo.arch;
			arch['view_id'] = viewInfo.view_id;
        },
	})

    ListController.include({
        init: function (parent, model, renderer, params) {
        	var self = this;
			var uid = session.uid;
			this._super.apply(this, arguments);
			var domain = [['view_id', '=', self.renderer.arch.view_id], ['user_id', '=', uid]];
            var fields = ['th_list_text'];
        	rpc.query({
                model: 'th.fields',
                method: 'search_read',
                args: [domain, fields],
            }).then(function(result){
            	if(result.length > 0){
            		self.col_list = _.filter(JSON.parse(result[0].th_list_text), function(elem){return elem.visible});
					var sortArray = _.pluck(self.col_list, 'name');
                    _.each(self.renderer.arch.children, function(elm){
                        if (!_.contains(sortArray, elm.attrs.name)){
                            elm.attrs.modifiers= '{"tree_invisible": true}';
                        }
                    });
                    sortArray = _.compact(sortArray);
					self.render_fields(sortArray);
				}
			});
            var col_values = this.prepare_col_vals();
            self.$DColumns = $(QWeb.render("ListviewColumns",{'columns': col_values}));
			self.$DColumns.find('.th_ul').click(function (e) {
				e.stopPropagation();
            });
            self.$DColReset = $(QWeb.render("th_list_reset",{}));
        },

        fetch_invisible_fields: function(){
			var self = this;
        	this.invisible_fields = {};
        	this.invisible_field_names = [];
        	for(var i in self.renderer.arch.children){
        		var modifiers = self.renderer.arch.children[i].attrs.modifiers;
        		if(modifiers.column_invisible){
        			this.invisible_fields[self.renderer.arch.children[i].attrs.name] = self.renderer.arch.children[i];
        			this.invisible_field_names.push(self.renderer.arch.children[i].attrs.name);
        		}
            }
        },

        prepare_col_vals: function(){
        	var self = this;
        	var col_vals = [];
        	_.each(_.pairs(this.renderer.state.fields), function(field){
        	    if (field[1].type != 'many2many' && field[1].type != 'one2many'
					&& field[1].name != 'create_date' && field[1].name != 'write_date'){
	        		col_vals.push({string: field[1].string, name: field[0]});
	        	}
        	});
        	return col_vals;
        },

        precheck_li: function(){
        	var self = this;
        	var seq = 0;
        	self.col_list = [];
        	self.default_list = [];
        	self.$DColumns.find('.columnCheckbox').removeAttr('checked');
        	for(var i in self.renderer.columns){
                self.$DColumns.find("#" + self.renderer.columns[i].attrs.name).prop('checked',true).attr('data-seq', seq);
                self.col_list.push({'name': self.renderer.columns[i].attrs.name, 'visible': true, 'seq': seq});
                self.default_list.push(self.renderer.columns[i].attrs.name);
                seq = seq + 1;
            }
        	return seq;
        },

        sort_elements: function(){
        	var self = this;
			var elems = self.$DColumns.find('.th_ul #dycollist');
			elems.sort(function(a, b) {
			    if (parseInt($(a).find('input').attr('data-seq')) < parseInt($(b).find('input').attr('data-seq')))
			    return -1;
			    if (parseInt($(a).find('input').attr('data-seq')) > parseInt($(b).find('input').attr('data-seq')))
			    return 1; return 0;
			}).appendTo(elems.parent());
			self.$DColumns.find('.th_ul li:last-child').after(self.$DColReset);
		},

        renderSidebar: function ($node) {
            var self = this;
            this._super.apply(this, arguments);
            if (self.$DColumns && ! _.isUndefined($node)){
                $node.append(self.$DColumns);
                this.col_list = [];
				var seq = self.precheck_li() - 1;
				self.sort_elements();

				self.$DColumns.find('.th_ul #dycollist').each(function(){
					$(this).attr('data-search-term', $(this).find('#ld').text().toLowerCase());
				});

				self.$DColumns.find("#dycolsrch").on('keyup', function(){
					var searchTerm = $(this).val().toLowerCase();
					$('.th_ul #dycollist').each(function(){
				        if ($(this).filter('[data-search-term *= ' + searchTerm + ']').length > 0 || searchTerm.length < 1) {
				            $(this).show();
				        } else {
				            $(this).hide();
				        }
				    });
				});

				self.$DColumns.find('.th_ul').sortable({
				     cancel: ".no-sort",
				     placeholder: "ui-state-highlight",
				     axis: "y",
				     items: "li:not(.no-sort)",
				     update : function( event, ul) {
				         $('.th_ul #dycollist').each(function(i){
				            $(this).find('input').attr('data-seq', i);
				            //updates the self.col_list sequence
				            var input_name = $(this).find('input').attr('name');
				            var col_field = _.find(self.col_list, function(item){
				            	return item.name == input_name;
				            });
				            if (col_field !== undefined ){col_field.seq = i};
				         });
				         self.col_list = _.sortBy(self.col_list, function(o) { return o.seq;});
				         var col_names = [];
				         $('#dycollist input:checked').each(function() {
				        	 col_names.push($(this).attr('name'));
				         });
				         //push only checked data
				         self.render_fields(col_names);
				     },
				});


				self.$DColumns.find('.columnCheckbox').change(function (e){
		        	var val_checked = $("#"+this.id).prop("checked");
		        	if (val_checked){
		        		seq = seq + 1;
		        		var id_search = _.findWhere(self.col_list,{name:this.id});
		        		if (id_search === undefined){
		        			self.col_list.push({'name':this.id,'visible':true,'seq':seq});
		        		}else{id_search.visible = true;id_search.seq = seq;}
		        	}
		        	else{
		        		var id_search = _.findWhere(self.col_list,{name:this.id});
		        		if (typeof id_search === undefined){
		        			self.col_list.push({'name':this.id,'visible':false,'seq':100});
		        		}else{id_search.visible = false;id_search.seq = 100;}
		        	}

		        	self.col_list = _.sortBy(self.col_list, function(o) { return o.seq;});
		        	var col_names = _.pluck(self.col_list, 'name');
		        	self.sort_elements();
		        	self.render_fields(col_names);
		        });

				self.$DColumns.find('#restore_list').click(function(e){
					var uid = session.uid;
					rpc.query({
						model: 'th.fields',
						method: 'search',
						args: [[["view_id", "=", self.renderer.arch.view_id],["user_id", "=", uid]]],
					}).then(function(result){
					    if(result.length > 0){
                            rpc.query({
                                model: 'th.fields',
                                method: 'unlink',
                                args: result,
                            }).then(function(e){
                                location.reload();
                            })
						}
					});
				});

            }
        },

        render_fields: function(col_names){
			var self = this;
			self.fetch_invisible_fields();
			self.renderer.arch.children = [];
			self.renderer.fields = {};
			for(var i in col_names){
				var cname = col_names[i];
				var search_col = _.findWhere(self.col_list,{name: cname});
				if(search_col.visible == true){
					self.renderer.arch.children.push({
						attrs:{
							modifiers: {},
							name: cname,
						},
						children: [],
						tag: 'field'
					});
				}
				else if(cname && $.inArray(cname, self.default_list))
				{
					self.renderer.arch.children.push({
						attrs:{
							modifiers: {"column_invisible": true},
							name: cname,
						},
						children: [],
						tag: 'field'
					});
				}
			}
            // //FIXME : invisble fields are not added to the arch
        	// for(var i in self.invisible_field_names){
        	// 	self.renderer.arch.children.push(self.invisible_fields[self.invisible_field_names[i]]);
        	// 	if (this.id){
        	// 		self.col_list.push({'name':this.id,'visible':false,'seq':100});
				// }
        	// }

       		self.renderer._processColumns({});
       		self.precheck_li();
       		self.sort_elements();
			self.renderer._renderView();
       		self.store_current_state();
		},
		store_current_state: function(){
			var self=this;
			var uid = session.uid;
			self.col_list = _.filter(self.col_list,function (value) {
			    return value.name !==null;
			})
			self.col_list = _.filter(self.col_list,function (value) {
			    return typeof value.name != 'undefined';
			})
			rpc.query({
                model: 'th.fields',
                method: 'search',
                args: [[["view_id", "=", self.renderer.arch.view_id],["user_id", "=", uid]]],
            }).then(function(results){
				if(results.length==1){
					rpc.query({
						model: 'th.fields',
						method: 'write',
						args: [results, {'th_list_text': JSON.stringify(self.col_list)}],
					})
        		}else{
					rpc.query({
						model: 'th.fields',
						method: 'create',
						args: [{
							'view_id': self.renderer.arch.view_id,
							'th_list_text': JSON.stringify(self.col_list),
							'user_id': uid
						}],
					})
        		}
			})
		},
    })

});