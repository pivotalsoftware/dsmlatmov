function barplot_d3(data) {



    document.getElementById("weekid").value = ""+data[0].week_id;
    d3.select("#anomaliestable").append("h4").html("Anomalous users for week: "+ data[0].week_id +"\<br>"); 



var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");


var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");
    //.ticks(10,"%");

d3.select("#anomaliestable").append("h4").html("") 

var svg = d3.select("#anomaliestable").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

/*d3.tsv("data.tsv", type, function(error, data) {
  if (error) throw error;

  x.domain(data.map(function(d) { return d.letter; }));
  y.domain([0, d3.max(data, function(d) { return d.frequency; })]);*/

  x.domain(data.map(function(d) { return d.account_name; }));
  y.domain([0, d3.max(data, function(d) { return d.pca_score; })]);



  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Risk Score");

  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.account_name); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.pca_score); })
      .attr("height", function(d) { return height - y(d.pca_score); })
      .attr("fill","blue");


function type(d) {
  d.pca_score = +d.pca_score1;
  return d;
}

}