// Websocket Client

// const socket = new WebSocket("ws://localhost:5000");
var socket = io.connect("ws:" + "//" + "localhost" + ":" + "5000");

// Event handler for new connections.
            // The callback function is invoked when a connection with the
            // server is established.
socket.on('connect', function() {
    console.log('CLIENT: Connected')
    socket.emit('my_event', {data: 'I\'m connected!'});
   // socket.disconnect()
});

socket.on('message', function(message) {
   // console.log(message);
    update(message)
})

var api = 'https://api.coindesk.com/v1/bpi/historical/close.json?start=2017-12-31&end=2018-04-01';
document.addEventListener("DOMContentLoaded", function(event) {
    fetch(api)
        .then(function(response) { return response.json(); })
        .then(function(data) {
            var parsedData = parseData(data)
            //drawChart(parsedData);
        })

        function parseData(data) {
            var arr = [];
            for (var i in data.bpi) {
                arr.push(
                    {
                    date: new Date(i), //date
                    value: +data.bpi[i] //convert string to number
                    });
            }
            return arr;
        }
});

var agentData = []
var data = []
var dataX = []
var barsData = []
var count = 0

// create random data
function newData(points){
  //  return d3.range(lineNumber).map(function(){
      return d3.range(points).map(function(item,idx){
        return {date:idx/(points-1), close:Math.random()*100};
      });
  //  });
}

let svgWidth = 800
let svgHeight = 500
let margin = {top: 20, right: 20, bottom: 30, left: 50}
var chart
var count
let num = 300

function drawChart() {

    chart = d3.select(".chart")
        .attr("width", svgWidth)
        .attr("height", svgHeight)
        .style("background-Color", "blue")
        .style("border", "1px solid red")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
}

drawChart()

function update(datax) {

    datax.close = parseInt(datax.close)
    datax.date = count
    count = count + 1
    data.push(datax)
    i = count
    console.log(count)

    console.log(i)

    //data = []

    //data = newData(2)

    // Fixing the time series later
    // var parseTime = d3.timeParse("%d-%b-%y");
    // var formatTime = d3.timeFormat("%B %d, %Y");
    // formatTime(new Date); // "June 30, 2015"
    // datax.date = Date(datax.date)
    // datax.date2 = parseTime(datax.date)

    // Generate Fake Agent Data

    dataxAgent = { "date": datax.date, "close":  datax.close  - 1 }

    agentData.push(dataxAgent)

    //latestDeltas.push(dataxAgent.close)

    width = svgWidth - margin.left - margin.right,
    height = svgHeight - margin.top - margin.bottom;

    var xScale = d3.scaleLinear().rangeRound([100, width - 100]);
    var yScale = d3.scaleLinear().rangeRound([height, 0]);

    var xScaleAgent = d3.scaleLinear().rangeRound([100, width - 100]);
    var yScaleAgent = d3.scaleLinear().rangeRound([height, 0]);

    var line = d3.line() // .curve(d3.curveMonotoneX)
        .x(function(d) { return xScale(d.date)})
        .y(function(d) { return yScale(d.close)})

    var agentLine = d3.line()
        .x(function(d) { return xScaleAgent(d.date)})
        .y(function(d) { return yScaleAgent(d.close)})

    var xMin = d3.min(data, function(d) { return d.date; });
    var xMax = d3.max(data, function(d) { return d.date; });

    var xMin1 = d3.min(data, function(d) { return d.close; });
    var xMax1 = d3.max(data, function(d) { return d.close; });

    var xMinAgent = d3.min(agentData, function(d) { return d.date; });
    var xMaxAgent = d3.max(agentData, function(d) { return d.date; });

    var xMin1Agent = d3.min(agentData, function(d) { return d.close; });
    var xMax1Agent = d3.max(agentData, function(d) { return d.close; });

    //xScale.domain(d3.extent(data, function(d) { console.log(d.date); return d.date }));
    //yScale.domain(d3.extent(data, function(d) { return d.value }));

    xScale.domain([0 , xMax + 5]);
    yScale.domain([xMin1 - 5, xMax1 + 5 ]);

    xScaleAgent.domain([0 , xMaxAgent + 5]);
    yScaleAgent.domain([xMin1 - 5, xMax1 + 5 ]);

    console.log('min: ' + xMin + ' max: ' + xMax);
    console.log('min: ' + xMinAgent + ' max: ' + xMaxAgent);

    // if no axis exists, create one
    // create axis scale
    var xAxis = d3.axisBottom()
        .scale(xScale)
        .tickPadding(10);

    var yAxis = d3.axisLeft()
        .scale(yScale)
        .tickPadding(10);

    var xAxisAgent = d3.axisBottom()
        .scale(xScaleAgent)
        .tickPadding(10);

    var yAxisAgent = d3.axisLeft()
        .scale(yScaleAgent)
        .tickPadding(10);

    if (chart.selectAll(".x.axis").nodes().length < 1 ){
        chart.append("g")
        .attr("transform", "translate(0," + height + ")")
        .attr("class","x axis")
        .call(xAxis)
    } else {
        chart.transition().duration(750).select('.x.axis').call(xAxis);
    }

    if (chart.selectAll(".y.axis").nodes().length < 1 ){
        chart.append("g")
            .call(d3.axisLeft(yScale))
            .attr("class","y axis")
            .append("text")
                .attr("fill", "#FFF")
                .attr("transform", "rotate(-90)")
                .attr("y", 6)
                .attr("dy", "0.71em")
                .attr("text-anchor", "end")
                .text("SEOULAI Price ($)");
    } else {
        chart.transition().duration(750).select('.y.axis').call(yAxis);
    }

    if (chart.selectAll(".y.axis.agent").nodes().length < 1 ){
        chart.append("g")
            .attr("transform", "translate(50,0)")
            .call(d3.axisLeft(yScaleAgent))
            .attr("class","y axis agent")
            .append("text")
                .attr("fill", "yellow")
                .attr("transform", "rotate(-90)")
                .attr("y", 6)
                .attr("dy", "0.71em")
                .attr("text-anchor", "end")
                .text("AI Prediction Price ($)");
    } else {
        chart.transition().duration(750).select('.y.axis.agent').call(yAxisAgent);
    }

    // generate line paths
    var lines = chart.selectAll(".line").data([data]).attr("class","line");

    // transition from previous paths to new paths
    lines.transition().duration(1500)
        .attr("d",line)

    // enter any new data
    lines.enter()
        .append("path")
        .attr("class","line")
        .attr("d",line)

    lines.merge(chart)
    lines.exit().remove();

    // Draw bars
    barsData.push(count)

    var rects = chart.selectAll('rect.day').data(barsData)
        //rects.transition().duration(1500)
        //    .attr('width', '10') // (width - 40) / data.lenght)
        //    .attrs'x', (d, i ) => count * 10) // i * (width- 40) / data.lenght)
        //    .attr('height', (d, i ) => {console.log(d[count-1].close); return d[count-1].close}) // (_, i) => data.close) // Math.abs(latestDeltas[i] * height / 10))
        //    .attr('fill', 'red') // (_, i) => latestDeltas[i] < 0 ? 'red' : 'green')
        //    .attr('y', (d, i) => 0  )// (d, i) => {10}); // h - Math.abs(latestDeltas[i] * height / 10) - 42);

        rects.enter()
            .append('rect')
            .attr("class","day")
            .attr('width', '10') // (width - 40) / data.lenght)
            .attr('x', (d, i) => count * 10) // i * (width- 40) / data.lenght)
            .attr('height', (d, i) => { return data[i].close })// (_, i) => data.close) // Math.abs(latestDeltas[i] * height / 10))
            .attr('fill', function() { return '#'+Math.floor(Math.random()*16777215).toString(16); }) // (_, i) => latestDeltas[i] < 0 ? 'red' : 'green')
            .attr('y', (d, i) => 0  )// (d, i) => {10}); // h - Math.abs(latestDeltas[i] * height / 10) - 42);

        //    .style("stroke", function(){
        //        return '#'+Math.floor(Math.random()*16777215).toString(16);
        //      });


        rects.merge(chart)
        rects.exit().remove();

    // generate line paths
    /*
    var agentLines = chart.selectAll(".line-agent").data([agentData]).attr("class","line-agent");

    // transition from previous paths to new paths
    agentLines.transition().duration(1500)
        .attr("d",agentLine)

    // enter any new data
    agentLines.enter()
        .append("path")
        .attr("class","line-agent")
        .attr("d",agentLine)

    agentLines.merge(chart)
    agentLines.exit().remove();*/
}

function tick() {
    // Push a new data point onto the back.
    data.push(random());
    // Redraw the line.
    d3.select(this)
        .attr("d", line)
        .attr("transform", null);
    // Slide it to the left.
    d3.active(this)
        .attr("transform", "translate(" + x(0) + ",0)")
      .transition()
        .on("start", tick);
    // Pop the old data point off the front.
    data.shift();
}