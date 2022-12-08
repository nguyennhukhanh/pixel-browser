import { Connection } from 'mysql2/promise';
import { Request, Response } from 'express';

export default function getDecorator(
    app: any,
    final: Promise<Connection | undefined>,
    route: string,
    exe: string,
) {
    app.get(route, async (req: Request, res: Response) => {
        async function connect() {
            try {
                if (final) {
                    const [rows] = await final.then((e: any) => e.execute(exe));
                    return await rows;
                } else {
                    console.log('Lỗi truy vấn!');
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
}
