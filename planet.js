class Planet {
    constructor(x, y, vx, vy, m, color) {
      this.pos = createVector(x, y);
      this.vel = createVector(vx, vy);
      this.acc = createVector(0, 0);
      this.mass = m;
      this.r = sqrt(this.mass) * 2;
      this.color = color;
    }
  
    applyForce(force) {
      let f = p5.Vector.div(force, this.mass);
      this.acc.add(f);
    }
  
    attract(planet) {
      let force = p5.Vector.sub(this.pos, planet.pos);
      let distanceSq = constrain(force.magSq(), 100, 1000);
      let G = 1;
      let strength = (G * (this.mass * planet.mass)) / distanceSq;
      force.setMag(strength);
      planet.applyForce(force);
    }
  
    update() {
      this.vel.add(this.acc);
      this.pos.add(this.vel);
      this.acc.set(0, 0);
    }
  
    show() {
      stroke(this.color[0], this.color[1], this.color[2], this.color[3]);
      strokeWeight(4);
      fill(this.color[0], this.color[1], this.color[2])
      ellipse(this.pos.x, this.pos.y, this.r * 2);
    }
  }