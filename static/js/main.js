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
       crear_chart(JSON.parse('['+limpia+']'), "column", "Distribución por Dictamen");
    }
  });
});






