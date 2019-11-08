// check-box value decide background-color.
                            $(document).on('click', "div[name='in_out']", function(event){
                                var v = $("div[name='in_out'] div input:checked").attr('data-value');
                                if (v =='O') {
                                    bg.css("background-color","#adff2f");
                                }
                                else if(v =='I') {
                                    bg.css("background-color","#ffc0cb");
                                }
                            });
