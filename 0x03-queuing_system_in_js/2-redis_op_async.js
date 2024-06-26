import { createClient, print } from 'redis'
import { promisify } from 'util'

const client = createClient();

client.on('connect', () => {
	console.log('Redis client connected to the server');
});

client.on('error', (err) => {
	console.log(`Redis client not connected to the server: ${err.message}`);
});

const setNewSchool = (schoolName, value) => {
	client.set(schoolName, value, print);
};

const promisifiedClientGet = promisify(client.get).bind(client);

const displaySchoolValue = async (schoolName) => {
	try {
		const reply = await promisifiedClientGet(schoolName);
		console.log(reply);
	} catch (err) {
		console.log(err.message);
	}

}

const execute = async () => {
	await displaySchoolValue('Holberton');
	setNewSchool('HolbertonSanFrancisco', '100');
	await displaySchoolValue('HolbertonSanFrancisco');
};

execute()
