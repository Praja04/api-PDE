const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000; // Ubah sesuai dengan port yang Anda inginkan

app.use(bodyParser.json());

app.post('/api/button', (req, res) => {
    const buttonState = req.body.buttonState;
    console.log('Button state:', buttonState);
    // Di sini Anda bisa menambahkan logika untuk menangani data dari ESP8266
    res.send('Data diterima dari ESP8266');
});

app.listen(port, () => {
    console.log(`Server berjalan di http://localhost:${port}`);
});
