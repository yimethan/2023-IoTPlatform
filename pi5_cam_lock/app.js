var createError = require('http-errors');
var express = require('express');
var path = require('path');

var app = express();

const { spawn } = require('child_process');

const port = 3000;

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.get('/gas/:mode', function (req, res) {
    const { mode } = req.params

    if (mode == "on") {
        const gasProcess = spawn('python3', ['/home/user/term_project/routes/gas_on.py']);
        gasProcess.stdout.on('data', function (data) {
            console.log(data.toString());
        });
    
        gasProcess.stderr.on('data', (data) => {
            console.error(`Python script error: ${data}`);
            res.status(500).send('Internal Server Error');
        });
        
        gasProcess.on('close', (code) => {
            pythonProcess.on('close', (code) => {
                if (code === 0) {
                  res.status(200).send('Successfully gas on');
                } else {
                  res.status(500).send('Error while gas on');
                }
            });
        });
    } else if (mode == "off") {
        const gasProcess = spawn('python3', ['/home/user/term_project/routes/gas_off.py']);
        gasProcess.stdout.on('data', function (data) {
            console.log(data.toString());
        });
    
        gasProcess.stderr.on('data', (data) => {
            console.error(`Python script error: ${data}`);
            res.status(500).send('Internal Server Error');
        });
        
        gasProcess.on('close', (code) => {
            pythonProcess.on('close', (code) => {
                if (code === 0) {
                  res.status(200).send('Successfully gas off');
                } else {
                  res.status(500).send('Error while gas off');
                }
            });
        });
    }   
});

app.get('/outmode/:name', function (req, res) { // 외출 모드 켰을 때
    
    const {name} = req.params
    const requestData = req.body.data;
    console.log(requestData);

    if (name == "on") {

        console.log('outmode on')
        const pythonProcess = spawn('python3', ['/home/user/term_project/routes/save_pic.py']);
        pythonProcess.stdout.on('data', function (data) {
            console.log(data.toString());
        });
    
        pythonProcess.stderr.on('data', (data) => {
            console.error(`Python script error: ${data}`);
            res.status(500).send('Internal Server Error');
        });
        
        pythonProcess.on('close', (code) => {
            pythonProcess.on('close', (code) => {
                if (code === 0) {
                  // 성공적으로 실행된 경우
                  res.status(200).send('Successfully outmode on');
                } else {
                  // 실행 중에 오류가 발생한 경우
                  res.status(500).send('Error while outmode on');
                }
            });
        });

        const gasProcess = spawn('python3', ['/home/user/term_project/routes/gas_on.py']);
        gasProcess.stdout.on('data', function (data) {
            console.log(data.toString());
        });
    
        gasProcess.stderr.on('data', (data) => {
            console.error(`Python script error: ${data}`);
            res.status(500).send('Internal Server Error');
        });
        
        gasProcess.on('close', (code) => {
            pythonProcess.on('close', (code) => {
                if (code === 0) {
                  res.status(200).send('Successfully gas on');
                } else {
                  res.status(500).send('Error while gas on');
                }
            });
        });
    
    } else if (name == "off") {
        console.log('outmode off')
        const pythonProcess = spawn('python3', ['/home/user/term_project/routes/save_stop.py']);
        pythonProcess.stdout.on('data', function (data) {
            console.log(data.toString());
        });
    
        pythonProcess.stderr.on('data', (data) => {
            console.error(`Python script error: ${data}`);
            res.status(500).send('Internal Server Error');
        });
        
        pythonProcess.on('close', (code) => {
            pythonProcess.on('close', (code) => {
                if (code === 0) {
                  // 성공적으로 실행된 경우
                  res.status(200).send('Successfully outmode off');
                } else {
                  // 실행 중에 오류가 발생한 경우
                  res.status(500).send('Error while outmode off');
                }
            });
        });
        const gasProcess = spawn('python3', ['/home/user/term_project/routes/gas_off.py']);
        gasProcess.stdout.on('data', function (data) {
            console.log(data.toString());
        });
    
        gasProcess.stderr.on('data', (data) => {
            console.error(`Python script error: ${data}`);
            res.status(500).send('Internal Server Error');
        });
        
        gasProcess.on('close', (code) => {
            pythonProcess.on('close', (code) => {
                if (code === 0) {
                  res.status(200).send('Successfully gas off');
                } else {
                  res.status(500).send('Error while gas off');
                }
            });
        });
    }
});

module.exports = app;

app.listen(port, () => {
    console.log('Express 서버가 3000 포트에서 실행 중입니다.');
});