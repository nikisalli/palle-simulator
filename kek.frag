#include "math/constants.glsl"

varying vec2 v_position;
uniform float px[10];
uniform float py[10];
uniform float pc[10];

const float x_scale = 5.;
const float y_scale = 5.;

float f(float x, float y) {
    float voltage = 0;
    for(int i = 0; i < 10; i++) {
        voltage += (9e9 * pc[i]) / sqrt(pow((x - px[i]), 2) + pow((y - py[i]), 2));
    }

    if(voltage > 1){
        voltage = 1;
    } else if (voltage < -1){
        voltage = -1;
    }
    return voltage;
}

vec4 jet(float x) {
    vec3 a, b;
    float c;
    if (x < 0.34) {
        a = vec3(0, 0, 0.5);
        b = vec3(0, 0.8, 0.95);
        c = (x - 0.0) / (0.34 - 0.0);
    } else if (x < 0.64) {
        a = vec3(0, 0.8, 0.95);
        b = vec3(0.85, 1, 0.04);
        c = (x - 0.34) / (0.64 - 0.34);
    } else if (x < 0.89) {
        a = vec3(0.85, 1, 0.04);
        b = vec3(0.96, 0.7, 0);
        c = (x - 0.64) / (0.89 - 0.64);
    } else {
        a = vec3(0.96, 0.7, 0);
        b = vec3(0.5, 0, 0);
        c = (x - 0.89) / (1.0 - 0.89);
    }
    return vec4(mix(a, b, c), 1.0);
}

void main() {
    vec2 pos = v_position;
    gl_FragColor = jet(f(x_scale * pos.x, y_scale * pos.y) * 0.5 + 0.5);
}