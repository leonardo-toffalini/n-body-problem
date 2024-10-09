function setup() {
    createCanvas(windowWidth, windowHeight - 40);

    initializePlanets();

    var button = createButton("Restart");
    button.mousePressed(initializePlanets);
}

function draw() {
  background(242, 238, 203);

  updateDynamic(planets);

  // Representing attraction towards the center
  show_center_attraction = false;
  if (show_center_attraction) {
    showCenterAttraction(planets);
  }

  // Visualizing the planets
  // noStroke();
  stroke(255, 153, 61);
  strokeWeight(4);
  fill(255, 153, 61);
  for (planet of planets) {
    circle(planet.pos.x, planet.pos.y, 20);
  }

  stroke(255, 0, 0);

  // Center of mass of the three planets
  x_center = y_center = 0;
  for (planet of planets) {
    x_center += planet.pos.x / planets.length;
    y_center += planet.pos.y / planets.length;
  }
  point(x_center, y_center);

  // Collision detection on the boundaries
  for (planet of planets) {
    planet.checkBoundaries();
  }
}
