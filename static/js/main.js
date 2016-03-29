function crear_chart(datos, tipo_graf, titulo){
  var chart = new CanvasJS.Chart("chartContainer", {
	theme: "theme2",//theme1
	title:{
		text: titulo              
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

//Ajax para vistas CAMPANAS
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

$("#exoneraciones_periodo").change(function(e){
  console.log($("#exoneraciones_periodo").val());

  window.location.href = "/reports/campanas/exoneraciones/"+$("#exoneraciones_periodo").val()+"/";
});

$("#flujo_periodo").change(function(e){
  console.log($("#flujo_periodo").val());

  window.location.href = "/reports/campanas/flujo/"+$("#flujo_periodo").val()+"/";
});



//Ajax para vistas RVGL
$("#banca_periodo,#banca_analista ").change(function(e){
  console.log($("#banca_periodo").val());
  console.log($("#banca_analista").val());

  $.ajax({
    data: {periodo: $("#banca_periodo").val(),
	   analista: $("#banca_analista").val(), 
           csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
          },
    type: 'POST',
    url: '/reports/rvgl/json_banca/',
    success: function(json){
       var limpia = json.replace(/'seco'/g,'"label"');
       limpia = limpia.replace(/'num_seco'/g,'"y"');
       limpia = limpia.replace(/: u'/g,": '");
       limpia = limpia.replace(/}{/g,"},{");
       limpia = limpia.replace(/'/g,'"');
       limpia = limpia.replace(/&quot;/ig,'"');
       console.log(limpia);
       var result = JSON.parse('['+limpia+']');
       console.log(result);
       crear_chart(result, "pie", "Distribución según Banca");
       var html = "";
       for (var datos in result){
        html = html + "<tr> <td></td><td>"+result[datos].label+"</td>"+"<td>"+result[datos].y+"</td></tr>";
       };
       $("#tabla_banca").html(html);
    }
  });
});


$("#dictamen_producto, #dictamen_periodo").change(function(e){
  console.log($("#dictamen_producto").val());
  console.log($("#dictamen_periodo").val());

  $.ajax({
    data: {producto: $("#dictamen_producto").val(), 
           periodo: $("#dictamen_periodo").val(),
           csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
          },
    type: 'POST',
    url: '/reports/rvgl/json_dictamen/',
    success: function(json){
       var limpia = json.replace(/'dictamen'/g,'"label"');
       limpia = limpia.replace(/'num_dictamen'/g,'"y"');
       limpia = limpia.replace(/: u'/g,": '");
       limpia = limpia.replace(/}{/g,"},{");
       limpia = limpia.replace(/'/g,'"');
       limpia = limpia.replace(/&quot;/ig,'"');
       console.log(limpia);
       var result = JSON.parse('['+limpia+']');
       console.log(result);
       crear_chart(result, "column", "Distribución por Dictamen");
       var html = "";
       for (var datos in result){
        html = html + "<tr> <td></td><td>"+result[datos].label+"</td>"+"<td>"+result[datos].y+"</td></tr>";
       };
       $("#tabla_dictamen").html(html);
    }
  });
});

$("#producto_periodo,#producto_analista ").change(function(e){
  console.log($("#producto_periodo").val());
  console.log($("#producto_analista").val());

  $.ajax({
    data: {periodo: $("#producto_periodo").val(),
	   analista: $("#producto_analista").val(), 
           csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
          },
    type: 'POST',
    url: '/reports/rvgl/json_producto/',
    success: function(json){
       var limpia = json.replace(/'producto_esp'/g,'"label"');
       limpia = limpia.replace(/'num_producto'/g,'"y"');
       limpia = limpia.replace(/: u'/g,": '");
       limpia = limpia.replace(/}{/g,"},{");
       limpia = limpia.replace(/'/g,'"');
       limpia = limpia.replace(/&quot;/ig,'"');
       console.log(limpia);
       var result = JSON.parse('['+limpia+']');
       console.log(result);
       crear_chart(result, "bar", "Distribución por producto");
       var html = "";
       for (var datos in result){
        html = html + "<tr> <td></td><td>"+result[datos].label+"</td>"+"<td>"+result[datos].y+"</td></tr>";
       };
       $("#tabla_producto").html(html);
    }
  });
});

$("#buro_periodo,#buro_analista ").change(function(e){
  console.log($("#buro_periodo").val());
  console.log($("#buro_analista").val());

  $.ajax({
    data: {periodo: $("#buro_periodo").val(),
	   analista: $("#buro_analista").val(), 
           csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
          },
    type: 'POST',
    url: '/reports/rvgl/json_buro/',
    success: function(json){
       var limpia = json.replace(/'dic_buro'/g,'"label"');
       limpia = limpia.replace(/'num_buro'/g,'"y"');
       limpia = limpia.replace(/: u'/g,": '");
       limpia = limpia.replace(/}{/g,"},{");
       limpia = limpia.replace(/'/g,'"');
       limpia = limpia.replace(/&quot;/ig,'"');
       console.log(limpia);
       var result = JSON.parse('['+limpia+']');
       console.log(result);
       crear_chart(result, "doughnut", "Distribución según buro");
       var html = "";
       for (var datos in result){
        html = html + "<tr> <td></td><td>"+result[datos].label+"</td>"+"<td>"+result[datos].y+"</td></tr>";
       };
       $("#tabla_buro").html(html);
    }
  });
});

$("#importexprod_periodo,#importexprod_analista ").change(function(e){
  console.log($("#importexprod_periodo").val());
  console.log($("#importexprod_analista").val());

  $.ajax({
    data: {periodo: $("#importexprod_periodo").val(),
	   analista: $("#importexprod_analista").val(), 
           csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
          },
    type: 'POST',
    url: '/reports/rvgl/json_importexprod/',
    success: function(json){
       console.log(json);
       var limpia = json.replace(/'producto_esp'/g,'"label"');
       limpia = limpia.replace(/'sum_importexprod'/g,'"y"');
       limpia = limpia.replace(/Decimal\('/g,'');
       limpia = limpia.replace(/'\)/g,'');
       limpia = limpia.replace(/: u'/g,": '");
       limpia = limpia.replace(/}{/g,"},{");
       limpia = limpia.replace(/'/g,'"');
       limpia = limpia.replace(/&quot;/ig,'"');
       console.log(limpia);
       var result = JSON.parse('['+limpia+']');
       console.log(result);
       crear_chart(result, "bar", "Importe solicitado por Producto");
       var html = "";
       for (var datos in result){
        html = html + "<tr> <td></td><td>"+result[datos].label+"</td>"+"<td>"+result[datos].y+"</td></tr>";
       };
       $("#tabla_importexprod").html(html);
    }
  });
});


$("#tiempo_banca, #tiempo_periodo, #tiempo_analista").change(function(e){
  console.log($("#tiempo_banca").val());
  console.log($("#tiempo_periodo").val());
  console.log($("#tiempo_analista").val());

  $.ajax({
    data: {banca: $("#tiempo_banca").val(), 
           periodo: $("#tiempo_periodo").val(),
           analista: $("#tiempo_analista").val(),
           csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
          },
    type: 'POST',
    url: '/reports/rvgl/json_tiempo/',
    success: function(json){
       var limpia = json.replace(/'dias_eval'/g,'"label"');
       limpia = limpia.replace(/'num_tiempo'/g,'"y"');
       limpia = limpia.replace(/: u'/g,": '");
       limpia = limpia.replace(/}{/g,"},{");
       limpia = limpia.replace(/'/g,'"');
       limpia = limpia.replace(/&quot;/ig,'"');
       console.log(limpia);
       var result = JSON.parse('['+limpia+']');
       console.log(result);
       crear_chart(result, "column", "Distribución por Tiempo Dictaminado");
       var html = "";
       for (var datos in result){
        html = html + "<tr> <td></td><td>"+result[datos].label+"</td>"+"<td>"+result[datos].y+"</td></tr>";
       };
       $("#tabla_tiempo").html(html);
    }
  });
});

$("#importexdict_periodo,#importexdict_analista ").change(function(e){
  console.log($("#importexdict_periodo").val());
  console.log($("#importexdict_analista").val());

  $.ajax({
    data: {periodo: $("#importexdict_periodo").val(),
	   analista: $("#importexdict_analista").val(), 
           csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
          },
    type: 'POST',
    url: '/reports/rvgl/json_importexdict/',
    success: function(json){
       console.log(json);
       var limpia = json.replace(/'dictamen'/g,'"label"');
       limpia = limpia.replace(/'sum_importexdict'/g,'"y"');
       limpia = limpia.replace(/Decimal\('/g,'');
       limpia = limpia.replace(/'\)/g,'');
       limpia = limpia.replace(/: u'/g,": '");
       limpia = limpia.replace(/}{/g,"},{");
       limpia = limpia.replace(/'/g,'"');
       limpia = limpia.replace(/&quot;/ig,'"');
       console.log(limpia);
       var result = JSON.parse('['+limpia+']');
       console.log(result);
       crear_chart(result, "bar", "Importe generado por Dictamen");
       var html = "";
       for (var datos in result){
        html = html + "<tr> <td></td><td>"+result[datos].label+"</td>"+"<td>"+result[datos].y+"</td></tr>";
       };
       $("#tabla_importexdict").html(html);
    }
  });
});


$("#dictamenxsco_periodo, #dictamenxsco_analista").change(function(e){
  console.log($("#dictamenxsco_periodo").val());
  console.log($("#dictamenxsco_analista").val());

  window.location.href = "/reports/rvgl/dictamenxsco/"+$("#dictamenxsco_periodo").val()+"/"+$("#dictamenxsco_analista").val()+"/";
});


$("#scoxllenado_periodo, #scoxllenado_analista").change(function(e){
  console.log($("#scoxllenado_periodo").val());
  console.log($("#scoxllenado_analista").val());

  $.ajax({
    data: {periodo: $("#scoxllenado_periodo").val(),
           analista: $("#scoxllenado_analista").val(),
           csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
          },
    type: 'POST',
    url: '/reports/rvgl/json_scoxllenado/',
    success: function(json){
       var limpia = json.replace(/'sco'/g,'"label"');
       limpia = limpia.replace(/'num_scoxllenado'/g,'"y"');
       limpia = limpia.replace(/: u'/g,": '");
       limpia = limpia.replace(/}{/g,"},{");
       limpia = limpia.replace(/'/g,'"');
       limpia = limpia.replace(/&quot;/ig,'"');
       console.log(limpia);
       var result = JSON.parse('['+limpia+']');
       console.log(result);
       crear_chart(result, "pie", "Por llenado de Scoring");
       var html = "";
       for (var datos in result){
        html = html + "<tr> <td></td><td>"+result[datos].label+"</td>"+"<td>"+result[datos].y+"</td></tr>";
       };
       $("#tabla_scoxllenado").html(html);
    }
  });
})


$("#scoxforzaje_periodo, #scoxforzaje_analista").change(function(e){
  console.log($("#scoxforzaje_periodo").val());
  console.log($("#scoxforzaje_analista").val());

  $.ajax({
    data: {periodo: $("#scoxforzaje_periodo").val(),
           analista: $("#scoxforzaje_analista").val(),
           csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
          },
    type: 'POST',
    url: '/reports/rvgl/json_scoxforzaje/',
    success: function(json){
       var limpia = json.replace(/'seg_prime'/g,'"label"');
       limpia = limpia.replace(/'num_scoxforzaje'/g,'"y"');
       limpia = limpia.replace(/: u'/g,": '");
       limpia = limpia.replace(/}{/g,"},{");
       limpia = limpia.replace(/'/g,'"');
       limpia = limpia.replace(/&quot;/ig,'"');
       console.log(limpia);
       var result = JSON.parse('['+limpia+']');
       console.log(result);
       crear_chart(result, "pie", "Por Nivel de forzaje");
       var html = "";
       for (var datos in result){
        html = html + "<tr> <td></td><td>"+result[datos].label+"</td>"+"<td>"+result[datos].y+"</td></tr>";
       };
       $("#tabla_scoxforzaje").html(html);
    }
  });
})


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
})


$("#top20terr_periodo, #top20terr_analista").change(function(e){
  console.log($("#top20terr_periodo").val());
  console.log($("#top20terr_analista").val());

  window.location.href = "/reports/rvgl/top20terr/"+$("#top20terr_periodo").val()+"/"+$("#top20terr_analista").val()+"/";
})
