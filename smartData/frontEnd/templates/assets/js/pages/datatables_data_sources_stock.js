$(function() {
//初始化时间输入选项框
    var time = new Date();
    var day = ("0" + time.getDate()).slice(-2);
    var month = ("0" + (time.getMonth() + 1)).slice(-2);
    var currentYear = time.getFullYear();
    var startYear = time.getFullYear()-3 + "-" + (month) + "-" + (day);
    if(time.getHours()<18)
    {
        var preDate = new Date(new Date()-24*60*60*1000);
        day = ("0" + preDate.getDate()).slice(-2);
        month = ("0" + (preDate.getMonth() + 1)).slice(-2);
        startYear = preDate.getFullYear()-3 + "-" + (month) + "-" + (day);
    }
   // $('#kStartDate').val(startYear);
 //   var today = time.getFullYear() + "-" + (month) + "-" + (day);
 //   $('#kEndDate').val(today);

    $('#financeStartDate').val(startYear);
    var today = time.getFullYear() + "-" + (month) + "-" + (day);
    $('#financeEndDate').val(today);

    var quarters = ["0331", "0630", "0930", "1231"];
    var quartersCN = ["年第一季度", "年中报", "年第三季度", "年年报"];
    for (var i = 0; i < 35; i++)
    {
        for(var j=3; j>0; j--)
        {
            var item ={};
            item["id"]= String(currentYear-i) + quarters[j];
            item["text"] = String(currentYear-i) + quartersCN[j];
            reportPeriodList.push(item);
        }
    }

//获取可选指数
     $.ajax({
              url:"/static/assets/data/indexs.json" , // 请求路径
              type:"POST" , //请求方式
              success:function (response) {
                  responseJson=JSON.parse(response);
                  indexsListJson = responseJson['data'];
                  for (var key in responseJson['data']) {
                  var item ={};
                  item["id"]=  key;
                  item["text"]=  responseJson['data'][key];
//                           console.log(item["id"]);
//                           console.log(item["text"]);
                        indexsList.push(item);
                  };
                  $(".select-kIndexs").select2({
                    width: '100%',
                    multiple: true,
                    data: indexsList
                }).val(["000001.SH","399006.SZ"]).trigger("change");

              },//响应成功后的回调函数
              error:function () {
                  alert("出错啦...");
              },//表示如果请求响应出现错误，会执行的回调函数
              dataType:"text"//设置接受到的响应数据的格式
          });
 //用可选指数去初始化指数输入框 start
    // Add jQuery UI Sortable support
    $(".select-kIndexs").select2("container").find("ul.select2-choices").sortable({
        containment: 'parent',
        start: function() { $(".select-kIndexs").select2("onSortStart"); },
        update: function() { $(".select-kIndexs").select2("onSortEnd"); }
    });
 //用可选指数去初始化指数输入框 end

//获取财务指标可选参数
     $.ajax({
              url:"/static/assets/data/financialIndicators.json" , // 请求路径
              type:"POST" , //请求方式
              success:function (response) {
                  responseJson=JSON.parse(response);
                  financialIndicatorsJson = responseJson['data'];
                      for (var key in financialIndicatorsJson) {
                      var item ={};
                      item["id"]=  key;
                      item["text"]=  financialIndicatorsJson[key];
//                               console.log(item["id"]);
//                               console.log(item["text"]);
                            financialIndicatorsList.push(item);
                      }
                  $(".select-financialIndicators").select2({
                        width: '50%',
                        multiple: true,
                        data: financialIndicatorsList
                    }).val(["roic"]).trigger("change");
              },//响应成功后的回调函数
              error:function () {
                  alert("出错啦...");
              },//表示如果请求响应出现错误，会执行的回调函数
              dataType:"text"//设置接受到的响应数据的格式
          });

 //用可选财务指标参数去初始化财务指标输入框 start
    // Add jQuery UI Sortable support
    $(".select-financialIndicators").select2("container").find("ul.select2-choices").sortable({
        containment: 'parent',
        start: function() { $(".select-financialIndicators").select2("onSortStart"); },
        update: function() { $(".select-financialIndicators").select2("onSortEnd"); }
    });
 //用可选财务指标参数去初始化财务指标输入框 end

//报告期输入框 start
    $(".select-reportPeriod").select2({
        width: '50%',
        multiple: false,
        data: reportPeriodList
    });

    // Add jQuery UI Sortable support
    $(".select-reportPeriod").select2("container").find("ul.select2-choices").sortable({
        containment: 'parent',
        start: function() { $(".select-reportPeriod").select2("onSortStart"); },
        update: function() { $(".select-reportPeriod").select2("onSortEnd"); }
    });
 //报告期输入框 end

 //根据后台返回的数据初始化 起止时间
    var startDateFormat = startDate.slice(0,4) + "-"+ startDate.slice(4,6) + "-"+ startDate.slice(6,8);
    var endDateFormat = endDate.slice(0,4) + "-"+ endDate.slice(4,6) + "-"+ endDate.slice(6,8);
    $('#kStartDate').val(startDateFormat);
    $('#kEndDate').val(endDateFormat);
    document.getElementById("title_industry").innerHTML = industryName;
    document.getElementById("title_stockName").innerHTML = stockName;

 //根据初次从后台返回的数据初始化 同板块股票
 for (var key in stocksName) {
		  var item ={};
		  item["id"]=  key;
		  item["text"]=  stocksName[key];
				stocksList.push(item);
		  }
	$(".select-kStocks").select2({
                    width: '100%',
                    multiple: true,
                    data: stocksList
                });

});
