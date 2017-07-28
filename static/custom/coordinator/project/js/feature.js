$(document).ready(function() {
	 var BarChartSampleData = {
	    labels: ["January", "February", "March", "April", "May", "June", "July"],
	    datasets: [
	        {
	            label: "My Second dataset",
	            fillColor: "rgba(151,187,205,0.5)",
	            strokeColor: "rgba(151,187,205,0.8)",
	            highlightFill: "rgba(151,187,205,0.75)",
	            highlightStroke: "rgba(151,187,205,1)",
	            data: [28, 48, 40, 19, 86, 27, 90]
	        }
	    ]
	};
	

    var ctx = document.getElementById("feature-analysis").getContext("2d");

	window.BarChartSample = new Chart(
		document.getElementById("feature-analysis").getContext("2d")
	).Bar(BarChartSampleData,{ responsive:true });

}); 
