function crear_chart(datos, tipo_graf, titulo){
  var chart = new CanvasJS.Chart("chartContainer9", {
	theme: "theme2",//theme1
	title:{
		text: titulo,              
	},
	animationEnabled: true,   // change to true
	data: [              
	{
		// Change type to "bar", "area", "spline", "pie",etc.
		type: tipo_graf,
		dataPoints: datos
	}
	]
  });
  chart.render();
}


$("#tog_menu").click(function(e) {
  e.preventDefault();
  $("#wrapper").toggleClass("toggled");
});

$("#resumen_evaluacion").change(function(e){
  console.log($("#resumen_evaluacion").val());
  window.location.href = "/reports/seguimiento/departamentos_web/"+$("#resumen_evaluacion").val()+"/";
});

$(".check").click(function(event){
   var list = [];
   $('input[class="check"]:checked').map(function(){
       list.push($(this).val());
   });
   console.log($('input[class="check"]:checked').length);
   if( $('input[class="check"]:checked').length == 0){
      $(this).prop('checked',true);
   }
   else{
      var string = list.toString();
      window.location.href = "/reports/campanas/exoneraciones/"+string+"/";
      console.log(string);
  }
});


$("#ofertas_periodo").change(function(e){
  console.log($("#ofertas_periodo").val());

  window.location.href = "/reports/campanas/ofertas/"+$("#ofertas_periodo").val()+"/";
});

$("#detalles_segmento, #detalles_periodo").change(function(e){
  console.log($("#detalles_segmento").val());
  console.log($("#detalles_periodo").val());

  window.location.href = "/reports/campanas/detalles/"+$("#detalles_segmento").val()+"/"+$("#detalles_periodo").val()+"/";
 
});

$("#caidas_periodo").change(function(e){
  console.log($("#caidas_periodo").val());

  window.location.href = "/reports/campanas/caidas/"+$("#caidas_periodo").val()+"/";
});

$("#flujo_periodo").change(function(e){
  console.log($("#flujo_periodo").val());

  window.location.href = "/reports/campanas/flujo/"+$("#flujo_periodo").val()+"/";
});

//Ajax para vistas RVGL
$("#rvglresumen_periodo,#rvglresumen_analista").change(function(e){
  console.log($("#rvglresumen_periodo").val());
  console.log($("#rvglresumen_analista").val());

  window.location.href = "/reports/rvgl/resumen/"+$("#rvglresumen_periodo").val()+"/"+$("#rvglresumen_analista").val()+"/";
});

$("#rvglresumenximpo_periodo,#rvglresumenximpo_analista").change(function(e){
  console.log($("#rvglresumenximpo_periodo").val());
  console.log($("#rvglresumenximpo_analista").val());

  window.location.href = "/reports/rvgl/resumenximporte/"+$("#rvglresumenximpo_periodo").val()+"/"+$("#rvglresumenximpo_analista").val()+"/";
});

$("#tiempo_periodo, #tiempo_analista").change(function(e){
  console.log($("#tiempo_periodo").val());
  console.log($("#tiempo_analista").val());

  window.location.href = "/reports/rvgl/tiempo/"+$("#tiempo_periodo").val()+"/"+$("#tiempo_analista").val()+"/";
});

$("#rvglresumenxsco_periodo, #rvglresumenxsco_analista").change(function(e){
  console.log($("#rvglresumenxsco_periodo").val());
  console.log($("#rvglresumenxsco_analista").val());

  window.location.href = "/reports/rvgl/resumenxsco/"+$("#rvglresumenxsco_periodo").val()+"/"+$("#rvglresumenxsco_analista").val()+"/";
});

$("#dictamenxsco_periodo, #dictamenxsco_analista").change(function(e){
  console.log($("#dictamenxsco_periodo").val());
  console.log($("#dictamenxsco_analista").val());

  window.location.href = "/reports/rvgl/dictamenxsco/"+$("#dictamenxsco_periodo").val()+"/"+$("#dictamenxsco_analista").val()+"/";
});

$("#scoxdictamen_periodo, #scoxdictamen_analista").change(function(e){
  console.log($("#scoxdictamen_periodo").val());
  console.log($("#scoxdictamen_analista").val());

  $.ajax({
    data: {periodo: $("#scoxdictamen_periodo").val(),
           analista: $("#scoxdictamen_analista").val(),
           csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
          },
    type: 'POST',
    url: '/reports/rvgl/json_scoxdictamen/',
    success: function(json){
       var limpia = json.replace(/'dictamen_sco'/g,'"label"');
       limpia = limpia.replace(/'num_scoxdictamen'/g,'"y"');
       limpia = limpia.replace(/: u'/g,": '");
       limpia = limpia.replace(/}{/g,"},{");
       limpia = limpia.replace(/'/g,'"');
       limpia = limpia.replace(/&quot;/ig,'"');
       console.log(limpia);
       var result = JSON.parse('['+limpia+']');
       console.log(result);
       crear_chart(result, "pie", "Por Dictamen de Scoring");
       var html = "";
       for (var datos in result){
        html = html + "<tr> <td></td><td>"+result[datos].label+"</td>"+"<td>"+result[datos].y+"</td></tr>";
       };
       $("#tabla_scoxdictamen").html(html);
    }
  });
});

$("#resumen_periodo").change(function(e){
  console.log($("#resumen_periodo").val());

  window.location.href = "/reports/campanas/resumen/"+$("#resumen_periodo").val()+"/";
});

$("#top20terr_periodo, #top20terr_analista").change(function(e){
  console.log($("#top20terr_periodo").val());
  console.log($("#top20terr_analista").val());

  window.location.href = "/reports/rvgl/top20terr/"+$("#top20terr_periodo").val()+"/"+$("#top20terr_analista").val()+"/";
});

$("#top20gest_periodo, #top20gest_analista").change(function(e){
  console.log($("#top20gest_periodo").val());
  console.log($("#top20gest_analista").val());

  window.location.href = "/reports/rvgl/top20gest/"+$("#top20gest_periodo").val()+"/"+$("#top20gest_analista").val()+"/";
});

$("#top20clie_periodo, #top20clie_analista").change(function(e){
  console.log($("#top20clie_periodo").val());
  console.log($("#top20clie_analista").val());

  window.location.href = "/reports/rvgl/top20clie/"+$("#top20clie_periodo").val()+"/"+$("#top20clie_analista").val()+"/";
});

$("#top20ofic_periodo, #top20ofic_analista").change(function(e){
  console.log($("#top20ofic_periodo").val());
  console.log($("#top20ofic_analista").val());

  window.location.href = "/reports/rvgl/top20ofic/"+$("#top20ofic_periodo").val()+"/"+$("#top20ofic_analista").val()+"/";
});

//distritos
/*$("#ancon").hover(function(){
   $(this).css("cursor","pointer");

});

$("#ancon").click(function(){
   $("#ancon").attr("fill","#ffff00");
   alert("hola mundo");
});
*/
// sliders
$('#ex1').slider({
	formatter: function(value) {
		return 'Current value: ' + value;
	}
});

$("#ex13").change(function(e){
  console.log($("#ex13").val());

  $.ajax({
    data: {periodo: $("#ex13").val(),
           csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
          },
    type: 'POST',
    url: '/reports/seguimiento/json_mapa/',
    success: function(json){

       var limpia = json.replace(/Decimal\('/g,'');
       limpia = limpia.replace(/'\)/g,'');
       limpia = limpia.replace(/: u'/g,": '");
       limpia = limpia.replace(/}{/g,"},{");
       limpia = limpia.replace(/'/g,'"');
       limpia = limpia.replace(/&quot;/ig,'"');
       var result = JSON.parse('['+limpia+']');

       var html = "";
       for (var datos in result){
        html = html + "<tr><td>"+result[datos].distrito+"</td>"+"<td>"+result[datos].contrato.toFixed(0)+"</td>"+"<td>"+result[datos].inver.toFixed(0)+"</td>"+"<td>"+result[datos].mora.toFixed(2)+"%"+"</td></tr>";
       };
       $("#tabla_mapa").html(html);
    }
  });
});





