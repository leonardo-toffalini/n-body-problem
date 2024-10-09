let G = 3;
let NUM_PLANETS = 3;

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
  for (let i = 0; i < NUM_PLANETS; i++) {
    planets.push(new Planet());
  }
}

function calculateAcceleration(planet) {
  planet.a = createVector(); // Reset acceleration each iteration

  for (other of planets) {
    if (planet == other) {
      continue;
    }
    dir_vec = p5.Vector.sub(other.pos, planet.pos);
    scale = dir_vec.mag() ; // This should be magSq but it looks better this way
    if (scale < 20) { scale = 20; } // Avoid division by small numer
    dir_vec.normalize();
    component = dir_vec.mult(G * other.mass / scale);
    planet.a = planet.a.add(component);
  }
}

function updatePosition(planet, type = "simplectic_euler") {
  if (type == "simplectic_euler") {
    // simplectic Euler
    // v_{n+1} = v_n + a_n
    // x_{n+1} = x_n + v_{n+1}
    planet.v = planet.v.add(planet.a);
    planet.pos = planet.pos.add(planet.v);
  }
  else if (type == "explicit_euler") {
    // explicit Euler
    // x_{n+1} = x_n + v_n
    // v_{n+1} = v_n + a_n
    planet.pos = planet.pos.add(planet.v);
    planet.v = planet.v.add(planet.a);
  }
  else if (type == "rk4") {
    // TODO
    // Runge-Kutta 4
    // k1 = h * f(t_n, y_n)
    // k2 = h * f(t_n + h/2, y_n + k1/2)
    // k3 = h * f(t_n + h/2, y_n + k2/2)
    // k4 = h * f(t_n + h, y_n + k3)
    // y_{n+1} = y_n + (k1 + 2*k2 + 2*k3 + k4) / 6
  }
}

function updateDynamic(type = "explicit_euler") {
  for (planet of planets) {
    calculateAcceleration(planet);
  }
  for (planet of planets) {
    updatePosition(planet, type);
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