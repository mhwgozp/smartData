
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
    $('#kStartDate').val(startYear);
    var today = time.getFullYear() + "-" + (month) + "-" + (day);
    $('#kEndDate').val(today);

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

//// 获取所有板块的当期的财务指标并显示在表中
//    $('.datatable-ajax').dataTable({
//        ajax: 'static/assets/data/industryIndicator.json',
//        "columnDefs": [
//      {
//       "render": function (data, type, row) {
//        return "<a href='industry/?industryCode=" + row[1]+"'>"+row[0]+"</a>";
//       },
//       "targets": 0
//      },
//      { "visible": false, "targets": [ 1 ] }
//     ]
//    });

//获取财务指标可选参数
     $.ajax({
              url:"/static/assets/data/financialIndicators.json" , // 请求路径
              type:"POST" , //请求方式
              success:function (response) {
                  responseJson=JSON.parse(response);
                      for (var key in responseJson['data']) {
                      var item ={};
                      item["id"]=  key;
                      item["text"]=  responseJson['data'][key];
    //                           console.log(item["id"]);
    //                           console.log(item["text"]);
                            financialIndicatorsList.push(item);
                      }
              },//响应成功后的回调函数
              error:function () {
                  alert("出错啦...");
              },//表示如果请求响应出现错误，会执行的回调函数
              dataType:"text"//设置接受到的响应数据的格式
          });

 //用可选财务指标参数去初始化财务指标输入框 start
    $(".select-financialIndicator").select2({
        width: '40%',
        multiple: false,
        data: financialIndicatorsList
    });

    // Add jQuery UI Sortable support
    $(".select-financialIndicator").select2("container").find("ul.select2-choices").sortable({
        containment: 'parent',
        start: function() { $(".select-financialIndicator").select2("onSortStart"); },
        update: function() { $(".select-financialIndicator").select2("onSortEnd"); }
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

});
