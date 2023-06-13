var express = require('express');
var app = express();

const GPIO = require('onoff').Gpio;

const PIN_LED = 23;
const PIN_BUTTON = 24;
// GPIO 기준 핀 번호

let buttonState = false;

const led = new GPIO(PIN_LED, 'out');
const button = new GPIO(PIN_BUTTON, 'in', 'rising', { debounceTimeout: 200 });

const { exec } = require('child_process');

exec('cvlc --fullscreen --vout mmal_vout concert.mp4', (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error.message}`);
    return;
  }
  console.log(`stdout: ${stdout}`);
  console.error(`stderr: ${stderr}`);
});

function buttonCallback() {
  if (buttonState) {
    led.writeSync(0);
    buttonState = false;
  } else {
    led.writeSync(1);
    buttonState = true;
  }
}

button.watch(buttonCallback);

process.on('SIGINT', () => {
  led.unexport();
  button.unexport();
  process.exit();
});

app.get('/led/:mode', function (req, res) { // 수면 모드에서 조명 제어
  const {mode} = req.params;
  if (mode == 'on') {
      led.writeSync(1);
      console.log("LED on");
  } else if (mode == 'off') {
      led.writeSync(0);
      console.log("LED off");
  }
});

app.get('/tv/:mode', function (req, res) { // 수면 모드에서  TV 제어
  const {mode} = req.params;
  if (mode == 'on') {

    exec('killall -9 vlc', (error, stdout, stderr) => {
      if (error) {
        console.error(`Error: ${error.message}`);
        return;
      }
      console.log(`stdout: ${stdout}`);
      console.error(`stderr: ${stderr}`);
    
      exec('vlc --fullscreen --vout mmal_vout concert.mp4', (error, stdout, stderr) => {
        if (error) {
          console.error(`Error: ${error.message}`);
          return;
        } else {
          console.log("TV on");
        }
        console.log(`stdout: ${stdout}`);
        console.error(`stderr: ${stderr}`);
      });
    });
  } else if (mode == 'off') {

    exec('killall -9 vlc', (error, stdout, stderr) => {
      if (error) {
        console.error(`Error: ${error.message}`);
        return;
      }
      console.log(`stdout: ${stdout}`);
      console.error(`stderr: ${stderr}`);
    });
    
    exec('vlc --fullscreen --vout mmal_vout blank.png', (error, stdout, stderr) => {
      if (error) {
        console.error(`Error: ${error.message}`);
        return;
      } else {
        console.log("TV off");
      }
      console.log(`stdout: ${stdout}`);
      console.error(`stderr: ${stderr}`);
    });
  }
});

module.exports = app;

app.listen(3000, () => {
  console.log('Express 서버가 3000 포트에서 실행 중입니다.');
});