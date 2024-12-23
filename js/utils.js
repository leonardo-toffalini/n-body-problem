const G = 500;
const NUM_PLANETS = 2;
const dist_tol = 20;

class Planet {
  constructor(pos = null, v = null, a = null, mass = 1) {
    if (pos == null) {
      this.pos = createVector(random(width / 3, (2 * width) / 3), random(height / 3, (2 * height) / 3));
    } else {
      this.pos = pos;
    }
    if (v == null) {
      this.v = createVector(random(-1, 1), random(-1, 1));
    } else if (!(v instanceof p5.Vector)) {
      this.v = createVector(v.x, v.y);
    } else {
      this.v = v;
    }
    if (a == null) {
      this.a = createVector();
    } else if (!(a instanceof p5.Vector)) {
      this.a = createVector(a.x, a.y);
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

function initializePlanets(planets, choreo = "random") {
  while (planets.length > 0) {
    planets.pop();
  }
  if (choreo == "random") {
    poses = [null, null, null];
    vels = [null, null, null];
    masses = [1, 1, 1];
  }
  else if (choreo == "central dance") {
    poses = [createVector(width / 4, height / 2), createVector(width / 2, height / 2), createVector(3 * width / 4, height / 2)];
    vels = [];
    for (pos of poses) {
      vels.push(pos.copy().sub(createVector(width / 2, height / 2)).normalize().rotate(PI / 2).setMag(1.5));
    }
    masses = [1, 2, 1];
  }
  
  for (let i = 0; i < NUM_PLANETS; i++) {
    planets.push(new Planet(pos = poses[i], v = vels[i], a = null, mass = masses[i]));
  }
}

function calculateAcceleration(planet, planets) {
  planet.a = createVector(); // Reset acceleration each iteration

  for (other of planets) {
    if (planet == other) {
      continue;
    }
    dir_vec = p5.Vector.sub(other.pos, planet.pos);
    scale = dir_vec.magSq() ; // This should be magSq but it looks better using only mag
    if (scale < dist_tol) { scale = 20; } // Avoid division by small numer
    dir_vec.normalize();
    component = dir_vec.mult(G * other.mass / scale);
    planet.a = planet.a.add(component);
  }
}

function updatePosition(planet, type = "simplectic_euler") {
  if (type == "simplectic_euler") {
    // v_{n+1} = v_n + a_n
    // x_{n+1} = x_n + v_{n+1}
    planet.v = planet.v.add(planet.a);
    planet.pos = planet.pos.add(planet.v);
  } else if (type == "explicit_euler") {
    // x_{n+1} = x_n + v_n
    // v_{n+1} = v_n + a_n
    planet.pos = planet.pos.add(planet.v);
    planet.v = planet.v.add(planet.a);
  } else if (type == "rk4") {
    // TODO
    // k1 = h * f(t_n, y_n)
    // k2 = h * f(t_n + h/2, y_n + k1/2)
    // k3 = h * f(t_n + h/2, y_n + k2/2)
    // k4 = h * f(t_n + h, y_n + k3)
    // y_{n+1} = y_n + (k1 + 2*k2 + 2*k3 + k4) / 6
  }
}

function updateDynamic(type = "explicit_euler", planets) {
  for (planet of planets) {
    calculateAcceleration(planet, planets);
  }
  for (planet of planets) {
    updatePosition(planet, type);
  }
}

function checkCollisions(planets) {
  for (let i = 0; i < planets.length; i++) {
    for (let j = i + 1; j < planets.length; j++) {
      let planet = planets[i];
      let other = planets[j];
      if (planet.pos.dist(other.pos) < 10 * Math.cbrt(max(planet.mass, other.mass))) {
        combined_pos = p5.Vector.add(planet.pos, other.pos).div(2);
        combined_mass = planet.mass + other.mass;
        planets.splice(j, 1);
        planets.splice(i, 1);
        planets.push(new Planet(combined_pos, createVector(), createVector(), combined_mass));
        i--;
        break;
      }
    }
  }
  return planets;
}

function showCenterAttraction(planets) {
    strokeWeight(2);
    let x_center = 0;
    let y_center = 0;
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

function getKineticEnergy(planets) {
  let energy = 0;
  for (planet of planets) {
    energy += 0.5 * planet.mass * max(planet.v.magSq(), 0.01);
  }
  return energy;
}

function getPotentialEnergy(planets) {
  let energy = 0;
  for (planet of planets) {
    for (other of planets) {
      if (planet == other) { continue; }
      energy += - planet.mass * other.mass / planet.pos.dist(other.pos);
    }
  }
  return energy;
}

function getEnergy(planets) {
  return getKineticEnergy(planets) + getPotentialEnergy(planets);
}
