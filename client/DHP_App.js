function getBathValue(){
  var uiBathroom = document.getElementsByName("uiBathroom");
  for (var i in uiBathroom) {
      if (uiBathroom[i].checked) {
          return parseInt(i) + 1;
      }
  }
  return -1;
}

function getBHKValue(){
  var uiBHK = document.getElementsByName("uiBHK");
  for (var i in uiBHK) {
      if (uiBHK[i].checked) {
          return parseInt(i) + 1;
      }
  }
  return -1;
}

function getParkingValue(){
  var uiParking = document.getElementsByName("uiParking");
  for (var i in uiParking) {
      if (uiParking[i].checked) {
          return parseInt(i) + 1;
      }
  }
  return -1;
}

function onPageLoad(){
  console.log("document loaded");

  var url = "http://127.0.0.1:5000/get_Locality_name";
  $.get(url, function(data, status) {
      console.log("got response for get_Locality_name");
      if (data) {
          var Locality = data.Locality;
          var uiLocality = document.getElementById("uiLocality");
          $('#uiLocality').empty();
          for (var i in Locality) {
              var opt = new Option(Locality[i]);
              $('#uiLocality').append(opt);
          }
      }
  });

  var url = "http://127.0.0.1:5000/get_Furnishing";
  $.get(url, function(data, status) {
      console.log("got response for get_Furnishing");
      if (data) {
          var Furnishing = data.Furnishing;
          var uiFurnishing = document.getElementById("uiFurnishing");
          $('#uiFurnishing').empty();
          for (var i in Furnishing) {
              var opt = new Option(Furnishing[i]);
              $('#uiFurnishing').append(opt);
          }
      }
  });

  var url = "http://127.0.0.1:5000/get_Type";
  $.get(url, function(data, status) {
      console.log("got response for get_Type");
      if (data) {
          var Type = data.Type;
          var uiType = document.getElementById("uiType");
          $('#uiType').empty();
          for (var i in Type) {
              var opt = new Option(Type[i]);
              $('#uiType').append(opt);
          }
      }
  });
}

function onClickedEstimatePrice() {
  var Area = document.getElementById("uiSqft").value;
  var BHK = getBHKValue();
  var Bathroom = getBathValue();
  var Parking = getParkingValue();
  var Locality = document.getElementById("uiLocality").value;
  var Furnishing = document.getElementById("uiFurnishing").value;
  var Type = document.getElementById("uiType").value;
  var estPrice = document.getElementById("uiEstimatedPrice");

  var url = "http://127.0.0.1:5000/get_Predict_Price";

  $.post(url, {
      Area: parseFloat(Area),
      Locality: Locality,
      Furnishing: Furnishing,
      Type: Type,
      BHK: BHK,
      Bathroom: Bathroom,
      Parking: Parking
  }, function(data, status) {
      console.log(data.estimated_price);
      estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " </h2>";
      console.log(status);
  });
}

window.onload = onPageLoad;
