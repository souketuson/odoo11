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
            core.bus.on('click', "div[name='in_out'] div input:checked", this.bgChanger); //過磅進出貨變色
            core.bus.on('DOM_updated', "span[name='in_out']", this.post_bgChanger); // 過磅進出貨變色
            core.bus.on('click', "button .o_pager_next", this.post_bgChanger); //過磅下一筆變色
            core.bus.on('click', this, this.elf_Click); //版面1搜尋舊檔
            core.bus.on('click', this, this.return_Click); //版面1退回
            core.bus.on('click', this, this.return2_Click); //版面2退回
            core.bus.on('keypress', this, this.keypress_focus); //key jump
            core.bus.on('click', this, this.cuckoo); // 點擊報時

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
                $('button[name="wizard_comfirm"]').attr("disabled", true);
                $('div .hidden_on_bush').addClass('hide', 0);
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
                $('button[name="wizard_comfirm"]').attr("disabled", false);
                $('div .hidden_on_bush').removeClass('hide', 0);
                comfirm.css('display','none');
                wizard[0].innerText = "開啟舊檔搜尋";
                wizard.css("background-color","#5f5e97");
                wizard.hover(function(e) {
                      $(this).css("background-color",e.type === "mouseenter"?"#5f5e97":"#7c7bad")
                });
            }

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
        return2_Click: function() {
            if ($('div .purchase2_for_js').length ==1){
                var div = $('div #toggle_return');
                var btn = $("div[name='return_btn'] input");
                var wizard = $('.mummy_return');
                if (btn.prop('checked')==true){
                    div.css('display','unset');
                    wizard.removeClass("glyphicon glyphicon-random");
                    wizard.addClass('glyphicon glyphicon-remove');
                    wizard.css("background-color","#80b1b3");
                    wizard.hover(function(e) {
                          $(this).css("background-color",e.type === "mouseenter"?"#568e8f":"#80b1b3")
                    });
                }
                else if (btn.prop('checked')==false){
                    div.css('display','none');

                    wizard.removeClass("glyphicon glyphicon-remove");
                    wizard.addClass('glyphicon glyphicon-random');

                    wizard.css("background-color","#7c7bad");
                    wizard.hover(function(e) {
                          $(this).css("background-color",e.type === "mouseenter"?"#5f5e97":"#7c7bad")
                    });
                }
            }
        },
        keypress_focus: function(event){
            var da = document.activeElement;
            if ($('div .purchase2_for_js').length ==1 && (event.which== 13) && da.tagName == "INPUT"){
                // light red: #ffcccc, light yellow: #ffffcc, light purple: #ccccff,
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
                var isFocus = (da.parentNode.parentNode.getAttribute('name')) ? da.parentNode.parentNode.getAttribute('name') : da.getAttribute('name');
                var color_set = function(field){
                    field.addClass('pulse', 0).removeClass('pulse', 2000);
                };
                console.log('last field:',isFocus);
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
                    prat.click();
                    color_set(prat);
                    break;
                case 'processing_attache':
                    bat.focus();
                    color_set(bat);
                    break;
                case 'batch':
                    cusn.focus();
                    color_set(cusn);
                    break;
                case 'customer_no':
                    cls.focus();
                    cls.click();
                    color_set(cls);
                    break;
                case 'clsf_code':
                    pcs.focus();
                    color_set(pcs);
                    break;
                case 'product_code_searchbox':
                    sl.focus();
                    sl.click();
                    color_set(sl);
                    break;
                case 'strength_level':
                    txt.focus();
                    txt.click();
                    color_set(txt);
                    break;
                case 'txtur_code':
                    nor.focus();
                    nor.click();
                    color_set(nor);
                    break;
                case 'norm_code':
                    len.focus();
                    len.click();
                    color_set(len);
                    break;
                case 'len_code':
                    lend.focus();
                    color_set(lend);
                    break;
                case 'len_descript':
                    forh.focus();
                    forh.click();
                    color_set(forh);
                    break;
                case 'fullorhalf':
                    pro.click();
                    pro.focus();
                    break;
                case 'proces_code':
                    sur.focus();
                    sur.click();
                    color_set(sur);
                    break;
                case 'surface_code':
                    sur_next.focus();
                    sur_next.click();
                    color_set(sur_next);
                    break;
                case 'elecpl_code':
                    num1.focus();
                    color_set(num1);
                    break;
                case 'num1':
                    unit1.focus();
                    unit1.click();
                    color_set(unit1);
                    break;
                case 'unit1':
                    stor.focus();
                    color_set(stor);
                    break;
                case 'storeplace':
                    net.focus();
                    color_set(net);
                    break;
                case 'net':
                    pro1.focus();
                    pro1.click();
                    color_set(pro1);
                    break;
                case 'process1':
                    pro2.focus();
                    pro2.click();
                    color_set(pro2);
                    break;
                case 'process2':
                    wirf.focus();
                    color_set(wirf);
                    break;
                case 'wire_furn':
                    surh.focus();
                    color_set(surh);
                    break;
                case 'surfhrd':
                    corh.focus();
                    color_set(corh);
                    break;
                case 'corehrd':
                    tenh.focus();
                    color_set(tenh);
                    break;
                case 'tensihrd':
                    carb.focus();
                    color_set(carb);
                    break;
                case 'carburlayer':
                    tor.focus();
                    color_set(tor);
                    break;
                case 'torsion':
                    tem2.focus();
                    color_set(tem2);
                    break;
                case 'tempturing2':
                    ordf.focus();
                    color_set(ordf);
                    break;
                case 'order_furn':
                    not1.focus();
                    color_set(not1);
                    break;
                case 'notices1':
                    not2.focus();
                    color_set(not2);
                    break;
                case 'notices2':
                    not3.focus();
                    color_set(not3);
                    break;
                case 'notices3':
                    qcn1.focus();
                    color_set(qcn1);
                    break;
                case 'qcnote1':
                    qcn2.focus();
                    color_set(qcn2);
                    break;
                case 'qcnote2':
                    qcn3.focus();
                    color_set(qcn3);
                    break;
                case 'qcnote3':
                    prn1.focus();
                    color_set(prn1);
                    break;
                case 'prodnote1':
                    prn2.focus();
                    color_set(prn2);
                    break;
                case 'prodnote2':
                    prn3.focus();
                    color_set(prn3);
                    break;
                case 'prodnote3':
                    norc.focus();
                    color_set(norc);
                    break;
                case 'norcls':
                    wxr.focus();
                    color_set(wxr);
                    break;
                case 'wxr_txtur':
                    wxh.focus();
                    color_set(wxh);
                    break;
                case 'wxrhard':
                    _time.focus();
                    color_set(_time);
                    break;
                }
            }
        },
        cuckoo: function(){
            if($('div .process_for_js').length == 1){
                var today=new Date()
                var _t = String(today.getHours()) + ':'+ String(today.getMinutes());
                var isFocus = document.activeElement.getAttribute('name');
                switch(isFocus){
                    case 'ptime1':
                        $('input[name="ptime1"]').val(_t);
                        break;
                    case 'ptime2':
                        $('input[name="ptime2"]').val(_t);
                        break;
                    case 'ptime3':
                        $('input[name="ptime3"]').val(_t);
                        break;
                };
            }
        },
    });

    // Init a new bgdrawer when the web client is ready
    /*core.bus.on('web_client_ready', null, function () {new bgdrawer();});
    return {'bgdrawer': bgdrawer,};*/

    var my_widget = new bgdrawer(this);
    my_widget.appendTo($(".o_form_sheet"));
});





