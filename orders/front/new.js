var myHeaders = new Headers();
myHeaders.append("x-amz-access-token", "Atza|IwEBINvbQfCueIgMImDTK7O8Rn3fOQAwr0c-HlxPOmHX_J_ZQBpOWJ_t7fABhuujRgp2bYJMMZX5VITgyas5N6bp64viZFkM-oq_nUvhNMV8T8JLIJYauVr-LKYTzbu6q0J94VStqdIBtcMNinfSKCTAu6tX-MCSJCAKMYaPxjsZ_GE-LwyTed3Aq8Iw8NtpzjVNVuHrvHyowLEKvVgg3WDYj9SwvTpgVdbUUR4y2gbTBi5KgjmiA8ifaN3aA6vteCsNkCAs4fWJym01gy_oCOZQCwN2MxKs1rtUtFT2RMQtSPu9FBY0J3iV0amohZyz83m6CiI");

myHeaders.append("Access-Control-Allow-Origin", "*");
myHeaders.append("Origin","http://127.0.0.1:5500/");
var requestOptions = {
  method: 'GET',
  headers: myHeaders,
    redirect: 'follow',
  params: 'state=200'
};

fetch("https://sandbox.sellingpartnerapi-eu.amazon.com/orders/v0/orders?MarketplaceIds=ATVPDKIKX0DER&CreatedAfter=TEST_CASE_200", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));