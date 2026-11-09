
from flask import Flask, jsonify, render_template_string, request
import json
import urllib.request
import urllib.error
import socket
import os

app = Flask(__name__)

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")
MODEL_NAME = os.environ.get("MODEL_NAME", "qwen2.5:3b")

DASHBOARD_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VEXOR NX | AI Intelligence</title>

<script src="https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js"></script>

<style>
:root {
 --bg:#070811;
 --panel:#13162a;
 --border:#34345c;
 --purple:#9b72ff;
 --cyan:#35e5f2;
 --muted:#9297b4;
 --white:#f4f3ff;
}
*{box-sizing:border-box}
body{
 margin:0;color:var(--white);
 background:
 radial-gradient(ellipse at 15% 0%,#292052,transparent 35%),
 radial-gradient(ellipse at 90% 20%,#092d3c,transparent 30%),
 var(--bg);
 font-family:Segoe UI,Arial,sans-serif;
 min-height:100vh;
}
header{
 display:flex;align-items:center;justify-content:space-between;
 padding:18px 5%;border-bottom:1px solid var(--border);
 background:#080914ee;position:sticky;top:0;z-index:5;
}
.brand{display:flex;align-items:center;gap:13px}
.logo{
 width:45px;height:45px;border-radius:14px;
 display:grid;place-items:center;font-size:25px;font-weight:bold;
 background:linear-gradient(135deg,#8d5cff,#22d8e8);
}
.brand h1{margin:0;font-size:22px;letter-spacing:3px}
.brand small{color:var(--muted);letter-spacing:2px;font-size:10px}
.topstatus{color:#7fffc7;font-size:12px}
main{width:min(1450px,94%);margin:25px auto 50px}
.hero{text-align:center;padding:25px 10px 30px}
.eyebrow{color:var(--cyan);letter-spacing:4px;font-size:11px}
.hero h2{font-size:clamp(30px,5vw,50px);margin:12px 0}
.gradient{
 background:linear-gradient(90deg,#a77bff,#42e6f0);
 -webkit-background-clip:text;background-clip:text;color:transparent;
}
.muted{color:var(--muted);font-size:12px}
.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:17px}
.panel{
 background:#13162ae8;border:1px solid var(--border);
 border-radius:20px;padding:21px;min-width:0;
 box-shadow:0 12px 40px #0005;
}
.panel h3{font-size:15px;letter-spacing:1px;margin:0 0 15px}
.panel h3 span{color:var(--cyan)}
.core-panel{grid-column:span 4;text-align:center;min-height:300px}
.ai-panel{grid-column:span 8}
.gesture-panel,.pdf-panel,.phone-panel,.system-panel{grid-column:span 6}
.core{
 width:150px;height:150px;margin:25px auto;
 border-radius:50%;display:grid;place-items:center;
 font-size:45px;font-weight:bold;
 border:2px solid var(--purple);
 background:radial-gradient(circle,#34266c,#11142b 65%);
 box-shadow:0 0 30px #9165ff88,inset 0 0 25px #35e5f244;
 animation:pulse 3s infinite ease-in-out;
}
@keyframes pulse{
 50%{transform:scale(1.04);box-shadow:0 0 45px #35e5f288}
}
.status{color:var(--cyan);font-size:13px}
button,.upload{
 border:1px solid #8065d9;border-radius:11px;color:white;
 background:linear-gradient(120deg,#6745ba,#273d70);
 padding:11px 15px;cursor:pointer;font-weight:600;
 display:inline-block;font-size:12px;
}
button:hover,.upload:hover{box-shadow:0 0 18px #8b68ff66}
button.secondary{background:#151a30;border-color:#39435f}
button:disabled{opacity:.5;cursor:not-allowed}
.controls{display:flex;flex-wrap:wrap;gap:9px;margin-top:13px}
textarea{
 width:100%;min-height:70px;resize:vertical;
 background:#090d1c;border:1px solid #343653;
 color:white;border-radius:10px;padding:12px;outline:none;
}
.reply{
 background:#0b1022;border:1px solid #292d4d;
 border-radius:12px;padding:14px;min-height:75px;
 margin:12px 0;color:#d8d9ed;font-size:13px;
 line-height:1.6;white-space:pre-wrap;overflow-wrap:anywhere;
}
.chat-tools{
 display:flex;justify-content:space-between;
 align-items:center;gap:10px;flex-wrap:wrap;
}
#aiStatus{color:var(--cyan)}
#gestureVideo{display:none}
.camera-wrap{
 width:100%;min-height:190px;background:#080b17;
 border:1px solid #303452;border-radius:13px;overflow:hidden;
 position:relative;
}
#gestureCanvas{width:100%;display:block}
.camera-placeholder{
 position:absolute;inset:0;display:grid;
 place-items:center;color:var(--muted);font-size:13px;
}
#gestureName{color:var(--cyan);font-size:14px;margin-top:12px}
.pdf-info{
 display:flex;justify-content:space-between;
 gap:10px;color:var(--muted);font-size:12px;margin:12px 0;
}
#pdfCanvas{
 width:100%;max-height:390px;object-fit:contain;
 background:white;border-radius:8px;display:none;
}
.small-stat{
 display:flex;justify-content:space-between;
 padding:12px 0;border-bottom:1px solid #292d46;font-size:13px;
}
.value{color:var(--cyan)}
footer{text-align:center;color:#666c89;font-size:11px;padding:25px}
@media(max-width:850px){
 .core-panel,.ai-panel,.gesture-panel,.pdf-panel,
 .phone-panel,.system-panel{grid-column:span 12}
 header{padding:14px 4%}
}
</style>
</head>

<body>
<header>
 <div class="brand">
  <div class="logo">V</div>
  <div>
   <h1>VEXOR <span class="gradient">NX</span></h1>
   <small>INTELLIGENCE WORKSPACE</small>
  </div>
 </div>
 <div class="topstatus"><a href="/" style="color:inherit;text-decoration:none">← OFFICIAL WEBSITE</a> &nbsp; · &nbsp; ● DASHBOARD</div>
</header>

<main>
<section class="hero">
 <div class="eyebrow">NEXT GENERATION INTELLIGENCE</div>
 <h2>WELCOME TO <span class="gradient">VEXOR NX</span></h2>
 <p class="muted">Your personal laptop-and-phone intelligence workspace.</p>
</section>

<section class="grid">

<div class="panel core-panel">
 <h3><span>01 /</span> VEXOR CORE</h3>
 <div class="core">V</div>
 <div class="status" id="coreStatus">CORE READY</div>
 <p class="muted">VOICE • VISION • LOCAL AI</p>
</div>

<div class="panel ai-panel">
 <h3><span>02 /</span> INTELLIGENT AI ASSISTANT</h3>
 <p class="muted">Powered by your local Qwen 2.5 3B model.</p>

 <div class="reply" id="assistantReply">
 VEXOR NX is online. How can I help you?
 </div>

 <textarea id="commandInput"
 placeholder="Ask VEXOR NX anything..."></textarea>

 <div class="controls">
  <button id="sendCommand">SEND MESSAGE</button>
  <button id="micButton" class="secondary">🎙 START VOICE</button>
  <button id="stopSpeech" class="secondary">STOP SPEAKING</button>
  <button id="clearChat" class="secondary">CLEAR CHAT</button>
 </div>

 <div class="chat-tools">
  <p class="muted" id="voiceStatus">Voice assistant ready.</p>
  <p class="muted" id="aiStatus">Checking local AI...</p>
 </div>
</div>

<div class="panel gesture-panel">
 <h3><span>03 /</span> GESTURE RECOGNITION</h3>
 <p class="muted">Control your PDF reader using your hand.</p>

 <video id="gestureVideo" playsinline></video>

 <div class="camera-wrap">
  <canvas id="gestureCanvas"></canvas>
  <div class="camera-placeholder" id="cameraPlaceholder">
   CAMERA IS OFF
  </div>
 </div>

 <div id="gestureName">Gesture: Waiting</div>
 <p class="muted">
  ✌ Next page · ✊ Previous page · ✋ Read page
 </p>

 <div class="controls">
  <button id="startCamera">START CAMERA</button>
  <button id="stopCamera" class="secondary">STOP CAMERA</button>
 </div>
</div>

<div class="panel pdf-panel">
 <h3><span>04 /</span> SMART PDF READER</h3>
 <p class="muted">Select a PDF from your laptop.</p>

 <label class="upload">
  SELECT PDF
  <input id="pdfInput" type="file" accept="application/pdf" hidden>
 </label>

 <div class="pdf-info">
  <span id="pdfName">No PDF selected</span>
  <span id="pageInfo">Page 0 / 0</span>
 </div>

 <canvas id="pdfCanvas"></canvas>

 <div class="controls">
  <button id="prevPage" class="secondary">← PREVIOUS</button>
  <button id="nextPage">NEXT →</button>
  <button id="readPage" class="secondary">🔊 READ PAGE</button>
  <button id="stopReading" class="secondary">STOP READING</button>
 </div>

 <p class="muted" id="pdfStatus">PDF reader ready.</p>
</div>

<div class="panel phone-panel">
 <h3><span>05 /</span> PHONE CONNECTION</h3>
 <p class="muted">
  Connect your phone and laptop to the same Wi-Fi network.
 </p>
 <div class="reply" id="phoneStatus">
  Connection has not been tested.
 </div>
 <div class="controls">
  <button id="checkPhone">CHECK SERVER</button>
 </div>
</div>

<div class="panel system-panel">
 <h3><span>06 /</span> SYSTEM MONITOR</h3>

 <div class="small-stat">
  <span>Dashboard</span><span class="value">VEXOR NX</span>
 </div>
 <div class="small-stat">
  <span>Flask Server</span><span class="value" id="serverState">CHECKING</span>
 </div>
 <div class="small-stat">
  <span>Local AI</span><span class="value" id="modelState">CHECKING</span>
 </div>
 <div class="small-stat">
  <span>Camera</span><span class="value" id="cameraState">OFF</span>
 </div>
 <div class="small-stat">
  <span>PDF Reader</span><span class="value" id="pdfState">READY</span>
 </div>
 <div class="small-stat">
  <span>Voice</span><span class="value" id="voiceState">READY</span>
 </div>
</div>

</section>
</main>

<footer>VEXOR NX · PERSONAL INTELLIGENCE WORKSPACE · HEAD FOUNDER: NITISH KUMAR</footer>

<script>
/* =========================================
   SERVER AND AI STATUS
========================================= */

async function checkServer(){
 try{
  const r=await fetch('/api/ping');
  const d=await r.json();

  document.getElementById('serverState').textContent='ONLINE';
  document.getElementById('phoneStatus').textContent='✓ '+d.message;
 }catch(e){
  document.getElementById('serverState').textContent='OFFLINE';
  document.getElementById('phoneStatus').textContent='Server unavailable.';
 }
}

async function checkAI(){
 try{
  const r=await fetch('/api/health');
  const d=await r.json();

  document.getElementById('modelState').textContent=
   d.model_available?'ONLINE':(d.ollama?'MODEL MISSING':'OFFLINE');

  document.getElementById('aiStatus').textContent=
   d.model_available?'Qwen 2.5 3B is ready.':
   (d.ollama?'Ollama is running, but the model is missing.':'Start Ollama first.');
 }catch(e){
  document.getElementById('modelState').textContent='OFFLINE';
  document.getElementById('aiStatus').textContent='Could not connect to Ollama.';
 }
}

document.getElementById('checkPhone').onclick=checkServer;
checkServer();
checkAI();

/* =========================================
   SPEECH OUTPUT
========================================= */

function speak(text){
 if(!('speechSynthesis' in window)) return;

 speechSynthesis.cancel();

 const u=new SpeechSynthesisUtterance(text);
 u.lang='en-IN';
 u.rate=1;

 speechSynthesis.speak(u);
}

/* =========================================
   VEXOR LOCAL AI
========================================= */

let aiHistory=[];
let waitingForAI=false;

async function askVexorAI(message){

 if(waitingForAI) return;

 waitingForAI=true;

 const reply=document.getElementById('assistantReply');
 const status=document.getElementById('voiceStatus');
 const send=document.getElementById('sendCommand');

 aiHistory.push({role:'user',content:message});

 reply.textContent='VEXOR NX is thinking...';
 status.textContent='Connecting to local intelligence...';
 send.disabled=true;

 try{

  const response=await fetch('/api/chat',{
   method:'POST',
   headers:{'Content-Type':'application/json'},
   body:JSON.stringify({
    messages:aiHistory.slice(-12)
   })
  });

  const data=await response.json();

  if(!response.ok){
   throw new Error(data.error||'AI request failed.');
  }

  aiHistory.push({
   role:'assistant',
   content:data.reply
  });

  aiHistory=aiHistory.slice(-12);

  reply.textContent=data.reply;
  status.textContent='VEXOR NX AI ONLINE';

  document.getElementById('coreStatus').textContent='AI ACTIVE';

  speak(data.reply);

 }catch(error){

  aiHistory.pop();

  reply.textContent='AI ERROR: '+error.message;
  status.textContent='AI CONNECTION ERROR';

 }finally{

  waitingForAI=false;
  send.disabled=false;

 }
}

function sendMessage(){

 const input=document.getElementById('commandInput');
 const message=input.value.trim();

 if(!message||waitingForAI) return;

 input.value='';
 askVexorAI(message);

}

document.getElementById('sendCommand').onclick=sendMessage;

document.getElementById('commandInput').addEventListener('keydown',e=>{
 if(e.key==='Enter'&&!e.shiftKey){
  e.preventDefault();
  sendMessage();
 }
});

document.getElementById('clearChat').onclick=()=>{
 aiHistory=[];
 document.getElementById('assistantReply').textContent=
  'Conversation cleared. VEXOR NX is ready.';
 speechSynthesis.cancel();
};

/* =========================================
   VOICE INPUT
========================================= */

let recognition=null;

const SpeechRecognition=
 window.SpeechRecognition||window.webkitSpeechRecognition;

if(SpeechRecognition){

 recognition=new SpeechRecognition();
 recognition.lang='en-IN';
 recognition.continuous=false;
 recognition.interimResults=false;

 recognition.onstart=()=>{
  document.getElementById('voiceStatus').textContent='Listening...';
  document.getElementById('voiceState').textContent='LISTENING';
 };

 recognition.onresult=event=>{
  document.getElementById('commandInput').value=
   event.results[0][0].transcript;
  sendMessage();
 };

 recognition.onerror=event=>{
  document.getElementById('voiceStatus').textContent=
   'Voice error: '+event.error;
 };

 recognition.onend=()=>{
  document.getElementById('voiceState').textContent='READY';
 };

}else{

 document.getElementById('voiceStatus').textContent=
  'Voice input unavailable. Use Chrome.';

}

document.getElementById('micButton').onclick=()=>{
 if(recognition){
  try{recognition.start();}
  catch(e){
   document.getElementById('voiceStatus').textContent=
    'Voice recognition is already active.';
  }
 }
};

document.getElementById('stopSpeech').onclick=()=>{
 speechSynthesis.cancel();
 document.getElementById('voiceStatus').textContent='Speech stopped.';
};

/* =========================================
   PDF READER
========================================= */

if(window.pdfjsLib){
 pdfjsLib.GlobalWorkerOptions.workerSrc=
 'https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js';
}

let pdfDocument=null;
let currentPage=1;

const pdfCanvas=document.getElementById('pdfCanvas');
const pdfContext=pdfCanvas.getContext('2d');

document.getElementById('pdfInput').onchange=async event=>{

 const file=event.target.files[0];

 if(!file) return;

 try{

  if(!window.pdfjsLib){
   throw new Error('PDF library unavailable. Refresh the page.');
  }

  pdfDocument=await pdfjsLib.getDocument({
   data:await file.arrayBuffer()
  }).promise;

  currentPage=1;

  document.getElementById('pdfName').textContent=file.name;
  document.getElementById('pdfState').textContent='LOADED';

  pdfCanvas.style.display='block';

  await renderPage();

  document.getElementById('pdfStatus').textContent=
   'PDF loaded successfully.';

 }catch(error){

  document.getElementById('pdfStatus').textContent=
   'PDF error: '+error.message;

 }

};

async function renderPage(){

 if(!pdfDocument) return;

 const page=await pdfDocument.getPage(currentPage);

 const viewport=page.getViewport({scale:1.35});

 pdfCanvas.width=viewport.width;
 pdfCanvas.height=viewport.height;

 await page.render({
  canvasContext:pdfContext,
  viewport:viewport
 }).promise;

 document.getElementById('pageInfo').textContent=
  'Page '+currentPage+' / '+pdfDocument.numPages;

}

async function changePage(direction){

 if(!pdfDocument){
  document.getElementById('pdfStatus').textContent=
   'Select a PDF first.';
  return;
 }

 const target=currentPage+direction;

 if(target<1||target>pdfDocument.numPages) return;

 currentPage=target;
 await renderPage();

}

document.getElementById('prevPage').onclick=()=>changePage(-1);
document.getElementById('nextPage').onclick=()=>changePage(1);

async function readCurrentPage(){

 if(!pdfDocument){
  document.getElementById('pdfStatus').textContent=
   'Select a PDF first.';
  return;
 }

 try{

  const page=await pdfDocument.getPage(currentPage);
  const content=await page.getTextContent();

  const text=content.items.map(item=>item.str).join(' ');

  if(!text.trim()){
   document.getElementById('pdfStatus').textContent=
    'No selectable text found on this page.';
   return;
  }

  speak(text);

  document.getElementById('pdfStatus').textContent=
   'Reading page '+currentPage+'.';

 }catch(error){

  document.getElementById('pdfStatus').textContent=
   'Could not read this page.';

 }

}

document.getElementById('readPage').onclick=readCurrentPage;

document.getElementById('stopReading').onclick=()=>{
 speechSynthesis.cancel();
 document.getElementById('pdfStatus').textContent='Reading stopped.';
};

/* =========================================
   HAND GESTURE RECOGNITION
========================================= */

const video=document.getElementById('gestureVideo');
const canvas=document.getElementById('gestureCanvas');
const ctx=canvas.getContext('2d');

let hands=null;
let camera=null;
let cameraRunning=false;
let lastGestureAction=0;

function fingerExtended(lm,tip,pip){
 return lm[tip].y<lm[pip].y;
}

function identifyGesture(lm){

 const index=fingerExtended(lm,8,6);
 const middle=fingerExtended(lm,12,10);
 const ring=fingerExtended(lm,16,14);
 const pinky=fingerExtended(lm,20,18);

 const count=[index,middle,ring,pinky].filter(Boolean).length;
 const thumbUp=lm[4].y<lm[3].y;

 if(count===4) return 'OPEN PALM';

 if(index&&middle&&!ring&&!pinky) return 'VICTORY';

 if(count===0&&thumbUp) return 'THUMB UP';

 if(count===0) return 'FIST';

 if(index&&!middle&&!ring&&!pinky) return 'POINTING';

 if(index&&middle&&ring&&!pinky) return 'THREE FINGERS';

 return 'HAND DETECTED';

}

function performGestureAction(name){

 const now=Date.now();

 if(now-lastGestureAction<1800) return;

 if(name==='VICTORY'){

  lastGestureAction=now;
  changePage(1);

  document.getElementById('gestureName').textContent=
   'VICTORY — Next page';

 }else if(name==='FIST'){

  lastGestureAction=now;
  changePage(-1);

  document.getElementById('gestureName').textContent=
   'FIST — Previous page';

 }else if(name==='OPEN PALM'){

  lastGestureAction=now;
  readCurrentPage();

  document.getElementById('gestureName').textContent=
   'OPEN PALM — Read page';

 }

}

function onHandResults(results){

 if(!cameraRunning) return;

 const width=video.videoWidth||640;
 const height=video.videoHeight||480;

 canvas.width=width;
 canvas.height=height;

 ctx.save();
 ctx.clearRect(0,0,width,height);

 ctx.translate(width,0);
 ctx.scale(-1,1);

 ctx.drawImage(results.image,0,0,width,height);

 let detected='No hand detected';

 if(results.multiHandLandmarks&&results.multiHandLandmarks.length){

  for(const lm of results.multiHandLandmarks){

   drawConnectors(
    ctx,lm,HAND_CONNECTIONS,
    {color:'#35e5f2',lineWidth:4}
   );

   drawLandmarks(
    ctx,lm,
    {color:'#ff4fd8',lineWidth:2,radius:4}
   );

   detected=identifyGesture(lm);
   performGestureAction(detected);

  }

 }

 ctx.restore();

 if(detected==='No hand detected'){

  document.getElementById('gestureName').textContent=
   'Gesture: Waiting';

 }else if(!['VICTORY','FIST','OPEN PALM'].includes(detected)){

  document.getElementById('gestureName').textContent=
   'Gesture: '+detected;

 }

}

async function startGestureCamera(){

 if(cameraRunning){
  document.getElementById('gestureName').textContent=
   'Camera is already running.';
  return;
 }

 try{

  if(!navigator.mediaDevices||
     !navigator.mediaDevices.getUserMedia){
   throw new Error('Open the dashboard using localhost.');
  }

  if(!window.Hands||!window.Camera){
   throw new Error('Gesture libraries did not load. Check internet.');
  }

  hands=new Hands({
   locateFile:file=>
    'https://cdn.jsdelivr.net/npm/@mediapipe/hands/'+file
  });

  hands.setOptions({
   maxNumHands:1,
   modelComplexity:1,
   minDetectionConfidence:0.65,
   minTrackingConfidence:0.6
  });

  hands.onResults(onHandResults);

  camera=new Camera(video,{
   onFrame:async()=>{
    if(hands&&cameraRunning){
     await hands.send({image:video});
    }
   },
   width:640,
   height:480
  });

  cameraRunning=true;

  await camera.start();

  document.getElementById('cameraPlaceholder').style.display='none';
  document.getElementById('cameraState').textContent='ON';
  document.getElementById('coreStatus').textContent='VISION ACTIVE';
  document.getElementById('gestureName').textContent=
   'Gesture: Show your hand';

 }catch(error){

  cameraRunning=false;

  document.getElementById('gestureName').textContent=
   'Camera error: '+error.message;

  document.getElementById('cameraState').textContent='OFF';

 }

}

function stopGestureCamera(){

 cameraRunning=false;

 if(camera){
  camera.stop();
  camera=null;
 }

 if(video.srcObject){
  video.srcObject.getTracks().forEach(track=>track.stop());
  video.srcObject=null;
 }

 if(hands){
  hands.close();
  hands=null;
 }

 ctx.clearRect(0,0,canvas.width,canvas.height);

 document.getElementById('cameraPlaceholder').style.display='grid';
 document.getElementById('cameraState').textContent='OFF';
 document.getElementById('coreStatus').textContent='CORE READY';
 document.getElementById('gestureName').textContent=
  'Gesture: Camera stopped';

}

document.getElementById('startCamera').onclick=startGestureCamera;
document.getElementById('stopCamera').onclick=stopGestureCamera;

window.addEventListener('beforeunload',stopGestureCamera);

</script>
</body>
</html>
"""


HOME_HTML = r"""
<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#080b18">
<meta name="description" content="VEXOR NX — an experimental AI workspace combining an assistant, voice, computer vision and document tools.">
<title>VEXOR NX | Intelligence Beyond Limits</title>
<style>
:root{--bg:#070a14;--panel:#10182b;--line:#263653;--cyan:#42e8f5;--violet:#9b78ff;--muted:#a5b2ca;--white:#f4f7ff}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(ellipse at 12% 0%,#25204d 0,transparent 36%),radial-gradient(ellipse at 90% 18%,#073344 0,transparent 30%),var(--bg);color:var(--white);font-family:Inter,Segoe UI,Arial,sans-serif;min-height:100vh}
a{color:inherit;text-decoration:none}.wrap{width:min(1120px,92%);margin:auto}.nav{height:76px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #ffffff18}.brand{display:flex;align-items:center;gap:12px;font-weight:900;letter-spacing:3px}.mark{width:40px;height:40px;border-radius:13px;display:grid;place-items:center;background:linear-gradient(135deg,var(--violet),var(--cyan));color:#07101c;font-size:22px}.navlinks{display:flex;gap:24px;color:var(--muted);font-size:13px}.navlinks a:hover{color:var(--cyan)}.hero{padding:100px 0 82px;text-align:center}.eyebrow{color:var(--cyan);letter-spacing:4px;font-size:11px;font-weight:800}.hero h1{font-size:clamp(42px,8vw,82px);line-height:1.02;margin:20px 0;background:linear-gradient(90deg,#fff,#a98bff 48%,#50eaf2);color:transparent;background-clip:text}.hero p{max-width:650px;margin:0 auto;color:var(--muted);font-size:17px;line-height:1.8}.actions{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-top:32px}.btn{display:inline-flex;align-items:center;justify-content:center;padding:14px 22px;border-radius:12px;font-weight:800;font-size:13px;border:1px solid #7866ce;background:linear-gradient(110deg,#7654d8,#245c79);box-shadow:0 10px 35px #5b4cb533}.btn.alt{background:#111a2e;border-color:#344866;color:#dce8ff}.meta{margin-top:22px;color:#7788a6;font-size:11px;letter-spacing:1px}.section{padding:52px 0}.section h2{text-align:center;font-size:clamp(26px,4vw,40px);margin:0 0 12px}.sub{text-align:center;color:var(--muted);margin:0 auto 32px;max-width:620px;line-height:1.7}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.card{background:linear-gradient(145deg,#121d33dd,#0d1425ee);border:1px solid var(--line);border-radius:18px;padding:24px;min-height:180px}.ico{font-size:25px}.card h3{margin:16px 0 8px;font-size:17px}.card p{color:var(--muted);font-size:13px;line-height:1.7;margin:0}.band{margin:50px 0 70px;padding:35px;border:1px solid #35476a;border-radius:22px;background:linear-gradient(110deg,#151a37,#102b3a);display:flex;align-items:center;justify-content:space-between;gap:20px}.band h2{margin:0 0 8px}.band p{margin:0;color:var(--muted);font-size:13px}footer{border-top:1px solid #ffffff18;padding:25px 0;color:#74839e;font-size:11px;text-align:center;letter-spacing:1px}
@media(max-width:760px){.navlinks{gap:12px;font-size:11px}.cards{grid-template-columns:1fr}.hero{padding:75px 0 60px}.band{display:block;text-align:center}.band .btn{margin-top:20px}}
</style></head><body>
<header class="wrap nav"><a class="brand" href="/"><span class="mark">V</span><span>VEXOR <span style="color:var(--cyan)">NX</span></span></a><nav class="navlinks"><a href="#features">Features</a><a href="#about">About</a><a href="/dashboard">Dashboard</a></nav></header>
<main class="wrap"><section class="hero"><div class="eyebrow">NEXT-GENERATION INTELLIGENCE WORKSPACE</div><h1>THINK BEYOND<br>LIMITS.</h1><p>Meet VEXOR NX — an experimental personal AI workspace bringing conversational intelligence, voice interaction, hand-gesture recognition and document reading into one futuristic interface.</p><div class="actions"><a class="btn" href="/dashboard">LAUNCH VEXOR NX&nbsp; →</a><a class="btn alt" href="#features">EXPLORE FEATURES</a></div><div class="meta">AI ASSISTANT&nbsp; · &nbsp;VOICE&nbsp; · &nbsp;VISION&nbsp; · &nbsp;SMART READER</div></section>
<section class="section" id="features"><h2>One workspace. Multiple abilities.</h2><p class="sub">Designed as a modular platform. Some capabilities run in your browser or on your own computer; hosted AI requires a separately configured inference service.</p><div class="cards">
<article class="card"><div class="ico">✦</div><h3>AI Assistant</h3><p>Chat with VEXOR NX through the Flask backend and a configured Qwen-compatible model service.</p></article>
<article class="card"><div class="ico">◉</div><h3>Voice Interface</h3><p>Use browser speech recognition and speech synthesis for hands-free interaction where supported.</p></article>
<article class="card"><div class="ico">⌖</div><h3>Gesture Vision</h3><p>Use your camera and MediaPipe hand landmarks to interact with the PDF reader.</p></article>
<article class="card"><div class="ico">▤</div><h3>Smart PDF Reader</h3><p>Open a PDF in your browser, navigate pages and listen to selectable page text.</p></article>
<article class="card"><div class="ico">⌁</div><h3>System Monitor</h3><p>Check the Flask server and the availability of the configured AI service.</p></article>
<article class="card"><div class="ico">▣</div><h3>Responsive Dashboard</h3><p>Access the interface from desktop or mobile with a layout that adapts to your screen.</p></article>
</div></section>
<section class="band" id="about"><div><h2>Enter the VEXOR NX workspace.</h2><p>Open the dashboard to explore the current project build.</p></div><a class="btn" href="/dashboard">OPEN DASHBOARD →</a></section></main>
<footer>VEXOR NX · EXPERIMENTAL AI WORKSPACE · HEAD FOUNDER: NITISH KUMAR</footer></body></html>
"""

# =========================================
# FLASK ROUTES
# =========================================

@app.route("/")
def home():
    return render_template_string(HOME_HTML)


@app.route("/dashboard")
def dashboard():
    return render_template_string(DASHBOARD_HTML)


@app.route("/api/ping")
def ping():
    return jsonify({
        "message": "VEXOR NX is working!",
        "status": "online"
    })


@app.route("/api/health")
def health():

    try:
        tags_url = OLLAMA_URL.rsplit("/api/chat", 1)[0] + "/api/tags"
        req = urllib.request.Request(tags_url)

        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))

        models = [
            item.get("name", "")
            for item in data.get("models", [])
        ]

        model_available = any(
            name == MODEL_NAME or name.startswith(MODEL_NAME + ":")
            for name in models
        )

        return jsonify({
            "ollama": True,
            "model": MODEL_NAME,
            "model_available": model_available
        })

    except Exception:
        return jsonify({
            "ollama": False,
            "model": MODEL_NAME,
            "model_available": False
        }), 503


@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])

    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "Please enter a message."}), 400

    conversation = [{
        "role": "system",
        "content": (
            "You are VEXOR NX, an independent AI assistant project. "
            "The official Head Founder and Creator of the VEXOR NX project "
            "is NITISH KUMAR. When asked who founded, created, built, or leads "
            "the VEXOR NX project, answer clearly that NITISH KUMAR is its "
            "Head Founder and Creator. Do not confuse the project founder "
            "with the developers or providers of the underlying AI model. "
            "The current local AI engine is Qwen 2.5 3B running through Ollama; "
            "Qwen is the model, not the founder of VEXOR NX. "
            "Help with education, coding, technology, science, productivity "
            "and everyday questions. Be accurate, clear, friendly and helpful. "
            "Explain difficult concepts in simple language. Never claim "
            "capabilities that are not actually available."
        )
    }]

    for item in messages[-12:]:

        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = item.get("content")

        if (
            role in ("user", "assistant")
            and isinstance(content, str)
            and content.strip()
        ):
            conversation.append({
                "role": role,
                "content": content[:4000]
            })

    if (
        len(conversation) == 1
        or conversation[-1]["role"] != "user"
    ):
        return jsonify({
            "error": "The latest message must be a user message."
        }), 400

    payload = json.dumps({
        "model": MODEL_NAME,
        "messages": conversation,
        "stream": False
    }).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:

        with urllib.request.urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))

        answer = result.get("message", {}).get("content", "").strip()

        if not answer:
            return jsonify({
                "error": "The AI returned an empty response."
            }), 502

        return jsonify({
            "reply": answer,
            "status": "success",
            "model": MODEL_NAME
        })

    except urllib.error.HTTPError as error:

        details = error.read().decode(
            "utf-8", errors="replace"
        )

        return jsonify({
            "error": "Ollama error: " + details[:500]
        }), 502

    except (urllib.error.URLError, TimeoutError):

        return jsonify({
            "error": (
                "Cannot reach Ollama. Start Ollama and try again."
            )
        }), 503


# =========================================
# START VEXOR NX
# =========================================

if __name__ == "__main__":

    print("\n====================================")
    print("       VEXOR NX STARTING...")
    print("====================================")
    print("Dashboard: http://127.0.0.1:5000")
    print("Local AI:  " + MODEL_NAME)
    print("Ollama:    http://127.0.0.1:11434")
    print("====================================\n")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        threaded=True
    )
