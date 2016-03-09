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


$("#tiempo_banca, #tiempo_periodo").change(function(e){
  console.log($("#tiempo_banca").val());
  console.log($("#tiempo_periodo").val());

  $.ajax({
    data: {banca: $("#tiempo_banca").val(), 
           periodo: $("#tiempo_periodo").val(),
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
       $("#tabla_dictamen").html(html);
    }
  });
});




