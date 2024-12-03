let planets = [];
let stoppedTime = false;

function keyPressed() {
    if (key == "s") {
        saveGif("central_dance", 10);
    }
}

function butPres() {
    stoppedTime = !stoppedTime;
}

function mousePressed() {
    // if the curser is on the top left corner ignore the mouse press
    if (mouseX < 120 && mouseY < 120) {
        return;
    }
    // if the cursor is on an existing planet delete it
    console.log(planets);
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

  // button = createButton("Restart");
  // button.mousePressed(initializePlanets(planets, choreo = "random"));
  // button.position(20, 10);

  button = createButton("Stop Time");
  button.mousePressed(butPres);
  button.position(20, 40);
}

function draw() {
  background(15, 15, 15, 90);
  textSize(20);
  textAlign(CENTER);
  textStyle(BOLD);
  stroke(0);
  fill(255);
  text("Click on the screen to add a planet, or click on an existing planet to remove it.", windowWidth/2, 20);

  if (!stoppedTime) {
    updateDynamic(type = "simplectic_euler", planets = planets);
  }

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
