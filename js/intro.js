(function(){
var I=document.getElementById('intro'),cv=document.getElementById('cv'),ni=document.querySelector('.i-niki'),tape=document.querySelector('.i-tape'),txt=document.querySelector('.i-txt'),st=document.querySelector('.i-strips'),P=null,E=null,raf=0,T=[];
function prep(cb){if(P)return cb();var im=new Image();im.onload=function(){var w=150,h=Math.round(w*im.naturalHeight/im.naturalWidth),c=document.createElement('canvas');c.width=w;c.height=h;var x=c.getContext('2d');x.drawImage(im,0,0,w,h);var d=x.getImageData(0,0,w,h).data,s=7,pts=[];
 function A(i,j){return(i<0||j<0||i>=w||j>=h)?0:d[(j*w+i)*4+3]}
 for(var j=0;j<h;j+=2)for(var i=0;i<w;i+=2){if(A(i,j)<128)continue;var o=(j*w+i)*4,hr=d[o]>170&&d[o+1]>150&&d[o+2]<120,pk=d[o]>200&&d[o+1]<120,ed=A(i-3,j)<128||A(i+3,j)<128||A(i,j-3)<128||A(i,j+3)<128;s=(s*16807)%2147483647;var r=s/2147483647;if(hr||pk||(ed?r<.8:r<.45)){var a=r*6.283*7,rr=.7+((s*7)%100)/80;pts.push({x:i/w,y:j/h,k:hr?1:pk?2:0,ax:Math.cos(a)*rr*1.6,ay:Math.sin(a)*rr*1.6,ar:h/w})}}
 P=pts;E=[];var G={},cs=.03;P.forEach(function(p,i){var k=Math.floor(p.x/cs)+','+Math.floor(p.y*p.ar/cs);(G[k]=G[k]||[]).push(i)});
 P.forEach(function(p,i){var gx=Math.floor(p.x/cs),gy=Math.floor(p.y*p.ar/cs),b=[];for(var u=-1;u<=1;u++)for(var v=-1;v<=1;v++)(G[(gx+u)+','+(gy+v)]||[]).forEach(function(k){if(k===i)return;var q=P[k];b.push([(q.x-p.x)*(q.x-p.x)+(q.y-p.y)*(q.y-p.y)*p.ar*p.ar,k])});b.sort(function(a,c){return a[0]-c[0]});b.slice(0,3).forEach(function(c){if(c[1]>i)E.push([i,c[1]])})});cb()};im.src=ni.src}
function L(){var W=innerWidth,H=innerHeight,ar=P[0].ar,hh=W>=800?H*.92:H*.62,ww=hh/ar;return{W:W,H:H,hh:hh,ww:ww,ox:W>=800?W*.2:W*.5-ww/2,oy:H-hh}}
var COL=['#39FF14','#00E5FF','#B026FF','#FF6A00'];
function build(){var B=L(),dpr=Math.min(devicePixelRatio||1,2);cv.width=B.W*dpr;cv.height=B.H*dpr;cv.style.width=B.W+'px';cv.style.height=B.H+'px';
 ni.style.cssText='left:'+B.ox+'px;top:'+B.oy+'px;height:'+B.hh+'px';var x=cv.getContext('2d'),t0=performance.now(),ox=B.ox*dpr,oy=B.oy*dpr,ww=B.ww*dpr,hh=B.hh*dpr;
 function f(t){var k=Math.min(1,(t-t0)/1100),e=1-Math.pow(1-k,4),j=(1-e)*14*dpr;x.clearRect(0,0,cv.width,cv.height);
  var q=P.map(function(p){var s=1-e;return[ox+(p.x+p.ax*s)*ww+(Math.random()-.5)*j,oy+(p.y+p.ay*s)*hh+(Math.random()-.5)*j]});
  x.globalCompositeOperation='lighter';x.lineWidth=1.3*dpr;x.strokeStyle=COL[Math.floor(t/90)%4];x.globalAlpha=.25+.6*e;x.beginPath();
  E.forEach(function(g){x.moveTo(q[g[0]][0],q[g[0]][1]);x.lineTo(q[g[1]][0],q[g[1]][1])});x.stroke();x.globalAlpha=1;
  q.forEach(function(p,i){var r=(i%7?1.5:3)*dpr,kk=P[i].k;x.fillStyle=kk==1?'#F6E83B':kk==2?'#FF2E88':'#A9F1DF';x.fillRect(p[0]-r,p[1]-r,r*2,r*2)});
  document.getElementById('cnt').textContent=String(Math.floor(e*100)).padStart(3,'0')+'% LOUD';
  if(k<1)raf=requestAnimationFrame(f)}raf=requestAnimationFrame(f)}
function at(ms,fn){T.push(setTimeout(fn,ms))}
function shake(){I.classList.remove('i-shake');void I.offsetWidth;I.classList.add('i-shake')}
function reset(){T.forEach(clearTimeout);T=[];cancelAnimationFrame(raf);I.style.display='';I.style.opacity=1;cv.style.opacity=1;['i-on','i-slam','i-park'].forEach(function(c){document.querySelectorAll('.'+c).forEach(function(e){e.classList.remove(c)})});tape.style.cssText='';ni.style.transition='';st.classList.remove('go')}
function play(){reset();var s=document.querySelector('.i-strobe'),a=document.querySelector('.i-big.a'),b=document.querySelector('.i-big.b');
 s.classList.add('i-on');at(150,function(){a.classList.add('i-on');shake()});at(450,function(){b.classList.add('i-on');shake()});
 at(900,function(){prep(build)});
 at(1900,function(){a.classList.remove('i-on');b.classList.remove('i-on')});
 at(2050,function(){ni.classList.add('i-on');cv.style.transition='opacity .4s';cv.style.opacity=.35});
 at(2300,function(){tape.classList.add('i-slam');shake()});
 at(2800,function(){txt.classList.add('i-on');shake()});
 at(3300,function(){tape.classList.remove('i-slam');tape.style.cssText='opacity:1;transform:translate(-50%,-50%) scale(1) rotate(-3deg)';void tape.offsetWidth;tape.classList.add('i-park');tape.style.cssText='opacity:1;left:'+(innerWidth*.72)+'px;top:'+(innerHeight*.18)+'px;transform:translate(-50%,-50%) scale(.6) rotate(-3deg)'});
 at(4600,finish)}
function finish(){if(st.classList.contains('go'))return;T.forEach(clearTimeout);st.classList.add('go');setTimeout(function(){I.style.display='none';cancelAnimationFrame(raf)},500);setTimeout(function(){st.classList.remove('go')},1300)}
addEventListener('keydown',function(e){if(e.key==='Escape')finish()});
document.getElementById('i-skip').onclick=finish;var seen=0;try{seen=localStorage.wcIntro}catch(e){}if(!seen&&!matchMedia('(prefers-reduced-motion: reduce)').matches&&!/[?&]nointro/.test(location.search)){document.documentElement.classList.add('intro-on');play()}else I.style.display='none';window.wcReplay=function(){document.documentElement.classList.add('intro-on');play()};
})();