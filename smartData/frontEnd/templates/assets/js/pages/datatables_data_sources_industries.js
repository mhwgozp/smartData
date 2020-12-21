
$(function() {
//初始化时间输入选项框
    var time = new Date();
    var day = ("0" + time.getDate()).slice(-2);
    var month = ("0" + (time.getMonth() + 1)).slice(-2);
    var startYear = time.getFullYear()-5 + "-" + (month) + "-" + (day);
    if(time.getHours()<18)
    {
        var preDate = new Date(new Date()-24*60*60*1000);
        day = ("0" + preDate.getDate()).slice(-2);
        month = ("0" + (preDate.getMonth() + 1)).slice(-2);
        startYear = preDate.getFullYear()-5 + "-" + (month) + "-" + (day);
    }
    $('#startDate').val(startYear);
    var today = time.getFullYear() + "-" + (month) + "-" + (day);
    $('#endDate').val(today);

// 获取所有板块的当期的财务指标并显示在表中
    $('.datatable-ajax').dataTable({
        ajax: 'static/assets/data/industryIndicator.json',
        "columnDefs": [
      {
       "render": function (data, type, row) {
        return "<a href='/industry/?industryCode=" + row[1]+ "&industryName=" +row[0]+ "'>"+row[0]+"</a>";
       },
       "targets": 0
      },
      { "visible": false, "targets": [ 1 ] }
     ]
    });

//获取可选板块参数
     $.ajax({
              url:"static/assets/data/industryClassify.json" , // 请求路径
              type:"POST" , //请求方式
              success:function (response) {
                  responseJson=JSON.parse(response);
                  industryClassifyJson = responseJson['data'];
                  for (var key in responseJson['data']) {
                  var item ={};
                  item["id"]=  key;
                  item["text"]=  responseJson['data'][key];
//                           console.log(item["id"]);
//                           console.log(item["text"]);
                        industryClassifyList.push(item);
                  }
              },//响应成功后的回调函数
              error:function () {
                  alert("出错啦...");
              },//表示如果请求响应出现错误，会执行的回调函数
              dataType:"text"//设置接受到的响应数据的格式
          });

//获取财务指标可选参数
     $.ajax({
              url:"static/assets/data/financialIndicators.json" , // 请求路径
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

 //用可选板块参数去初始化板块输入框 start
    $(".select-industryClassifys").select2({
        width: '40%',
        multiple: true,
        data: industryClassifyList
    });

    // Add jQuery UI Sortable support
    $(".select-industryClassifys").select2("container").find("ul.select2-choices").sortable({
        containment: 'parent',
        start: function() { $(".select-industryClassifys").select2("onSortStart"); },
        update: function() { $(".select-industryClassifys").select2("onSortEnd"); }
    });
 //用可选板块参数去初始化板块输入框 end

 //用可选财务指标参数去初始化财务指标输入框 start
    $(".select-financialIndicators").select2({
        width: '40%',
        multiple: false,
        data: financialIndicatorsList
    });

    // Add jQuery UI Sortable support
    $(".select-financialIndicators").select2("container").find("ul.select2-choices").sortable({
        containment: 'parent',
        start: function() { $(".select-financialIndicators").select2("onSortStart"); },
        update: function() { $(".select-financialIndicators").select2("onSortEnd"); }
    });
 //用可选财务指标参数去初始化财务指标输入框 end

 //清除所选项
    $(".access-clear").click(function () {
        $(".select-industryClassifys").select2("val", "");
        $(".select-financialIndicators").select2("val", "");
        industryClassifySelected.splice(0,industryClassifySelected.length);
        financialIndicatorsSelected.splice(0,financialIndicatorsSelected.length);
    });
});
