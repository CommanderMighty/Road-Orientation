mapboxgl.accessToken =
  "pk.eyJ1Ijoic2FuZGZpZWxkLWRldiIsImEiOiJjbHNjYWRmZnUwbmQ3MmpudGVtOGYyZnR6In0.yuIWc7NiZrYskyf9NYhCmw";

WKTs = [
  "POINT (174.4513638653 -36.8860243241)",
  "POINT (174.4497720357 -36.8913620998)",
  "POINT (174.556297882 -37.0165364501)",
  "POINT (174.4712833983 -36.9534253801)",
  "POINT (174.5438302975 -36.9442337643)",
  "POINT (174.4801522996 -36.9775084447)",
  "POINT (174.4699737384 -36.9573123506)",
  "POINT (174.7312755423 -37.1828783774)",
  "POINT (175.056786306 -36.9781819942)",
  "POINT (175.000106141 -36.9285970881)",
  "POINT (174.9726129099 -36.9410602158)",
  "POINT (174.9097212116 -36.871404902)",
  "POINT (174.9110686595 -36.8818525921)",
];

roadNames = [
  "BETHELLS RD (WCC)",
  "BETHELLS RD (WCC)",
  "WHATIPU RD",
  "SEAVIEW RD (PIHA)",
  "PIHA RD",
  "KAREKARE RD",
  "BEACH VALLEY RD",
  "GLENBROOK BEACH RD",
  "CLEVEDON-KAWAKAWA RD",
  "WAIKOPUA RD",
  "WHITFORD-MARAETAI RD",
  "EASTERN BEACH RD",
  "BUCKLANDS BEACH RD",
];

coordinates = WKTs.map((WKT) => {
  const coordinates = WKT.match(/-?\d+\.\d+/g);

  if (coordinates.length !== 2) {
    throw new Error("Invalid point format");
  }

  return coordinates.map(parseFloat);
});

processedRoadNames = roadNames.map((name) => {
  const indexRD = name.indexOf(" RD");
  const indexST = name.indexOf(" ST");
  const index = Math.max(indexRD, indexST);
  if (index !== -1) {
    return name.substring(0, index + 3);
  } else {
    return name;
  }
});

var map;
var ctx;
var h = 300; // size of the chart canvas
var r = h / 2; // radius of the polar histogram
var numBins = 64; // number of orientation bins spread around 360 deg.

const initialiseMap = () => {
  map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/cjf4m44iw0uza2spb3q0a7s41",
    center: coordinates[0], // [longitude, latitude] format
    zoom: 20,
    hash: true,
  });

  map.addControl(
    new MapboxGeocoder({ accessToken: mapboxgl.accessToken }),
    "bottom-right"
  );
  map.addControl(new mapboxgl.NavigationControl(), "top-left");

  var canvas = document.getElementById("canvas");
  ctx = canvas.getContext("2d");

  canvas.style.width = canvas.style.height = h + "px";
  canvas.width = canvas.height = h;

  if (window.devicePixelRatio > 1) {
    canvas.width = canvas.height = h * 2;
    ctx.scale(2, 2);
  }

  map.on("load", function () {
    updateOrientations();
    // update the chart on moveend; we could do that on move,
    // but this is slow on some zoom levels due to a huge amount of roads
    map.on("moveend", updateOrientations);
  });
};

const clearAndResetCanvas = () => {
  // Clear and reset the canvas
  ctx.clearRect(0, 0, h, h);
  var bearing = map.getBearing();
  ctx.save();
  ctx.translate(r, r);
  ctx.rotate((-bearing * Math.PI) / 180);

  ctx.fillStyle = "rgba(255,255,255,0.8)";
  ctx.beginPath();
  ctx.arc(0, 0, r, 0, 2 * Math.PI, false);
  ctx.fill();

  ctx.strokeStyle = "rgba(0,0,0,0.15)";
  ctx.beginPath();
  ctx.moveTo(-r, 0);
  ctx.lineTo(r, 0);
  ctx.moveTo(0, -r);
  ctx.lineTo(0, r);
  ctx.stroke();
};

function calcOrientation(bins) {
  let xSum = 0;
  let ySum = 0;

  for (let i = 0; i < bins.length / 2; i++) {
    if (bins[i] > 0) {
      let deg = i * 5.625;
      let rad = (deg * Math.PI) / 180;
      let x = bins[i] * Math.sin(rad);
      let y = bins[i] * Math.cos(rad);

      xSum += Math.abs(x);
      ySum += Math.abs(y);
    }
  }
  return ySum > xSum ? "N/S" : "E/W";
}

function updateOrientations() {
  clearAndResetCanvas();

  var features = map.queryRenderedFeatures({ layers: ["road"] });
  if (features.length === 0) {
    ctx.restore();
    return;
  }

  var ruler = cheapRuler(map.getCenter().lat);
  var bounds = map.getBounds();
  var bbox = [
    bounds.getWest(),
    bounds.getSouth(),
    bounds.getEast(),
    bounds.getNorth(),
  ];
  var bins = new Float64Array(numBins);

  for (var i = 0; i < features.length; i++) {
    if (
      !processedRoadNames.includes(features[i].properties.name?.toUpperCase())
    ) {
      console.log("No", features[i].properties.name);
      continue;
    } else {
      console.log("Yes", features[i].properties.name);
    }

    var geom = features[i].geometry;
    var lines =
      geom.type === "LineString" ? [geom.coordinates] : geom.coordinates;

    // clip lines to screen bbox for more exact analysis
    var clippedLines = [];
    for (var j = 0; j < lines.length; j++) {
      clippedLines.push.apply(clippedLines, lineclip(lines[j], bbox));
    }

    // update orientation bins from each clipped line
    for (j = 0; j < clippedLines.length; j++) {
      analyzeLine(
        bins,
        ruler,
        clippedLines[j],
        features[i].properties.oneway !== "true"
      );
    }
  }

  var binMax = Math.max.apply(null, bins);

  console.log(calcOrientation(bins));

  // Visualise using the canvas
  for (i = 0; i < numBins; i++) {
    var a0 = ((((i - 0.5) * 360) / numBins - 90) * Math.PI) / 180;
    var a1 = ((((i + 0.5) * 360) / numBins - 90) * Math.PI) / 180;
    ctx.fillStyle = interpolateSinebow(((2 * i) % numBins) / numBins);
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.arc(0, 0, r * Math.sqrt(bins[i] / binMax), a0, a1, false);
    ctx.closePath();
    ctx.fill();
  }

  ctx.restore();
}

function analyzeLine(bins, ruler, line, isTwoWay) {
  for (var i = 0; i < line.length - 1; i++) {
    var bearing = ruler.bearing(line[i], line[i + 1]);
    var distance = ruler.distance(line[i], line[i + 1]);

    // Canvas related, remove later
    var k0 = Math.round(((bearing + 360) * numBins) / 360) % numBins; // main bin
    var k1 = Math.round(((bearing + 180) * numBins) / 360) % numBins; // opposite bin

    bins[k0] += distance;
    if (isTwoWay) bins[k1] += distance;
  }
}

// rainbow colors for the chart http://basecase.org/env/on-rainbows
// TODO: remove once done
function interpolateSinebow(t) {
  t = 0.5 - t;
  var r = Math.floor(250 * Math.pow(Math.sin(Math.PI * (t + 0 / 3)), 2));
  var g = Math.floor(250 * Math.pow(Math.sin(Math.PI * (t + 1 / 3)), 2));
  var b = Math.floor(250 * Math.pow(Math.sin(Math.PI * (t + 2 / 3)), 2));
  return "rgb(" + r + "," + g + "," + b + ")";
}

function pauseForSeconds(seconds) {
  return new Promise((resolve) => setTimeout(resolve, seconds * 1000));
}

initialiseMap();
