import { createQueue } from 'kue'

const queue = createQueue();

const sendNotification = (phoneNumber, message) => {
	console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
};

queue.process('push_notification_code', (job) => {
	const phone = job.data.phoneNumber;
	const msg = job.data.message;
	sendNotification(phone, msg);
});
