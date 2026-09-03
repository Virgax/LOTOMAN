(function(){
 // INSPECTOR — solo lee. No hace clic, no selecciona, no compra.
 var sel=function(el){var s=el.tagName.toLowerCase();
   if(el.id)return s+'#'+el.id;
   if(el.className&&typeof el.className==='string')
     s+='.'+el.className.trim().split(/\s+/).slice(0,4).join('.');
   return s;};
 var vis=function(el){var r=el.getBoundingClientRect();return r.width>0&&r.height>0;};

 // 1) Candidatos a "bola": elemento hoja cuyo texto es un número 1..80
 var bolas={};
 document.querySelectorAll('*').forEach(function(el){
   if(el.children.length)return;
   var t=(el.textContent||'').trim();
   if(!/^0?\d{1,2}$/.test(t))return;
   var n=parseInt(t,10); if(n<1||n>80)return;
   if(!vis(el))return;
   var k=sel(el.parentElement&&el.parentElement.children.length>10?el:el);
   (bolas[k]=bolas[k]||{sel:k,nums:[],ej:''}).nums.push(n);
   if(!bolas[k].ej)bolas[k].ej=el.outerHTML.slice(0,300);
 });
 var grupos=Object.values(bolas).filter(function(g){return g.nums.length>=20;})
   .sort(function(a,b){return b.nums.length-a.nums.length;});

 // 2) Botones y elementos clicables con texto
 var btns=[];
 document.querySelectorAll('button,a[role=button],[onclick],input[type=button],input[type=submit],div[class*=btn],div[class*=boton]')
  .forEach(function(el){
   var t=(el.textContent||el.value||'').trim().slice(0,40);
   if(!t||!vis(el))return;
   btns.push({txt:t,sel:sel(el),dis:!!el.disabled});
  });

 // 3) Saldo / totales visibles
 var plata=[];
 document.querySelectorAll('*').forEach(function(el){
   if(el.children.length)return;
   var t=(el.textContent||'').trim();
   if(/^RD\$|^\$\s?[\d,]+/.test(t)&&t.length<20&&vis(el))
     plata.push({txt:t,sel:sel(el)});
 });

 var rep={url:location.href,titulo:document.title,
   grupos_de_bolas:grupos.slice(0,3).map(function(g){
     return {selector:g.sel,cuantos:g.nums.length,
             min:Math.min.apply(null,g.nums),max:Math.max.apply(null,g.nums),
             ejemplo_html:g.ej};}),
   botones:btns.slice(0,40), montos:plata.slice(0,15)};

 var txt=JSON.stringify(rep,null,1);
 var ok=function(){alert('Inspector: '+grupos.length+' grupo(s) de bolas, '+
   btns.length+' botones.\nReporte copiado al portapapeles.\nPégaselo a Claude.');};
 if(navigator.clipboard&&navigator.clipboard.writeText){
   navigator.clipboard.writeText(txt).then(ok,function(){console.log(txt);
     alert('No pude copiar. El reporte está en la consola (F12).');});
 }else{console.log(txt);
   var ta=document.createElement('textarea');ta.value=txt;
   ta.style.cssText='position:fixed;top:5%;left:5%;width:90%;height:80%;z-index:99999';
   document.body.appendChild(ta);ta.select();
   alert('Reporte en el cuadro de texto: cópialo y pégaselo a Claude.');}
})();
