{
    // reference: https://d3-graph-gallery.com/
    // set the dimensions and margins of the map
    var margin = { top: 0, right: 0, bottom: 0, left: 0 },
        width = 1000,
        height = 600;


    var path = d3.geoPath();

    var svg = d3.select("#overview")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append('g')
        .attr('class', 'map');

    var projection = d3.geoMercator()
        .scale(130)
        .translate([width / 2, height / 1.5]);

    var path = d3.geoPath().projection(projection);

    var color = d3.scaleThreshold()
        .domain([3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5])
        .range(["rgb(247,251,255)", "rgb(222,235,247)", "rgb(198,219,239)", "rgb(158,202,225)", "rgb(107,174,214)", "rgb(66,146,198)", "rgb(33,113,181)", "rgb(8,81,156)", "rgb(8,48,107)", "rgb(3,19,43)"]);

    // parse the file form json and csv
    queue()
        .defer(d3.json, "world_countries.json")
        .defer(d3.csv, "happiness_index.csv")
        .await(ready);
    //
    // var the fuction for match the country with its own life index 
    var lifeindexById = {};

    function ready(error, data, life_index) {

        life_index.forEach(function (d) {
            lifeindexById[d.id] = +d.life_index;
        });
        data.features.forEach(function (d) {
            d.life_index = lifeindexById[d.id];
        });

        // draw the map
        svg.append("g")
            .attr("class", "countries")
            .selectAll("path")
            .data(data.features)
            .enter()
            .append("path")
            .attr("d", path)
            .style("fill", function (d) {
                return color(lifeindexById[d.id]);
            })
            .style('stroke', 'white')
            .style('stroke-width', 1.5)
            .style("opacity", 0.8)
            // tooltips format and add tooltips
            .style("stroke", "white")
            .style('stroke-width', 0.3)
            .on('mouseover', function (d) {

                tip.show(d);

                d3.select(this)
                    .style("opacity", 1)
                    .style("stroke", "white")
                    .style("stroke-width", 3);
            })
            .on('mouseout', function (d) {
                tip.hide(d);

                d3.select(this)
                    .style("opacity", 0.8)
                    .style("stroke", "white")
                    .style("stroke-width", 0.3);
            });

    }
    var format = d3.format(",");

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (d) {
            return "<strong>Country: </strong><span class='details'>" + d.properties.name + "<br></span>" +
                "<strong>Average Satisfication index: </strong><span class='details'>" + format(d.life_index) + "</span>";
        });


    svg.call(tip);
}