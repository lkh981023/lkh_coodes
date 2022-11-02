{
    // reference: https://d3-graph-gallery.com/
    // set the dimensions and margins of the graph
    var margin = { top: 10, right: 30, bottom: 30, left: 60 },
        width = 460 - margin.left - margin.right,
        height = 450 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#visual_two")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    //Read the data
    d3.csv('first_ten_countries.csv', function (data) {

        var Tooltip = d3.select("#visual_two")
            .append("div")
            .style("opacity", 0)
            .attr("class", "tooltip")
            .style("background-color", "rgb(174, 240, 232)")
            .style("border-radius", "5px")
            .style("padding", "10px")
            .style("color", "white")
            .style("position", "relative")


        // Three function that change the tooltip when user hover / move / leave a cell
        var mouseover = function (d) {
            d3.select(this)
                .style("stroke", "black")
                .style("opacity", 1);
            Tooltip
                .style('opacity', 1)
                .style("left", (d3.mouse(this)[0] + 50) + "px")
                .style("top", (d3.mouse(this)[1] - 400) + "px")
        }


        var mousemove = function (d) {
            Tooltip
                .html("Country name: " + d.Entity + "<br> Averge life satisfaction index: <br>" +
                    d.satisfaction_index)
                .style("left", (d3.mouse(this)[0] + 50) + "px")
                .style("top", (d3.mouse(this)[1] - 400) + "px")
        }
        var mouseleave = function (d) {
            Tooltip
                .style("opacity", 0)
            d3.select(this)
                .style("stroke", "none")
                .style("opacity", 0.8)
        }
        var x = d3.scaleBand()
            .range([0, width])
            .domain(data.map(function (d) { return d.Entity; }))
            .padding(0.2);
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x))
            .selectAll("text")
            .attr("transform", "translate(-10,0)rotate(-15)")
            .style("text-anchor", "end");

        // Add Y axis
        var y = d3.scaleLinear()
            .domain([7, 8])
            .range([height, 0]);
        svg.append("g")
            .call(d3.axisLeft(y));
        svg.selectAll("mybar")
            .data(data)
            .enter()
            .append("rect")
            .attr("x", function (d) { return x(d.Entity); })
            .attr("width", x.bandwidth())
            .attr("fill", "#94dfff")
            // no bar at the beginning thus:
            .attr("height", function (d) { return height - y(0); }) // always equal to 0
            .attr("y", function (d) { return y(0); })
            .on("mouseover", mouseover)
            .on("mousemove", mousemove)
            .on("mouseleave", mouseleave)

        // add animation and set the duration to ensure the animation will show when user scroll to this part
        Animation
        svg.selectAll("rect")
            .transition()
            .duration(2800)
            .attr("y", function (d) { return y(d.satisfaction_index); })
            .attr("height", function (d) { return height - y(d.satisfaction_index); })
            .delay(function (d, i) { console.log(i); return (i * 100) })


    })
}