document.getElementById("myChart").style.width = "640";
document.getElementById("myChart").style.height = "480";

var myLineChart = null;

function queryAPI() {
   var url = 'http://localhost:5000/apps/' + $("#apps").prop('value');
   var params = {};
   var metric = $("#metric").prop('value');
   var min_metric_val = $("#min_metric_val").prop('value');
   var max_metric_val = $("#max_metric_val").prop('value');
   var start_date = $("#start_date").prop('value');
   var end_date = $("#end_date").prop('value');

   /* Build the URL based on parameters present */
   if (start_date != "") {
      params["start_date"] = start_date;
   }

   if (end_date != "") {
      params["end_date"] = end_date;
   }

   if (min_metric_val != "") {
      params['min_' + metric] = min_metric_val;
   }

   if (max_metric_val != "") {
      params['max_' + metric] = max_metric_val;
   }
   params["metric"] = metric;

   var numParams = Object.keys(params).length;
   if (numParams > 1) {
      url += "?";
   }

   for (var key in params) {
      url += (key + "=" + params[key]);
      if (numParams > 1) { // If not the last parameter
         url += "&";
      }
      numParams--;
   }
   /* Done building URL */

   /* Query our API for original and selected metric windowed averages */
   $.get(url, function (return_data) {
      var metric = $("#metric").prop('value');
      var dates = [];
      var ratings = [];
      var dateToWinAvg = return_data['win_avg_stars'];

      var ratingsMetric = [];
      var dateToWinAvgMetric = return_data['win_avg_' + metric];

      $('#loading_icon').css('visibility', 'hidden'); // Hide loading indicator b/c got data back

      for (date in dateToWinAvg) {
         dates.push(date);
         ratings.push(dateToWinAvg[date]);
      }

      for (date in dateToWinAvgMetric) {
         ratingsMetric.push(dateToWinAvgMetric[date]);
      }

      // Get the context of the canvas element we want to select
      var ctx = document.getElementById("myChart").getContext("2d");
      var data = {
         labels: dates,
         datasets: [
            {
               label: "Original Ratings",
               fillColor: "rgba(220,220,220,0.2)",
               strokeColor: "rgba(220,220,220,1)",
               pointColor: "rgba(220,220,220,1)",
               pointStrokeColor: "#fff",
               pointHighlightFill: "#fff",
               pointHighlightStroke: "rgba(220,220,220,1)",
               data: ratings
            },
            {
               label: "[METRIC] Rating",
               fillColor: "rgba(151,187,205,0.2)",
               strokeColor: "rgba(151,187,205,1)",
               pointColor: "rgba(151,187,205,1)",
               pointStrokeColor: "#fff",
               pointHighlightFill: "#fff",
               pointHighlightStroke: "rgba(151,187,205,1)",
               data: ratingsMetric
            }
         ]
      };

      var options = {

         ///Boolean - Whether grid lines are shown across the chart
         scaleShowGridLines: true,

         //String - Colour of the grid lines
         scaleGridLineColor: "rgba(0,0,0,.05)",

         //Number - Width of the grid lines
         scaleGridLineWidth: 1,

         //Boolean - Whether to show horizontal lines (except X axis)
         scaleShowHorizontalLines: true,

         //Boolean - Whether to show vertical lines (except Y axis)
         scaleShowVerticalLines: true,

         //Boolean - Whether the line is curved between points
         bezierCurve: true,

         //Number - Tension of the bezier curve between points
         bezierCurveTension: 0.4,

         //Boolean - Whether to show a dot for each point
         pointDot: true,

         //Number - Radius of each point dot in pixels
         pointDotRadius: 4,

         //Number - Pixel width of point dot stroke
         pointDotStrokeWidth: 1,

         //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
         pointHitDetectionRadius: 20,

         //Boolean - Whether to show a stroke for datasets
         datasetStroke: true,

         //Number - Pixel width of dataset stroke
         datasetStrokeWidth: 2,

         //Boolean - Whether to fill the dataset with a colour
         datasetFill: true,

         //String - A legend template
         legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"

      };

      if (metric == 'wordcloud') {
         if (myLineChart != null) {
            myLineChart.destroy();
         }
         WordCloud(document.getElementById('myChart'), {list: return_data.word_count, fontFamily: 'Times, serif'});
      } else {
         myLineChart = new Chart(ctx).Line(data, options);
         document.getElementById("legend").innerHTML = myLineChart.generateLegend();
      }

   });
}



$("#submitBtn").click(function() {
   queryAPI();
   $('#loading_icon').css('visibility', 'visible');
});

$(document).ready(function () {
   $.get('http://localhost:5000/apps', function (data) {
      var select = document.getElementById("apps");

      for (var i = 0; i < data.length;i++) {
         var app = data[i];
         var el = document.createElement("option");
         el.text = app['product_name'];
         el.value = app['product'];
         select.appendChild(el);
      }
      queryAPI();

   })
});
