let planets = [];

function keyPressed() {
    if (key == "s") {
        saveGif("central_dance", 10);
    }
}

function setup() {
  createCanvas(600, 600);

  initializePlanets(planets, choreo = "central dance");

  // button = createButton("Restart");
  // button.mousePressed(initializePlanets);
  // button.position(20, 10);
}

function draw() {
  background(15, 15, 15, 90);

  updateDynamic(type = "simplectic_euler", planets = planets);

  // Representing attraction towards the center
  show_center_attraction = false;
  if (show_center_attraction) {
    showCenterAttraction(planets);
  }

  // Visualizing the planets
  // noStroke();
  planet_color = color(150, 219, 219);
  stroke(planet_color);
  strokeWeight(4);
  fill(planet_color);
  for (planet of planets) {
    circle(planet.pos.x, planet.pos.y, 20 * Math.cbrt(planet.mass));
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
  // planets = checkCollisions(planets);
}
