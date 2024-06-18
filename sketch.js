function setup() {
    createCanvas(windowWidth, windowHeight - 40);

    initializePlanets();

    var button = createButton("Restart");
    button.mousePressed(initializePlanets);
}

class Planet {
  constructor(pos = null, v = null, a = null) {
    if (pos == null) {
      this.pos = createVector(random(width / 3, (2 * width) / 3), random(height / 3, (2 * height) / 3));
    } else {
      this.pos = pos;
    }
    if (v == null) {
      this.v = createVector(random(-1, 1), random(-1, 1));
    } else {
      this.v = v;
    }
    if (a == null) {
      this.a = createVector();
    } else {
      this.a = a;
    }
  }

  checkBoundaries() {
      if (this.pos.x - 20 <= 0 || this.pos.x + 20 >= width) {
          this.v.x *= -1;
      }
      if (this.pos.y - 20 <= 0 || this.pos.y + 20 >= height) {
          this.v.y *= -1;
      }
  }
}

function initializePlanets() {
  planet1 = new Planet();
  planet2 = new Planet();
  planet3 = new Planet();
  planets = [planet1, planet2, planet3];
}

function updateAcceleration(planet) {
  for (other of planets) {
    if (planet == other) {
      continue;
    }
    tmp = p5.Vector.sub(other.pos, planet.pos);
    tmp.div(tmp.mag());
    planet.a = planet.a.add(tmp);
  }
}

function draw() {
  background(242, 238, 203, 50);

  for (planet of planets) {
    updateAcceleration(planet);
  }

  for (planet of planets) {
    planet.a.setMag(0.02);
    planet.v = planet.v.add(planet.a);
    planet.pos = planet.pos.add(planet.v);
  }

  // Representing attraction towards the center
  // strokeWeight(2)
  // for (planet of planets) {
  //   line(planet.pos.x,
  //     planet.pos.y,
  //     (planets[0].pos.x + planets[1].pos.x + planets[2].pos.x) / 3,
  //     (planets[0].pos.y + planets[1].pos.y + planets[2].pos.y) / 3);
  // }

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
  point((planet1.pos.x + planet2.pos.x + planet3.pos.x) / 3, (planet1.pos.y + planet2.pos.y + planet3.pos.y) / 3);

  // Collision detection on the boundaries
  for (planet of planets) {
    planet.checkBoundaries();
  }
}
