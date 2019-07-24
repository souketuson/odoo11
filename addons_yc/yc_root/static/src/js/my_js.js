// odoo.define(moduleNmae, dependencies, function)
odoo.define('yc_root.my_JS', function (require) {"use strict";
    var core = require('web.core');

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
            core.bus.on('click', "div[name='in_out'] div input:checked", this.bgChanger);
            core.bus.on('DOM_updated', "span[name='in_out']", this.post_bgChanger);
            core.bus.on('click', "button .o_pager_next", this.post_bgChanger);
            core.bus.on('click', this, this.elf_Click);
            //core.bus.on('click', this, this.return_Click);
            core.bus.on('click', this, this.return2_Click);
            core.bus.on('keypress', this, this.keypress_focus);

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
        elf_Click: function() {
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
                wizard.css("background-color","#5f5e97");
                wizard.hover(function(e) {
                      $(this).css("background-color",e.type === "mouseenter"?"#5f5e97":"#7c7bad")
                });
            }

        },
        return_Click: function() {
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
        },
        return2_Click: function() {
            if ($('div .purchase2_for_keypress').length ==1){
                var div = $('div #toggle_return');
                var btn = $("div[name='return_btn'] input");
                var wizard = $('.mummy_return');
                if (btn.prop('checked')==true){
                    div.css('display','unset');
                    wizard.removeClass("glyphicon glyphicon-random");
                    wizard.addClass('glyphicon glyphicon-remove');
                    wizard.css("background-color","#568e8f");
                    wizard.hover(function(e) {
                          $(this).css("background-color",e.type === "mouseenter"?"#568e8f":"#80b1b3")
                    });
                }
                else if (btn.prop('checked')==false){
                    div.css('display','none');

                    wizard.removeClass("glyphicon glyphicon-remove");
                    wizard.addClass('glyphicon glyphicon-random');

                    wizard.css("background-color","#5f5e97");
                    wizard.hover(function(e) {
                          $(this).css("background-color",e.type === "mouseenter"?"#5f5e97":"#7c7bad")
                    });
                }
            }
        },
        keypress_focus: function(event){
            if ($('div .purchase2_for_keypress').length ==1 && (event.which== 13) ){
                // light red: #ffcccc, light yellow: #ffffcc, light purple: #ccccff,
                // cce6ff,d0e6fb
                var _color = "#ccccff";
                var _time = $('input[name="time"]');
                var _day =  $('div[name="day"] input');
                var carn = $('div[name="car_no"] input');
                var prat = $('div[name="processing_attache"] input');
                var bat = $('input[name="batch"]');
                var cusn = $('input[name="customer_no"]');
                var cls = $('div[name="clsf_code"] input');
                var pcs = $('input[name="product_code_searchbox"]');
                var sl = $('div[name="strength_level"] input');
                var txt = $('div[name="txtur_code"] input');
                var nor = $('div[name="norm_code"] input');
                var len = $('div[name="len_code"] input');
                var lend = $('input[name="len_descript"]');
                var forh = $('select[name="fullorhalf"]');
                var pro = $('div[name="proces_code"] input');
                var sur = $('div[name="surface_code"] input');
                var sur_next = $('div[name="elecpl_code"] input').length == 1 ? $('div[name="elecpl_code"] input') : $('input[name="num1"]');
                var num1 = $('input[name="num1"]');
                var num2 = $('input[name="num2"]');
                var num3 = $('input[name="num3"]');
                var num4 = $('input[name="num4"]');
                var unit1 = $('div[name="unit1"] input');
                var unit2 = $('div[name="unit2"] input');
                var unit3 = $('div[name="unit3"] input');
                var unit4 = $('div[name="unit4"] input');
                var stor = $('input[name="storeplace"]');
                var net = $('input[name="net"]');
                var pro1 = $('div[name="process1"] input');
                var pro2 = $('div[name="process2"] input');
                var wirf = $('input[name="wire_furn"]');
                var surh = $('input[name="surfhrd"]');
                var corh = $('input[name="corehrd"]');
                var tenh = $('input[name="tensihrd"]');
                var carb = $('input[name="carburlayer"]');
                var tor = $('input[name="torsion"]');
                var tem2= $('input[name="tempturing2"]');
                var ordf = $('div[name="order_furn"] input');
                var not1 = $('input[name="notices1"]');
                var not2 = $('input[name="notices2"]');
                var not3 = $('input[name="notices3"]');
                var qcn1 = $('input[name="qcnote1"]');
                var qcn2 = $('input[name="qcnote2"]');
                var qcn3 = $('input[name="qcnote3"]');
                var prn1 = $('input[name="prodnote1"]');
                var prn2 = $('input[name="prodnote2"]');
                var prn3 = $('input[name="prodnote3"]');
                var norc = $('input[name="norcls"]');
                var wxr = $('input[name="wxr_txtur"]');
                var wxh = $('input[name="wxrhard"]');
                var isFocus = (document.activeElement.parentNode.parentNode.getAttribute('name')) ? document.activeElement.parentNode.parentNode.getAttribute('name') : document.activeElement.getAttribute('name');
                var color_set = function(field){
                    field.css('background-color', _color);
                    window.setTimeout(( () => field.css({'background-color': 'white',
                                                         'transition': 'background-color 1s linear'
                                                         }) ), 300);
                };
                console.log(isFocus);
                switch(isFocus){
                case 'time':
                    _day.focus();
                    break;
                case 'day':
                    carn.focus();
                    color_set(carn);
                    break;
                case 'day':
                    carn.focus();
                    color_set(carn);
                    break;
                case 'car_no':
                    prat.focus();
                    color_set(prat);
                    break;
                case 'processing_attache':
                    bat.focus();
                    break;
                case 'batch':
                    cusn.focus();
                    break;
                case 'customer_no':
                    cls.focus();
                    color_set(cls);
                    break;
                case 'clsf_code':
                    pcs.focus();
                    break;
                case 'product_code_searchbox':
                    sl.focus();
                    color_set(sl);
                    break;
                case 'strength_level':
                    txt.focus();
                    color_set(txt);
                    break;
                case 'txtur_code':
                    nor.focus();
                    color_set(nor);
                    break;
                case 'norm_code':
                    len.focus();
                    color_set(len);
                    break;
                case 'len_code':
                    lend.focus();
                    break;
                case 'len_descript':
                    forh.focus();
                    color_set(forh);
                    break;
                case 'fullorhalf':
                    pro.focus();
                    break;
                case 'proces_code':
                    sur.focus();
                    color_set(sur);
                    break;
                case 'surface_code':
                    sur_next.focus();
                    color_set(sur_next);
                    break;
                case 'elecpl_code':
                    num1.focus();
                    break;
                case 'num1':
                    unit1.focus();
                    color_set(unit1);
                    break;
                case 'unit1':
                    stor.focus();
                    color_set(stor);
                    break;
                case 'storeplace':
                    net.focus();
                    break;
                case 'net':
                    pro1.focus();
                    color_set(pro1);
                    break;
                case 'process1':
                    pro2.focus();
                    color_set(pro2);
                    break;
                case 'process2':
                    wirf.focus();
                    break;
                case 'wire_furn':
                    surh.focus();
                    break;
                case 'surfhrd':
                    corh.focus();
                    break;
                case 'corehrd':
                    tenh.focus();
                    break;
                case 'tensihrd':
                    carb.focus();
                    break;
                case 'carburlayer':
                    tor.focus();
                    break;
                case 'torsion':
                    tem2.focus();
                    break;
                case 'tempturing2':
                    ordf.focus();
                    color_set(ordf);
                    break;
                case 'order_furn':
                    not1.focus();
                    break;
                case 'notices1':
                    not2.focus();
                    break;
                case 'notices2':
                    not3.focus();
                    break;
                case 'notices3':
                    qcn1.focus();
                    break;
                case 'qcnote1':
                    qcn2.focus();
                    break;
                case 'qcnote2':
                    qcn3.focus();
                    break;
                case 'qcnote3':
                    prn1.focus();
                    break;
                case 'prodnote1':
                    prn2.focus();
                    break;
                case 'prodnote2':
                    prn3.focus();
                    break;
                case 'prodnote3':
                    norc.focus();
                    break;
                case 'norcls':
                    wxr.focus();
                    break;
                case 'wxr_txtur':
                    wxh.focus();
                    break;
                case 'wxrhard':
                    _time.focus();
                    break;
                }
            }
        },
    });

    // Init a new bgdrawer when the web client is ready
    /*core.bus.on('web_client_ready', null, function () {new bgdrawer();});
    return {'bgdrawer': bgdrawer,};*/

    var my_widget = new bgdrawer(this);
    my_widget.appendTo($(".o_form_sheet"));
});





