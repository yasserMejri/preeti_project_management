$(document).ready(function() {

	var data = {
		labels : ["Apple","Samsung","SONY","Motorola","Nokia","Microsoft","Xiaomi", "Apple","Samsung","SONY","Motorola","Nokia","Microsoft","Xiaomi"],
		datasets : [
			{
				label: "First dataset",
				fillColor : "rgba(128, 222, 234, 0.6)",
				strokeColor : "#ffffff",
				pointColor : "#00bcd4",
				pointStrokeColor : "#ffffff",
				pointHighlightFill : "#ffffff",
				pointHighlightStroke : "#ffffff",
				data: [100, 50, 20, 40, 80, 50, 80, 60, 20, 90, 80, 50, 85, 40]
			},
		]
	};

	var modelsLineChart_w = document.getElementById("models-line-chart").getContext("2d");
	window.modelsLineChart = new Chart(modelsLineChart_w).Line(data, {		
		scaleShowGridLines : true,///Boolean - Whether grid lines are shown across the chart		
		scaleGridLineColor : "rgba(255,255,255,0.4)",//String - Colour of the grid lines		
		scaleGridLineWidth : 1,//Number - Width of the grid lines		
		scaleShowHorizontalLines: true,//Boolean - Whether to show horizontal lines (except X axis)		
		scaleShowVerticalLines: false,//Boolean - Whether to show vertical lines (except Y axis)		
		bezierCurve : true,//Boolean - Whether the line is curved between points		
		bezierCurveTension : 0.4,//Number - Tension of the bezier curve between points		
		pointDot : true,//Boolean - Whether to show a dot for each point		
		pointDotRadius : 5,//Number - Radius of each point dot in pixels		
		pointDotStrokeWidth : 2,//Number - Pixel width of point dot stroke		
		pointHitDetectionRadius : 20,//Number - amount extra to add to the radius to cater for hit detection outside the drawn point		
		datasetStroke : true,//Boolean - Whether to show a stroke for datasets		
		datasetStrokeWidth : 3,//Number - Pixel width of dataset stroke		
		datasetFill : true,//Boolean - Whether to fill the dataset with a colour				
		animationSteps: 15,// Number - Number of animation steps		
		animationEasing: "easeOutQuart",// String - Animation easing effect			
		tooltipTitleFontFamily: "'Roboto','Helvetica Neue', 'Helvetica', 'Arial', sans-serif",// String - Tooltip title font declaration for the scale label		
		scaleFontSize: 12,// Number - Scale label font size in pixels		
		scaleFontStyle: "normal",// String - Scale label font weight style		
		scaleFontColor: "#fff",// String - Scale label font colour
		tooltipEvents: ["mousemove", "touchstart", "touchmove"],// Array - Array of string names to attach tooltip events		
		tooltipFillColor: "rgba(255,255,255,0.8)",// String - Tooltip background colour		
		tooltipTitleFontFamily: "'Roboto','Helvetica Neue', 'Helvetica', 'Arial', sans-serif",// String - Tooltip title font declaration for the scale label		
		tooltipFontSize: 12,// Number - Tooltip label font size in pixels
		tooltipFontColor: "#000",// String - Tooltip label font colour		
		tooltipTitleFontFamily: "'Roboto','Helvetica Neue', 'Helvetica', 'Arial', sans-serif",// String - Tooltip title font declaration for the scale label		
		tooltipTitleFontSize: 14,// Number - Tooltip title font size in pixels		
		tooltipTitleFontStyle: "bold",// String - Tooltip title font weight style		
		tooltipTitleFontColor: "#000",// String - Tooltip title font colour		
		tooltipYPadding: 8,// Number - pixel width of padding around tooltip text		
		tooltipXPadding: 16,// Number - pixel width of padding around tooltip text		
		tooltipCaretSize: 10,// Number - Size of the caret on the tooltip		
		tooltipCornerRadius: 6,// Number - Pixel radius of the tooltip border		
		tooltipXOffset: 10,// Number - Pixel offset from point x to tooltip edge
		responsive: true
		});	

	var callsLineChart_w = document.getElementById("calls-line-chart").getContext("2d");
	window.callsLineChart = new Chart(callsLineChart_w).Line(data, {		
		scaleShowGridLines : true,///Boolean - Whether grid lines are shown across the chart		
		scaleGridLineColor : "rgba(255,255,255,0.4)",//String - Colour of the grid lines		
		scaleGridLineWidth : 1,//Number - Width of the grid lines		
		scaleShowHorizontalLines: true,//Boolean - Whether to show horizontal lines (except X axis)		
		scaleShowVerticalLines: false,//Boolean - Whether to show vertical lines (except Y axis)		
		bezierCurve : true,//Boolean - Whether the line is curved between points		
		bezierCurveTension : 0.4,//Number - Tension of the bezier curve between points		
		pointDot : true,//Boolean - Whether to show a dot for each point		
		pointDotRadius : 5,//Number - Radius of each point dot in pixels		
		pointDotStrokeWidth : 2,//Number - Pixel width of point dot stroke		
		pointHitDetectionRadius : 20,//Number - amount extra to add to the radius to cater for hit detection outside the drawn point		
		datasetStroke : true,//Boolean - Whether to show a stroke for datasets		
		datasetStrokeWidth : 3,//Number - Pixel width of dataset stroke		
		datasetFill : true,//Boolean - Whether to fill the dataset with a colour				
		animationSteps: 15,// Number - Number of animation steps		
		animationEasing: "easeOutQuart",// String - Animation easing effect			
		tooltipTitleFontFamily: "'Roboto','Helvetica Neue', 'Helvetica', 'Arial', sans-serif",// String - Tooltip title font declaration for the scale label		
		scaleFontSize: 12,// Number - Scale label font size in pixels		
		scaleFontStyle: "normal",// String - Scale label font weight style		
		scaleFontColor: "#fff",// String - Scale label font colour
		tooltipEvents: ["mousemove", "touchstart", "touchmove"],// Array - Array of string names to attach tooltip events		
		tooltipFillColor: "rgba(255,255,255,0.8)",// String - Tooltip background colour		
		tooltipTitleFontFamily: "'Roboto','Helvetica Neue', 'Helvetica', 'Arial', sans-serif",// String - Tooltip title font declaration for the scale label		
		tooltipFontSize: 12,// Number - Tooltip label font size in pixels
		tooltipFontColor: "#000",// String - Tooltip label font colour		
		tooltipTitleFontFamily: "'Roboto','Helvetica Neue', 'Helvetica', 'Arial', sans-serif",// String - Tooltip title font declaration for the scale label		
		tooltipTitleFontSize: 14,// Number - Tooltip title font size in pixels		
		tooltipTitleFontStyle: "bold",// String - Tooltip title font weight style		
		tooltipTitleFontColor: "#000",// String - Tooltip title font colour		
		tooltipYPadding: 8,// Number - pixel width of padding around tooltip text		
		tooltipXPadding: 16,// Number - pixel width of padding around tooltip text		
		tooltipCaretSize: 10,// Number - Size of the caret on the tooltip		
		tooltipCornerRadius: 6,// Number - Pixel radius of the tooltip border		
		tooltipXOffset: 10,// Number - Pixel offset from point x to tooltip edge
		responsive: true
		});	

	setInterval(function(){
	  // Get a random index point
	  var indexToUpdate = Math.round(Math.random() * (data.labels.length-1));
	  if (typeof modelsLineChart != "undefined"){
		  // Update one of the points in the second dataset
		  if(modelsLineChart.datasets[0].points[indexToUpdate].value){
		  		modelsLineChart.datasets[0].points[indexToUpdate].value = Math.round(Math.random() * 100);
		  }
		  modelsLineChart.update();
	  }
	  	
	  
	}, 2000);

	setInterval(function(){
	  // Get a random index point
	  var indexToUpdate = Math.round(Math.random() * (data.labels.length-1));
	  if (typeof callsLineChart != "undefined"){
		  // Update one of the points in the second dataset
		  var len = callsLineChart.datasets[0].points.length;
		  for(var i = 1; i < len; i ++) {
		  	var t = callsLineChart.datasets[0].points[i].value;
		  	callsLineChart.datasets[0].points[i - 1].value = t;
		  }
		  callsLineChart.datasets[0].points[len - 1].value = Math.round(Math.random() * 100);
		  // if(callsLineChart.datasets[0].points[indexToUpdate].value){
		  // 		callsLineChart.datasets[0].points[indexToUpdate].value = Math.round(Math.random() * 100);
		  // }
		  // if(callsLineChart.datasets[1].points[indexToUpdate].value){
		  // 		callsLineChart.datasets[1].points[indexToUpdate].value = Math.round(Math.random() * 100);	
		  // }
		  callsLineChart.update();
	  }
	  	
	  
	}, 20000);


});
