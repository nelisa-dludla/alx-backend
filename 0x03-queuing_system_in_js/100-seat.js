import { createClient } from 'redis'
import { promisify } from 'util'
import { createQueue } from 'kue'
import express from 'express'

const client = createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

const reserveSeat = async (number) => {
	await setAsync('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
	const availableSeats = await getAsync('available_seats');
	return availableSeats;
};

client.on('connect', async () => {
	await reserveSeat(50);
});

const queue = createQueue();
const app = express();
const port = 1245;
let reservationEnabled = true;

app.get('/available_seats', async (req, res) => {
	const availableSeats = await getAsync('available_seats');
	res.json({"numberOfAvailableSeats":availableSeats});
});

app.get('/reserve_seat', (req, res) => {
	if (!reservationEnabled) {
		return res.json({ "status": "Reservation are blocked" });
	}

	const job = queue.create('reserve_seat')
				.on('complete', () => {
					console.log(`Seat reservation job ${job.id} completed`);
				})
				.on('failed', (err) => {
					console.log(`Seat reservation job ${job.id} failed: ${err}`);
				})
				.save((err) => {
					if (err) {
						return res.json({ "status": "Reservation failed" });
					}
					return res.json({ "status": "Reservation in process" });
				});
});

app.get('/process', (req, res) => {
	res.json({ "status": "Queue processing" });

	queue.process('reserve_seat', async (job, done) => {
		const currentAvailableSeats = await getCurrentAvailableSeats();
		const updatedAvailableSeats = currentAvailableSeats - 1;

		if (updatedAvailableSeats === 0) {
			reservationEnabled = false;
			await setAsync('available_seats', updatedAvailableSeats);
			done();
		} else if (updatedAvailableSeats >= 0) {
			await setAsync('available_seats', updatedAvailableSeats);
			done();
		}
		done(Error('Not enough seats available'));
	});
});

app.listen(port);
