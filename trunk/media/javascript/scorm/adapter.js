var debug = false;
//show that the SCORM Adapter is here
var API = this;	

/*
* TODO:gs:a try to replace with prototype.js ajax stuff which works for most browsers
* right now only used for moz, as ie has some problems with state handler
* room for improvement by makeing it into one function that works for both
*/
function scormApiRequest(remoteUrl)
{
		this.remoteOLATurl = remoteUrl;
		this.isMozilla = false;
		this.httpReq=false;
		
		this.reqCount = 0;
		
		this.sendSyncSingle	= asSendSyncSingle;
		if (window.XMLHttpRequest)
		{
			this.httpReq = new XMLHttpRequest();
			this.isMozilla = true;
			if (debug) dump("func:scormApiRequest :is Mozilla\n");
		}
		// code for IE
		else if (window.ActiveXObject)
		{
			try {
				this.httpReq = new ActiveXObject("Msxml2.XMLHTTP");
				if (debug) dump("func:scormApiRequest :is new IE \n");
			} catch (e) {
				try {
					this.httpReq = new ActiveXObject("Microsoft.XMLHTTP");
					if (debug) dump("func:scormApiRequest :is old IE \n");
				} catch (E) {
					this.httpReq = false;
				}
			}
		}
}

function asSendSyncSingle(apiCall, param1, param2) {
	// Sync - wait until data arrives
	//IE does not like this function, what's it for?
	//httpReq.multipart	= false;

	// Mozilla/Firefox bug 246518 workaround
	// a new XMLHttpRequest object if needed
	try {
		this.httpReq.onload = showReq;
		this.httpReq.onreadystatechange = showReq;
		this.httpReq.open('POST', this.remoteOLATurl, false );
	} catch (e) {
		this.httpReq = new XMLHttpRequest();
		this.httpReq.onload = showReq;
		this.httpReq.onreadystatechange = showReq;
		this.httpReq.open('POST', this.remoteOLATurl, false );
	  }

	this.httpReq.setRequestHeader('Content-Type','application/x-www-form-urlencoded'); 
	this.httpReq.send('apiCall='+ apiCall + '&apiCallParamOne='+ param1 + '&apiCallParamTwo='+ param2);
	if(this.isMozilla)
	{
		if (debug) dump("func:asSencSingle: post successfull, calling showReq\n");
		
		//add event listener geht auch! ev. besser?
		//httpReq.addEventListener("load", showReq, false)
		//this.httpReq.onload = showReq;
		//this.httpReq.onreadystatechange = showReq;
	} else {
		if (debug) dump("func:asSencSingle: post successfull by this.httpReq, calling showReq\n");
		//this.httpReq.onload = showReq;
		//this.httpReq.onreadystatechange = showReq;
	}
	//httpReq.send(null);
}


function showReq( event ) {
	if (debug) dump("func:showReq: inside func.: event type: " +event.type+"\n");
	// ready state 4 means document loaded
	//if ( event.target.readyState == 4 ) 
	if ( this.readyState == 4 ) 
	{
		bMsg = document.getElementById( 'apiReturnHandler' );
		//bMsg.innerHTML = event.target.responseText;
		bMsg.innerHTML = this.responseText;
		if (debug) dump("func:showReq: "+this.responseText+"\n");
	} else { dump( 'an error occured! Wrong readyState: ' + event.target.readyState +"\n"); }
}
	
	
/*************************************/

// global flag
var isIE = false;

// global request and XML document objects
var req;
var scormRTEresponse;

// retrieve XML document (reusable generic function);
function loadHTMLDoc(url,apiCall, param1, param2) {
    // branch for native XMLHttpRequest object
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
		req.onreadystatechange = processReqChange;
        //req.open("GET", url+'?apiCall='+ apiCall + '&apiCallParamOne='+ param1 + '&apiCallParamTwo='+ param2, false);
        req.open("POST", url, false)
        req.setRequestHeader('Content-Type','application/x-www-form-urlencoded'); 
        req.send('apiCall='+ apiCall + '&apiCallParamOne='+ param1 + '&apiCallParamTwo='+ param2);
    // branch for IE/Windows ActiveX version
    } else if (window.ActiveXObject) {
        isIE = true;
        req = new ActiveXObject("Microsoft.XMLHTTP");
        if (req) {
            req.onreadystatechange = processReqChange;
            //req.open("GET", url+'?apiCall='+ apiCall + '&apiCallParamOne='+ param1 + '&apiCallParamTwo='+ param2 + '&rnd='+increment(), false);
            //req.send();
            req.open("POST", url, false);
        	req.setRequestHeader('Content-Type','application/x-www-form-urlencoded'); 
        	req.send('apiCall='+ apiCall + '&apiCallParamOne='+ param1 + '&apiCallParamTwo='+ param2);
        }
    }
}

// handle onreadystatechange event of req object
function processReqChange(event){	
	// only if req shows "loaded"
	if (req.readyState == 4) {
		// only if "OK"
		if (req.status == 200) {
			rteResponseText = req.responseText;
			scormRTEresponse = rteResponseText.substring(rteResponseText.indexOf("<p>")+3,rteResponseText.indexOf("</p>")); 
			//dump(scormRTEresponse);
		} else { dump("There was a problem retrieving the XMLHttpRequest data:\n"+ req.statusText+"\n"); }
	}
}
/*****************************************************************
* function to produce incremental ints
* to cheat ie chache
******************************************************************/
var counter = 0;
function increment(){
	return counter++;
}


/******************************************************************
* passes the scorm api calls to the backend
* over a synchronous XmlHttpRequest.
* Code uses different ways for moz and ie.
*******************************************************************/
function passApiCall(apiCall, param1, param2){
	if(window.ActiveXObject || (navigator.userAgent.indexOf("Safari") != -1)){
		loadHTMLDoc(olatCommandUri,apiCall,param1,param2);
		return scormRTEresponse;
	}else if(window.XMLHttpRequest && (navigator.userAgent.indexOf("Mozilla") != -1)){
		jsHttpRequest.sendSyncSingle(apiCall,param1, param2);
		var responseHTML = document.getElementById( 'apiReturnHandler' ).innerHTML;
		return responseHTML.substring(responseHTML.indexOf("<p>")+3,responseHTML.indexOf("</p>"));
	}else{
		dump("Browser does not support the needed XmlHttpRequest\n");
	}
}


/**
* triggers the onunload stuff often used in scorm content to finish an sco by
* opening the iframe document for writing (IE) or replacing the content doc (Mozilla).
*/
function olatonunload(){
	if (debug) dump("func:olatonunload: is called\n");
	if(window.frameId && document.getElementById(frameId) && this.frames[frameId]){
		if(window.ActiveXObject){
			//on IE by opening the document, the onunload event gets triggered
			var iframeDoc = this.frames[frameId].document;
			iframeDoc.open();
			iframeDoc.write("<html><body></body></html>");
			iframeDoc.close();
		} else {
			// Mozilla and others
			var iframeDoc = document.getElementById(frameId).contentDocument;
			iframeDoc.location.replace("about:blank");
			//delay(200);
			//if((new Date().getTime() - lastRequest) > 60000) alert("Current SCO will be finised befor initializing next SCO or terminating! Press OK to proceed.");
			
			var delayReq = new XMLHttpRequest();
			//"false" waits until the result arrived;
			delayReq.open('GET', olatCommandUri, false );
			delayReq.send(null);
		}
	}
	return true;
}
function delay(gap){
	var then,now; then=new Date().getTime();
	now=then;
	while((now-then)<gap)
	{now=new Date().getTime();}
}

/******************************************************************
* SCORM API FUNCTIONS 
* These functions are used in the SCORM content to
* communicate with the LMS.
*******************************************************************/
function doLMSInitialize (s) {
	return true;
}
var v = "";
function doLMSSetValue (l, r) {
	v=l;
}
function doLMSGetValue (s) {
	return v;
}
function doLMSCommit (s) {
	return true;
}
function doLMSFinish () {
	return true;
}

function LMSInitialize (s) {
	return passApiCall('LMSInitialize',s,'');
}
function LMSFinish (s) {
	return passApiCall('LMSFinish',s,'');
}
function LMSSetValue (l, r) {
	return passApiCall('LMSSetValue',l,r);
}
function LMSGetValue (s) {
	return passApiCall('LMSGetValue',s,'');
}
function LMSGetLastError () {
	return passApiCall('LMSGetLastError','','');
}
function LMSGetErrorString (s) {
	return passApiCall('LMSGetErrorString',s,'');
}
function LMSGetDiagnostic (s) {
	return passApiCall('LMSGetDiagnostic',s,'');
}
function LMSCommit (s) {
	return passApiCall('LMSCommit',s,'');
}