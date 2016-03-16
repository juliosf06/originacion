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
       limpia = limpia.replace(/'sum_importe'/g,'"y"');
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


$("#dictamenxsco_producto, #dictamenxsco_periodo").change(function(e){
  console.log($("#dictamenxsco_producto").val());
  console.log($("#dictamenxsco_periodo").val());

  $.ajax({
    data: {producto: $("#dictamenxsco_producto").val(), 
           periodo: $("#dictamenxsco_periodo").val(),
           csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
          },
    type: 'POST',
    url: '/reports/rvgl/json_dictamenxsco/',
    success: function(json){
       var limpia = json.replace(/'dictamen'/g,'"label"');
       limpia = limpia.replace(/'num_dictamenxsco'/g,'"y"');
       limpia = limpia.replace(/: u'/g,": '");
       limpia = limpia.replace(/}{/g,"},{");
       limpia = limpia.replace(/'/g,'"');
       limpia = limpia.replace(/&quot;/ig,'"');
       console.log(limpia);
       var result = JSON.parse('['+limpia+']');
       console.log(result);
       crear_chart(result, "column", "Distribución de Dictamen por Scoring");
       var html = "";
       for (var datos in result){
        html = html + "<tr> <td></td><td>"+result[datos].label+"</td>"+"<td>"+result[datos].y+"</td></tr>";
       };
       $("#tabla_dictamen").html(html);
    }
  });
});




