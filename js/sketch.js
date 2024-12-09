let planets = [];
let stoppedTime = false;
let energyHistory = [];
const maxEnergyHistory = 100;
let minEnergy = Infinity; // Initialize to a very high value
let maxEnergy = -Infinity; // Initialize to a very low value
let showEnergyGraph = false; // Variable to track visibility of the energy graph

function keyPressed() {
    if (key == "s") {
        saveGif("central_dance", 10);
    }
    if (key == " ") {
        stopTime();
    }
    return false;
}

function stopTime() {
    stoppedTime = !stoppedTime;
}

function mousePressed() {
    // if the curser is on the top left corner ignore the mouse press
    if (mouseX < 120 && mouseY < 120) {
        return;
    }
    // if the cursor is on an existing planet delete it
    for (let planet of planets) {
        if (dist(mouseX, mouseY, planet.pos.x, planet.pos.y) <= 20 * Math.cbrt(planet.mass)) {
            planets.splice(planets.indexOf(planet), 1);
            return;
        }
    }

    let planet = new Planet(createVector(mouseX, mouseY), createVector(random(-1, 1), random(-1, 1)), createVector(), 1);
    planets.push(planet);
}

function setup() {
  createCanvas(windowWidth, windowHeight);

  initializePlanets(planets, choreo = "random");

  button = createButton("Stop Time");
  button.mousePressed(stopTime);
  button.position(20, 20);

  // Create the "Show Energy" button
  let energyButton = createButton("Show Energy");
  energyButton.mousePressed(() => {
    showEnergyGraph = !showEnergyGraph; // Toggle visibility
    energyButton.html(showEnergyGraph ? "Hide Energy" : "Show Energy"); // Update button text
  });
  energyButton.position(20, 50); // Position the button below the Stop Time button
}

function draw() {
  background(15, 15, 15, 90);
  textSize(20);
  textAlign(CENTER);
  textStyle(BOLD);
  noStroke();
  fill(230);
  text("Click on the screen to add a planet, or click on an existing planet to remove it.", windowWidth / 2, 35);

  if (!stoppedTime) {
    updateDynamic(type = "simplectic_euler", planets = planets);
  }

  // Calculate total energy
  let totalEnergy = getEnergy(planets);
  
  // Update min and max energy values
  if (totalEnergy < minEnergy) {
    minEnergy = totalEnergy;
  }
  if (totalEnergy > maxEnergy) {
    maxEnergy = totalEnergy;
  }

  energyHistory.push(totalEnergy);
  if (energyHistory.length > maxEnergyHistory) {
    energyHistory.shift();
  }

  // Draw the energy graph if the toggle is on
  if (showEnergyGraph) {
    drawEnergyGraph();
  }

  // Visualizing the planets
  planet_color = color(150, 219, 219);
  stroke(planet_color);
  strokeWeight(4);
  fill(planet_color);
  for (planet of planets) {
    circle(planet.pos.x, planet.pos.y, 20 * Math.cbrt(planet.mass));
  }

  stroke(255, 0, 0);

  // Center of mass of the planets
  let x_center = 0;
  let y_center = 0;
  for (planet of planets) {
    x_center += planet.pos.x / planets.length;
    y_center += planet.pos.y / planets.length;
  }
  point(x_center, y_center);

  // Collision detection on the boundaries
  for (planet of planets) {
    planet.checkBoundaries();
  }
  planets = checkCollisions(planets);

}

function drawEnergyGraph() {
  let graphHeight = 100;
  let graphWidth = width - 40;
  let startX = 20;
  let startY = height - graphHeight - 20;

  // Draw graph background without borders
  noStroke();
  fill(15);
  rect(startX, startY, graphWidth, graphHeight);

  // Draw energy line
  stroke(172, 225, 175);
  noFill();
  beginShape();
  for (let i = 0; i < energyHistory.length; i++) {
    let x = map(i, 0, maxEnergyHistory, startX, startX + graphWidth);
    
    // Normalize energy value
    let normalizedEnergy = map(energyHistory[i], minEnergy, maxEnergy, 0, graphHeight);
    let y = startY + graphHeight - normalizedEnergy;

    vertex(x, y);
  }
  endShape();

  // Draw labels
  noStroke();
  fill(230);
  textSize(12);
  textAlign(LEFT);
  text("Energy", startX + 5, startY + 15);
}
