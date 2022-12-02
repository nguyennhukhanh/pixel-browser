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
            console.log('Đã kết nối');
            return await connection;
        }
    } catch (e) {
        console.log('Lỗi kết nối', e);
    }
}
module.exports = { connect };
