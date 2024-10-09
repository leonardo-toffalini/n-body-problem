let G = 100;

class Planet {
  constructor(pos = null, v = null, a = null, mass = 1) {
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
    this.mass = mass;
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
  planets = [];
  for (let i = 0; i < 3; i++) {
    planets.push(new Planet());
  }
}

function updateAcceleration(planet) {
  for (other of planets) {
    if (planet == other) {
      continue;
    }
    dir_vec = p5.Vector.sub(other.pos, planet.pos);
    scale = dir_vec.mag() ** 2;
    dir_vec.normalize();
    component = dir_vec.mult(G * other.mass / scale);
    planet.a = planet.a.add(component);
  }
}

function updatePosition(planet) {
    planet.a.setMag(0.02);
    planet.v = planet.v.add(planet.a);
    planet.pos = planet.pos.add(planet.v);
}

function updateDynamic(planets) {
  for (planet of planets) {
    updateAcceleration(planet);
  }
  for (planet of planets) {
    updatePosition(planet);
  }
}

function showCenterAttraction(planets) {
    strokeWeight(2);
    x_center = y_center = 0;
    for (planet of planets) {
      x_center += planet.pos.x / planets.length;
      y_center += planet.pos.y / planets.length;
    }

    for (planet of planets) {
      line(
        planet.pos.x,
        planet.pos.y,
        x_center,
        y_center
      );
    }
}