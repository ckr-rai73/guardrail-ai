const SftpClient = require('ssh2-sftp-client');
const { Client } = require('ssh2');

const config = {
    host: '72.61.241.106',
    username: 'root',
    password: 'Muskan21072709@'
};

const localFilePath = './deploy.zip';
const remoteFilePath = '/tmp/deploy.zip';
const targetDir = '/var/www/guardrail';

async function deploy() {
    const sftp = new SftpClient();
    try {
        console.log('Connecting to SFTP...');
        await sftp.connect(config);
        console.log('Uploading deploy.zip...');
        await sftp.put(localFilePath, remoteFilePath);
        console.log('Upload complete.');
        await sftp.end();

        console.log('Connecting to SSH for remote commands...');
        const conn = new Client();
        conn.on('ready', () => {
            console.log('SSH connection ready.');

            const runCommand = (cmd, allowedCodes = [0]) => {
                return new Promise((resolve, reject) => {
                    console.log(`Running: ${cmd}`);
                    conn.exec(cmd, (err, stream) => {
                        if (err) return reject(err);
                        stream.on('close', (code) => {
                            if (allowedCodes.includes(code)) resolve();
                            else reject(new Error(`Command failed with code ${code}: ${cmd}`));
                        }).on('data', (data) => {
                            process.stdout.write(data);
                        }).stderr.on('data', (data) => {
                            process.stderr.write(data);
                        });
                    });
                });
            };

            (async () => {
                try {
                    await runCommand(`mkdir -p ${targetDir}`);
                    await runCommand(`unzip -o ${remoteFilePath} -d ${targetDir}`, [0, 1]);
                    await runCommand(`cd ${targetDir} && npm -v`);
                    await runCommand(`pm2 -v`);
                    await runCommand(`cd ${targetDir} && npm install --production`);
                    await runCommand(`pm2 restart guardrail || pm2 start "npm run start" --name guardrail --cwd ${targetDir}`);
                    await runCommand(`pm2 save`);
                    console.log('Deployment successful!');
                    process.exit(0);
                } catch (e) {
                    console.error('Remote command execution failed:', e.message);
                    process.exit(1);
                } finally {
                    conn.end();
                }
            })();
        }).connect(config);

    } catch (err) {
        console.error('Deployment error:', err.message);
        process.exit(1);
    }
}

deploy();
