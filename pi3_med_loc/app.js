var express = require('express');
var app = express();

const { spawn } = require('child_process');

const room_process = spawn('python3', ['/home/User/term_project/routes/room.py']);
room_process.stdout.on('data', function (data) {
  console.log(data.toString());
});
room_process.stderr.on('data', (data) => {
  console.error(`Python script error: ${data}`);
});

const med_process = spawn('python3', ['/home/User/term_project/routes/med_time.py']);
med_process.stdout.on('data', function (data) {
  console.log(data.toString());
});
med_process.stderr.on('data', (data) => {
  console.error(`Python script error: ${data}`);
  res.status(500).send('Internal Server Error');
});

module.exports = app;
app.listen(3000, () => {
  console.log('Express 서버가 3000 포트에서 실행 중입니다.');
});