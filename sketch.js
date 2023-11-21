let planets = [];
let numberOfPlanets = 5;
let showSun = true;

function setup() {
  createCanvas(windowWidth, windowHeight - 40);

  initializePlanets();

  var button = createButton("Restart");
  button.mousePressed(initializePlanets);
}

function initializePlanets() {
  for (let i = 0; i < numberOfPlanets; i++) {
      let pos = p5.Vector.random2D();
      let v = pos.copy();
      v.setMag(random(3, 5));
      pos.setMag(random(100, 150));
      v.rotate(PI / 2);
      let m = random(10, 15);
      planets[i] = new Planet(pos.x, pos.y, v.x, v.y, m, this.color = [255, 153, 61, 255]);
  }
sun = new Planet(0, 0, 0, 0, 50, [255, 40, 55, 40]);
}

function checkBoundaries() {
  for (planet of planets) {
    if (planet.pos.x - 20 <= -width/2 || planet.pos.x + 20 >= width/2) {
      planet.v.x *= -1;
    }
    if (planet.pos.y - 20 <= -height/2 || planet.pos.y + 20 >= height/2) {
      planet.v.y *= -1;
    }
  }
}

function draw() {
  background(242, 238, 203, 50);
  translate(width/2, height/2);

  for (let planet of planets) {
    sun.attract(planet);
    for (let other of planets) {
      if (other != planet) {
        planet.attract(other);
      }
    }
  }

  for (let planet of planets) {
    planet.update();
    planet.show();
  }
  if (showSun) {
    sun.show();
    checkBoundaries();
  }
}
