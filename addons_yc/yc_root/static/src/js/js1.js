var unescapeHTML = function unescapeHTML(escapedHTML) {
return escapedHTML.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');
                    };


export {unescapeHTML};