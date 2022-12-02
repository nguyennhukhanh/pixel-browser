const express = require('express');
const path = require('path');
const morgan = require('morgan');
const { engine } = require('express-handlebars');
const app = express();
const db = require('./config/connect');
const port = 1410;

const final = db.connect();

app.use(express.static(path.join(__dirname, 'views')));
//Logger
app.use(morgan('combined'));

//Template engine
app.engine(
    'hbs',
    engine({
        extname: '.hbs',
    }),
);

app.set('view engine', 'hbs');
app.set('views', path.join(__dirname, 'views'));

//Mỗi lần gọi tuyến đường là gọi lại db
app.get('/history', async (req, res) => {
    async function connect() {
        const mysql = require('mysql2/promise');
        try {
            const connection = await mysql.createConnection({
                host: 'localhost',
                user: 'root',
                password: '1029384756',
                database: 'browserhistory',
            });
            if (connection) {
                const [rows] = await final.then((e) =>
                    e.execute('SELECT * FROM browserhistory.cache'),
                );
                console.log('Đã kết nối');
                return await rows;
            }
        } catch (e) {
            console.log('Lỗi kết nối', e);
        }
    }
    let rows = connect();
    rows.then(function (target) {
        res.render('index', { target });
    });
});

app.get('/delete/:id', async (req, res) => {
    let par = req.params.id;
    async function connect() {
        const mysql = require('mysql2/promise');
        try {
            const connection = await mysql.createConnection({
                host: 'localhost',
                user: 'root',
                password: '1029384756',
                database: 'browserhistory',
            });
            if (connection) {
                const [rows] = await final.then((e) =>
                    e.execute(`DELETE FROM cache WHERE id=${par}`),
                );
                console.log('Đã kết nối');
                return await rows;
            }
        } catch (e) {
            console.log('Lỗi kết nối', e);
        }
    }
    let rows = connect();
    rows.then(function (target) {
        res.redirect('/history');
    });
});

app.get('/delete-all', async (req, res) => {
    async function connect() {
        const mysql = require('mysql2/promise');
        try {
            const connection = await mysql.createConnection({
                host: 'localhost',
                user: 'root',
                password: '1029384756',
                database: 'browserhistory',
            });
            if (connection) {
                const [rows] = await final.then((e) =>
                    e.execute(`DELETE FROM cache`),
                );
                console.log('Đã kết nối');
                return await rows;
            }
        } catch (e) {
            console.log('Lỗi kết nối', e);
        }
    }
    let rows = connect();
    rows.then(function (target) {
        res.redirect('/history');
    });
});

app.get('/home', async (req, res) => {
    return res.render('home', { home: true });
});

// async function showAll() {
//   const [rows] = await final.then(e => e.execute('SELECT * FROM browserhistory.cache'));
//   return await rows;
// }

// const show = showAll()

// //Mỗi lần gọi tuyến đường là không gọi lại db nhưng không load được những gì diễn ra sau nó
// app.get('/', async (req, res) => {
//   show.then(function (target) {
//     res.render("index", { target })
//   })
// })

app.listen(port, () => {
    console.log(`Lắng nghe cổng ${port}`);
});
