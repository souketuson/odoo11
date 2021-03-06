// 載入這個script後 到其他頁面功能還會一直存在
// solution1: 其他頁面進入後refresh
// solution2: listen 在某些元素存在時才啟動
// 開啟退回列表
$(document).on('click', "label.btn", function(event){
    var keeper =$('div.purchase2_for_js');
    if (keeper.length==1){
        var div = $('div #toggle_return');
        var btn = $("div[name='return_btn'] input");
        var comfirm = $('button.comfirm_return');
        var wizard = $('.mummy_return');
        if (btn.prop('checked')==true){
            div.css('display','unset');
            comfirm.removeClass('disabled');
            wizard.removeClass("glyphicon glyphicon-random");
            wizard.addClass('glyphicon glyphicon-remove');
            wizard.css("background-color","#80b1b3");
            wizard.hover(function(e) {
                $(this).css("background-color",e.type === "mouseenter"?"#568e8f":"#80b1b3")
            });
        }
        else if (btn.prop('checked')==false){
            div.css('display','none');
            comfirm.addClass('disabled');
            wizard.removeClass("glyphicon glyphicon-remove");
            wizard.addClass('glyphicon glyphicon-random');

            wizard.css("background-color","#7c7bad");
            wizard.hover(function(e) {
                $(this).css("background-color",e.type === "mouseenter"?"#5f5e97":"#7c7bad")
            });
        }
    }
});
// 鍵盤導航 重複載入頁面 keypress會重複執行
// 在前端頁面用getScript() 及 變數 防止重複抓取腳本
$(this).keypress(function(e){
    var keeper =$('div.purchase2_for_js');
    if (keeper.length==1){
        var da = document.activeElement;
        if (e.which== 13 && da.parentNode.parentNode.nodeName != '#document'){
            console.log(e.which);
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
            var stor = $('div[name="storeplace_id"]');
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
    }
});

// 先disable 退回btn
//$(document).ready(function(){
//   $('button.comfirm_return').attr("disabled",true);
//});







// note autocomplete
/*$( function() {
    var tags = [
        ' 彎曲須矯直.','.扭力作中限.','0.08低於HV300','0.10mm:RC45MIN','0.12高於HV220','0.15MM450↑判','0.28MM400↓判','08AV2243',
        '0BOJ2173','0CFE4187','0度楔型塊','10中生料暫不作','10度板拉力測試','10度楔型塊','10條HV450↑','11CJ2149','135A2044.A重作',
        '15SA2063','15條HV500↑','1A','1B','1B柱仔旁','1B電腦桌上','20度不能有裂痕','21UA2105','22PS3101轉重染','231V2132',
        '23條HV412↓','250-320HV30測','26KB3140','28UR2117轉出','28UR2118轉出','299B3100','2A','2A.','2B.H重回','2小捆勿拆勿混',
        '30KG扭力不可斷','30KG扭不可斷裂','30度斜敲擊','30條HV380↑','3A.','3B','3C9B1092','3叉WT','3船退回品','4/23待通知再做',
        '42RB2079.6-9轉','450HV0.3判讀','450HV0.5判定','4度契型塊','64PCS','6度契型塊','80度頭部敲擊','A55J2118','A控制室.勿放氨',
        'A爐前','C3B53115','C8JA2128', 'CP0.25','CP0.25.回火520','CP0.25回火450','CP0.25回火470','CP0.25回火520','CP0.35-0.40',
        'CP0.5-0.6','CP0.7.換電鍍桶','CP0.7-0.9','C重作','C爐重作','FORD-SPC','GM.品留樣10支','GM汽車用螺絲','HR15N 77判讀','HRB92-94',
        'HRC 48-50最好','HRC:37-43','HRC32判讀','HRC40判讀','HRC42判HV0.5','HRC42判HV0.5測','HRC42判荷500g','HRC42判測牙底',
        'HRC42判測牙腹','HRC42判讀','HRC45判測牙底','HRC45判讀','HRC45判讀HV0.5','HRC60判讀','HRC轉換HB測','HV 420判','HV:100-200HV30',
        'HV0.3轉換HR30N','HV1HV550判','HV30測','HV400HV0.3判讀','HV400判讀','HV412判0.3','HV412判HV0.5','HV412判測牙底','HV412判讀',
        'HV413判讀','HV420判','HV420判讀','HV425判讀','HV446判HV0.5測','HV446判讀','HV450HV0.5判讀','HV450判HV0.3測','HV450判測牙山',
        'HV450判測牙底','HV450判讀','HV450判讀HV0.5','HV450判讀點','HV454判','HV480判讀','HV500判讀','HV512判讀','HV513判讀','HV520判讀',
        'HV530判讀','HV550判讀','HV567判','HV567判讀','HV580判','HV600判讀HV0.5','HV653判讀','HV700判讀','HV換算測表面','H重回','H重烘',
        'H爐前','H爐前H重回','H爐重回','H爐桌上','IK10.9','M10荷重33700N','M重作','NG品入料薄一點','NO1-3大重回','NYLON頭不破裂','OK可交',
        'OK掛紅標籤','OK掛紅標籤分重','OK掛紅標籤去油','OK掛紅標籤剔檢','OK掛紅標籤淋油','OK掛紅標籤換報','OK掛紅標籤篩選','OK掛紅籤去油',
        'OK掛紅籤去油.','OK掛紅籤待送','OK掛紅籤洗柴油','OK掛紅籤重作','OK掛紅籤淋油','OK掛黃標簽可出','OK掛黃標籤註明','OK請用袋裝',
        'OK請留10支給曾','OK請換報紙','OK繫紅單H重染','OK繫紅單H烘乾','OK繫紅單換報紙','O度楔形塊','RC45判讀','W.1050.RC37-45',
        'W: HV 160-320','W:100-250HV','W:1006-1010','W:1008','W:1008-1012','W:1008HRC42-50','W:1010','W:1010/HV200','W:1020',
        'W:1050','W:1050.1008','W:1050.300-390','W:1050/HV200↑','W:1050-1065','W:1050-1070','W:1050-1075','W:1050HRC30-38',
        'W:1050HRC36-40','W:1050HRC38-43','W:1050HRC38-46','W:1050HRC40-50','W:1050HRC41-47','W:1050HRC42-46','W:1050HRC42-48',
        'W:1050HRC43-50','W:1050RC30-48','W:1050RC35-45','W:1050RC40-48','W:1050RC40-50','W:1055-1065','W:1055RC36-48','W:1060',
        'W:1060,1050','W:1060.1008','W:1060.RC42-50','W:1060-1006','W:1060-1070','W:1060HRC42-53','W:1060HRC45/53',
        'W:1060RC45-53','W:1080/1008','W:160-430HV10','W:300-390HV5','W:430-530','W:HRC 35-45','W:HRC 37-40','W:HRC30-39',
        'W:HRC33-40','W:HRC35-40','W:HRC36-44','W:HRC36-47','W:HRC37-43','W:HRC38-45','W:HRC38-46','W:HRC38-48','W:HRC40-45',
        'W:HRC40-48','W:HRC40-50','W:HRC42-50','W:HRC45-53','W:HRC57-62','W:HV 430-530','W:HV125-320','W:HV140(MIN)',
        'W:HV140-250','W:HV160-320','W:HV160-320HV5','W:HV160-430','W:HV180(MIN)','W:HV200(MIN)','W:HV200-300','W:HV247-310',
        'W:HV300-370','W:HV300-390','W:HV300-390HV5','W:HV320-430','W:HV340-490','W:HV350-425','W:HV350-490','W:HV360-430',
        'W:HV372-484','W:HV380-420','W:HV392-513','W:HV400-500','W:HV410-490','W:HV410-520','W:HV420-500','W:HV420-510',
        'W:HV430-530','W:RC30-48','W:RC45-53HV0.5','W:S50C42-50HRC','W:SK7RC30-48','W:心部HRC36-42','W:外徑12mm','W1050.HRC30-38',
        'W1065HV430-510','W1070HRC42-50','WHV200HV30測','WHV300-370HV10','W厚度過大特採','一桶一桶做','人工只排一層','人工收人工排',
        '人工收料','人工排收勿重疊','入料排一層','入料薄ㄧ點','入料薄一點','三種爐號勿混合','下料勿重疊','下料前要比對','下料前請重秤重',
        '下料厚2支高','下料看同爐號','下料時勿重疊','下貨到棧板','上面鋪報紙','已先回火過','已回火過','已作過攻速失敗','已咬酸過','已咬酸電鍍過',
        '已研磨過','已做酸洗過','已做應消過','已電鍍過','已滲碳.高週波','已滲碳過','已滲碳電鍍過','已酸洗過','已熱處理過','已調質OK','已調質過',
        '已調質電鍍過','已應力消除','不可少收桶數','不可水洗','不可牙緊','不可生銹','不可有裂痕','不可低於HV295','不可重疊','不可浸油','不可掉色',
        '不可淬裂','不可脫碳','不可脫碳附報告','不可黑化','不可墊報紙','不可鋪報紙','不可龜裂','不可縮孔','不可斷頭','不可彎曲','不可變形',
        '不良品送噴砂','不要求心部','不要求拉力','不要前洗','不要鋪報紙','不能斷頭','不測彎曲度','不黑化+水性油','中洗不要洗','中洗舖海綿墊',
        '仁.不可浸油','仁.用人工排收','仁武','仁武.L重作','內六點平頭螺絲','六角 凹頭螺絲','六角塞規測孔徑','分開做.白單','分開做.黃單',
        '分開做.橘單','分開做.藍單','分開處理勿混合','分開裂料','分爐號勿混合','切勿牙鬆','勿切料','勿水淬','勿用吸盤送料機','勿放氨','勿前洗',
        '勿前洗,勿浸油','勿前洗.勿牙傷','勿前洗.勿混合','勿前洗.勿黑化','勿前洗.微黑','勿重疊','勿重疊勿碰傷','勿重疊勿縮孔','勿重疊勿變形',
        '勿重疊縮孔混合','勿消時間','勿消電腦','勿混合','勿混合分開作','勿脫殼','勿測拉力','勿測試.勿遺失','勿測試拉力','勿黑勿前洗','勿黑化入料薄',
        '勿跳過','勿與前批混合','勿鋸料','勿鋸料測試','勿檢測','勿縮孔','孔徑5.562測試','少油','尺寸比對ok再作','引擎螺絲','心.華司HV10測',
        '心:HV 1 KG測','心:HV測試轉換','心:直接HRC測','心:參考RC27-30','心:參考RC34-37','心:荷重500g測','心HR30N測','心HRA60kg測轉',
        '心HRA60測試轉','心HRC測','心HV0.3測','心HV0.3測0.5處','心HV10測','心HV1kg測→HRC','心HV340-360佳','心HV5,表HV0.5','心HV5.表HV1',
        '心HV5表0.3測','心勿超HRC37','心勿超HRC38','心勿超HRC42','心勿超HRC43','心勿超HV370','心以HRC檢驗','心以HV3或HV5測','心以HV500g測',
        '心以HV測','心部:HRB 92-94','心部:HRC25MIN','心部:HV30測','心部30N測試','心部500g鑲埋測','心部HRC28-32','心部HRC29.2',
        '心部HRC測試','心部HV→HRC測','心部HV0.3測','心部HV10測','心部HV1KG測','心部HV30測','心部HV5測','心部RC測試','心部不均不足',
        '心部勿超HRC38','心部以HRC測試','心部以HV0.5測','心部以HV10測試','心部以HV30測','心部以HV3測','心部以HV5測試','心部以維氏500g',
        '心部用30N測','心部用HV測','心部作中上限','心部參考用','心部測30N→HRC','心部測30N→HV','心部測HV→HRC','心部測RC換算HB','心部測牙及桿徑',
        '心部測空心位置','心部測桿徑','心部硬度太硬','心部硬度做下限','心部硬度參考用','心部硬度過高','心部請作上限','心部請做下限','心部請做上限',
        '心部鑲埋HRC測','心測0.5mm處','心測15N→HRC','心測15N-HRC','心測HR30N→HRC','心測HRC→HV','心測HV→HRC','心測M16-1.5處',
        '心測桿徑10mm處','心測頭部及牙部','心硬+30HV判','手拿輾牙防牙傷', '支數勿短少','比對尺寸OK再作','比對清楚再作','水性防鏽油','牙不一樣',
        '牙勿撞傷','牙勿撞傷.H爐前','牙底不能裂開','牙底有油膜','牙部.孔內生銹','牙距不同勿混合','牙緊退回','牙數不同勿混合','以412HV0.5判',
        '以HRC 50判讀','以HRC42判讀','以HRC45判讀','以HRC50判讀','以HV400判讀','以HV500g測試','以HV500判讀','以HV550判讀','以HV值判定',
        '以RC42判讀','以原桶裝回','以原船編號裝回','出貨分重量','出貨打紅刊勿混','出貨附材質証明','出貨附棧板1個','出貨附製程條件','加長回火時間',
        '包樣品1包給曾小姐看外觀','包樣品給客戶檢驗','卡爐','卡爐從0AIB3066','卡爐復碳調質','可做乾再淋油','只可檢測1支','只作1KG勿消時',
        '只求彎曲度30度','只要求表面','只要求保證荷重','只能拉3只','只淬火不回火','只測拉力','只測表面','只測硬.拉各1支','外六點輪緣螺絲',
        '外勞宿舍','外銷日本','外觀不良','外觀脫殼','左豐2船1B','平1012彈1065','平W:HRC38-45','平W:HV200-300','平W200-250HV10',
        '平華RC38-45','平華司:1008','未分檢勿混合','未作退回','未超心部6RC即','生料20支給品管','生料先吊磅','生料先過磅再做','生料脫碳','生銹',
        '用10度測拉力','用6°板測斜楔','用HRA刻度測試','用力大船桶裝','用友信船桶裝','用客戶指定油','用排平放孔朝上','用旋入板','用旋入板測扭力',
        '白皮可作乾性','皮膜脫落及油銹','目標 HRB70','目標HRC 28-34','目標HRC26-30','目標HRC30-36','目標HRC32-36','目標HRC35','交春雨',
        '先放試片','先惕檢看比例','全程用船型桶裝','再清洗後H回火','回火後再輾牙','回軟.搓牙','如有NG速重處理','安全部品號碼','成品穿透扭81.6',
        '成品請勿檢測','收料勿用耙子扒','收料用原船桶裝','收料時勿碰傷','收料時裝成3圓','有卡爐','有倒角勿混合','有線材一起','此批分6種爐號',
        '此批分船(中)桶','此批生料淋過雨','此批共2種爐號','此批共3種爐號','此批共4種爐號','此批共5種爐號','此批共6種爐號','此批共7種爐號',
        '此批含圓(船)桶','此船有4種規格','灰磷酸鋅','灰磷酸鹽','自主及首末件檢','伸長720MPA','伸長率:10%最小','伸長率:12%','伸長率:15%最小',
        '伸長率:20%','伸長率:22%','伸長率:30%MIN','伸長率:8%','伸長率:9%','伸長率:9%(MIN)','伸長率:9%最小','伸長率10%','伸長率10%(MIN)',
        '伸長率10%以上','伸長率12%(MIN)','伸長率12%以上','伸長率13%','伸長率13%(MIN)','伸長率14％','伸長率14%以上','伸長率14℅',
        '伸長率14以上','伸長率15%','伸長率15%(MIN)','伸長率15%以上','伸長率16%','伸長率16%以上','伸長率17%','伸長率17%↑','伸長率17%以上',
        '伸長率18%','伸長率22%','伸長率26%(MIN)','伸長率7%以上','伸長率8%','伸長率8%↑','伸長應力940MPA','作5KG勿消時間','作HV286-372中',
        '作之前比對尺寸','作好袋裝','作時注意標籤材','作時客戶要來看','作時請核對頭記','作淬火轉H回火','作熱處理報告','作頭部敲擊15°',
        '作頭部敲擊25°','作襄埋測5點','判 讀HV400','判心實測+HV25','判心實測+HV30','判讀HV412HV0.5','判讀HV420','判讀HV446',
        '判讀HV450HV0.5','判讀RC45測牙底','判讀測高低牙','判讀點:HV550','判讀點550 HV1','判讀點HRC40','判讀點HRC45','判讀點HV 446',
        '判讀點HV 650','判讀點HV336','判讀點HV392','判讀點HV402','判讀點HV412','判讀點HV420','判讀點HV480','判讀點HV515','判讀點HV530',
        '判讀點HV545','判讀點RC50','含油白皮','尾部不同勿混合','尾割溝需26IN/L','抗拉:14800N↑','抗拉:152000N↑','抗拉:57.9KN↑',
        '抗拉29Nm(MIN)','抗拉最小4181','扭:夾華司轉C牙','扭34.2-80.9Nm','扭力不足','扭力客戶要求','扭力控制在下限','扭力最小33N-m',
        '扭力測外梅花處','扭力測頭部處','扭矩:29000lbf','扭矩:31900lbf','扭矩:45100lbf','扭矩:59400lbf','扭矩控制在中限','扭距:55N-CM(MI',
        '批號不同勿混合','改做電鍍','材質不一樣勿混','材質不同勿混','材質不同勿混合','材質不苻.','材質不詳放試片','材質相混','材質混合',
        '每一批勿混合','每一批只切1支','每桶放試片2支','每桶留生料2支','沒標籤,磁鐵','汽車用','汽車螺絲','車修品勿撞傷','車廠用','防止彎曲',
        '防氫脆','防脫碳(附報告)','依27FQ4139','依IFI第7版標準','依微小微克300g','依微小維克1Kg','依微小維克500g','依圖測','其他暫不做',
        '底徑加15條','延伸80%','延伸率:10%','延伸率:12%最小','延伸率:18%(MIN','延伸率:22%','延伸率10%(MIN)','延伸率15000N','延伸率16%',
        '延伸率16%以上','延伸率18%(MIN)','延伸率18%↑','延伸率22%(MIN)','延展15度(MIN)','延展性:10度','延展性:16%↑','延展性:8-10%',
        '延展性15度MIN','延展性7度↑','延展性測試7度','延展性敲擊10度','拉:最小5.42KN','拉1361-1542kgf','拉1724-1905kgf','拉力:27KN最小',
        '拉力:67300N','拉力0度板','拉力102.4(MAX)','拉力均不可斷頭','拉力客戶要求','拉力做上限','拉力參考','拉力參考用','拉力斜契6。板',
        '拉力斜楔10°板','拉力斜楔4°板','拉力斜楔6°板','拉力荷重:800KG','拉力最小14100L','拉力最小18.7KN','拉力最小29200N','拉力最小75.9KN',
        '拉力最小784MPA','拉力測M8處','拉伸率:最小15%','拉伸率;最小15%','拋光成品0.38↑','抽樣8支','抽樣數12支','抽樣數5支','抽樣數7支',
        '抽樣數8支','抽樣數每船5粒','拆開用排列做','放試片OK','注意勿縮孔','注意尺寸差一點','注意頭部厚度','油性防鏽油','油槽取出','表&心勿超2°↑',
        '表&心以HV1測','表&心以HV1測試','表,心以HV0.3測','表,心部以HV1測','表.心:HV0.3測','表.心HV0.3測','表.心HV0.5測','表.心HV1.0測',
        '表.心HV10測','表.心HV1測','表.心HV30測','表.心以HV10測','表.心皆要測試','表.心測HV換算','表.心測高低牙','表:15N測','表:15N測試',
        '表:15N轉換','表:HV0.5測','表:HV500g荷重','表:量測HV500g','表≦心+HRC 2','表0.05心0.50mm','表0.05心0.5mm','表0.05滲碳0.50',
        '表0.18:HRC50↓','表0.3orHV0.5','表15N轉換','表HR15N測桿徑','表HV→HRC測','表HV0.2心HV0.3','表HV0.3,心HV30','表HV0.3,心HV5',
        '表HV0.3.心HV1','表HV0.3心HV0.3','表HV0.3心HV0.5','表HV0.3心HV10','表HV0.3心HV3','表HV0.3心HV30','表HV0.3心HV5',
        '表HV0.3或0.5測','表HV0.3測','表HV0.3測頭部','表HV0.5,心HV1','表HV0.5.心HV1','表HV0.5.心HV10','表HV0.5RC42測','表HV0.5心HV1.0',
        '表HV0.5心HV10','表HV0.5測','表HV1.心HV10測','表HV10測','表HV1測','表HV2.5,心HV30','表HV3,心HV10測','表HV3,心HV30測',
        '表HV3心HV10測','表HV5,心HV30測','表HV5.心HV10測','表HV5.心HV3','表HV500G測','表勿超心+2HRC','表勿超心+3HRC','表勿超心+50HV',
        '表勿超心+HV20','表勿超心+HV30','表勿超心+HV50','表勿超心3HRC','表勿超心HRC3','表心HRC150KN測','表心HV0.3','表心HV0.3or0.5',
        '表心HV0.5測','表心HV10測','表心HV30測','表心皆要測','表心測HRC→HB','表以0.05mm基準','表以HR15N測試','表以HV0.05測','表以HV0.3測',
        '表以HV10測','表以HV30測','表面HV0.3','表面下限','表面不可脫碳','表面不要太軟','表面不漂亮','表面勿超過心部','表面太高','表面心部HV轉換',
        '表面以HRC測','表面以HV0.5測','表面可HV換算','表面拉力無要求','表面處理不良','表面測0.05m/m','表面測0.08mm處','表面測HV30',
        '表面測在M8處','表面測尾端','表面測花齒部','表面測桿徑','表面測華司面','表面測頭部','表面測頭頂處','表面硬度參考用','表面請做上限',
        '表荷:300G','表測0.05mm處','表測0.05心0.50','表測0.08mm處','表測0.11mm處','表測HR15N→HRC','表測HV->HR15N','表測HV→HR15N',
        '表測牙底0.05MM','表測桿身15N測','表測桿徑','表測桿徑RC測試','表測頭部0.05mm','表測頭部的平面','表測頭部做鑲埋','表硬≧心+HV30',
        '表硬太硬','表硬測對邊','表硬測頭部','表與心HV0.3測','表與心皆測頭部','表與心部做上限','長尺寸勿彎曲','長尺寸請用排','附1支試片',
        '附2只環規','附CQI-9驗報告','附牙板1塊','附牙規測孔徑','附成品30支','附恆溫試驗報告','附英文報告','附套管1支','附脫碳測試報告',
        '附報告.曲線圖','附插規1支','附插規勿縮孔','附插規測孔徑','附測孔徑帽5只','附測孔徑螺帽3','附量管測彎曲','附溫度曲線圖','附試片1支',
        '附試棒1支測試','附試驗用樣品','附模具一支','附熱處理曲線圖','附檢查成績書','附螺絲測保證','附鑲埋試片2支','保:105.06kg/mm',
        '保:1143.3N/mm2','保:120000psi↑','保:17365.8kgf','保:34-38kg/mm','保:38-34KG/MM2','保:8.23KN','保:最小13.1KN',
        '保:最小580MPA','保1082N/mm2','保荷:11.6KN','保荷:1150N/mm2','保荷:60.3KN','保証荷重11.8KN','保証荷重45KN','保証荷重580MPA',
        '保証荷重8.23KN','保証荷重85KPSI','保證:10080kgf','保證:10150kgf','保證:10157kgf','保證:10270kgf','保證:1050MPA↑',
        '保證:106502N','保證:1071N/mm2','保證:1072N/mm2','保證:10750kgf','保證:1082MPa','保證:10890kgf','保證:10990kgf','保證:11.6KN',
        '保證:11000kgf','保證:11030kgf','保證:11400kgf','保證:1144N/mm2','保證:11500kgf','保證:1163kgf','保證:11790LBS',
        '保證:11791LBS','保證:120KSI','保證:12680kgf','保證:12690kgf','保證:12700LBS','保證:13.1KN','保證:13700kgf','保證:13780kgf',
        '保證:14300kgf','保證:14340kgf','保證:14350kgf','保證:14480kgf','保證:14500kgf','保證:14570kgf','保證:14626LBS',
        '保證:14730kgf','保證:14780kgf','保證:14800kgf','保證:14860kgf','保證:150000Psi','保證:16.7KN','保證:16730kgf',
        '保證:16827kgf','保證:17300kgf','保證:17330kgf','保證:17366kgf','保證:17819kgf','保證:17819LBS','保證:18.08KN↑',
        '保證:18600kgf','保證:19190kgf','保證:1920kgf','保證:1939kgf','保證:19470kgf','保證:20491LBS','保證:20492LBS','保證:20920kgf',
        '保證:21.2KN','保證:21000kgf','保證:21445kgf','保證:21527N','保證:2190kgf','保證:22149LBS','保證:2230Kgf','保證:22680kgf',
        '保證:22690kgf','保證:23.8KN','保證:23400kgf','保證:23720kgf','保證:23992LBS','保證:24205LBS','保證:24830kgf','保證:25132LBS',
        '保證:27270kgf','保證:28600kgf','保證:29400kgf','保證:30.4KN','保證:3000N','保證:31621LBS','保證:340KN(MIN','保證:34100kgf',
        '保證:36.3KN','保證:38100N','保證:38204LBS','保證:4000kgf','保證:4075kgf','保證:41818LBS','保證:448000Lbs','保證:46144LBS',
        '保證:48.1KN','保證:48.9KN','保證:5.1KN','保證:5065kgf','保證:515N/mm2','保證:5562kgf','保證:5680kgf','保證:59.2.勿混',
        '保證:59800N','保證:60300N','保證:6153kgf','保證:62000LBS','保證:6300kgf','保證:6330kgf','保證:6340kgf','保證:640MPA',
        '保證:647.6N/mm','保證:650MPA','保證:6640kgf','保證:7250kgf','保證:7700kgf','保證:8.23KN','保證:8040kgf','保證:8120kgf',
        '保證:8125kgf','保證:8460kgf','保證:8700kgf','保證:8700kgf↑','保證:883N/mm2','保證:9000KGF','保證:91155N','保證:9290kgf',
        '保證:9300kgf','保證:948N/mm2','保證:9682kgf','保證:9720kgf','保證1.91KN','保證107.738KN','保證1081.5Mpa','保證1081MPA↑',
        '保證11.35KN','保證11600N','保證12700LBS','保證17716LBS','保證203.5KN','保證21.2KN(MIN','保證21200KGF↑','保證21424LBS',
        '保證23993LBS','保證24205LBS','保證32558LBS','保證32559LBS','保證33143kgf','保證5.1KN','保證580N/mm2↑','保證640-900N/M',
        '保證6740kgf','保證720N/mm2','保證8230N','保證830MPA','保證85000PSI','保證85000PSI↑','保證970N/mm2','保證9770kgf↑',
        '保證荷重11.6KN','保證荷重120KSI','保證荷重13.1KN','保證荷重17.2KN','保證荷重21.2KN','保證荷重24.0KN','保證荷重33.7KN',
        '保證荷重58000N','保證荷重580N','保證荷重70KN','保證荷重7808KG','保證荷重88142N','保證荷重不足','前4大G重作','前中洗放脫脂劑',
        '前中洗須洗乾淨','前令17RB1025','前令23QA1098','前有放試片','前洗中洗乾淨','前洗勿放水','前洗放脫脂劑','前洗洗乾淨','品保每桶留20支',
        '品保每筆留20支','品保留6支給曾','品保留測後樣品','品保留樣15支','品保留樣20支','品保留樣30支','品保留樣35支','品保留樣3支','品保留樣50支',
        '品保留樣5支','品保留樣60支','品保留樣6支','品保留樣80支','品保留樣品10支','品保留樣品15支','品保檢測12支','品留樣10支','品留樣每船2支',
        '品管每桶留1支','品管留樣10PCS','品管留樣20支','品管留樣30支','品管留樣3支','品管留樣40支','品管留樣50支','品管留樣5支','品管留樣6支',
        '品管留樣品','品管留樣品20支','品管留樣品40支','品管留樣品4支','品管留檢測後樣','品管測淬火硬度','品管請掛紅標籤','品管檢測脫碳層',
        '品樣留樣60支','客:520回火','客:600度/120分','客:HRC26-30','客650°F↑回火','客戶已電鍍過','客戶已熱處理OK','客戶不要求拉力',
        '客戶有附插規','客戶自行電鍍','客戶自行矯直','客戶作NG咬酸過','客戶作紅銹','客戶附4只環規','客戶附牙規','客戶附防銹油','客戶附塞規2支',
        '客戶附試棒','客戶附試棒10支','客戶附模具1只','客戶附環規','客戶附縲絲一段','客戶要450回火','客戶要520回火','客戶要530回火',
        '客戶要620回火','客戶要求水淬','客戶要求扭力','客戶要求滲碳層','客戶要做牙緊','客戶要測心部','客戶做NG','客戶國外電鍍','客戶標簽要撕掉',
        '客戶標櫼隨貨出','客戶標籤勿遺失','客戶彎曲不矯直','客指360/70回','客指扭力490KG','客要求39-42','客彎曲自行矯直','待品管主管檢測',
        '待通知再交貨','待通知再作','待通知在交','待試樣OK再作','後作高週波','後做高週波','後做衝擊測試','後製程搓牙','流程卡勿遺失','相同規格檢1批',
        '紅銹重染黑','要合3A牙規','要求保證荷重','要前洗','要做降伏測試','要篩選放紅刊','重作從08GR1019','重染黑','重盈自調質過','重量磅OK再作',
        '降:441MAP最小','降:760-860MPA','降伏:1080N/mm2','降伏:117(MIN)','降伏:130000PSI','降伏:13500LBS','降伏:14500磅',
        '降伏:153000PSI','降伏:450MPA','降伏:480N/MM2','降伏:490/mm2','降伏:50KG','降伏:640MPA','降伏:706MPA↑','降伏:73kg(MIN)',
        '降伏:760-860MP','降伏:80KG/mm2','降伏:82KSI(MIN','降伏:940Mpa↑','降伏350N/MM2','降伏450MPa↑','降伏500MPA','降伏640N/mm2',
        '降伏72KG/MM2','降伏800N/mm','降伏82.7KN(MIN','降伏92KSI(MIN)','降伏940N/mm2↑','降伏強度159612','降伏強度34.6','降伏點28000ib',
        '降伏點720MPA','降伏點720MPA↑','降伏點80kg/mm2','降伏點95KG/MM2','降伏點強156420','首末件檢查表','原始標籤隨貨出','特急明早結關',
        '特急星期一早交','留牙傷生料2支','留牙傷生料5支','留生料牙傷10支','真直度:0.16mm','真直度0.25mm↓','真直度最大0.50','真直度量測桿徑',
        '退回品','退回品不黑化','高週波,依圖測','做白皮可','做在310以下','做好待通知再送','做至淬火取出','做前請先吊磅','做衝擊測試',
        '做頭部敲擊25度','參考W:HV140min','參考W:HV180min','參考W:HV180Ref','從12IS2081轉23','從19I51005轉出','從1CQ72022取出',
        '從2281028轉出','從46BA2052轉出','控制HRB70','掛紅刊分重量','掛紅刊勿出貨','掛紅刊惕撿','掛紅刊換報紙','掛紅刊暫不出','掛紅標簽分重量',
        '掛紅標籤去油','掛紅標籤淋油','掛紅標籤換報紙','掛紅籤暫不交','斜楔11萬2PSI↑','旋入:2.4N-M(MA','旋入扭力:138kg','旋入扭力:25KG',
        '旋入扭最大44KG','旋入扭最大47.9','旋入測試','旋扭204KG(MAX)','旋扭最大24.4KG','桿徑不足','桶子不可鋪報紙','桶子全面鋪報紙',
        '桶子全面擦乾淨','桶子板子隨桶裝','桶底勿鋪報紙','桶底四周鋪報紙','桶底面蓋10層報','桶底面蓋3層報','桶底面邊蓋厚紙','桶底桶面蓋報紙',
        '桶底桶面鋪報紙','桶底擦乾淨','桶面要蓋報紙','桶面蓋厚紙板','桶面蓋報紙','桶擦乾淨勿鋪報','梅花針孔不同','氫脆121KG/CM↑','氫脆扭24.4KG',
        '氫脆扭44KG-CM','氫脆扭力18.5KG','氫脆扭力44KG','氫脆扭力44KG/C','氫脆扭力86.7','清前中洗以利電','淋到雨','淋雨重作','淬火後HRC47↑',
        '淬火後度RC44','淬火後硬度RC47','淬火後樣品5支','淬火留樣20支','現場留生料20支','現場留生料2只','現場留生料5支','第1-第2船H重回',
        '第4-第5船B重作','第6-10卡爐彎曲','脫碳0.015MM(MA','脫碳料勿混合','脫碳層測1/4"牙','荷24400LBS(MIN','荷重:830N/mm2','荷重15200N↑',
        '荷重35500N(MIN','貨在建揚','貨好請通知自載','貨收完蓋報紙','貨放在圓桶裡','部份已電鍍過','最大負荷1300KG','割溝勿重壓縮孔','剩1圓未作',
        '報告附作業條件','換牙板勿混合','換電桶測脫碳層','換電鍍桶','換電鍍桶.CP0.4','換電鍍桶依圖測','棧板隨貨歸還','測孔徑.勿縮孔.',
        '測牙底HRC42','測四角心部','測扭矩8英鎊↑','測表面下0.05mm','測表面與心部','測桿身','測脫碳層','測試延伸率','測試花齒','測試品留給客戶',
        '測試對邊','測試點0.05mm處','測試點頭部中心','測彎曲度','測灣曲90度','無法重染油退回','無倒角勿混合','無爐號勿混合','硬度.扭力客戶要求',
        '硬度90.7-92.2','硬度HV0.5測','硬度勿超HRC36','硬度太高','硬度作入規範內','硬度作上限','硬度作中限','硬度客戶要求','硬度要到中下限',
        '硬度參考用','硬度測試座面','硬度請在範圍內','硬度請作上限','硬度請做中上限','硬度請控制上限','硬度儘量作下限','等通知再交','華司:SS400',
        '華司1008','華司1010','華司1015','華司1018','華司1035','華司1050','華司1050.1008','華司1050-1065','華司1055','華司1060',
        '華司1060.1008','華司1065','華司1065C','華司1080','華司10B21','華司HRC 38-43','華司HRC 38-45','華司HRC30-40','華司HRC30-51',
        '華司HRC33-40','華司HRC35-40','華司HRC35-45','華司HRC37-43','華司HRC38-45','華司HRC38-48','華司HRC39-43','華司HRC40-48',
        '華司HRC40-50','華司HRC41-47','華司HRC42-46','華司HRC42-48','華司HRC42-50','華司HRC42-52','華司HV 90-220','華司HV160-320',
        '華司HV160-430','華司HV160-450','華司HV180參考','華司HV300(MIN)','華司HV300-390','華司HV360-430','華司HV380-420','華司HV5測試',
        '華司S50C','華司S50C,1008','華司SAPH440','華司不可脆裂','華司不足可出','華司孔徑不同','華司心RC38-44','華司以HV 10測','華司以HV10測',
        '華司以HV5測','華司材質1035','華司材質不同','華司彈簧鋼','裂料分開','量規檢驗真直度','須作曲線圖','須換新磅單','黃色標簽','黑化處理',
        '黑磷酸鹽','焠火後硬度HR47','圓桶勿多收少收','微黑.勿前洗','微滲碳0.05MM','新','新令:42751157','楔拉44600N(MIN','極細牙勿牙傷',
        '溫度只供參考','裝9分滿','裝九分滿','裝八分滿.','試片OK','試片請品管檢查','試作5KG.','達可銹','電鍍不良','電鍍別不同勿混','墊圈組合螺絲',
        '實測值表RC34.4','對邊不一樣勿混','對邊不同.勿混','敲擊90度彎曲測','敲擊不可斷頭','敲擊測試10°↑','敲擊測試10以上','敲擊測試15度',
        '敲擊測試60度','敲擊試驗5度','敲擊彎曲15MIN','滲:HRC52判讀','滲0.23HV450↑','滲0.33HV450↓','滲碳不良','滲碳不足','滲碳太深',
        '滲碳前後測孔徑','滲碳層0.03(MIN','滲碳層以HV450','滲碳層附金相','滲碳層客戶要求','滲碳層客要求','滲碳層做上限','滲碳層做中限',
        '滲碳層務必達到','滲碳層參考用','滲碳層測中心點','滲碳層測牙山','滲碳層測牙底','滲碳層測牙部','滲碳層測花齒底','滲碳層測高低牙',
        '滲碳層測對邊','滲碳層無要求','滲碳層過高','滲碳層過深','滲碳層驗對邊','需作脫碳測試','需附降伏強度','需測保證荷重','彈W:HV350-425',
        '彈簧W:HRC28-48','彈簧W:HRC30-48','彈簧W:HRC38-48','彈簧W:HRC42-50','樣品新新自取','標籤顏色不同','熱浸鋅','熱處理OK',
        '盤W:HRC40-50','盤W:HV420-510','盤華RC40-50','線材徑不同分開','線材徑不同勿混','線材廠不同勿混','線徑不同勿混合','衝擊值8kgf-m/c',
        '衝擊測試20度','請下薄','請分開處理','請以HRC測試','請出英式報告','請用人工收料','請用人工排收','請用原桶裝回','請用排勿撞傷','請先放試片',
        '請作1支鑲埋','請作襄埋2支','請作鑲埋試驗','請放試片5支','請品管測孔徑','請品管測脫碳層','請品管測彎曲度','請原桶裝回','請核對材質規格',
        '請提供6PCS樣品','請款2次','請測孔徑','請測表面硬度','請測華司硬度','請填上回火溫度','鋪海綿墊勿碰撞','橫式拉力14500k','橫拉:14500kg↑',
        '辦公室','選裂料嚴重8只','鋸料測試1支','頭外徑過大','頭型不同勿混合','頭記不一樣勿混','頭記不同勿混合','頭部16邊','頭部18邊',
        '頭部不同勿混合','頭部作25度敲擊','頭部做20度彎曲','頭部做25度試驗','頭部硬度偏高','頭部較不明顯','頭部對邊不同','頭部敲擊:12度',
        '頭部敲擊10度','頭部敲擊10度牙','頭部敲擊15度','頭部敲擊15度牙','頭部敲擊25度','頭部敲擊30度↑','頭部敲擊45度','頭部敲擊5度',
        '頭部敲擊60。','頭部敲擊60度','頭部敲擊7度↑','頭部敲擊80度','頭部敲擊勿斷裂','頭部彎曲測試','壓扁不可裂頭','壓紙做記號','壓齒時斷裂',
        '應力消除→滲碳','應力消除→調質','檢附淬火樣4支','檢測頭部硬度','矯直OK測20支','矯直彎曲°1.4m','磷酸鹽','縮小率50%(MIN)','螺絲勿遺失',
        '螺絲勿檢測','螺絲心部作上限','螺絲功能不考慮','螺絲無要求硬度','螺絲硬度作上限','螺絲硬度做下限','螺絲請勿切勿少','避免螺絲骯髒',
        '斷面收縮:50%↑','斷面積:20.1(NO','斷面積50%(MIN)','斷面縮率:48%','斷面縮率35%','斷面縮率40%','斷面縮率40MIN','斷面縮率40以上',
        '斷面縮率45%','斷面縮率50%↑','斷面縮減率40％','斷頭.退回品','斷縮率36%(min)','斷縮率48%最小','舊令:09SS1006','舊令:3A8A1001',
        '舊令:42751024','轉H','轉H回火','轉H爐染黑','轉H爐烘乾','鎖緊扭力:900','鎖緊扭力900kgf','顏色盡量偏藍色','爐號相混','鐵片材質S45C',
        '鐵亨倉庫','彎曲:0.3mm(MAX','彎曲:5度楔型塊','彎曲不矯直','彎曲度:A,B級','彎曲度0.28(MAX','彎曲度0.36最大','彎曲度0.40MM',
        '彎曲度0.40最大','彎曲度15MIN','彎曲度15度','彎曲度30度MIN','彎曲度80度以上','彎曲度B級','彎曲度問穎翊','彎曲測試:5度','彎曲測試30度↑',
        '彎曲測試7°MIN','彎曲測試在牙部','彎曲試驗','彎曲試驗:30度','彎曲敲擊15度','彎敲15°以上','彎敲90°不可斷','驗12支附鑲埋','鑲埋4支',
        '鑲埋用HRC測','鑲埋測頭部0.05'
];
    $("input[name='notices1'],[name='notices2'],[name='notices3'],[name='qcnote1'],[name='qcnote2'],[name='qcnote3'],[name='prodnote1'],[name='prodnote2'],[name='prodnote3']").autocomplete({
        source:tags
    });
});
*/