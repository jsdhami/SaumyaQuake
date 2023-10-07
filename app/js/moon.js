const colorScale = d3.scaleOrdinal([
  "red",
  "mediumblue",
  "darkgreen",
  "yellow",
]);
const labelsTopOrientation = new Set([
  "Apollo 12",
  "Luna 2",
  "Luna 20",
  "Luna 21",
  "Luna 24",
  "LCROSS Probe",
]); // avoid label collisions
const elem = document.getElementById("globeViz");

// this is for nakamura data to be globally
let nakaData = [];




//  // Gen random data
 const N = 27;

    const gData = [...Array(N).keys()].map(() => ({
      lat: (Math.random() - 0.5) * 180,
      lng: (Math.random() - 0.5) * 360,
      maxR: Math.random() * 20 + 3,
      propagationSpeed: (Math.random() - 0.5) * 20 + 1,
      repeatPeriod: Math.random() * 2000 + 200
    }));
    const colorInterpolator = t => `rgba(255,100,50,${Math.sqrt(1-t)})`;


  // nakamura event show
  fetch("./nakamura_1979_sm_locations.json")
    .then((pollo) => pollo.json())
    .then((nakamura) => {
      console.log(nakamura);
      nakaData = nakamura;
    });
// //////////
    const weightColor = d3.scaleLinear()
    .domain([0, 60])
    .range(['lightblue', 'darkred'])
    .clamp(true);


start();
function start() {
  const moon = Globe()
    .globeImageUrl("./lunar_surface.jpg")
    .bumpImageUrl("./lunar_bumpmap.jpg")
    .backgroundImageUrl("//unpkg.com/three-globe/example/img/night-sky.png")
    .showAtmosphere(false) // moon has no atmosphere
    .labelSize(1.7)
    .labelDotRadius(0.4)
    
// nakamura ring
    .ringsData(gData)
    .ringColor(() => colorInterpolator)
    .ringMaxRadius('maxR')
    .ringPropagationSpeed('propagationSpeed')
    .ringRepeatPeriod('repeatPeriod')
   
    
    .labelDotOrientation((d) =>
      labelsTopOrientation.has(d.label) ? "top" : "bottom"
    )
    .labelColor((d) => colorScale(d.agency))

    .labelLabel(
      (d) => `
    <div class="bg-black ">
      <div class="me-2 mx-2 mb-2">
      <div><b>${d.label}</b></div>
      <div>${d.agency} - ${d.program} Program</div>
      <div>Landing on <i>${new Date(d.date).toLocaleDateString()}</i></div>
      <div>Location: <li>Lat: ${d.lat}</li>
      <li>Lan: ${d.lng}</li>
      </div>
      </div>
      </div>
    `
    )
    .hexBinPointLat(d => d.geometry.coordinates[1])
      .hexBinPointLng(d => d.geometry.coordinates[0])
      .hexBinPointWeight(d => d.properties.mag)
      .hexAltitude(({ sumWeight }) => sumWeight * 0.0025)
      .hexTopColor(d => weightColor(d.sumWeight))
      .hexSideColor(d => weightColor(d.sumWeight))
      .hexLabel(d => `
        <b>${d.points.length}</b> earthquakes in the past month:<ul><li>
          ${d.points.slice().sort((a, b) => b.properties.mag - a.properties.mag).map(d => d.properties.title).join('</li><li>')}
        </li></ul>
      `)


// Danger zone start
.heatmapPointLat('lat')
      .heatmapPointLng('lng')
      .heatmapPointWeight('pop')
      .heatmapBandwidth(0.9)
      .heatmapColorSaturation(2.8)
      .enablePointerInteraction(true)
      
 // danger end
      
      (document.getElementById('globeViz'));

      fetch('output.geojson').then(res => res.json()).then(equakes => {
        moon.hexBinPointsData(equakes.features);
      });



    (
  
     elem
  );


// start danger zone
 let isdanger = true; // Initialize the state variable
 // Function to perform the first action
 function showdanger() {
   // Code for the first action

   
    // danger zone fetch data
   fetch('./danger_zone.csv').then(res => res.text())
   .then(csv => d3.csvParse(csv, ({ lat, lng, pop }) => ({ lat: +lat, lng: +lng, pop: +pop })))
   .then(data => moon.heatmapsData([data]));
   
   // danger zone end
   
      

   // Update the state variable
   isdanger = false;
 }

 // 


 // Function to show the previous condition
 function showithoutdanger() {
   if (isdanger) {
   
  
      // danger zone fetch data
     fetch('./danger_zone.csv').then(res => res.text())
     .then(csv => d3.csvParse(csv, ({ lat, lng, pop }) => ({ lat: +lat, lng: +lng, pop: +pop })))
     .then(data => moon.heatmapsData([data]));
     
     // danger zone end
     
     
     
   } else {
     // Code to show the previous
   
      // danger zone fetch data
     fetch('./danger_zone_no.csv').then(res => res.text())
     .then(csv => d3.csvParse(csv, ({ lat, lng, pop }) => ({ lat: +lat, lng: +lng, pop: +pop })))
     .then(data => moon.heatmapsData([data]));
     
     // danger zone end
    
     // Update the state variable
     isdanger = true;
   }
 }

 // Add a click event listener to the button
 document.getElementById("danger_zone").addEventListener("click", function () {
   if (isdanger) {
     showdanger(); // Execute the first action on the first click
   } else {
     showithoutdanger();
   }
 });

 // end danger zone


























  // this is for home button in left buttom side
  const rotateButton = document.getElementById("rotateButton");
  const rotateImage = document.getElementById("rotateImage");
  rotateButton.addEventListener("click", function () {
    // window.location.href = "/app";
    location.reload();
    rotateImage.classList.toggle("rotated");
  });

  // this is for tropo button to show tropology in moon map

  // const tropo = document.getElementById("tropo");

  // function changeClassName(tropo_c, ntg) {
  //   const chc = document.getElementById(tropo_c);
  //   chc.className = ntg;
  // }
  // tropo.addEventListener("click", function () {
  //   moon.globeImageUrl("./height.jpg");
  //   changeClassName("tropo_c", "ntg");
  // });

  // start tropography

  let istropo = true; // Initialize the state variable
  // Function to perform the first action
  function showtropo() {
    // Code for the first action

    function changeClassName(tropo_c, ntg) {
      const chc = document.getElementById(tropo_c);
      chc.className = ntg;
    }
    moon.globeImageUrl("./height.jpg");
    changeClassName("tropo_c", "ntg");

    // Update the state variable
    istropo = false;
  }

  // 


  // Function to show the previous condition
  function showithouttropo() {
    if (istropo) {
      moon.globeImageUrl("./height.jpg");
      function changeClassName(tropo_c, ntg) {
        const chc = document.getElementById(tropo_c);
        chc.className = ntg;
      }
      changeClassName("tropo_c", "ntg");
    } else {
      // Code to show the previous
    
      moon.globeImageUrl("./lunar_surface.jpg");
      
      // Update the state variable
      istropo = true;
    }
  }

  // Add a click event listener to the button
  document.getElementById("tropo").addEventListener("click", function () {
    if (istropo) {
      showtropo(); // Execute the first action on the first click
    } else {
      showithouttropo();
    }
  });

  // end tropography

  // this is for lag. and lat. line in moon map

  // const lal = document.getElementById("lal");
  // lal.addEventListener("click", function () {
  //   moon.showGraticules(true);
  // });

  // start lat and lng button action

  let isLat = true; // Initialize the state variable
  // Function to perform the first action
  function showLat() {
    // Code for the first action
    moon.showGraticules(true);
    // Update the state variable
    isLat = false;
  }

  // Function to show the previous condition
  function showithoutlat() {
    if (isLat) {
      moon.showGraticules(true);
    } else {
      // Code to show the previous

      moon.showGraticules(false);

      // Update the state variable
      isLat = true;
    }
  }

  // Add a click event listener to the button
  document.getElementById("lal").addEventListener("click", function () {
    if (isLat) {
      showLat(); // Execute the first action on the first click
    } else {
      showithoutlat(); // Show the previous condition on the second click
    }
  });

  // end the latitude side button

  // this is for landing site on moon

  // const landing = document.getElementById("landing");
  //   landing.addEventListener("click", function () {
  //     moon.labelText("label");

  //     });

  let isLandingsite = true; // Initialize the state variable
  // Function to perform the first action
  function showLandingSite() {
    // Code for the first action

    fetch("./moon_landings.json")
      .then((r) => r.json())
      .then((landingSites) => {
        moon.labelsData(landingSites);
        moon.onLabelClick((d) => window.open(d.url, "_blank"));
         });
    moon.labelText("label");
    // Update the state variable
    isLandingsite = false;
  }

  // Function to show the previous condition
  function showPreviousCondition() {
    if (isLandingsite) {
      fetch("./moon_landings.json")
        .then((r) => r.json())
        .then((landingSites) => {
          moon.labelsData(landingSites);
          moon.onLabelClick((d) => window.open(d.url, "_blank"));
        });
        moon.labelText("label");
    } else {
      // Code to show the previous

      fetch("./cleanedData.json")
        .then((r) => r.json())
        .then((landingSites) => {
          moon.labelsData(landingSites);
        });

      // Update the state variable
      isLandingsite = true;
    }
  }

  // Add a click event listener to the button
  document.getElementById("landing").addEventListener("click", function () {
    if (isLandingsite) {
      showLandingSite(); // Execute the first action on the first click
    } else {
      showPreviousCondition(); // Show the previous condition on the second click
    }
  });

}
