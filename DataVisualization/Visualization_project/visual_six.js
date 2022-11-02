{

    // reference: https://d3-graph-gallery.com/
    var margin = { top: 10, right: 20, bottom: 30, left: 50 },
        width = 500 - margin.left - margin.right,
        height = 420 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#visual_six")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    //Read the data
    d3.csv('clustergroup3.csv', function (data) {

        // Add X axis
        var x = d3.scaleLinear()
            .domain([4, 8])
            .range([0, width]);
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x))


        // Add Y axis
        var y = d3.scaleLinear()
            .domain([0, 2600])
            .range([height, 0]);
        svg.append("g")
            .call(d3.axisLeft(y));

        // Add a scale for bubble size


        // Add a scale for bubble color
        var myColor = d3.scaleLinear()
            .range(["white", "#1172fa"])
            .domain([290, 600]);

        // -1- Create a tooltip div that is hidden by default:
        var tooltip = d3.select("#visual_six")
            .append("div")
            .style("opacity", 0)
            .attr("class", "tooltip")
            .style("background-color", "rgb(174, 240, 232)")
            .style("border-radius", "5px")
            .style("padding", "10px")
            .style("color", "white")
            .style("position", "relative")

        // -2- Create 3 functions to show / update (when mouse move but stay on same circle) / hide the tooltip
        var showTooltip = function (d) {
            tooltip
                .transition()
                .duration(200)
            tooltip
                .style("opacity", 1)
                .html("Country/Region: " + d.Entity + '<br>Average Life satisfaction index:' + d.Life_satisfaction
                    + '<br>Average working hour: ' + d.workinghour + '<br>Work-Life ratio: ' + d.worklife_ratio)
                .style("left", (d3.mouse(this)[0] + 30) + "px")
                .style("top", (d3.mouse(this)[1] - 300) + "px")
        }
        var moveTooltip = function (d) {
            tooltip
                .style("left", (d3.mouse(this)[0] + 30) + "px")
                .style("top", (d3.mouse(this)[1] - 300) + "px")
        }
        var hideTooltip = function (d) {
            tooltip
                .transition()
                .duration(200)
                .style("opacity", 0)
        }

        // Add dots
        svg
            .append('g')
            .selectAll("dot")
            .data(data)
            .enter()
            .append("circle")
            .attr("class", "bubbles")
            .attr("cx", function (d) { return x(d.Life_satisfaction); })
            .attr("cy", function (d) { return y(d.workinghour); })
            .attr("r", 10)
            .style("fill", function (d) { return myColor(d.worklife_ratio); })
            .on("mouseover", showTooltip)
            .on("mousemove", moveTooltip)
            .on("mouseleave", hideTooltip)

    })
}