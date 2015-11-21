document.getElementById("myChart").style.width = "640";
document.getElementById("myChart").style.height = "480";

function queryAPI() {

   var url = 'http://localhost:5000/apps/14831371782';
   var params = {};
   var metric = $("#metric").prop('value');
   var start_date = $("#start_date").prop('value');
   var end_date = $("#end_date").prop('value');

   if (start_date != "") {
      params["start_date"] = start_date;
   }

   if (end_date != "") {
      params["end_date"] = end_date;
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

   // Query our API for
   $.get(url, function(return_data) {
      var ratings = [];
      var metric = $("#metric").prop('value');

      for (var obj in return_data) {
        ratings.push(obj.stars);
      }


      ratings = ratings.reverse(); // I think the results are returned newest to oldest

      // Get the context of the canvas element we want to select
      var ctx = document.getElementById("myChart").getContext("2d");
      var data = {
          labels: ["Oct 02", "Oct 04", "Oct 06", "Oct 08", "Oct 10", "Oct 12",
                   "Oct 14", "Oct 16", "Oct 18", "Oct 20", "Oct 22"],
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
                  data: [1, 2, 3, 3.5, 4, 4.5, 4, 1, 3, 4, 4.2, 4] // XXX: Dummy data
              }
          ]
      };

       var options = {

          ///Boolean - Whether grid lines are shown across the chart
          scaleShowGridLines : true,

          //String - Colour of the grid lines
          scaleGridLineColor : "rgba(0,0,0,.05)",

          //Number - Width of the grid lines
          scaleGridLineWidth : 1,

          //Boolean - Whether to show horizontal lines (except X axis)
          scaleShowHorizontalLines: true,

          //Boolean - Whether to show vertical lines (except Y axis)
          scaleShowVerticalLines: true,

          //Boolean - Whether the line is curved between points
          bezierCurve : true,

          //Number - Tension of the bezier curve between points
          bezierCurveTension : 0.4,

          //Boolean - Whether to show a dot for each point
          pointDot : true,

          //Number - Radius of each point dot in pixels
          pointDotRadius : 4,

          //Number - Pixel width of point dot stroke
          pointDotStrokeWidth : 1,

          //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
          pointHitDetectionRadius : 20,

          //Boolean - Whether to show a stroke for datasets
          datasetStroke : true,

          //Number - Pixel width of dataset stroke
          datasetStrokeWidth : 2,

          //Boolean - Whether to fill the dataset with a colour
          datasetFill : true,

          //String - A legend template
          legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"

      };

      if(metric == 'wordcloud') {
         WordCloud(document.getElementById('myChart'), { list: return_data.word_count, fontFamily: 'Times, serif'} );
      } else {
         var myLineChart = new Chart(ctx).Line(data, options);
         document.getElementById("legend").innerHTML = myLineChart.generateLegend();
      }

   });
}

queryAPI();

$("#submitBtn").click(queryAPI);
