          function completarInfo(lista){
              var analistas = lista[0];
              var oficinas = lista[1];
              var codOficina = lista[2];
              var actividad = lista[3];
              var pertenece = lista[4];
              
              if(pertenece == true){
                  document.getElementById("seccion_sancion").style.display= 'none';
              }else{
                  document.getElementById("seccion_sancion").style.display= 'block';
              }
              
              var today = new Date();
              var t = today.toISOString().substring(0, 10);
              
              document.getElementById("fechaVisita").value = t;
              document.getElementById("fechaVisita").innerHTML = t;
              
              document.getElementById("analista").value = analistas;
              document.getElementById("analista").innerHTML = analistas;
              document.getElementById("analista").disabled = true;
              
              
              document.getElementById("oficinas").options[0]=new Option("");
              document.getElementById("actividad").options[0]=new Option("");
              for(i=0;i<oficinas.length;i++){
                  document.getElementById("oficinas").options[i+1]=new Option(codOficina[i] + " - " + oficinas[i], codOficina[i]);
              }
              for(i=0;i<actividad.length;i++){
                  document.getElementById("actividad").options[i+1]=new Option(actividad[i], actividad[i]);
              }
              
              
          }
          
          function AbrirMensaje(id,Principal){
              document.getElementById(id).style.display = "block";
              document.getElementById(Principal).style.display = "none";
              if(id == "mensaje"){
                  document.getElementById('header').scrollIntoView()
              }
              document.getElementById('btn_Cerrar').style.display = "block";
              document.getElementById('btn_Abrir').style.display = "none";
          }
          function CerrarMensaje(id,Principal){
              document.getElementById(id).style.display = "none";
              document.getElementById(Principal).style.display = "block";
              document.getElementById('btn_Abrir').scrollIntoView();
              document.getElementById('btn_Cerrar').style.display = "none";
              document.getElementById('btn_Abrir').style.display = "block";
          }
          
          function AgregarProducto(){
              var table = document.getElementById("tablaProductos");
              var idx = table.rows.length-1;
              var row = table.insertRow(idx);
              for (var i = 0; i< idx ;i++){
                //var e = document.getElementById("Prod"+i);
                //var camp = e.options[e.selectedIndex].text;
              }
              
              var cell1 = row.insertCell(0);
              var cell2 = row.insertCell(1);
              var cell3 = row.insertCell(2);
              var cell4 = row.insertCell(3);
              var cell5 = row.insertCell(4);
              var cell6 = row.insertCell(5);
              var cell7 = row.insertCell(6);
              cell1.innerHTML = '<input class="form-control" id = "Prod'+idx+'"/>';
              cell2.innerHTML = '<input class="form-control" id="unidades_vendidas_'+idx+'" onkeyup=";validarNumero(id);calcular_ingresos_comercio();"/>';
              cell3.innerHTML = '<select class="form-control" id="unidades_x_presentacion_'+idx+'">'+
                                      '<option value="0"></option>'+
                                      '<option value="Galones">Galones</option>'+
                                      '<option value="Kilos">Kilos</option>'+
                                      '<option value="Litros">Litros</option>'+
                                      '<option value="Metros">Metros</option>'+
                                      '<option value="Pies">Pies</option>'+
                                      '<option value="Rollos">Rollos</option>'+
                                      '<option value="Sacos">Sacos</option>'+
                                      '<option value="Otros">Otros</option>'+
                                  '</select>';
              cell4.innerHTML = '<input class="form-control" id="pcompra_'+idx+'" onkeyup="validarNumero(id);calcular_ingresos_comercio();"/>';
              cell5.innerHTML = '<input class="form-control" id="pventa_'+idx+'" onkeyup="validarNumero(id);calcular_ingresos_comercio();"/>';
              cell6.innerHTML = '<div id="util_bruta_'+idx+'">';
              cell7.innerHTML = '<div id="ventas_x_prod_'+idx+'">';
          }
          function EliminarProducto(){
              var table = document.getElementById("tablaProductos")
              var idx = table.rows.length -2
              if(table.rows.length>3){
                  table.deleteRow(idx);
                  calcular_ingresos_comercio();
              }
          }
          function AgregarPatrimonio1(){
              
              var table = document.getElementById("tablaPatrimonioInmueble");
              var idx = table.rows.length-1;
              var row = table.insertRow(idx);
                  
              var cell1 = row.insertCell(0);
              var cell2 = row.insertCell(1);
              var cell3 = row.insertCell(2);
              var cell4 = row.insertCell(3);
              var cell5 = row.insertCell(4);
              var cell6 = row.insertCell(5);
              var cell7 = row.insertCell(6);
              var cell8 = row.insertCell(7);
              cell1.innerHTML = '<input class="form-control" id = "Ubic_'+idx+'"/>';
              cell2.innerHTML = '<input class="form-control" id="Propietario_'+idx+'"/>';
              cell3.innerHTML = '<input class="form-control" id="Uso_'+idx+'"/>';
              cell4.innerHTML = '<select class="form-control" id="Realizable_'+idx+'" onchange="calcular_valor_evaluado_Total();">'+
                                      '<option value="0"></option>'+
                                      '<option value="Si">Si</option>'+
                                      '<option value="No">No</option>'+
                                  '</select>';
                                  //calcular_util_bruta('+"'"+idx+"'"+');
              cell5.innerHTML = '<input class="form-control" id="Metraje_'+idx+'" onkeyup="validarNumero(id);calcular_valor_declarado_Total();"/>';
              cell6.innerHTML = '<input class="form-control" id="Precio_'+idx+'" onkeyup="validarNumero(id);calcular_valor_declarado_Total();"/>';
              cell7.innerHTML = '<div id="Val_Inm_Dec_'+idx+'">';
              cell8.innerHTML = '<div id="Val_Inm_Eva_'+idx+'">';
          }
          function EliminarPatrimonio1(){
              var table = document.getElementById("tablaPatrimonioInmueble")
              var idx = table.rows.length -2
              if(table.rows.length>3){
                  table.deleteRow(idx);
                  calcular_valor_declarado_Total();
              }
          }
          
          function AgregarPatrimonio2(){
              
              var table = document.getElementById("tablaPatrimonioVehiculos");
              var idx = table.rows.length-1;
              var row = table.insertRow(idx);
                  
              var cell1 = row.insertCell(0);
              var cell2 = row.insertCell(1);
              var cell3 = row.insertCell(2);
              var cell4 = row.insertCell(3);
              var cell5 = row.insertCell(4);
              cell1.innerHTML = '<select class="form-control" id="Veh_Maq_'+idx+'" onchange="Calcular_Valor_Bien_Total();">'+
                                      '<option value="0"></option>'+
                                      '<option value="Vehiculo">Vehiculo</option>'+
                                      '<option value="Maquinaria">Maquinaria</option>'+
                                  '</select>';
                                  //calcular_util_bruta('+"'"+idx+"'"+');
              cell2.innerHTML = '<input class="form-control" id="Placa_'+idx+'"/>';
              cell3.innerHTML = '<input class="form-control" id="Valor_Nuevo_'+idx+'" onkeyup="validarNumero(id);Calcular_Valor_Bien_Total();"/>';
              cell4.innerHTML = '<input class="form-control" id="Antiguedad_'+idx+'" onkeyup="validarNumero(id);Calcular_Valor_Bien_Total();"/>';
              cell5.innerHTML = '<div id="Valor_Bien_'+idx+'">';
          }
          function EliminarPatrimonio2(){
              var table = document.getElementById("tablaPatrimonioVehiculos")
              var idx = table.rows.length -2
              if(table.rows.length>3){
                  table.deleteRow(idx);
              }
          }
          
          function Limpiar(){
              alert("Función Deshabilitada")
          }
          function convNro(nroComas) {
              var arreglo = String(nroComas).split(",");
              var sinComas = arreglo.join("");
              if(isNaN(sinComas)){
                  return 0;
              }
              return Number(sinComas);
          }
          function validarNumero(id) {
              if (document.getElementById(id).value != "") {
                  var conComas = document.getElementById(id).value;
                  
                  var texto = conComas.split(",");
                  var sinComas = texto.join("");
                  var n = sinComas.indexOf(".");
                  var siguiente = "";
                  if(Number(n)!=-1){
                      siguiente = sinComas.charAt(n+1);
                  }
                  if (sinComas.length > 15) {
                      alert("Excedio la cantidad permitida de dígitos");
                      document.getElementById(id).value = "";
                  } else {
                      if (isNaN(sinComas)) {
                          alert("Ingrese un número válido");
                          document.getElementById(id).value = "";
                      } else {
                          var nuevo =  Number(sinComas).toLocaleString('en');
                          //alert(nuevo);
                          if(Number(n)==-1){
                              document.getElementById(id).value = nuevo;
                              document.getElementById(id).setAttribute('value',nuevo);
                          }else{
                              if(siguiente==""){
                                  document.getElementById(id).value = nuevo+".";
                                  document.getElementById(id).setAttribute('value',nuevo+".");
                              }else{
                                  document.getElementById(id).value = nuevo;
                                  document.getElementById(id).setAttribute('value',nuevo);
                              }
                              
                          }
                      }
                  }
              }
          }
          
          function calcular_ventas_prod(idx){
              var unidades_vendidas = convNro(document.getElementById("unidades_vendidas_"+idx).value);
              var pventa = convNro(document.getElementById("pventa_"+idx).value);
              var ventas_x_prod = pventa * unidades_vendidas;
              document.getElementById("ventas_x_prod_"+idx).innerHTML = Number(ventas_x_prod).toLocaleString('en');
              document.getElementById("ventas_x_prod_"+idx).value = ventas_x_prod;
              calcular_ventas_prod_Total();
          }
          function calcular_ventas_prod_Total(){
              var table = document.getElementById("tablaProductos");
              var filas = table.rows.length-1;
              var ventas_x_prod_Total = 0;
              for (var idx=1;idx<filas;idx++){
                  var unidades_vendidas = convNro(document.getElementById("unidades_vendidas_"+idx).value);
                  var pventa = convNro(document.getElementById("pventa_"+idx).value);
                  var ventas_x_prod = pventa * unidades_vendidas;
                  // var ventas_x_prod = convNro(document.getElementById("ventas_x_prod_"+idx).value);
                  // if(!isNaN(ventas_x_prod)){
                  ventas_x_prod_Total += ventas_x_prod;
                  // }
              }
              document.getElementById("vtas_comercio_base").innerHTML = Number(ventas_x_prod_Total).toLocaleString('en');
              document.getElementById("vtas_comercio_base").value = ventas_x_prod_Total;
              document.getElementById("ventas_x_prod_Total").innerHTML = Number(ventas_x_prod_Total).toLocaleString('en');
              document.getElementById("ventas_x_prod_Total").value = ventas_x_prod_Total;
              
              document.getElementById("egp_ventas").innerHTML = Number(ventas_x_prod_Total).toLocaleString('en');
              document.getElementById("egp_ventas").value = ventas_x_prod_Total;
          }
          function calcular_util_bruta(idx){
              var pcompra = convNro(document.getElementById("pcompra_"+idx).value);
              var pventa = convNro(document.getElementById("pventa_"+idx).value);
              var util_bruta = 0;
              if(pventa !=0){
                  util_bruta = 1-pcompra/pventa;
              }
              document.getElementById("util_bruta_"+idx).innerHTML = Number(util_bruta).toLocaleString('en');
              document.getElementById("util_bruta_"+idx).value = util_bruta;
              calcular_util_bruta_Total();
          }
          function calcular_util_bruta_Total(){
              var table = document.getElementById("tablaProductos");
              var filas = table.rows.length-1;
              var util_bruta_Total = 0;
              for (var idx=1;idx<filas;idx++){
                  var pcompra = convNro(document.getElementById("pcompra_"+idx).value);
                  var pventa = convNro(document.getElementById("pventa_"+idx).value);
                  var util_bruta = 0;
                  if(pventa !=0){
                      util_bruta = 1-pcompra/pventa;
                  }
                  util_bruta_Total += util_bruta;
              }
              document.getElementById("util_bruta_Total").innerHTML = Number(util_bruta_Total).toLocaleString('en');
              document.getElementById("util_bruta_Total").value = util_bruta_Total;
          }
          function calcular_informalidad(){
              var declarado = convNro(document.getElementById("declarado").value);
              var real = convNro(document.getElementById("vtas_comercio_base").value);
              if (real > 0) {
                  var informalidad = Number((1 - declarado / real) * 100).toFixed();
                  document.getElementById("informalidad").innerHTML = informalidad + "%";
                  document.getElementById("informalidad").value = informalidad;
              } else {
                  document.getElementById("informalidad").innerHTML = "";
              }
              var egp_impuestos = declarado * 0.015;
              document.getElementById("egp_impuestos").value = egp_impuestos;
              egp_impuestos = Number(egp_impuestos).toFixed(0);
              document.getElementById("egp_impuestos").innerHTML = Number(egp_impuestos).toLocaleString('en');
              
          }
          function calcular_Margen_Utilidad_Bruta(){
              var table = document.getElementById("tablaProductos");
              var filas = table.rows.length-1;
              var margen_utilidad_bruta = 0
              for (var idx=1;idx<filas;idx++){
                  var pcompra = convNro(document.getElementById("pcompra_"+idx).value);
                  var unidades_vendidas = convNro(document.getElementById("unidades_vendidas_"+idx).value);
                  margen_utilidad_bruta += pcompra * unidades_vendidas;
              }
              var vtas_comercio_base = convNro(document.getElementById("vtas_comercio_base").value);
              if(vtas_comercio_base != 0){
                  margen_utilidad_bruta = (1 - (convNro(margen_utilidad_bruta)/vtas_comercio_base))*100;
                  document.getElementById("margen_bruto").innerHTML = Number(margen_utilidad_bruta).toFixed() + "%";
                  document.getElementById("margen_bruto").value = Number(margen_utilidad_bruta).toFixed();
              }
              var margen_bruto_referencial = convNro(document.getElementById("margen_bruto_referencial").value);
              var egp_costoven = 0;
              if(margen_utilidad_bruta>margen_bruto_referencial){
                  egp_costoven = (100-margen_bruto_referencial) * vtas_comercio_base /100;
              }else{
                  egp_costoven = (100-margen_utilidad_bruta) * vtas_comercio_base/100;
              }
              document.getElementById("egp_costoven").innerHTML = Number(Number(egp_costoven).toFixed()).toLocaleString('en');;
              document.getElementById("egp_costoven").value = Number(egp_costoven).toFixed();
          }
          
          function calcular_ingresos_comercio(){
              var table = document.getElementById("tablaProductos");
              var filas = table.rows.length-1;
              for (var idx=1;idx<filas;idx++){
                  calcular_util_bruta(idx);
                  calcular_ventas_prod(idx)
              }
              calcular_informalidad();
              calcular_Margen_Utilidad_Bruta();
              Calcular_EGP();
          }
          function calcular_planilla_comercio() {
              var num = convNro(document.getElementById("num_planilla_comercio").value);
              var sueldo = convNro(document.getElementById("sueldo_planilla_comercio").value);
              if (num > 0 && sueldo > 0) {
                  document.getElementById("total_planilla_comercio").innerHTML = Number(num * sueldo).toLocaleString('en');
                  document.getElementById("total_planilla_comercio").value = Number(num * sueldo);
                  document.getElementById("gastop_comercio_1").innerHTML = Number(num * sueldo).toLocaleString('en');
                  document.getElementById("gastop_comercio_1").value = Number(num * sueldo);
              } else {
                  document.getElementById("total_planilla_comercio").innerHTML = "";
                  document.getElementById("total_planilla_comercio").value = 0;
                  document.getElementById("gastop_comercio_1").innerHTML = "";
                  document.getElementById("gastop_comercio_1").value = 0;
              }
          }
          function calcular_gastop_comercio() {
              calcular_planilla_comercio();
              var gastop1 = convNro(document.getElementById("gastop_comercio_1").value);
              var gastop2 = convNro(document.getElementById("gastop_comercio_2").value);
              var gastop3 = convNro(document.getElementById("gastop_comercio_3").value);
              var gastop4 = convNro(document.getElementById("gastop_comercio_4").value);
              var gastop5 = convNro(document.getElementById("gastop_comercio_5").value);
              document.getElementById("total_gastop_comercio").innerHTML = Number(gastop1 + gastop2 + gastop3 + gastop4 + gastop5).toLocaleString('en');
              document.getElementById("total_gastop_comercio").value = Number(gastop1 + gastop2 + gastop3 + gastop4 + gastop5);
              document.getElementById("egp_gastop").innerHTML = Number(gastop1 + gastop2 + gastop3 + gastop4 + gastop5).toLocaleString('en');
              document.getElementById("egp_gastop").value = Number(gastop1 + gastop2 + gastop3 + gastop4 + gastop5);
              Calcular_EGP();
          }
          function calcular_gastopersonal() {
              var gasto1 = convNro(document.getElementById("miembros").value) * 360;
              var gasto2 = convNro(document.getElementById("alquiler").value);
              var gasto3 = convNro(document.getElementById("deuda_personal").value);
              var gasto4 = convNro(document.getElementById("otros_personal").value);
          
              document.getElementById("gastos_implicitos").innerHTML = Number(gasto1).toLocaleString('en');
              document.getElementById("total_gastpersonal").innerHTML = Number(gasto1 + gasto2 + gasto3 + gasto4).toLocaleString('en');
              document.getElementById("gastos_implicitos").value = Number(gasto1);
              document.getElementById("total_gastpersonal").value = Number(gasto1 + gasto2 + gasto3 + gasto4);
              document.getElementById("egp_gastfam").innerHTML = Number(gasto1 + gasto2 + gasto3 + gasto4).toLocaleString('en');
              document.getElementById("egp_gastfam").value = Number(gasto1 + gasto2 + gasto3 + gasto4);
              Calcular_EGP();
          }
          function calcular_valor_declarado(idx){
              var Metraje = convNro(document.getElementById("Metraje_"+idx).value);
              var Precio = convNro(document.getElementById("Precio_"+idx).value);
              var Val_Inm_Dec = Metraje * Precio;
              document.getElementById("Val_Inm_Dec_"+idx).innerHTML = Number(Val_Inm_Dec).toLocaleString('en');
              document.getElementById("Val_Inm_Dec_"+idx).value = Val_Inm_Dec;
              return convNro(Val_Inm_Dec);
          }
          function calcular_valor_declarado_Total(){
              var table = document.getElementById("tablaPatrimonioInmueble");
              var filas = table.rows.length-1;
              var Val_Inm_Dec_Total = 0;
              for (var idx=1;idx<filas;idx++){
                  Val_Inm_Dec_Total += calcular_valor_declarado(idx);
              }
              document.getElementById("Val_Inm_Dec_Total").innerHTML = Number(Val_Inm_Dec_Total).toLocaleString('en');
              document.getElementById("Val_Inm_Dec_Total").value = Val_Inm_Dec_Total;
              calcular_valor_evaluado_Total();
          }
          function calcular_valor_evaluado(idx){
              var Realizable = document.getElementById("Realizable_"+idx).value
              var factor = 0;
              if(Realizable == "Si"){
                  factor = 0.75;
              }else if(Realizable == "No"){
                  factor = 0.5;
              }
              var Val_Inm_Dec = convNro(document.getElementById("Val_Inm_Dec_"+idx).value);
              var Val_Inm_Eva = Val_Inm_Dec * factor;
              document.getElementById("Val_Inm_Eva_"+idx).innerHTML = Number(Val_Inm_Eva).toLocaleString('en');
              document.getElementById("Val_Inm_Eva_"+idx).value = Val_Inm_Eva;
              if(factor == 0){
                      document.getElementById("Val_Inm_Eva_"+idx).innerHTML = Number(Val_Inm_Eva).toLocaleString('en');
                      document.getElementById("Val_Inm_Eva_"+idx).value = Val_Inm_Eva;
              }
              return convNro(Val_Inm_Eva);
          }
          
          function calcular_valor_evaluado_Total(){
              var table = document.getElementById("tablaPatrimonioInmueble");
              var filas = table.rows.length-1;
              var Val_Inm_Eva_Total = 0;
              for (var idx=1;idx<filas;idx++){
                  Val_Inm_Eva_Total += calcular_valor_evaluado(idx);
              }
              document.getElementById("Val_Inm_Eva_Total").innerHTML = Number(Val_Inm_Eva_Total).toLocaleString('en');
              document.getElementById("Val_Inm_Eva_Total").value = Val_Inm_Eva_Total;
              
              document.getElementById("bg_13").innerHTML = Number(Val_Inm_Eva_Total).toLocaleString('en');
              document.getElementById("bg_13").value = Val_Inm_Eva_Total;
              Calcular_BG();
          }
          function Agregar_Financimiento_LP(){
              var vIndex = [];
              vIndex.push("Inicio")
              var idx = Number(document.getElementById("cant_finan_LP").value);
              var total = idx;
              var i = 1;
              while(i<=total){
                  vIndex.push(document.getElementById("Tipo_Prod_LP_"+i).selectedIndex)
                  i = i+1;
              }
              
              i= 1;
              idx += 1;
              var financiamiento = '<div class="col-xs-12" id = "Largo_Plazo_'+idx+'" style="height:547px;">'+
                                      '<h1>Largo Plazo</h1>'+
                                      '<h3>('+idx+'° Financiamiento)</h3>'+
                                      '<table class="table table-hover">'+
                                      '	<tr><th colspan="3" class="cabezera">Propuesta de financiamiento Largo Plazo</th></tr>'+
                                      '	<tr>'+
                                      '		<td>Tipo de producto</td>'+
                                      '		<td colspan="2">'+
                                      '			<select class="form-control" id="Tipo_Prod_LP_'+idx+'" onchange="Calcular_Propuestas_LP();">'+
                                      '				<option value="0"></option>'+
                                      '				<option value="Leasing Mobiliario">Leasing Mobiliario</option>'+
                                      '				<option value="Leasing Inmobiliario">Leasing Inmobiliario</option>'+
                                      '				<option value="Préstamo para adquisición de inmueble">Préstamo para adquisición de inmueble</option>'+
                                      '				<option value="Préstamo para adquisición de bienes muebles">Préstamo para adquisición de bienes muebles</option>'+
                                      '				<option value="Subrogación de deuda">Subrogación de deuda</option>'+
                                      '				<option value="Otro">Otro</option>'+
                                      '			</select>'+
                                      '		</td>'+
                                      '	</tr>'+
                                      '	<tr>'+
                                      '		<td>Precio Venta</td>'+
                                      '		<td><input min="0"  class="form-control" id="Precio_Venta_'+idx+'" onkeyup="validarNumero(id);Calcular_Propuestas_LP();"/></td>'+
                                      '		<td>100%</td>'+
                                      '	</tr>'+
                                      '	<tr>'+
                                      '		<td style="width:40%;">Importe de Financiamiento</td>'+
                                      '		<td><input  min="0"  class="form-control" id="Finan_LP_'+idx+'" onkeyup="validarNumero(id);Calcular_Propuestas_LP();" /></td>'+
                                      '		<td><div id="Porc_LP_1_1"></div></td>'+
                                      '	</tr>'+
                                      '	<tr>'+
                                      '		<td>Cuota Inicial</td><td><div id="Cuota_Inicial_LP_'+idx+'"></div></td><td><div id="Porc_LP_1_2"></div></td>'+
                                      '	</tr>'+
                                      '	<tr>'+
                                      '		<td>Tasa anual</td><td><div><input style = "width:24.5%; display:inline"  min="0"  id="TEA_LP_'+idx+'" class="form-control" onkeyup="validarNumero(id);Calcular_Propuestas_LP();"/><b>&nbsp;%</b></div></td><td></td>'+
                                      '	</tr>'+
                                      '	<tr>'+
                                      '		<td>Tasa mensual</td><td><div id="TEM_LP_'+idx+'"></div></td><td></td>'+
                                      '	</tr>'+
                                      '	<tr>'+
                                      '		<td>Cuota</td><td><div id="Cuota_LP_'+idx+'"></div></td><td></td>'+
                                      '	</tr>'+
                                      '	<tr>'+
                                      '		<td>Plazo (Meses)</td><td><input  min="0"  class="form-control" id="Plazo_LP_'+idx+'" onkeyup="validarNumero(id);Calcular_Propuestas_LP()"/></td><td></td>'+
                                      '	</tr>'+
                                      '	<tr>'+
                                      '		<td>Gtia para Prop:</td><td><input  min="0"  class="form-control" id="GTIA_LP_'+idx+'" onkeyup="validarNumero(id);Calcular_Propuestas_LP();"/></td><td></td>'+
                                      '	</tr>'+
                                      '</table>'+
                                      '<input type="hidden" id="Cuota_LP_'+idx+'_hidden" name="Cuota_LP_'+idx+'_hidden">'+
                                  '</div>';
                              
              
              
              document.getElementById("Financimiento_LP").innerHTML += financiamiento;
              document.getElementById("cant_finan_LP").value = idx;
              
              while(i<=total){
                  document.getElementById("Tipo_Prod_LP_"+i).selectedIndex = vIndex[i]
                  i = i+1;
              }
              
          }
          function Agregar_Financimiento_CP(){
              var vIndex = [];
              vIndex.push("Inicio")
              var idx = Number(document.getElementById("cant_finan_CP").value);
              var total = idx;
              var i = 1;
              while(i<=total){
                  vIndex.push(document.getElementById("Tipo_Prod_CP_"+i).selectedIndex)
                  i = i+1;
              }
              
              i= 1;
              idx += 1;
              var financiamiento = '<div class="col-xs-12" id = "Corto_Plazo_'+idx+'" style="height:547px;">'+
          '							<h1>Corto Plazo</h1>'+
          '							<h3>('+idx+'° Financiamiento)</h3>'+
          '							<table class="table table-hover">'+
          '								<tr><th colspan="2" class="cabezera">Propuesta de financiamiento Corto Plazo</th></tr>'+
          '								<tr>'+
          '									<td>Tipo de producto</td>'+
          '									<td>'+
          '										<select class="form-control" id="Tipo_Prod_CP_'+idx+'" onchange="Calcular_Propuestas_CP();">'+
          '											<option value=""></option>'+
          '											<option value="Financiamiento de Importación">Financiamiento de Importación</option>'+
          '											<option value="Financiamiento de Exportación">Financiamiento de Exportación</option>'+
          '											<option value="Préstamo para capital de trabajo">Préstamo para capital de trabajo</option>'+
          '											<option value="Tarjeta capital de trabajo">Tarjeta capital de trabajo</option>'+
          '											<option value="Descuento de letra/factura negociable">Descuento de letra/factura negociable</option>'+
          '											<option value="Tarjeta Empresarial">Tarjeta empresarial</option>'+
          '											<option value="Préstamo para adquisición de bienes muebles pequeños">Préstamo para adquisición de bienes muebles pequeños</option>'+
          '											<option value="Subrogación de deuda">Subrogación de deuda</option>'+
          '											<option value="Incremento de línea de TKT">Incremento de línea de TKT</option>'+
          '											<option value="Incremento de línea de T/C">Incremento de línea de T/C empresarial</option>'+
          '											<option value="Otro">Otro</option>'+
          '										</select>'+
          '									</td>'+
          '								</tr>'+
          '								<tr>'+
          '									<td style="width:40%;">Importe de Financiamiento</td>'+
          '									<td><input  min="0"  id="Finan_CP_'+idx+'" class="form-control" onkeyup="validarNumero(id);Calcular_Propuestas_CP()"/></td>'+
          '								</tr>'+
          '								<tr>'+
          '									<td>Tasa anual</td>'+
          '									<td><div><input style="width:20%; display:inline;"  min="0"  id="TEA_CP_'+idx+'" class="form-control" onkeyup="validarNumero(id);Calcular_Propuestas_CP();"/> <b>%</b></div></td>'+
          '								</tr>'+
          '								<tr>'+
          '									<td>Tasa mensual</td>'+
          '									<td><div id="TEM_CP_'+idx+'"></div></td>'+
          '								</tr>'+
          '								<tr>'+
          '									<td>Cuota</td>'+
          '									<td><div id="Cuota_CP_'+idx+'"></div></td>'+
          '								</tr>'+
          '								<tr>'+
          '									<td>Plazo (Meses)</td>'+
          '									<td><input  min="0"  id="Plazo_CP_'+idx+'" class="form-control" onkeyup="validarNumero(id);Calcular_Propuestas_CP()"/></td>'+
          '								</tr>'+
          '								<tr>'+
          '									<td>Gastos finan. 1°cuota</td>'+
          '									<td><div id="GastFin_CP_'+idx+'"></div></td>'+
          '								</tr>'+
          '							</table>'+
          '							<input type="hidden" id="GastFin_CP_'+idx+'_hidden" name="GastFin_CP_'+idx+'_hidden"/>'+
          '                         <input type="hidden" id="Cuota_CP_'+idx+'_hidden" name="Cuota_CP_'+idx+'_hidden">'+
          '						</div>'
                              
                              
              
              
              document.getElementById("Financimiento_CP").innerHTML += financiamiento;
              document.getElementById("cant_finan_CP").value = idx;
              
              
              while(i<=total){
                  document.getElementById("Tipo_Prod_CP_"+i).selectedIndex = vIndex[i]
                  i = i+1;
              }
              Calcular_Propuestas_CP();
              
          }
          function Eliminar_Financimiento_LP(){
              var idx = document.getElementById("cant_finan_LP").value;
              if(idx>0){
                  var padre = document.getElementById("Financimiento_LP");
                  var hijo = document.getElementById("Largo_Plazo_"+idx);
                  var oldChild = padre.removeChild(hijo);
                  document.getElementById("cant_finan_LP").value = idx-1;
              }
          }
          function Eliminar_Financimiento_CP(){
              var idx = document.getElementById("cant_finan_CP").value;
              if(idx>0){
                  var padre = document.getElementById("Financimiento_CP");
                  var hijo = document.getElementById("Corto_Plazo_"+idx);
                  var oldChild = padre.removeChild(hijo);
                  document.getElementById("cant_finan_CP").value = idx-1;
              }
          }
          function Calcular_Propuestas_LP(){
              var idx = document.getElementById("cant_finan_LP").value;
              
              
              for (var i = 1; i <= idx;i++){
                  var Tipo_Prod = document.getElementById("Tipo_Prod_LP_"+i).value;
                  document.getElementById("Tipo_Prod_LP_"+i).setAttribute('value',Tipo_Prod);
                  var vIndex = document.getElementById("Tipo_Prod_LP_"+i).selectedIndex;    
                  document.getElementById("Tipo_Prod_LP_"+i).setAttribute('selectedIndex',vIndex);
                  
                  Calcular_Cuota_Inicial_LP(i);
                  Calcular_Porcentajes_LP(i);
                  Calcular_Tasa_Mensual_LP(i);
                  Calcular_Cuota_LP(i);
              }
              Calcular_EGP();
              Calcular_Porcentajes_BG();
          }
          function Calcular_Cuota_Inicial_LP(idx) {
              var Tipo_Prod = document.getElementById("Tipo_Prod_LP_"+idx).value;
              if(Tipo_Prod !="Subrogación de deuda"){
                  var Precio_Venta = convNro(document.getElementById("Precio_Venta_"+idx).value);
                  var Finan_LP = convNro(document.getElementById("Finan_LP_"+idx).value);
                  var Cuota_Inicial = Precio_Venta - Finan_LP;
                  if (Precio_Venta > Finan_LP) {
                      document.getElementById("Cuota_Inicial_LP_"+idx).innerHTML = Number(Cuota_Inicial).toLocaleString('en');
                      document.getElementById("Cuota_Inicial_LP_"+idx).value = Cuota_Inicial;
                  } else {
                      document.getElementById("Cuota_Inicial_LP_"+idx).innerHTML = "";
                      document.getElementById("Cuota_Inicial_LP_"+idx).value = 0;
                  }
              }else{
                  document.getElementById("Cuota_Inicial_LP_"+idx).innerHTML = "";
                  document.getElementById("Cuota_Inicial_LP_"+idx).value = 0;	
              }
          }
          function Calcular_Porcentajes_LP(idx) {
              var Precio_Venta = convNro(document.getElementById("Precio_Venta_"+idx).value);
              var Finan_LP = convNro(document.getElementById("Finan_LP_"+idx).value);
              var Cuota_Inicial = convNro(document.getElementById("Cuota_Inicial_LP_"+idx).value);
              var Porc_Finan = Finan_LP / Precio_Venta * 100;
              var Porc_Cuota = Cuota_Inicial / Precio_Venta * 100;
              
              if (Precio_Venta > Finan_LP) {
                  document.getElementById("Porc_LP_1_1").innerHTML = Number(Porc_Finan).toFixed(0) + "%";
                  document.getElementById("Porc_LP_1_1").value = Porc_Finan;
                  
                  document.getElementById("Porc_LP_1_2").innerHTML = Number(Porc_Cuota).toFixed(0) + "%";
                  document.getElementById("Porc_LP_1_2").value = Porc_Cuota;
              } else {
                  document.getElementById("Porc_LP_1_1").innerHTML = "";
                  document.getElementById("Porc_LP_1_1").value = 0;
                  document.getElementById("Porc_LP_1_2").innerHTML = "";
                  document.getElementById("Porc_LP_1_2").value = 0;
              }
          }
          function Calcular_Tasa_Mensual_LP(idx) {
              var TEA_LP = convNro(document.getElementById("TEA_LP_"+idx).value);
              
              if ( TEA_LP > 0) {
                  var TEM_LP = ((Math.pow(1 + TEA_LP / 100, 1 / 12) - 1) * 100);
              
                  document.getElementById("TEM_LP_"+idx).innerHTML = Number(TEM_LP).toFixed(2) + "%";
                  document.getElementById("TEM_LP_"+idx).value = Number(TEM_LP).toFixed(2) + "%";
              } else {
                  document.getElementById("TEM_LP_"+idx).innerHTML = "";
              }
          }
          function Calcular_Cuota_LP(idx) {
              var Plazo_LP = convNro(document.getElementById("Plazo_LP_"+idx).value);
              var Finan_LP = convNro(document.getElementById("Finan_LP_"+idx).value);
              var TEA_LP = convNro(document.getElementById("TEA_LP_"+idx).value);
              
              if (Plazo_LP > 0 && Finan_LP > 0 && TEA_LP > 0) {
          
                  var TEM_LP = Math.pow(1 + TEA_LP / 100, 1 / 12) - 1;
                  document.getElementById("Cuota_LP_"+idx).innerHTML = Number((Finan_LP / ((1 - Math.pow(1 + TEM_LP, -Plazo_LP)) / (TEM_LP))).toFixed()).toLocaleString('en');
                  document.getElementById("Cuota_LP_"+idx).value = Number((Finan_LP / ((1 - Math.pow(1 + TEM_LP, -Plazo_LP)) / (TEM_LP))).toFixed());
                  document.getElementById("Cuota_LP_"+idx+"_hidden").value = Finan_LP / ((1 - Math.pow(1 + TEM_LP, -Plazo_LP)) / (TEM_LP));
                  document.getElementById("Cuota_LP_"+idx+"_hidden").setAttribute('value',(Finan_LP / ((1 - Math.pow(1 + TEM_LP, -Plazo_LP)) / (TEM_LP))));
                 
              } else {
                  document.getElementById("Cuota_LP_"+idx).innerHTML = "";
              }
          }
          
          function Calcular_Cuotas_LP_Total(){
              var idx = document.getElementById("cant_finan_LP").value;
              var total = 0;
              for (var i = 1; i <= idx;i++){
                  total = total + convNro(document.getElementById("Cuota_LP_"+idx).value);
              }
              return total;
          }
          function Calcular_Propuestas_CP(){
              var idx = document.getElementById("cant_finan_CP").value;
              
              for (var i = 1; i <= idx;i++){
                  var Tipo_Prod = document.getElementById("Tipo_Prod_CP_"+i).value;
                  document.getElementById("Tipo_Prod_CP_"+i).setAttribute('value',Tipo_Prod);
                  var vIndex = document.getElementById("Tipo_Prod_CP_"+i).selectedIndex;    
                  document.getElementById("Tipo_Prod_CP_"+i).setAttribute('selectedIndex',vIndex);
                  
                  Calcular_Tasa_Mensual_CP(i);
                  Calcular_Cuota_CP(i);
                  Calcular_GastFin_CP(i);
              }
              Calcular_EGP();
          }
          function Calcular_Tasa_Mensual_CP(idx) {
              var TEA_CP = convNro(document.getElementById("TEA_CP_"+idx).value);
              if ( TEA_CP > 0) {
                  var TEM_CP = ((Math.pow(1 + TEA_CP / 100, 1 / 12) - 1) * 100);
                  document.getElementById("TEM_CP_"+idx).innerHTML = Number(TEM_CP).toFixed(2) + "%";
                  document.getElementById("TEM_CP_"+idx).value = Number(TEM_CP).toFixed(2) + "%";
              } else {
                  document.getElementById("TEM_CP_"+idx).innerHTML = "";
              }
          }
          function Calcular_Cuota_CP(idx) {
              var Plazo_CP = convNro(document.getElementById("Plazo_CP_"+idx).value);
              var Finan_CP = convNro(document.getElementById("Finan_CP_"+idx).value);
              var TEA_CP = convNro(document.getElementById("TEA_CP_"+idx).value);
              
              if (Plazo_CP > 0 && Finan_CP > 0 && TEA_CP > 0) {
          
                  var TEM_CP = Math.pow(1 + TEA_CP / 100, 1 / 12) - 1;
                  document.getElementById("Cuota_CP_"+idx).innerHTML = Number((Finan_CP / ((1 - Math.pow(1 + TEM_CP, -Plazo_CP)) / (TEM_CP))).toFixed()).toLocaleString('en');
                  document.getElementById("Cuota_CP_"+idx).value = Number((Finan_CP / ((1 - Math.pow(1 + TEM_CP, -Plazo_CP)) / (TEM_CP))).toFixed());
                  document.getElementById("Cuota_CP_"+idx+"_hidden").value = Finan_CP / ((1 - Math.pow(1 + TEM_CP, -Plazo_CP)) / (TEM_CP));
                  document.getElementById("Cuota_CP_"+idx+"_hidden").setAttribute('value',(Finan_CP / ((1 - Math.pow(1 + TEM_CP, -Plazo_CP)) / (TEM_CP))));
              } else {
                  document.getElementById("Cuota_CP_"+idx).innerHTML = "";
                  document.getElementById("Cuota_CP_"+idx+"_hidden").setAttribute('value',0);
              }
          }
          function Calcular_GastFin_CP(idx) {
              var Finan_CP = convNro(document.getElementById("Finan_CP_"+idx).value);
              var TEA_CP = convNro(document.getElementById("TEA_CP_"+idx).value);
              if (Finan_CP > 0 && TEA_CP > 0) {
                  
                  var GastFin_CP = Finan_CP * (Math.pow(1 + TEA_CP / 100, 1 / 12) - 1);
                  
                  document.getElementById("GastFin_CP_"+idx).innerHTML = Number(GastFin_CP.toFixed()).toLocaleString('en');
                  document.getElementById("GastFin_CP_"+idx).value = GastFin_CP.toFixed();
                  
                  document.getElementById("GastFin_CP_"+idx+"_hidden").value = GastFin_CP;
                  document.getElementById("GastFin_CP_"+idx+"_hidden").setAttribute('value',GastFin_CP);
                  return convNro(GastFin_CP);
              } else {
                  document.getElementById("GastFin_CP_"+idx).innerHTML = "";
                  document.getElementById("GastFin_CP_"+idx+"_hidden").value = 0;
                  document.getElementById("GastFin_CP_"+idx+"_hidden").setAttribute('value','');
                  return 0;
              }
              
          }
          function Calcular_Valor_Bien(idx){
              var Veh_Maq = document.getElementById("Veh_Maq_"+idx).value;
              var Valor_Nuevo = convNro(document.getElementById("Valor_Nuevo_"+idx).value);
              var Antiguedad = convNro(document.getElementById("Antiguedad_"+idx).value);
              var Factor = 0;
              var Valor_Bien = 0;
              if(Veh_Maq!=0 && Valor_Nuevo>0 && Antiguedad >0){
                  if(Veh_Maq == "Vehiculo"){
                      switch (true){
                          case (0<Antiguedad && Antiguedad<3):
                              Factor = 1;
                              break;
                          case (2<Antiguedad && Antiguedad<5):
                              Factor = 0.8;
                              break;
                          case (4<Antiguedad && Antiguedad<7):
                              Factor = 0.6;
                              break;
                          case (6<Antiguedad && Antiguedad<9):
                              Factor = 0.4;
                              break;
                          case (8<Antiguedad):
                              Factor = 0.2;
                              break;
                      }
                  }else if(Veh_Maq == "Maquinaria"){
                      switch (true){
                          case (0<Antiguedad && Antiguedad<5):
                              Factor = 1;
                              break;
                          case (4<Antiguedad && Antiguedad<10):
                              Factor = 0.7;
                              break;
                          case (9<Antiguedad && Antiguedad<15):
                              Factor = 0.5;
                              break;
                          case (14<Antiguedad):
                              Factor = 0.3;
                              break;
                      }		
                  }
                  Valor_Bien = Valor_Nuevo * Factor;
                  document.getElementById("Valor_Bien_"+idx).innerHTML = Number(Valor_Bien).toLocaleString('en');
                  document.getElementById("Valor_Bien_"+idx).value = Valor_Bien;
              }else{
                  document.getElementById("Valor_Bien_"+idx).innerHTML = '';
                  document.getElementById("Valor_Bien_"+idx).value = '';
              }
              return Valor_Bien;
          }
          function Calcular_Valor_Bien_Total(){
              var table = document.getElementById("tablaPatrimonioVehiculos");
              var filas = table.rows.length-1;
              var Valor_Bien_Total = 0;
              for (var idx=1;idx<filas;idx++){
                  Valor_Bien_Total += Calcular_Valor_Bien(idx);
              }
              
              document.getElementById("Valor_Bien_Total").innerHTML = Number(Valor_Bien_Total).toLocaleString('en');
              document.getElementById("Valor_Bien_Total").value = Valor_Bien_Total;
              
              document.getElementById("bg_14").innerHTML = Number(Valor_Bien_Total).toLocaleString('en');
              document.getElementById("bg_14").value = Valor_Bien_Total;
              Calcular_BG();
          }
          
          function Calcular_EGP(){
              var ventas = convNro(document.getElementById("egp_ventas").value);
              var costo = convNro(document.getElementById("egp_costoven").value);
              var gOperativo = convNro(document.getElementById("egp_gastop").value);
              var uOperativa = ventas - costo - gOperativo;
              document.getElementById("egp_uoperativa").innerHTML = Number(uOperativa).toLocaleString('en');
              document.getElementById("egp_uoperativa").value = uOperativa;
              var egp_gastfinan = Calcular_Gastos_Financieros();
              var egp_gastfam = convNro(document.getElementById("egp_gastfam").value);
              var egp_otrosing = convNro(document.getElementById("egp_otrosing").value);
              var egp_impuestos = convNro(document.getElementById("egp_impuestos").value);
              var egp_uneta = uOperativa - egp_gastfinan - egp_gastfam + egp_otrosing - egp_impuestos;
              document.getElementById("egp_uneta").value = egp_uneta;
              document.getElementById("egp_uneta").innerHTML = Number(Number(egp_uneta).toFixed(0)).toLocaleString('en');
              Calcular_BG();
              Calcular_EGP_P();
              Calcular_Ratios();
          }
          function Calcular_Gastos_Financieros(){
              var egp_gastfinan = 0;
              var suma1 = 0;
              
              
              var PA_table = document.getElementById("tablaPrestamoAdquisicion");
              var PA_filas = PA_table.rows.length-1;
              var PA_S5 = 0;
              for (var idx=0;idx<PA_filas;idx++){
                  PA_S5 = PA_S5 + convNro(document.getElementById("PA_Cuota_Pagar_Aprox_"+idx).value);
              }
              
              var cuotas = Calcular_Cuotas_LP_Total();
              
              suma1 = convNro(cuotas) + convNro(PA_S5);
              
              
              var suma2 = 0;
              
              var LTC_table = document.getElementById("tablaLineaTarjetaCapital");
              var LTC_filas = LTC_table.rows.length-1;
              var PCCT_table = document.getElementById("tablaPrestamoComercial");
              var PCCT_filas = PCCT_table.rows.length-1;
              var PC_table = document.getElementById("tablaPrestamoCancelable");
              var PC_filas = PC_table.rows.length-1;
              
              var S1 = 0;
              var LTC_S1 = 0;
              for (var idx=0;idx<LTC_filas;idx++){
                  LTC_S1 = LTC_S1 + convNro(document.getElementById("LTC_Costo_Financiero_"+idx).value);
              }
              var PCCT_S1 = 0;
              for (var idx=0;idx<PCCT_filas;idx++){
                  PCCT_S1 = PCCT_S1 + convNro(document.getElementById("PCCT_Costo_Financiero_"+idx).value);
              }
              
              S1 = LTC_S1 + PCCT_S1;
              
              var S2 = 0;
              var PC_S2 = 0;
              for (var idx=0;idx<PC_filas;idx++){
                  PC_S2 = PC_S2 + convNro(document.getElementById("PC_Costo_Financiero_"+idx).value);
              }
              
              var i1 = convNro(S1) + convNro(PC_S2);
              
              
              var i2 = 0;
              
              var idx = document.getElementById("cant_finan_CP").value;
              for (var i = 1; i <= idx;i++){
                  i2 = i2 + Calcular_GastFin_CP(i);
              }
              
              
              
              suma2 = i1 + i2;
              egp_gastfinan = suma1 + suma2;
              document.getElementById("egp_gastfinan").value = egp_gastfinan;
              egp_gastfinan = Number(egp_gastfinan).toFixed(0);
              document.getElementById("egp_gastfinan").innerHTML = Number(egp_gastfinan).toLocaleString('en');
              return convNro(egp_gastfinan);
          }
          function Calcular_EGP_P(){
              var egp_ventas = convNro(document.getElementById("egp_ventas").value);
            
              if(egp_ventas != 0){
                  document.getElementById("egp_ventas_p").value = "100";
                  document.getElementById("egp_ventas_p").innerHTML = "100%";
                  var egp_costoven = convNro(document.getElementById("egp_costoven").value);
                  var egp_costoven_p = egp_costoven *100 / egp_ventas
                  document.getElementById("egp_costoven_p").value = egp_costoven_p;
                  document.getElementById("egp_costoven_p").innerHTML = Number(egp_costoven_p).toFixed(0) + "%";
                  var egp_gastop = convNro(document.getElementById("egp_gastop").value);
                  var egp_gastop_p = egp_costoven *100/egp_ventas;
                  document.getElementById("egp_gastop_p").value = egp_gastop_p;
                  document.getElementById("egp_gastop_p").innerHTML = Number(egp_gastop_p).toFixed(0) + "%";
                  var egp_uoperativa = egp_ventas - egp_costoven - egp_gastop;
                  var egp_uoperativa_p = egp_uoperativa *100/egp_ventas;
                  document.getElementById("egp_uoperativa_p").value = egp_uoperativa_p;
                  document.getElementById("egp_uoperativa_p").innerHTML = Number(egp_uoperativa_p).toFixed(0) + "%";
                  var egp_gastfinan = convNro(document.getElementById("egp_gastfinan").value);
                  var egp_gastfinan_p = egp_gastfinan *100/egp_ventas;
                  document.getElementById("egp_gastfinan_p").value = egp_gastfinan_p;
                  document.getElementById("egp_gastfinan_p").innerHTML = Number(egp_gastfinan_p).toFixed(0) + "%";
                  var egp_gastfam = convNro(document.getElementById("egp_gastfam").value);
                  var egp_gastfam_p = egp_gastfam *100/egp_ventas;
                  document.getElementById("egp_gastfam_p").value = egp_gastfam_p;
                  document.getElementById("egp_gastfam_p").innerHTML = Number(egp_gastfam_p).toFixed(0) + "%";
                  var egp_otrosing = convNro(document.getElementById("egp_otrosing").value);
                  var egp_otrosing_p = egp_otrosing *100/egp_ventas;
                  document.getElementById("egp_otrosing_p").value = egp_otrosing_p;
                  document.getElementById("egp_otrosing_p").innerHTML = Number(egp_otrosing_p).toFixed(0) + "%";
                  var egp_impuestos = convNro(document.getElementById("egp_impuestos").value);
                  var egp_impuestos_p = egp_impuestos *100/egp_ventas;
                  document.getElementById("egp_impuestos_p").value = egp_impuestos_p;
                  document.getElementById("egp_impuestos_p").innerHTML = Number(egp_impuestos_p).toFixed(0) + "%";
                  var egp_uneta = egp_uoperativa - egp_gastfinan - egp_gastfam + egp_otrosing - egp_impuestos;
                  var egp_uneta_p = egp_uneta *100/egp_ventas;
                  document.getElementById("egp_uneta_p").value = egp_uneta_p;
                  document.getElementById("egp_uneta_p").innerHTML = Number(egp_uneta_p).toFixed(0) + "%";
              }else{
                  document.getElementById("egp_ventas_p").innerHTML = "";
                  document.getElementById("egp_costoven_p").innerHTML = "";
                  document.getElementById("egp_gastop_p").innerHTML = "";
                  document.getElementById("egp_uoperativa_p").innerHTML = "";
                  document.getElementById("egp_gastfinan_p").innerHTML = "";
                  document.getElementById("egp_gastfam_p").innerHTML = "";
                  document.getElementById("egp_otrosing_p").innerHTML = "";
                  document.getElementById("egp_impuestos_p").innerHTML = "";
                  document.getElementById("egp_uneta_p").innerHTML = "";
              }
          }
          function Calcular_Porcentajes_BG(){
              var total_activos = Calcular_Activos();
              
              if(total_activos != 0){
                  var bg_1 = convNro(document.getElementById("bg_1").value);
                  document.getElementById("bg_porc_1").innerHTML = Number(100* bg_1 / total_activos).toFixed(0) + "%";
                  var bg_2 = convNro(document.getElementById("bg_2").value);
                  document.getElementById("bg_porc_2").innerHTML = Number(100* bg_2 / total_activos).toFixed(0) + "%";
                  var bg_3 = convNro(document.getElementById("bg_3").value);
                  document.getElementById("bg_porc_3").innerHTML = Number(100* bg_3 / total_activos).toFixed(0) + "%";
                  var bg_4 = convNro(document.getElementById("bg_4").value);
                  document.getElementById("bg_porc_4").innerHTML = Number(100* bg_4 / total_activos).toFixed(0) + "%";
                  var bg_5 = convNro(document.getElementById("bg_5").value);
                  document.getElementById("bg_porc_5").innerHTML = Number(100* bg_5 / total_activos).toFixed(0) + "%";
                  var bg_6 = convNro(document.getElementById("bg_6").value);
                  document.getElementById("bg_porc_6").innerHTML = Number(100* bg_6 / total_activos).toFixed(0) + "%";
                  var bg_7 = convNro(document.getElementById("bg_7").value);
                  document.getElementById("bg_porc_7").innerHTML = Number(100* bg_7 / total_activos).toFixed(0) + "%";
                  var bg_8 = convNro(document.getElementById("bg_8").value);
                  document.getElementById("bg_porc_8").innerHTML = Number(100* bg_8 / total_activos).toFixed(0) + "%";
                  var bg_9 = convNro(document.getElementById("bg_9").value);
                  document.getElementById("bg_porc_9").innerHTML = Number(100* bg_9 / total_activos).toFixed(0) + "%";
                  var bg_10 = convNro(document.getElementById("bg_10").value);
                  document.getElementById("bg_porc_10").innerHTML = Number(100* bg_10 / total_activos).toFixed(0) + "%";
                  var bg_11 = convNro(document.getElementById("bg_11").value);
                  document.getElementById("bg_porc_11").innerHTML = Number(100* bg_11 / total_activos).toFixed(0) + "%";
                  var total_activo_cte = convNro(document.getElementById("total_activo_cte").value);
                  document.getElementById("total_activo_cte_porc").innerHTML = Number(100* total_activo_cte / total_activos).toFixed(0) + "%";
                  
                  var bg_12 = convNro(document.getElementById("bg_12").value);
                  document.getElementById("bg_porc_12").innerHTML = Number(100* bg_12 / total_activos).toFixed(0) + "%";
                  var bg_13 = convNro(document.getElementById("bg_13").value);
                  document.getElementById("bg_porc_13").innerHTML = Number(100* bg_13 / total_activos).toFixed(0) + "%";
                  var bg_14 = convNro(document.getElementById("bg_14").value);
                  document.getElementById("bg_porc_14").innerHTML = Number(100* bg_14 / total_activos).toFixed(0) + "%";
                  var bg_15 = convNro(document.getElementById("bg_15").value);
                  document.getElementById("bg_porc_15").innerHTML = Number(100*bg_15 / total_activos).toFixed(0) + "%";
                  var total_activo_no_cte = convNro(document.getElementById("total_activo_no_cte").value );
                  document.getElementById("total_activo_no_cte_porc").innerHTML = Number(100*total_activo_no_cte/ total_activos).toFixed(0) + "%";
                  
                  var bg_16 = convNro(document.getElementById("bg_16").value);
                  document.getElementById("bg_porc_16").innerHTML = Number(100*bg_16 / total_activos).toFixed(0) + "%";
                  var bg_17 = convNro(document.getElementById("bg_17").value);
                  document.getElementById("bg_porc_17").innerHTML = Number(100*bg_17 / total_activos).toFixed(0) + "%";
                  var bg_18 = convNro(document.getElementById("bg_18").value);
                  document.getElementById("bg_porc_18").innerHTML = Number(100*bg_18 / total_activos).toFixed(0) + "%";
                  var total_pasivo_cte = convNro(document.getElementById("total_pasivo_cte").value);
                  document.getElementById("total_pasivo_cte_porc").innerHTML = Number(100* total_pasivo_cte/ total_activos).toFixed(0) + "%";
                  
                  var bg_19 = convNro(document.getElementById("bg_19").value)
                  document.getElementById("bg_porc_19").innerHTML = Number(100*bg_19 / total_activos).toFixed(0) + "%";
                  var bg_20 = convNro(document.getElementById("bg_20").value)
                  document.getElementById("bg_porc_20").innerHTML = Number(100*bg_20 / total_activos).toFixed(0) + "%";
                  var bg_21 = convNro(document.getElementById("bg_21").value)
                  document.getElementById("bg_porc_21").innerHTML = Number(100*bg_21 / total_activos).toFixed(0) + "%";
                  var total_pasivo_no_cte = document.getElementById("total_pasivo_no_cte").value;
                  document.getElementById("total_pasivo_no_cte_porc").innerHTML = Number(100* total_pasivo_no_cte/ total_activos).toFixed(0) + "%";
                  
                  var total_pasivo = convNro(document.getElementById("total_pasivo").value)
                  document.getElementById("total_pasivo_porc").innerHTML = Number(100* total_pasivo / total_activos).toFixed(0) + "%";
                  var patrimonio = convNro(document.getElementById("patrimonio").value)
                  document.getElementById("patrimonio_porc").innerHTML = Number(100*patrimonio / total_activos).toFixed(0) + "%";
              }else{
                  document.getElementById("bg_porc_1").innerHTML = "";
                  document.getElementById("bg_porc_2").innerHTML = "";
                  document.getElementById("bg_porc_3").innerHTML = "";
                  document.getElementById("bg_porc_4").innerHTML = "";
                  document.getElementById("bg_porc_5").innerHTML = "";
                  document.getElementById("bg_porc_6").innerHTML = "";
                  document.getElementById("bg_porc_7").innerHTML = "";
                  document.getElementById("bg_porc_8").innerHTML = "";
                  document.getElementById("bg_porc_9").innerHTML = "";
                  document.getElementById("bg_porc_10").innerHTML = "";
                  document.getElementById("bg_porc_11").innerHTML = "";
                  document.getElementById("total_activo_cte_porc").innerHTML = "";
                  
                  document.getElementById("bg_porc_12").innerHTML = "";
                  document.getElementById("bg_porc_13").innerHTML = "";
                  document.getElementById("bg_porc_14").innerHTML = "";
                  document.getElementById("bg_porc_15").innerHTML = "";
                  document.getElementById("total_activo_no_cte_porc").innerHTML = "";
                  
                  document.getElementById("bg_porc_16").innerHTML = "";
                  document.getElementById("bg_porc_17").innerHTML = "";
                  document.getElementById("bg_porc_18").innerHTML = "";
                  document.getElementById("total_pasivo_cte_porc").innerHTML = "";
                  
                  document.getElementById("bg_porc_19").innerHTML = "";
                  document.getElementById("bg_porc_20").innerHTML = "";
                  document.getElementById("bg_porc_21").innerHTML = "";
                  document.getElementById("total_pasivo_no_cte_porc").innerHTML = "";
                  
                  document.getElementById("total_pasivo_porc").innerHTML = "";
                  document.getElementById("patrimonio_porc").innerHTML = "";
                  
              }
          }
          
          function Calcular_BG(){

              Calcular_Activos();
              Calcular_Pasivos();
              Calcular_Patrimonio();
              Calcular_Porcentajes_BG();
              Calcular_Ratios();
          }
          function Calcular_Activos(){
              var actCorrientes = Calcular_Activos_Corrientes();
              var actNoCorrientes = Calcular_Activos_No_Corrientes();
              var total_activo = actCorrientes + actNoCorrientes;
              document.getElementById("total_activo").value = total_activo;
              document.getElementById("total_activo").innerHTML = Number(total_activo).toLocaleString('en');
              return convNro(total_activo);
          }
          function Calcular_Activos_Corrientes(){
              var bg_1 = convNro(document.getElementById("bg_1").value);
              var bg_2 = convNro(document.getElementById("bg_2").value);
              var bg_3 = convNro(document.getElementById("bg_3").value);
              var bg_4 = convNro(document.getElementById("bg_4").value);
              var bg_5 = Calcular_Inventarios();
              var actCorrientes = bg_1 + bg_2 + bg_3 + bg_4 + bg_5;
              document.getElementById("total_activo_cte").value = actCorrientes;
              document.getElementById("total_activo_cte").innerHTML = Number(actCorrientes).toLocaleString('en');
              return convNro(actCorrientes);
          }
          function Calcular_Inventarios(){
              var bg_6 = Calcular_Activos_CP();
              var bg_7 = convNro(document.getElementById("bg_7").value);
              var bg_8 = convNro(document.getElementById("bg_8").value);
              var bg_9 = convNro(document.getElementById("bg_9").value);
              var bg_10 = convNro(document.getElementById("bg_10").value);
              var bg_11 = Calcular_Linea_No_Utilizada();
              var inventarios = bg_6 + bg_7 + bg_8 + bg_9 + bg_10 + bg_11;
              document.getElementById("bg_5").value = inventarios;
              document.getElementById("bg_5").innerHTML = Number(inventarios).toLocaleString('en');
              return convNro(inventarios);
          }
          function Calcular_Activos_CP(){
              var idx = Number(document.getElementById("cant_finan_CP").value);
              var bg_6 = 0;
              for (var i = 0; i<idx; i++){
                  var Finan_CP = convNro(document.getElementById("Finan_CP_"+(i+1)).value);
                  bg_6 = bg_6 + Finan_CP;
              }
              document.getElementById("bg_6").value = bg_6;
              document.getElementById("bg_6").innerHTML = Number(bg_6).toLocaleString('en');
              return convNro(bg_6);
          }
          function Calcular_Linea_No_Utilizada(){
              var bg_11 = 0;
              
              var LTC_table = document.getElementById("tablaLineaTarjetaCapital");
              var LTC_filas = LTC_table.rows.length-1;
              
              var S1 = 0;
              for (var idx=0;idx<LTC_filas;idx++){
                  bg_11 = bg_11 + convNro(document.getElementById("LTC_Linea_Total_"+idx).value) - convNro(document.getElementById("LTC_Linea_Utilizada_"+idx).value);
              }
              
              document.getElementById("bg_11").value = bg_11;
              document.getElementById("bg_11").innerHTML = Number(bg_11).toLocaleString('en');
              
              return convNro(bg_11);
          }
          function Calcular_Activos_No_Corrientes(){
              var bg_12 = Calcular_Activos_LP();
              var bg_13 = convNro(document.getElementById("bg_13").value);
              var bg_14 = convNro(document.getElementById("bg_14").value);
              var bg_15 = convNro(document.getElementById("bg_15").value);
              var actNoCorrientes = bg_12 + bg_13 + bg_14 + bg_15;
              document.getElementById("total_activo_no_cte").value = actNoCorrientes;
              document.getElementById("total_activo_no_cte").innerHTML = Number(actNoCorrientes).toLocaleString('en');
              return convNro(actNoCorrientes);
          }
          function Calcular_Activos_LP(){
              var idx = Number(document.getElementById("cant_finan_LP").value);
              var actLP = 0;
              for (var i = 0; i<idx; i++){
                  var Precio_Venta = convNro(document.getElementById("Precio_Venta_"+(i+1)).value);
                  actLP = actLP + Precio_Venta;
              }
              document.getElementById("bg_12").value = actLP;
              document.getElementById("bg_12").innerHTML = Number(actLP).toLocaleString('en');
              return convNro(actLP);
          }
          function Calcular_Pasivos(){
              var pasCorrientes = Calcular_Pasivos_Corrientes();
              var pasNoCorrientes = Calcular_Pasivos_No_Corrientes();
              var total_pasivo = pasCorrientes + pasNoCorrientes;
              document.getElementById("total_pasivo").value = total_pasivo;
              document.getElementById("total_pasivo").innerHTML = Number(total_pasivo).toLocaleString('en');
              return convNro(total_pasivo)
          }
          function Calcular_Pasivos_Corrientes(){
              var bg_16 = Calcular_Deuda_Financiera_CP();
              var bg_17 = convNro(document.getElementById("bg_17").value);
              var bg_18 = convNro(document.getElementById("bg_18").value);
              var total_pasivo_cte = bg_16 + bg_17 + bg_18;
              document.getElementById("total_pasivo_cte").value = total_pasivo_cte;
              document.getElementById("total_pasivo_cte").innerHTML = Number(total_pasivo_cte).toLocaleString('en');
              return convNro(total_pasivo_cte);
          }
          function Calcular_Deuda_Financiera_CP(){
              var suma_cp = Calcular_Activos_CP();
              
              var LTC_table = document.getElementById("tablaLineaTarjetaCapital");
              var LTC_filas = LTC_table.rows.length-1;
              var PCCT_table = document.getElementById("tablaPrestamoComercial");
              var PCCT_filas = PCCT_table.rows.length-1;
              var PC_table = document.getElementById("tablaPrestamoCancelable");
              var PC_filas = PC_table.rows.length-1;
              
              var S1 = 0;
              var LTC_S1 = 0;
              for (var idx=0;idx<LTC_filas;idx++){
                  LTC_S1 = LTC_S1 + convNro(document.getElementById("LTC_Linea_Total_"+idx).value);
              }
              var PCCT_S1 = 0;
              for (var idx=0;idx<PCCT_filas;idx++){
                  PCCT_S1 = PCCT_S1 + convNro(document.getElementById("PCCT_Mes_Actual_"+idx).value);
              }
              
              S1 = LTC_S1 + PCCT_S1;
              
              var S2 = 0;
              var PC_S2 = 0;
              for (var idx=0;idx<PC_filas;idx++){
                  PC_S2 = PC_S2 + convNro(document.getElementById("PC_Monto_"+idx).value);
              }
              
              var pasCP = convNro(S1) + convNro(PC_S2)+ convNro(suma_cp);
              document.getElementById("bg_16").value = pasCP;
              document.getElementById("bg_16").innerHTML = Number(pasCP).toLocaleString('en');
              return convNro(pasCP);
          }
          function Calcular_Pasivos_No_Corrientes(){
              var bg_19 = Calcular_Deuda_Financiera_LP();
              var bg_20 = convNro(document.getElementById("bg_20").value);
              var bg_21 = convNro(document.getElementById("bg_21").value);
              var total_pasivo_cte = bg_19 + bg_20 + bg_21;
              document.getElementById("total_pasivo_no_cte").value = total_pasivo_cte;
              document.getElementById("total_pasivo_no_cte").innerHTML = Number(total_pasivo_cte).toLocaleString('en');
              return convNro(total_pasivo_cte);
          }
          function Calcular_Pasivos_LP(){
              var idx = Number(document.getElementById("cant_finan_LP").value);
              var pasLP = 0;
              for (var i = 0; i<idx; i++){
                  var Finan_LP = convNro(document.getElementById("Finan_LP_"+(i+1)).value);
                  pasLP = pasLP + Finan_LP;
              }
              
              return convNro(pasLP);
          }
          function Calcular_Deuda_Financiera_LP(){
              var suma_lp = Calcular_Pasivos_LP();
              var PA_table = document.getElementById("tablaPrestamoAdquisicion");
              var PA_filas = PA_table.rows.length-1;
              var PA_S4 = 0;
              
              for (var idx=0;idx<PA_filas;idx++){
                  PA_S4 = PA_S4 + convNro(document.getElementById("PA_Mes_Actual_"+idx).value);
              }
              var pasLP = convNro(suma_lp) + convNro(PA_S4);
              
              document.getElementById("bg_19").value = pasLP;
              document.getElementById("bg_19").innerHTML = Number(pasLP).toLocaleString('en');
              return convNro(pasLP);
          }
          function Calcular_Patrimonio(){
              var activos = Calcular_Activos();
              var pasivos = Calcular_Pasivos();
              var patrimonio = activos - pasivos;
              document.getElementById("patrimonio").value = patrimonio;
              document.getElementById("patrimonio").innerHTML = Number(patrimonio).toLocaleString('en');
              document.getElementById("pasivo_patrimonio").value = activos;
              document.getElementById("pasivo_patrimonio").innerHTML = Number(activos).toLocaleString('en');
              return convNro(patrimonio);
          }
          
          function getDatosCliente(){
              var lista = [];
              var regimen = document.getElementById('regimen').value;
              lista.push(regimen);
              var rvgl = convNro(document.getElementById('rvgl').value);
              lista.push(rvgl);
              var analista = document.getElementById('analista').value;
              lista.push(analista);
              var fechaVisita = document.getElementById('fechaVisita').value;
              lista.push(fechaVisita);
              var oficinas = document.getElementById('oficinas').value;
              lista.push(oficinas);
              var tipoCliente = document.getElementById('tipoCliente').value;
              lista.push(tipoCliente);
              var razonSocial = document.getElementById('razonSocial').value;
              lista.push(razonSocial);
              var ruc = convNro(document.getElementById('ruc').value);
              lista.push(ruc);
              var ubicacion = document.getElementById('ubicacion').value;
              lista.push(ubicacion);
              var aExp = convNro(document.getElementById('aExp').value);
              lista.push(aExp);
              var nroPtosVta = convNro(document.getElementById('nroPtosVta').value);
              lista.push(nroPtosVta);
              var nroAlmacenes = convNro(document.getElementById('nroAlmacenes').value);
              lista.push(nroAlmacenes);
              var actividad = document.getElementById('actividad').value;
              lista.push(actividad);
              var actEspecifica = document.getElementById('actEspecifica').value;
              lista.push(actEspecifica);
              var buro = document.getElementById('buro').value;
              lista.push(buro);
              var nroEnt = convNro(document.getElementById('nroEnt').value);
              lista.push(nroEnt);
              var edadRL = convNro(document.getElementById('edadRL').value);
              lista.push(edadRL);
              if (regimen == "" || rvgl == 0 || fechaVisita == "" || oficinas == "" || tipoCliente == "" || 
                  razonSocial == "" || ruc == 0 || ubicacion == "" || aExp == "" || nroPtosVta == "" || nroAlmacenes == "" || 
                  actividad == "" || actEspecifica == "" || buro == "" || nroEnt == "" || edadRL == "" ){
                  alert("Falta completar todos los datos del cliente")
                  return null;
              }
              if (edadRL <18){
                  alert("El representante legal debe ser mayor de edad");
                  return null;
              }
              return lista;
          }
          function getBalanceGeneral(){
              var lista = [];
              var bg_1 = convNro(document.getElementById('bg_1').value);
              lista.push(bg_1);
              var bg_porc_1 = convNro(document.getElementById('bg_porc_1').value);
              lista.push(bg_porc_1);
              var bg_2 = convNro(document.getElementById('bg_2').value);
              lista.push(bg_2);
              var bg_porc_2 = convNro(document.getElementById('bg_porc_2').value);
              lista.push(bg_porc_2);
              var bg_3 = convNro(document.getElementById('bg_3').value);
              lista.push(bg_3);
              var bg_porc_3 = convNro(document.getElementById('bg_porc_3').value);
              lista.push(bg_porc_3);
              var bg_4 = convNro(document.getElementById('bg_4').value);
              lista.push(bg_4);
              var bg_porc_4 = convNro(document.getElementById('bg_porc_4').value);
              lista.push(bg_porc_4);
              var bg_5 = convNro(document.getElementById('bg_5').value);
              lista.push(bg_5);
              var bg_porc_5 = convNro(document.getElementById('bg_porc_5').value);
              lista.push(bg_porc_5);
              var bg_6 = convNro(document.getElementById('bg_6').value);
              lista.push(bg_6);
              var bg_porc_6 = convNro(document.getElementById('bg_porc_6').value);
              lista.push(bg_porc_6);
              var bg_7 = convNro(document.getElementById('bg_7').value);
              lista.push(bg_7);
              var bg_porc_7 = convNro(document.getElementById('bg_porc_7').value);
              lista.push(bg_porc_7);
              var bg_8 = convNro(document.getElementById('bg_8').value);
              lista.push(bg_8);
              var bg_porc_8 = convNro(document.getElementById('bg_porc_8').value);
              lista.push(bg_porc_8);
              var bg_9 = convNro(document.getElementById('bg_9').value);
              lista.push(bg_9);
              var bg_porc_9 = convNro(document.getElementById('bg_porc_9').value);
              lista.push(bg_porc_9);
              var bg_10 = convNro(document.getElementById('bg_10').value);
              lista.push(bg_10);
              var bg_porc_10 = convNro(document.getElementById('bg_porc_10').value);
              lista.push(bg_porc_10);
              var bg_11 = convNro(document.getElementById('bg_11').value);
              lista.push(bg_11);
              var bg_porc_11 = convNro(document.getElementById('bg_porc_11').value);
              lista.push(bg_porc_11);
              
              var total_activo_cte = convNro(document.getElementById('total_activo_cte').value);
              lista.push(total_activo_cte);
              var total_activo_cte_porc = convNro(document.getElementById('total_activo_cte_porc').value);
              lista.push(total_activo_cte_porc);
          
              var bg_12 = convNro(document.getElementById('bg_12').value);
              lista.push(bg_12);
              var bg_porc_12 = convNro(document.getElementById('bg_porc_12').value);
              lista.push(bg_porc_12);
              var bg_13 = convNro(document.getElementById('bg_13').value);
              lista.push(bg_13);
              var bg_porc_13 = convNro(document.getElementById('bg_porc_13').value);
              lista.push(bg_porc_13);
              var bg_14 = convNro(document.getElementById('bg_14').value);
              lista.push(bg_14);
              var bg_porc_14 = convNro(document.getElementById('bg_porc_14').value);
              lista.push(bg_porc_14);
              var bg_15 = convNro(document.getElementById('bg_15').value);
              lista.push(bg_15);
              var bg_porc_15 = convNro(document.getElementById('bg_porc_15').value);
              lista.push(bg_porc_15);
          
              var total_activo_no_cte = convNro(document.getElementById('total_activo_no_cte').value);
              lista.push(total_activo_no_cte);
              var total_activo_no_cte_porc = convNro(document.getElementById('total_activo_no_cte_porc').value);
              lista.push(total_activo_no_cte_porc);
              
              var total_activo = convNro(document.getElementById('total_activo').value);
              lista.push(total_activo);
          
              var bg_16 = convNro(document.getElementById('bg_16').value);
              lista.push(bg_16);
              var bg_porc_16 = convNro(document.getElementById('bg_porc_16').value);
              lista.push(bg_porc_16);
              var bg_17 = convNro(document.getElementById('bg_17').value);
              lista.push(bg_17);
              var bg_porc_17 = convNro(document.getElementById('bg_porc_17').value);
              lista.push(bg_porc_17);
              var bg_18 = convNro(document.getElementById('bg_18').value);
              lista.push(bg_18);
              var bg_porc_18 = convNro(document.getElementById('bg_porc_18').value);
              lista.push(bg_porc_18);
              
              var total_pasivo_cte = convNro(document.getElementById('total_pasivo_cte').value);
              lista.push(total_pasivo_cte);
              var total_pasivo_cte_porc = convNro(document.getElementById('total_pasivo_cte_porc').value);
              lista.push(total_pasivo_cte_porc);
          
              var bg_19 = convNro(document.getElementById('bg_19').value);
              lista.push(bg_19);
              var bg_porc_19 = convNro(document.getElementById('bg_porc_19').value);
              lista.push(bg_porc_19);
              var bg_20 = convNro(document.getElementById('bg_20').value);
              lista.push(bg_20);
              var bg_porc_20 = convNro(document.getElementById('bg_porc_20').value);
              lista.push(bg_porc_20);
              var bg_21 = convNro(document.getElementById('bg_21').value);
              lista.push(bg_21);
              var bg_porc_21 = convNro(document.getElementById('bg_porc_21').value);
              lista.push(bg_porc_21);
          
              var total_pasivo_no_cte = convNro(document.getElementById('total_pasivo_no_cte').value);
              lista.push(total_pasivo_no_cte);
              var total_pasivo_no_cte_porc = convNro(document.getElementById('total_pasivo_no_cte_porc').value);
              lista.push(total_pasivo_no_cte_porc);
          
              var total_pasivo = convNro(document.getElementById('total_pasivo').value);
              lista.push(total_pasivo);
              var total_pasivo_porc = convNro(document.getElementById('total_pasivo_porc').value);
              lista.push(total_pasivo_porc);
          
              var patrimonio = convNro(document.getElementById('patrimonio').value);
              lista.push(patrimonio);
              var patrimonio_porc = convNro(document.getElementById('patrimonio_porc').value);
              lista.push(patrimonio_porc);
          
              var pasivo_patrimonio = convNro(document.getElementById('pasivo_patrimonio').value);
              lista.push(pasivo_patrimonio);
          
          
              return lista;
          }
          function getEstadoResultados(){
              var lista = [];
              
              var egp_ventas = convNro(document.getElementById("egp_ventas").value);
              lista.push(egp_ventas);
              var egp_costoven = convNro(document.getElementById("egp_costoven").value);
              lista.push(egp_costoven);
              var egp_costoven_p = egp_costoven *100 / egp_ventas
              lista.push(egp_costoven_p);
              var egp_gastop = convNro(document.getElementById("egp_gastop").value);
              lista.push(egp_gastop);
              var egp_gastop_p = egp_costoven *100/egp_ventas;
              lista.push(egp_gastop_p);
              var egp_uoperativa = egp_ventas - egp_costoven - egp_gastop;
              lista.push(egp_uoperativa);
              var egp_uoperativa_p = egp_uoperativa *100/egp_ventas;
              lista.push(egp_uoperativa_p);
              var egp_gastfinan = convNro(document.getElementById("egp_gastfinan").value);
              lista.push(egp_gastfinan);
              var egp_gastfinan_p = egp_gastfinan *100/egp_ventas;
              lista.push(egp_gastfinan_p);
              var egp_gastfam = convNro(document.getElementById("egp_gastfam").value);
              lista.push(egp_gastfam);
              var egp_gastfam_p = egp_gastfam *100/egp_ventas;
              lista.push(egp_gastfam_p);
              var egp_otrosing = convNro(document.getElementById("egp_otrosing").value);
              lista.push(egp_otrosing);
              var egp_otrosing_p = egp_otrosing *100/egp_ventas;
              lista.push(egp_otrosing_p);
              var egp_impuestos = convNro(document.getElementById("egp_impuestos").value);
              lista.push(egp_impuestos);
              var egp_impuestos_p = egp_impuestos *100/egp_ventas;
              lista.push(egp_impuestos_p);
              var egp_uneta = egp_uoperativa - egp_gastfinan - egp_gastfam + egp_otrosing - egp_impuestos;
              lista.push(egp_uneta);
              var egp_uneta_p = egp_uneta *100/egp_ventas;
              lista.push(egp_uneta_p);
              
              return lista;
          }
          function getCanalizacion(){
              var lista = [];
              var AnteriorIngresos = convNro(document.getElementById("AnteriorIngresos").value);
              lista.push(AnteriorIngresos);
              var AnteriorSMA = convNro(document.getElementById("AnteriorSMA").value);
              lista.push(AnteriorSMA);
              var EnCursoIngresos = convNro(document.getElementById("EnCursoIngresos").value);
              lista.push(EnCursoIngresos);
              var EnCursoSMA = convNro(document.getElementById("EnCursoSMA").value);
              lista.push(EnCursoSMA);
              return lista;
          }
          function getRatios(){
              var lista = [];
              var LiquidezCTE = convNro(document.getElementById("LiquidezCTE").value);
              lista.push(LiquidezCTE);
              var CapitalTrabajo = convNro(document.getElementById("CapitalTrabajo").value);
              lista.push(CapitalTrabajo);
              var DiasExistencias = convNro(document.getElementById("DiasExistencias").value);
              lista.push(DiasExistencias);
              var DiasCobro = convNro(document.getElementById("DiasCobro").value);
              lista.push(DiasCobro);
              var DiasPago = convNro(document.getElementById("DiasPago").value);
              lista.push(DiasPago);
              var CicloNegocio = convNro(document.getElementById("CicloNegocio").value);
              lista.push(CicloNegocio);
              var PayBack = convNro(document.getElementById("PayBack").value);
              lista.push(PayBack);
              var CoberturaDeuda = convNro(document.getElementById("CoberturaDeuda").value);
              lista.push(CoberturaDeuda);
              return lista;
          }
          function getDictamen(){
              var lista = [];
              var dictamen = document.getElementById('dictamen').value;
              lista.push(dictamen);
              var motivo = document.getElementById('motivo').value;
              lista.push(motivo);
              return lista;
          }
        var TEALTC = 0.3401;
		var TEAPCCT = 0.2362;
		var TEAPC = 0.2362;
		var TEAPA = 0.2133;
		var TEAPPLibre = 0.2556;
		var TEAPPVehicular = 0.1048;
		var TEAPPHipotecario = 0.0894;
		var TEATC = 0.4650;
		
		function retornarTEM(TEA){
			var TEA = Math.pow((1+TEA),(1/12))-1+0.0015;
			return Number(TEA).toFixed(10);
		}
		function Calcular_Cuota_Pagar(tasa,plazo,deuda){
			tasa = Number(tasa);
			plazo = Number(plazo);
			deuda = Number(deuda);
			var p1 = 1+tasa;
			var p2 = Math.pow(p1,-plazo);
			var p3 = 1 - p2;
			var p4 = p3/tasa;
			var p5 = deuda /p4
			p5 = convNro(p5);
			return Number(p5).toFixed(2);
		}
		function CalcularNroCuotas(Mes_Anterior,TEM,Cuota,Mes_Actual){
            if(Mes_Anterior>Mes_Actual){
                Mes_Anterior = Number(Mes_Anterior);
                TEM = Number(TEM);
                Cuota = Number(Cuota);
                Mes_Actual = Number(Mes_Actual);
                var cantCuotas = 0;
                var saldo = Mes_Anterior;
                if(Cuota >0){
                    while (saldo > 0){
                        Mes_Anterior = saldo;
                        var interes = Mes_Anterior * TEM;
                        var amorCap = Cuota - interes;
                        saldo = Mes_Anterior - amorCap;
                        cantCuotas = cantCuotas +1;
                    }
                }
                return cantCuotas-1;
            }
            return 0;
		}
		
		function EliminarLineaTarjeta(){
			var table = document.getElementById("tablaLineaTarjetaCapital")
			var idx = table.rows.length-1
			if(table.rows.length>1){
				table.deleteRow(idx);
			}
			Calcular_Linea_Tarjeta_Total();
		}
		function AgregarLineaTarjeta(){
			var table = document.getElementById("tablaLineaTarjetaCapital");
			var idx = table.rows.length;
			var row = table.insertRow(idx);
			idx = idx-1
			var cell1 = row.insertCell(0);
			var cell2 = row.insertCell(1);
			var cell3 = row.insertCell(2);
			//var cell4 = row.insertCell(3);
			//var cell5 = row.insertCell(4);
			var cell6 = row.insertCell(3);
			var cell7 = row.insertCell(4);
			var TEM = retornarTEM(TEALTC);
			TEM = Number(TEM).toFixed(4);
			cell1.innerHTML = '<div><input class="form-control" type="text" id="LTC_Banco_'+idx+'"/></div>';
			cell2.innerHTML = '<div><input class="form-control" type="text" id="LTC_Linea_Utilizada_'+idx+'" onkeyup="validarNumero(id);"/></div>';
			cell3.innerHTML = '<div><input class="form-control" type="text" id="LTC_Linea_Total_'+idx+'" onkeyup="validarNumero(id);Calcular_Linea_Tarjeta_Total()"/></div>';
			var cell4 = '<div style="display:none" id="LTC_TEA_'+idx+'">'+TEALTC*100+'%</div>';
			var cell5 = '<div style="display:none" id="LTC_TEM_'+idx+'">'+TEM*100+'%</div>';
			cell6.innerHTML = cell4+'<div id="LTC_Costo_Financiero_'+idx+'"></div>';
			cell7.innerHTML = cell5+'<div id="LTC_Costo_Aprox_Pagar_'+idx+'"></div>';
			
		}
		function Calcular_Linea_Tarjeta(idx){
			var LTC_Linea_Utilizada = convNro(document.getElementById("LTC_Linea_Utilizada_"+idx).value);
			var LTC_Linea_Total = convNro(document.getElementById("LTC_Linea_Total_"+idx).value);
			
			var TEM = retornarTEM(TEALTC);
			
			var LTC_Costo_Financiero = LTC_Linea_Total * TEM;
			LTC_Costo_Financiero = Number(LTC_Costo_Financiero).toFixed(2);
			
			var LTC_Costo_Aprox_Pagar = Calcular_Cuota_Pagar(TEM,24,LTC_Linea_Total);
			LTC_Costo_Aprox_Pagar = Number(LTC_Costo_Aprox_Pagar).toFixed(2);

			document.getElementById("LTC_Costo_Financiero_"+idx).innerHTML = Number(LTC_Costo_Financiero).toLocaleString('en');
			document.getElementById("LTC_Costo_Financiero_"+idx).value = LTC_Costo_Financiero;
			document.getElementById("LTC_Costo_Aprox_Pagar_"+idx).innerHTML = Number(LTC_Costo_Aprox_Pagar).toLocaleString('en');
			document.getElementById("LTC_Costo_Aprox_Pagar_"+idx).value = LTC_Costo_Aprox_Pagar;
		}
        function Calcular_Linea_Tarjeta_Total(){
			var table = document.getElementById("tablaLineaTarjetaCapital");
			var filas = table.rows.length-1;

			for (var idx=0;idx<filas;idx++){
				Calcular_Linea_Tarjeta(idx);
			}
            Calcular_Resumen();
            Calcular_Linea_No_Utilizada();
		}
		
		function EliminarPrestamoComercial(){
			var table = document.getElementById("tablaPrestamoComercial")
			var idx = table.rows.length-1
			if(table.rows.length>1){
				table.deleteRow(idx);
			}
			Calcular_Prestamo_Comercial_Total();
		}
		function AgregarPrestamoComercial(){
			var table = document.getElementById("tablaPrestamoComercial");
			var idx = table.rows.length;
			var row = table.insertRow(idx);
			idx = idx-1;
			var cell1 = row.insertCell(0);
			var cell2 = row.insertCell(1);
			var cell3 = row.insertCell(2);
			//var cell4 = row.insertCell(3);
			//var cell5 = row.insertCell(4);
			var cell6 = row.insertCell(3);
			var cell7 = row.insertCell(4);
			var cell8 = row.insertCell(5);
			var cell9 = row.insertCell(6);
			
			var TEM = retornarTEM(TEAPCCT);
			TEM = Number(TEM).toFixed(4);

			cell1.innerHTML = '<div><input class="form-control" type="text" id="PCCT_Banco_'+idx+'"/></div>';
			cell2.innerHTML = '<div><input class="form-control" type="text" id="PCCT_Mes_Anterior_'+idx+'" onkeyup="validarNumero(id);Calcular_Prestamo_Comercial_Total()"/></div>';
			cell3.innerHTML = '<div><input class="form-control" type="text" id="PCCT_Mes_Actual_'+idx+'" onkeyup="validarNumero(id);Calcular_Prestamo_Comercial_Total()"/></div>';
			var cell4 = '<div style="display:none" id="PCCT_TEA_'+idx+'">'+TEAPCCT*100+'%</div>';
			var cell5 = '<div style="display:none" id="PCCT_TEM_'+idx+'">'+Number(TEM*100).toFixed(2)+'%</div>';
			cell6.innerHTML = cell4+'<div id="PCCT_Amort_Capital_'+idx+'"></div>';
			cell7.innerHTML = cell5+'<div id="PCCT_Costo_Financiero_'+idx+'"></div>';
			cell8.innerHTML = '<div id="PCCT_Cuota_Pagar_Aprox_'+idx+'"></div>';
			cell9.innerHTML = '<div id="PCCT_Nro_Cuota_'+idx+'"></div>';

		}
		function Calcular_Prestamo_Comercial(idx){
			var PCCT_Mes_Anterior = convNro(document.getElementById("PCCT_Mes_Anterior_"+idx).value);
			var PCCT_Mes_Actual = convNro(document.getElementById("PCCT_Mes_Actual_"+idx).value);
			
			var PCCT_Amort_Capital = PCCT_Mes_Anterior - PCCT_Mes_Actual;
			document.getElementById("PCCT_Amort_Capital_"+idx).innerHTML = Number(PCCT_Amort_Capital).toLocaleString('en');
			document.getElementById("PCCT_Amort_Capital_"+idx).value = PCCT_Amort_Capital;

			var TEM = retornarTEM(TEAPCCT);
			var PCCT_Costo_Financiero = PCCT_Mes_Anterior * TEM;
			PCCT_Costo_Financiero = Number(PCCT_Costo_Financiero).toFixed(0);
			document.getElementById("PCCT_Costo_Financiero_"+idx).innerHTML = Number(PCCT_Costo_Financiero).toLocaleString('en');
			document.getElementById("PCCT_Costo_Financiero_"+idx).value = PCCT_Costo_Financiero;
			PCCT_Amort_Capital = Number(PCCT_Amort_Capital);
			PCCT_Costo_Financiero = Number(PCCT_Costo_Financiero);
			var PCCT_Cuota_Pagar_Aprox = PCCT_Amort_Capital + PCCT_Costo_Financiero;
			PCCT_Cuota_Pagar_Aprox = Number(PCCT_Cuota_Pagar_Aprox).toFixed(0);
			document.getElementById("PCCT_Cuota_Pagar_Aprox_"+idx).innerHTML = Number(PCCT_Cuota_Pagar_Aprox).toLocaleString('en');
			document.getElementById("PCCT_Cuota_Pagar_Aprox_"+idx).value = PCCT_Cuota_Pagar_Aprox;
			
			var PCCT_Nro_Cuota = CalcularNroCuotas(PCCT_Mes_Anterior,TEM,PCCT_Cuota_Pagar_Aprox,PCCT_Mes_Actual);
			document.getElementById("PCCT_Nro_Cuota_"+idx).innerHTML = Number(PCCT_Nro_Cuota).toLocaleString('en');
			document.getElementById("PCCT_Nro_Cuota_"+idx).value = PCCT_Nro_Cuota;	
			
		}
		function Calcular_Prestamo_Comercial_Total(){
			var table = document.getElementById("tablaPrestamoComercial");
			var filas = table.rows.length-1;

			for (var idx=0;idx<filas;idx++){
				Calcular_Prestamo_Comercial(idx);
			}
            Calcular_Resumen();
		}
		
		function EliminarPrestamoCancelable(){
			var table = document.getElementById("tablaPrestamoCancelable")
			var idx = table.rows.length-1
			if(table.rows.length>1){
				table.deleteRow(idx);
			}
			Calcular_Prestamo_Cancelable_Total();
		}
		function AgregarPrestamoCancelable(){
			var table = document.getElementById("tablaPrestamoCancelable");
			var idx = table.rows.length;
			var row = table.insertRow(idx);
			idx = idx-1;
			var cell1 = row.insertCell(0);
			var cell2 = row.insertCell(1);
			var cell3 = row.insertCell(2);
			//var cell4 = row.insertCell(3);
			//var cell5 = row.insertCell(4);
			var cell6 = row.insertCell(5);
			
			var TEM = retornarTEM(TEAPC);
			TEM = Number(TEM).toFixed(4);

			cell1.innerHTML = '<div><input class="form-control" type="text" id="PC_Banco_'+idx+'"/></div>';
			cell2.innerHTML = '<div><input class="form-control" type="text" id="PC_Monto_'+idx+'" onkeyup="validarNumero(id);Calcular_Prestamo_Cancelable_Total();"/></div>';
			cell3.innerHTML = '<div><input class="form-control" type="text" id="PC_Periodo_'+idx+'" onkeyup="validarNumero(id);"/></div>';
			var cell4 = '<div style="display:none" id="PC_TEA_'+idx+'">'+TEAPC*100+'%</div>';
			var cell5 = '<div style="display:none" id="PC_TEM_'+idx+'">'+Number(TEM*100).toFixed(2)+'%</div>';
			cell6.innerHTML = cell4+cell5+'<div id="PC_Costo_Financiero_'+idx+'"></div>';
			

		}
        
		function Calcular_Prestamo_Cancelable(idx){
			var PC_Monto = convNro(document.getElementById("PC_Monto_"+idx).value);
			
			var TEM = retornarTEM(TEAPC);
			
			var PC_Costo_Financiero = PC_Monto * TEM;
			PC_Costo_Financiero = Number(PC_Costo_Financiero).toFixed(2);
			document.getElementById("PC_Costo_Financiero_"+idx).innerHTML = Number(PC_Costo_Financiero).toLocaleString('en');
			document.getElementById("PC_Costo_Financiero_"+idx).value = PC_Costo_Financiero;
			
		}
		function Calcular_Prestamo_Cancelable_Total(){
			var table = document.getElementById("tablaPrestamoCancelable");
			var filas = table.rows.length-1;

			for (var idx=0;idx<filas;idx++){
				Calcular_Prestamo_Cancelable(idx);
			}
            Calcular_Resumen();
		}
		
		function EliminarPrestamoAdquisicion(){
			var table = document.getElementById("tablaPrestamoAdquisicion")
			var idx = table.rows.length-1
			if(table.rows.length>1){
				table.deleteRow(idx);
			}
			Calcular_Prestamo_Adquisicion_Total();
		}
		function AgregarPrestamoAdquisicion(){
			var table = document.getElementById("tablaPrestamoAdquisicion");
			var idx = table.rows.length;
			var row = table.insertRow(idx);
			idx = idx-1;
			var cell1 = row.insertCell(0);
			var cell2 = row.insertCell(1);
			var cell3 = row.insertCell(2);
			//var cell4 = row.insertCell(3);
			//var cell5 = row.insertCell(4);
			var cell6 = row.insertCell(3);
			var cell7 = row.insertCell(4);
			var cell8 = row.insertCell(5);
			var cell9 = row.insertCell(6);
			
			var TEM = retornarTEM(TEAPA);
			TEM = Number(TEM).toFixed(4);

			cell1.innerHTML = '<div><input class="form-control" type="text" id="PA_Banco_'+idx+'"/></div>';
			cell2.innerHTML = '<div><input class="form-control" type="text" id="PA_Mes_Anterior_'+idx+'" onkeyup="validarNumero(id);Calcular_Prestamo_Adquisicion_Total()"/></div>';
			cell3.innerHTML = '<div><input class="form-control" type="text" id="PA_Mes_Actual_'+idx+'" onkeyup="validarNumero(id);Calcular_Prestamo_Adquisicion_Total()"/></div>';
			var cell4 = '<div style="display:none" id="PA_TEA_'+idx+'">'+TEAPA*100+'%</div>';
			var cell5 = '<div style="display:none" id="PA_TEM_'+idx+'">'+Number(TEM*100).toFixed(2)+'%</div>';
			cell6.innerHTML = cell4+'<div id="PA_Amort_Capital_'+idx+'"></div>';
			cell7.innerHTML = cell5+'<div id="PA_Costo_Financiero_'+idx+'"></div>';
			cell8.innerHTML = '<div id="PA_Cuota_Pagar_Aprox_'+idx+'"></div>';
			cell9.innerHTML = '<div id="PA_Nro_Cuota_'+idx+'"></div>';

		}
		function Calcular_Prestamo_Adquisicion(idx){
			var PA_Mes_Anterior = convNro(document.getElementById("PA_Mes_Anterior_"+idx).value);
			var PA_Mes_Actual = convNro(document.getElementById("PA_Mes_Actual_"+idx).value);
			
			var PA_Amort_Capital = PA_Mes_Anterior - PA_Mes_Actual;
			document.getElementById("PA_Amort_Capital_"+idx).innerHTML = Number(PA_Amort_Capital).toLocaleString('en');
			document.getElementById("PA_Amort_Capital_"+idx).value = PA_Amort_Capital;
            
			var TEM = retornarTEM(TEAPA);
			var PA_Costo_Financiero = PA_Mes_Anterior * TEM;
			PA_Costo_Financiero = Number(PA_Costo_Financiero).toFixed(0);
			document.getElementById("PA_Costo_Financiero_"+idx).innerHTML = Number(PA_Costo_Financiero).toLocaleString('en');
			document.getElementById("PA_Costo_Financiero_"+idx).value = PA_Costo_Financiero;
			PA_Amort_Capital = Number(PA_Amort_Capital);
			PA_Costo_Financiero = Number(PA_Costo_Financiero);
			var PA_Cuota_Pagar_Aprox = PA_Amort_Capital + PA_Costo_Financiero;
			PA_Cuota_Pagar_Aprox = Number(PA_Cuota_Pagar_Aprox).toFixed(0);
			document.getElementById("PA_Cuota_Pagar_Aprox_"+idx).innerHTML = Number(PA_Cuota_Pagar_Aprox).toLocaleString('en');
			document.getElementById("PA_Cuota_Pagar_Aprox_"+idx).value = PA_Cuota_Pagar_Aprox;
			
			var PA_Nro_Cuota = CalcularNroCuotas(PA_Mes_Anterior,TEM,PA_Cuota_Pagar_Aprox,PA_Mes_Actual);
			document.getElementById("PA_Nro_Cuota_"+idx).innerHTML = Number(PA_Nro_Cuota).toLocaleString('en');
			document.getElementById("PA_Nro_Cuota_"+idx).value = PA_Nro_Cuota;	
            
			
		}
		function Calcular_Prestamo_Adquisicion_Total(){
			var table = document.getElementById("tablaPrestamoAdquisicion");
			var filas = table.rows.length-1;

			for (var idx=0;idx<filas;idx++){
				Calcular_Prestamo_Adquisicion(idx);
			}
            Calcular_Resumen();
		}
		
		function EliminarPrestamoPersonal(){
			var table = document.getElementById("tablaPrestamoPersonal")
			var idx = table.rows.length-1
			if(table.rows.length>1){
				table.deleteRow(idx);
			}
			Calcular_Prestamo_Personal_Total();
		}
		function AgregarPrestamoPersonal(){
			var table = document.getElementById("tablaPrestamoPersonal");
			var idx = table.rows.length;
			var row = table.insertRow(idx);
			idx = idx-1;
			var cell1 = row.insertCell(0);
			var cell2 = row.insertCell(1);
			var cell3 = row.insertCell(2);
			var cell4 = row.insertCell(3);
			//var cell5 = row.insertCell(4);
			//var cell6 = row.insertCell(5);
			var cell7 = row.insertCell(4);
			var cell8 = row.insertCell(5);
			var cell9 = row.insertCell(6);
			var cell10 = row.insertCell(7);
			
			cell1.innerHTML = '<div><input class="form-control" type="text" id="PP_Banco_'+idx+'"/></div>';
			cell2.innerHTML = '<div><select class="form-control" id="PP_Producto_'+idx+'" onchange = "Calcular_Prestamo_Personal_Total();"/><option value = "0"></option> <option value = "1">Vehicular</option> <option value = "2">Hipotecario</option> <option value = "3">Libre Disponibilidad</option> </select> </div>'; cell3.innerHTML = '<div><input class="form-control" type="text" id="PP_Mes_Anterior_'+idx+'" onkeyup="validarNumero(id);Calcular_Prestamo_Comercial_Total()"/></div>';
			cell3.innerHTML = '<div><input class="form-control" type="text" id="PP_Mes_Anterior_'+idx+'" onkeyup="validarNumero(id);Calcular_Prestamo_Personal_Total()"/></div>';
			cell4.innerHTML = '<div><input class="form-control" type="text" id="PP_Mes_Actual_'+idx+'" onkeyup="validarNumero(id);Calcular_Prestamo_Personal_Total()"/></div>';
			var cell5 = '<div style="display:none" id="PP_TEA_'+idx+'"></div>';
			var cell6 = '<div style="display:none" id="PP_TEM_'+idx+'"></div>';
			cell7.innerHTML = cell5+'<div id="PP_Amort_Capital_'+idx+'"></div>';
			cell8.innerHTML = cell6+'<div id="PP_Costo_Financiero_'+idx+'"></div>';
			cell9.innerHTML = '<div id="PP_Cuota_Pagar_Aprox_'+idx+'"></div>';
			cell10.innerHTML = '<div id="PP_Nro_Cuota_'+idx+'"></div>';

		}
		function Calcular_Prestamo_Personal(idx){
			var producto = document.getElementById("PP_Producto_"+idx).value;
			if(producto!=0){
				var TEA = 0;
				if(producto==1){
					TEA = TEAPPVehicular;
				}else if(producto==2){
					TEA = TEAPPHipotecario;
				}else if(producto==3){
					TEA = TEAPPLibre;
				}
				var TEM = retornarTEM(TEA);
				document.getElementById("PP_TEM_"+idx).value = TEM;
				document.getElementById("PP_TEM_"+idx).innerHTML = Number(TEM*100).toFixed(2) + "%";

				document.getElementById("PP_TEA_"+idx).value = TEA;
				document.getElementById("PP_TEA_"+idx).innerHTML = Number(TEA*100).toFixed(2) + "%";

				var PP_Mes_Anterior = convNro(document.getElementById("PP_Mes_Anterior_"+idx).value);
				var PP_Mes_Actual = convNro(document.getElementById("PP_Mes_Actual_"+idx).value);
				
				var PP_Amort_Capital = PP_Mes_Anterior - PP_Mes_Actual;
				document.getElementById("PP_Amort_Capital_"+idx).innerHTML = Number(PP_Amort_Capital).toLocaleString('en');
				document.getElementById("PP_Amort_Capital_"+idx).value = PP_Amort_Capital;

				TEM = Number(TEM);

				var PP_Costo_Financiero = PP_Mes_Anterior * TEM;
				PP_Costo_Financiero = Number(PP_Costo_Financiero).toFixed(0);
				document.getElementById("PP_Costo_Financiero_"+idx).innerHTML = Number(PP_Costo_Financiero).toLocaleString('en');
				document.getElementById("PP_Costo_Financiero_"+idx).value = PP_Costo_Financiero;
				PP_Amort_Capital = Number(PP_Amort_Capital);
				PP_Costo_Financiero = Number(PP_Costo_Financiero);
				var PP_Cuota_Pagar_Aprox = PP_Amort_Capital + PP_Costo_Financiero;
				PP_Cuota_Pagar_Aprox = Number(PP_Cuota_Pagar_Aprox).toFixed(0);
				document.getElementById("PP_Cuota_Pagar_Aprox_"+idx).innerHTML = Number(PP_Cuota_Pagar_Aprox).toLocaleString('en');
				document.getElementById("PP_Cuota_Pagar_Aprox_"+idx).value = PP_Cuota_Pagar_Aprox;

				var PP_Nro_Cuota = CalcularNroCuotas(PP_Mes_Anterior,TEM,PP_Cuota_Pagar_Aprox,PP_Mes_Actual);
				document.getElementById("PP_Nro_Cuota_"+idx).innerHTML = Number(PP_Nro_Cuota).toLocaleString('en');
				document.getElementById("PP_Nro_Cuota_"+idx).value = PP_Nro_Cuota;				

			}else{
				document.getElementById("PP_TEM_"+idx).value = 0;
				document.getElementById("PP_TEM_"+idx).innerHTML = "";

				document.getElementById("PP_TEA_"+idx).value = 0;
				document.getElementById("PP_TEA_"+idx).innerHTML = "";

				document.getElementById("PP_Amort_Capital_"+idx).innerHTML = "";
				document.getElementById("PP_Amort_Capital_"+idx).value = 0;

				document.getElementById("PP_Costo_Financiero_"+idx).innerHTML = "";
				document.getElementById("PP_Costo_Financiero_"+idx).value = 0;
				
				document.getElementById("PP_Cuota_Pagar_Aprox_"+idx).innerHTML = "";
				document.getElementById("PP_Cuota_Pagar_Aprox_"+idx).value = 0;
			}
		}
		function Calcular_Prestamo_Personal_Total(){
			var table = document.getElementById("tablaPrestamoPersonal");
			var filas = table.rows.length-1;

			for (var idx=0;idx<filas;idx++){
				Calcular_Prestamo_Personal(idx);
			}
            Calcular_Resumen();
		}
		
		function EliminarTarjetaConsumo(){
			var table = document.getElementById("tablaTarjetaConsumo")
			var idx = table.rows.length-1
			if(table.rows.length>1){
				table.deleteRow(idx);
			}
			Calcular_Tarjeta_Consumo_Total();
		}
		function AgregarTarjetaConsumo(){
			var table = document.getElementById("tablaTarjetaConsumo");
			var idx = table.rows.length;
			var row = table.insertRow(idx);
			idx = idx-1
			var cell1 = row.insertCell(0);
			var cell2 = row.insertCell(1);
			var cell3 = row.insertCell(2);
			//var cell4 = row.insertCell(3);
			//var cell5 = row.insertCell(4);
			var cell6 = row.insertCell(5);
			var cell7 = row.insertCell(6);
			var TEM = retornarTEM(TEATC);
			TEM = Number(TEM).toFixed(4);
			cell1.innerHTML = '<div><input class="form-control" type="text" id="TC_Banco_'+idx+'"/></div>';
			cell2.innerHTML = '<div><input class="form-control" type="text" id="TC_Linea_Utilizada_'+idx+'" onkeyup="validarNumero(id);Calcular_Tarjeta_Consumo_Total();"/></div>';
			cell3.innerHTML = '<div><input class="form-control" type="text" id="TC_Linea_Total_'+idx+'" onkeyup="validarNumero(id);Calcular_Tarjeta_Consumo_Total();"/></div>';
			var cell4 = '<div style="display:none" id="TC_TEA_'+idx+'">'+TEATC*100+'%</div>';
			var cell5 = '<div style="display:none" id="TC_TEM_'+idx+'">'+TEM*100+'%</div>';
			cell6.innerHTML = cell5+'<div id="TC_Costo_Financiero_'+idx+'"></div>';
			cell7.innerHTML = cell6+'<div id="TC_Costo_Aprox_Pagar_'+idx+'"></div>';
		}
		function Calcular_Tarjeta_Consumo(idx){
			var TC_Linea_Utilizada = convNro(document.getElementById("TC_Linea_Utilizada_"+idx).value);
			var TC_Linea_Total = convNro(document.getElementById("TC_Linea_Total_"+idx).value);
			
			var TEM = retornarTEM(TEATC);
			
			var TC_Costo_Financiero = (TC_Linea_Utilizada * TEM) + ((TC_Linea_Total - TC_Linea_Utilizada) * TEM * 0.36);
			TC_Costo_Financiero = Number(TC_Costo_Financiero).toFixed(0);
			
			var TC_Costo_Aprox_Pagar = 0;
			if (TC_Linea_Total !=0){
				var p1 = Calcular_Cuota_Pagar(TEM,36,TC_Linea_Utilizada);
				var p2 = Calcular_Cuota_Pagar(TEM,36,(TC_Linea_Total-TC_Linea_Utilizada)) * 0.36;
				p1 = Number(p1);
				p2 = Number(p2);
				TC_Costo_Financiero = Number(TC_Costo_Financiero);
				var p3 = p1 + p2 + TC_Costo_Financiero;
				
				TC_Costo_Aprox_Pagar = Number(p3).toFixed(0);
				
			}


			document.getElementById("TC_Costo_Financiero_"+idx).innerHTML = Number(TC_Costo_Financiero).toLocaleString('en');
			document.getElementById("TC_Costo_Financiero_"+idx).value = TC_Costo_Financiero;
			document.getElementById("TC_Costo_Aprox_Pagar_"+idx).innerHTML = Number(TC_Costo_Aprox_Pagar).toLocaleString('en');
			document.getElementById("TC_Costo_Aprox_Pagar_"+idx).value = TC_Costo_Aprox_Pagar;
		}
		function Calcular_Tarjeta_Consumo_Total(){
			var table = document.getElementById("tablaTarjetaConsumo");
			var filas = table.rows.length-1;

			for (var idx=0;idx<filas;idx++){
				Calcular_Tarjeta_Consumo(idx);
			}
            Calcular_Resumen();
		}
		function Calcular_Resumen(){
            var LTC_table = document.getElementById("tablaLineaTarjetaCapital");
			var LTC_filas = LTC_table.rows.length-1;
			var PCCT_table = document.getElementById("tablaPrestamoComercial");
			var PCCT_filas = PCCT_table.rows.length-1;
			var PA_table = document.getElementById("tablaPrestamoAdquisicion");
			var PA_filas = PA_table.rows.length-1;
			var TC_table = document.getElementById("tablaTarjetaConsumo");
			var TC_filas = TC_table.rows.length-1;
			var PP_table = document.getElementById("tablaPrestamoPersonal");
			var PP_filas = PP_table.rows.length-1;
            
            var S1 = 0;
			var LTC_S1 = 0;
			for (var idx=0;idx<LTC_filas;idx++){
				LTC_S1 = LTC_S1 + convNro(document.getElementById("LTC_Linea_Total_"+idx).value);
			}
			var PCCT_S1 = 0;
			for (var idx=0;idx<PCCT_filas;idx++){
				PCCT_S1 = PCCT_S1 + convNro(document.getElementById("PCCT_Mes_Actual_"+idx).value);
			}
			S1 = LTC_S1 + PCCT_S1;
			
			var S2 = 0;
			var PA_S2 = 0;
			for (var idx=0;idx<PA_filas;idx++){
				PA_S2 = PA_S2 + convNro(document.getElementById("PA_Mes_Actual_"+idx).value);
			}
			S2 = PA_S2;
			
			var S3 = 0;
			var TC_S3 = 0;
			for (var idx=0;idx<TC_filas;idx++){
				TC_S3 = TC_S3 + convNro(document.getElementById("TC_Linea_Total_"+idx).value);
			}
			
			var PP_S3 = 0;
			for (var idx=0;idx<PP_filas;idx++){
				PP_S3 = PP_S3 + convNro(document.getElementById("PP_Mes_Actual_"+idx).value);
			}
			S3 = TC_S3 + PP_S3;
			
			
			
			var S4 = 0;
			var LTC_S4 = 0;
			for (var idx=0;idx<LTC_filas;idx++){
				LTC_S4 = LTC_S4 + convNro(document.getElementById("LTC_Costo_Aprox_Pagar_"+idx).value);
			}
			
			var PCCT_S4 = 0;
			for (var idx=0;idx<PCCT_filas;idx++){
				PCCT_S4 = PCCT_S4 + convNro(document.getElementById("PCCT_Cuota_Pagar_Aprox_"+idx).value);
			}
			S4 = LTC_S4 + PCCT_S4;
			
			var S5 = 0;
			var PA_S5 = 0;
			for (var idx=0;idx<PA_filas;idx++){
				PA_S5 = PA_S5 + convNro(document.getElementById("PA_Cuota_Pagar_Aprox_"+idx).value);
			}
			S5 = PA_S5;
            
            var S6 = 0;
			var TC_S6 = 0;
			for (var idx=0;idx<TC_filas;idx++){
				TC_S6 = TC_S6 + convNro(document.getElementById("TC_Costo_Aprox_Pagar_"+idx).value);
			}
            var PP_S6 = 0;
			for (var idx=0;idx<PP_filas;idx++){
				PP_S6 = PP_S6 + convNro(document.getElementById("PP_Cuota_Pagar_Aprox_"+idx).value);
			}
            
			S6 = convNro(TC_S6) + convNro(PP_S6);
            
            var S7 = 0;
			var LTC_S7 = 0;
			for (var idx=0;idx<LTC_filas;idx++){
				LTC_S7 = LTC_S7 + convNro(document.getElementById("LTC_Costo_Financiero_"+idx).value);
			}
			
			var PCCT_S7 = 0;
			for (var idx=0;idx<PCCT_filas;idx++){
				PCCT_S7 = PCCT_S7 + convNro(document.getElementById("PCCT_Costo_Financiero_"+idx).value);
			}
			S7 = LTC_S7 + PCCT_S7;
            
            var S8 = 0;
			var PA_S8 = 0;
			for (var idx=0;idx<PA_filas;idx++){
				PA_S8 = PA_S8 + convNro(document.getElementById("PA_Costo_Financiero_"+idx).value);
			}
			S8 = PA_S8;
            
            var S9 = 0;
			var TC_S9 = 0;
			for (var idx=0;idx<TC_filas;idx++){
				TC_S9 = TC_S9 + convNro(document.getElementById("TC_Costo_Financiero_"+idx).value);
			}
            
       		var PP_S9 = 0;
			for (var idx=0;idx<PP_filas;idx++){
				PP_S9 = PP_S9 + convNro(document.getElementById("PP_Costo_Financiero_"+idx).value);
			}
			S9 = TC_S9 + PP_S9;
			
			document.getElementById("S1").value = S1;
			document.getElementById("S1").innerHTML = Number(Number(S1).toFixed(0)).toLocaleString('en');
			document.getElementById("S2").value = S2;
			document.getElementById("S2").innerHTML = Number(Number(S2).toFixed(0)).toLocaleString('en');
			document.getElementById("S3").value = S3;
			document.getElementById("S3").innerHTML = Number(Number(S3).toFixed(0)).toLocaleString('en');
			
			document.getElementById("S4").value = S4;
			document.getElementById("S4").innerHTML = Number(Number(S4).toFixed(0)).toLocaleString('en');
			document.getElementById("S5").value = S5;
			document.getElementById("S5").innerHTML = Number(Number(S5).toFixed(0)).toLocaleString('en');
			document.getElementById("S6").value = S6;
			document.getElementById("S6").innerHTML = Number(Number(S6).toFixed(0)).toLocaleString('en');
			
			document.getElementById("S7").value = S7;
			document.getElementById("S7").innerHTML = Number(Number(S7).toFixed(0)).toLocaleString('en');
			document.getElementById("S8").value = S8;
			document.getElementById("S8").innerHTML = Number(Number(S8).toFixed(0)).toLocaleString('en');
			document.getElementById("S9").value = S9;
			document.getElementById("S9").innerHTML = Number(Number(S9).toFixed(0)).toLocaleString('en');
			
            
			document.getElementById("deuda_personal").value = S6;
			document.getElementById("deuda_personal").innerHTML = Number(Number(S6).toFixed(0)).toLocaleString('en');
			calcular_gastopersonal();
		}
        
        function Calcular_Ratios(){
      
			var TPC = convNro(document.getElementById("total_pasivo_cte").value);
			var TAC = convNro(document.getElementById("total_activo_cte").value);
			var bg_5 = convNro(document.getElementById("bg_5").value);
			var egp_costoven = convNro(document.getElementById("egp_costoven").value);
			var egp_ventas = convNro(document.getElementById("egp_ventas").value);
			var bg_3 = convNro(document.getElementById("bg_3").value);
			var bg_17 = convNro(document.getElementById("bg_17").value);
            var bg_19 = convNro(document.getElementById("bg_19").value);
			var egp_gastfinan = convNro(document.getElementById("egp_gastfinan").value);
            var egp_uneta = convNro(document.getElementById("egp_uneta").value);
            
			var LiquidezCTE = TAC/TPC;
			if(TPC == 0){
				LiquidezCTE = 0;
			}
			var CapitalTrabajo = TAC-TPC;

			var DiasExistencias = ((bg_5*365)/(egp_costoven*12));
			if(egp_costoven == 0){
				DiasExistencias = 0;
			}
			var DiasCobro = ((bg_3*365)/(egp_ventas*12));
			if(egp_ventas == 0){
				DiasCobro = 0;
			}
			var DiasPago = ((bg_17*360)/(egp_costoven*12));
			if(egp_costoven == 0){
				DiasPago = 0;
			}
			var CicloNegocio = DiasExistencias + DiasCobro - DiasPago;
			
            var cuotas = convNro(Calcular_Cuotas_LP_Total());
            var PA_table = document.getElementById("tablaPrestamoAdquisicion");
            var PA_filas = PA_table.rows.length-1;
            var PA_S5 = 0;
            for (var idx=0;idx<PA_filas;idx++){
            PA_S5 = PA_S5 + convNro(document.getElementById("PA_Cuota_Pagar_Aprox_"+idx).value);
            }
            var suma1 = 0;
            suma1 = convNro(cuotas) + convNro(PA_S5);
            
            
            var payback = 0;
            if ((egp_uneta + suma1) != 0){
                payback = (bg_19/(egp_uneta + suma1))
            }
            
            var CoberturaDeuda = 0;
            
            if (egp_gastfinan!= 0){
                CoberturaDeuda = (egp_uneta + egp_gastfinan)/egp_gastfinan;
            }


			document.getElementById("LiquidezCTE").innerHTML = Number(LiquidezCTE).toFixed(2);
			document.getElementById("CapitalTrabajo").innerHTML = Number(Number(CapitalTrabajo).toFixed(2)).toLocaleString('en');
			document.getElementById("DiasExistencias").innerHTML = Number(DiasExistencias).toFixed(2);
			document.getElementById("DiasCobro").innerHTML = Number(DiasCobro).toFixed(2);
			document.getElementById("DiasPago").innerHTML = Number(DiasPago).toFixed(2);
			document.getElementById("CicloNegocio").innerHTML = Number(CicloNegocio).toFixed(2);
            document.getElementById("PayBack").innerHTML = Number(payback).toFixed(2);
            document.getElementById("CoberturaDeuda").innerHTML = Number(CoberturaDeuda).toFixed(2);
            

			document.getElementById("LiquidezCTE").value = Number(LiquidezCTE);
			document.getElementById("CapitalTrabajo").value = Number(CapitalTrabajo);
			document.getElementById("DiasExistencias").value = Number(DiasExistencias);
			document.getElementById("DiasCobro").value = Number(DiasCobro);
			document.getElementById("DiasPago").value = Number(DiasPago);
			document.getElementById("CicloNegocio").value = Number(CicloNegocio);
            document.getElementById("PayBack").value = Number(payback);
            document.getElementById("CoberturaDeuda").value = Number(CoberturaDeuda);
            cambioSancion();
		}
