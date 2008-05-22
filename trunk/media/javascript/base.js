var nLeftWidth        = 220;
var nLeftManageWidth  =  20;
var nRightWidth       = 190;
var c = null;

function startHighlight (id) {
  obj=eval(document.getElementById(id));
  c = obj.style.backgroundColor;
  obj.style.backgroundColor = '#203090';
  obj.style.color = '#ffffff';
}
function stopHighlight (id) {
  obj=eval(document.getElementById(id));
  //obj.style.backgroundColor = '#ffffff';
  obj.style.backgroundColor = c;
  obj.style.color = '#203090';
}

function show_actions(item,header) {
 document.getElementById(item).style.visibility = "visible";
 document.getElementById(header).style.visibility = "hidden";
}
function hide_actions(item,header) {
 document.getElementById(item).style.visibility = "hidden";
 document.getElementById(header).style.visibility = "visible";
}

function showHelp ( rDomain, rUrl ) {
  nWidth = 500
  nLeft  = screen.width - nWidth;
  cParam = "top=0,toolbar=yes,menubar=yes,scrollbars=yes,"
  winHelp = window.open(rDomain+rUrl,
            "_help",
            "width="+String(nWidth)+",height=600,left="+String(nLeft)+","+cParam);
  winHelp.focus();
}
function showTour () {
  nWidth = 450;
  nLeft  = screen.width - nWidth;
  winTour = window.open("tour/",
            "_tour",
            "width="+String(nWidth)+",height=500,left="+String(nLeft)+",top=0,toolbar=yes,menubar=yes,scrollbars=yes,"
            );
  winTour.focus();
}
